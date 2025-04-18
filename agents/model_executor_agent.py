import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.classification import Classifier
from models.regression import Regressor
from models.nlpmodel import NLPModel
from models.timeseries import TimeSeriesModel
from models.dataset import Dataset

import pandas as pd
import json
import h2o
from h2o.frame import H2OFrame
from openai import OpenAI
from dotenv import load_dotenv

from agents.task_classifier_agent import TaskClassifierAgent
from agents.feature_mapper_agent import FeatureMapperAgent

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ModelExecutorAgent:
    def __init__(self, dataset, task_type: str, target_column: str, features=None):
        self.dataset = dataset
        self.task_type = task_type
        self.target_column = target_column
        self.features = features or []
        self.model = None

    def run(self):
        if self.task_type == "classification":
            self.model = Classifier(dataset=self.dataset.get_data(), target=self.target_column, exclude=[])
            self.model.train_model()
        elif self.task_type == "regression":
            self.model = Regressor(dataset=self.dataset.get_data(), target=self.target_column, exclude=[])
            self.model.train_model()
        elif self.task_type == "nlp":
            self.model = NLPModel(dataset=self.dataset, text_columns=self.features, target_column=self.target_column)
            self.model.train()
        elif self.task_type == "time_series":
            self.model = TimeSeriesModel(dataset=self.dataset, date_column=self.features[0], target_column=self.target_column)
            self.model.train()

        print("✅ Model training complete")
        return self.model.save_best_model()

    def predict_from_query(self, query: str):
        try:
            feature_agent = FeatureMapperAgent(prompt=query, dataset_columns=self.dataset.columns(), target_column=self.target_column)
            features_info = feature_agent.run()
            features = features_info["features"]

            example_values = {}
            for col in features:
                unique_vals = self.dataset.get_data()[col].dropna().unique().tolist()
                example_values[col] = unique_vals[:5]

            feature_examples_text = "\n".join([f"{k}: example values -> {v}" for k, v in example_values.items()])

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that converts user queries into structured input data for ML models."},
                    {"role": "user", "content": f"Query: {query}\nFeatures: {features}\nMatch each feature's value to these examples as closely as possible:\n{feature_examples_text}"}
                ],
                functions=[{
                    "name": "structure_input",
                    "description": "Parse input values from user query using valid values.",
                    "parameters": {
                        "type": "object",
                        "properties": {feature: {"type": "string"} for feature in features},
                        "required": features
                    }
                }],
                function_call="auto"
            )

            input_values = json.loads(response.choices[0].message.function_call.arguments)
            df = pd.DataFrame([input_values])

            for col in features:
                train_col_dtype = self.dataset.get_data()[col].dtype
                if train_col_dtype == "object" or str(train_col_dtype).startswith("category"):
                    df[col] = df[col].astype("str")
                elif str(train_col_dtype).startswith("int"):
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")
                elif str(train_col_dtype).startswith("float"):
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype("float")

            h2o_df = H2OFrame(df)

            preds = self.model.aml.leader.predict(h2o_df).as_data_frame().iloc[:, 0].tolist()
            predicted_value = preds[0]

            # Format prediction value if it's a large float
            if isinstance(predicted_value, float):
                formatted_prediction = f"${predicted_value:,.2f}" if predicted_value > 100 else round(predicted_value, 2)
            else:
                formatted_prediction = predicted_value

            explanation = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a model explanation assistant. Explain what the prediction means in human terms."},
                    {"role": "user", "content": f"Query: {query}\nPrediction: {formatted_prediction}\nTarget Column: {self.target_column}"}
                ]
            ).choices[0].message.content

            print("🔮 Prediction:", formatted_prediction)
            print("🧠 LLM Explanation:", explanation)
            return formatted_prediction, explanation

        except Exception as e:
            print("❌ Prediction failed:", str(e))
            return None, "An error occurred while making the prediction. Please try again with a different query or check the dataset."


if __name__ == "__main__":  
    prompt = "Will a 60 year old man be a repeat buyer?"

    data = {
    "CustomerID": [101, 102, 103, 104, 105],
    "Age": [25, 45, 32, 28, 39],
    "Gender": ["male", "female", "female", "male", "female"],
    "PurchaseAmount": [200, 500, 150, 300, 450],
    "RepeatBuyer": [0, 1, 0, 1, 1]
    } 


    df = pd.DataFrame(data)
    df.to_csv("buyer.csv", index=False)

    dataset = Dataset(file_path="buyer.csv")

    task_agent = TaskClassifierAgent(prompt, dataset.columns())
    task_info = task_agent.run()
    task_type = task_info["task_type"]
    target_column = task_info["target_column"]
    print("🧠 Task Type:", task_type)
    print("🎯 Target Column:", target_column)
    print("")

    feature_agent = FeatureMapperAgent(prompt, dataset.columns(), target_column=target_column)
    features_info = feature_agent.run()
    features = features_info["features"]
    print("🧩 Selected Features:", features)
    print("")

    executor = ModelExecutorAgent(
        dataset=dataset,
        task_type=task_type,
        target_column=target_column,
        features=features
    )
    model_path = executor.run()

    print("✅ Model saved at:", model_path)

    pred, explanation = executor.predict_from_query(prompt)
