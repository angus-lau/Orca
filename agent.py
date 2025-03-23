import openai
import json

from models.dataset import Dataset

openai.api_key = "YOUR_OPENAI_API_KEY"

# -- These would be passed in during runtime --
prompt = "Will Tesla’s stock price go up next week?"
dataset = ""  # Instance of Dataset class

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