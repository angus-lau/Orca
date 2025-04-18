from flask import Blueprint, request, jsonify
from models.classification import Classifier
from models.regression import Regressor
from models.timeseries import TimeSeriesModel
from models.nlpmodel import NLPModel
from download import download_file
import os
import joblib

model_bp = Blueprint('models', __name__)

@model_bp.route('/train_data', methods=['POST'])
def train_data():
    try:
        model_type = request.json.get('model_type')
        args = request.json.get('args')
        
        file_id = args.get("file_id")
        file_name = args.get("file_name", "tmp_dataset.joblib")
        download_path = f"tmp/{file_name}"
        os.makedirs("tmp", exist_ok=True)
        download_file(file_id, download_path)
        dataset = joblib.load(download_path)

        if model_type == "time_series":
            model = TimeSeriesModel(dataset=dataset, date_column=args["date_column"], target_column=args["target_column"])
            model.train()
            return jsonify({"message": "TimeSeriesModel training complete"}), 200
        
        elif model_type == "nlp":
            model = NLPModel(dataset=dataset, text_columns=args["text_columns"], target_column=args["target_column"])
            model.train()
            return jsonify({"message": "NLPModel training complete"}), 200
        
        elif model_type == "classifier":
            model = Classifier(dataset=dataset, features=args["features"], target=args["target_column"])
            model.train_model()
            return jsonify({"message": "Classifier training complete"}), 200
        
        elif model_type == "regression":
            model = Regressor(dataset=dataset.get_data(), target=args["target_column"], exclude=args.get("exclude_columns", []))
            model.train_model()
            return jsonify({"message": "Regressor training complete"}), 200
        
        else:
            return jsonify({"error": "Invalid model type"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400