import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.classification import Classifier
from models.regression import Regressor
from models.nlpmodel import NLPModel
from models.timeseries import TimeSeriesModel
from models.dataset import Dataset

import pandas as pd


from agents.task_classifier_agent import TaskClassifierAgent
from agents.feature_mapper_agent import FeatureMapperAgent

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
    

if __name__ == "__main__":
    # Simulate a user prompt
    prompt = "Will a 38-year-old female passenger from 1st class survive the Titanic?"

    # Sample Titanic-like data
    data = {
        "Age": [22, 38, 26, 35, 28],
        "Sex": ["male", "female", "female", "female", "male"],
        "Pclass": [3, 1, 3, 1, 3],
        "Fare": [7.25, 71.83, 7.92, 53.10, 8.05],
        "Survived": [0, 1, 1, 1, 0]
    }
    df = pd.DataFrame(data)
    df.to_csv("titanic_sample.csv", index=False)

    # Load into custom Dataset class
    dataset = Dataset(file_path="titanic_sample.csv")

    # --- Step 1: Use TaskClassifierAgent ---
    task_agent = TaskClassifierAgent(prompt, dataset.columns())
    task_info = task_agent.run()
    task_type = task_info["task_type"]
    target_column = task_info["target_column"]
    print("🧠 Task Type:", task_type)
    print("🎯 Target Column:", target_column)
    print("")

    # --- Step 2: Use FeatureMapperAgent ---
    feature_agent = FeatureMapperAgent(prompt, dataset.columns(), target_column=target_column)
    features_info = feature_agent.run()
    features = features_info["features"]
    print("🧩 Selected Features:", features)
    print("")

    # --- Step 3: Run ModelExecutorAgent ---
    executor = ModelExecutorAgent(
        dataset=dataset,
        task_type=task_type,
        target_column=target_column,
        features=features
    )
    model_path = executor.run()

    print("✅ Model saved at:", model_path)
