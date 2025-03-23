import os
import json
import joblib
from dotenv import load_dotenv
from openai import OpenAI

from models.dataset import Dataset
from models.timeseries import TimeSeriesModel
from models.nlpmodel import NLPModel
from models.classification import Classifier
from models.regression import Regressor  # ✅ Added Regressor import

# Step 1: Load API Key
print("🔄 Loading environment variables...")
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file.")
print("🔐 OpenAI API key loaded.")
client = OpenAI(api_key=api_key)

# Step 2: Load prompt and dataset
prompt = "What's the closing price of the Microsoft stock tomorrow?"
print(f"🧠 Prompt: {prompt}")
print("📦 Loading dataset from joblib...")
dataset = joblib.load("persistance/microsoft.joblib")  # Instance of Dataset class
print(f"✅ Dataset loaded with columns: {dataset.columns()}")

# Step 3: Define function schemas (including Regressor)
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
    },
    {
        "name": "train_regression_model",
        "description": "Train a regression model given a target column and optional feature exclusions.",
        "parameters": {
            "type": "object",
            "properties": {
                "target_column": {"type": "string", "description": "The numeric column to predict"},
                "exclude_columns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional columns to exclude from training"
                }
            },
            "required": ["target_column"]
        }
    }
]

# Step 4: Send request to OpenAI
print("🤖 Sending prompt and dataset columns to OpenAI agent...")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are an AutoML assistant. Based on a user's question and dataset, select the right ML task (classification, regression, NLP, or time-series)."
        },
        {
            "role": "user",
            "content": f"Prompt: {prompt}\nDataset columns: {dataset.columns()}"
        }
    ],
    functions=functions,
    function_call="auto"
)

# Step 5: Handle function call
function_call = response.choices[0].message.function_call

if function_call:
    fn_name = function_call.name
    args = json.loads(function_call.arguments)

    print(f"🧭 LLM selected function: {fn_name}")
    print(f"📋 With arguments: {args}")

    if fn_name == "train_time_series_model":
        print("⏱ Initializing TimeSeriesModel...")
        model = TimeSeriesModel(
            dataset=dataset,
            date_column=args["date_column"],
            target_column=args["target_column"]
        )
        print("🚀 Training TimeSeriesModel...")
        model.train()
        print("✅ TimeSeriesModel training complete.")

    elif fn_name == "train_nlp_model":
        print("📝 Initializing NLPModel...")
        model = NLPModel(
            dataset=dataset,
            text_columns=args["text_columns"],
            target_column=args["target_column"]
        )
        print("🚀 Training NLPModel...")
        model.train()
        print("✅ NLPModel training complete.")

    elif fn_name == "train_classifier":
        print("🔢 Initializing Classifier...")
        model = Classifier(
            dataset=dataset,
            features=args["features"],
            target=args["target_column"],
            exclude=[]
        )
        print("🚀 Training Classifier...")
        model.train_model()
        print("✅ Classifier training complete.")

    elif fn_name == "train_regression_model":
        print("📈 Initializing Regressor...")
        model = Regressor(
            dataset=dataset.get_data(),  # Assuming dataset has a .get_data() method returning pandas DataFrame
            target=args["target_column"],
            exclude=args.get("exclude_columns", [])
        )
        print("🚀 Training Regressor...")
        model.train_model()
        print("✅ Regressor training complete.")

else:
    print("❌ No function call was returned by OpenAI.")
