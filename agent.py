import openai
import json
import joblib

from models.dataset import Dataset
from models.timeseries import TimeSeriesModel
from models.nlpmodel import NLPModel

openai.api_key = "YOUR_OPENAI_API_KEY"

# -- These would be passed in during runtime --
prompt = "Will Tesla’s stock price go up next week?"
dataset = joblib.load("persistance/dataset_instance.joblib")  # Instance of Dataset class

# -- Define available functions (schemas for OpenAI) --
functions = [
    {
        "name": "train_time_series_model",
        "description": "Train a time-series forecasting model with a date and target column.",
        "parameters": {
            "type": "object",
            "properties": {
                "date_column": {"type": "string", "description": "The datetime column name"},
                "target_column": {"type": "string", "description": "The target variable to forecast"},
            },
            "required": ["date_column", "target_column"]
        },
    },
    {
        "name": "train_nlp_model",
        "description": "Train a model using NLP with one or more text columns and a target column.",
        "parameters": {
            "type": "object",
            "properties": {
                "text_columns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Text columns to use"
                },
                "target_column": {"type": "string", "description": "The column to predict"}
            },
            "required": ["text_columns", "target_column"]
        }
    },
    {
        "name": "train_classifier",
        "description": "Train a classification model given features and a target.",
        "parameters": {
            "type": "object",
            "properties": {
                "features": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Feature columns"
                },
                "target_column": {"type": "string", "description": "The column to predict"}
            },
            "required": ["features", "target_column"]
        }
    }
]


response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=[
        {"role": "system", "content": "You are an AutoML assistant. Based on a user's question and dataset, select the right ML task (classification, NLP, or time-series)."},
        {"role": "user", "content": f"Prompt: {prompt}\nDataset columns: {dataset.columns()}"}
    ],
    functions=functions,
    function_call="auto"  # Let GPT choose
)

function_call = response.choices[0].message.get("function_call")


if function_call:
    fn_name = function_call["name"]
    args = json.loads(function_call["arguments"])

    if fn_name == "train_time_series_model":
        model = TimeSeriesModel(
            dataset=dataset,
            date_column=args["date_column"],
            target_column=args["target_column"]
        )
        model.train()
    
    elif fn_name == "train_nlp_model":
        model = NLPModel(
            dataset=dataset,
            text_columns=args["text_columns"],
            target_column=args["target_column"]
        )
        model.train()

    elif fn_name == "train_classifier":
        model = Classifier(
            dataset=dataset,
            features=args["features"],
            target=args["target_column"],
            exclude=[]
        )
        model.train_model()
