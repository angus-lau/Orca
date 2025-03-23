from flask import Flask, request, jsonify
from upload import upload_file
from download import list_files_in_folder, download_file
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from models.dataset import Dataset
from models.timeseries import TimeSeriesModel
from models.nlpmodel import NLPModel
from models.classification import Classifier
from models.regression import Regressor
import joblib

SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_IDS = {
    'models': '1vLuyS9c-r_kYkN_NZVLLbckdGGiXNOKi',
    'joblib': '1Yr4Q81G-xlvsJinw685W2DgREMj1LZuq'
}

app = Flask(__name__)

def get_service():
    creds = service_account.Credentials.from_service_account_file(
        'service_account.json', scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

@app.route('/')
def home():
    return "🚀 ORCA Flask API is running!"

@app.route('/upload', methods=['POST'])
def handle_upload():
    file_path = request.json.get('file_path')
    prompt = request.json.get('prompt')  # temporary placeholder for prompt

    if not file_path:
        return jsonify({'error': 'file_path is required'}), 400

    try:
        print(f"Received prompt: {prompt}")  # temporary
        # If it's a CSV, convert it to a joblib file first
        if file_path.endswith(".csv"):
            import pandas as pd
            df = pd.read_csv(file_path)
            new_path = file_path.replace(".csv", ".joblib")
            joblib.dump(df, new_path)
            file_path = new_path  # now upload the converted file

        upload_file(file_path)
        return jsonify({'message': 'File uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list/<folder_key>', methods=['GET'])
def list_files(folder_key):
    folder_id = FOLDER_IDS.get(folder_key)
    if not folder_id:
        return jsonify({'error': 'Invalid folder key'}), 400

    service = get_service()
    files = list_files_in_folder(service, folder_id)
    return jsonify(files)

@app.route('/download', methods=['POST'])
def handle_download():
    file_id = request.json.get('file_id')
    file_name = request.json.get('file_name')
    print(f"Received file_id: {file_id}")
    print(f"Received file_name: {file_name}")
    
    if not file_id or not file_name:
        return jsonify({'error': 'file_id and file_name are required'}), 400

    try:
        os.makedirs('downloads', exist_ok=True)
        download_path = f"downloads/{file_name}"
        print(f"Download path: {download_path}")
        download_file(file_id, download_path)
        print("Download successful.")
        return jsonify({'message': 'File downloaded successfully'})
    except Exception as e:
        print(f"Download failed with error: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/folders', methods=['GET'])
def list_folder_keys():
    return jsonify(list(FOLDER_IDS.keys()))

@app.route('/load_data', methods=['POST'])
def load_data():
    try:
        data_path = request.json.get('data_path')
        dataset = joblib.load(data_path)
        return jsonify({"message": "Dataset loaded successfully", "columns": dataset.columns.tolist()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/train_data', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True, port=5001)