from flask import Blueprint, request, jsonify
from upload import upload_file
import joblib
import pandas as pd

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def handle_upload():
    file_path = request.json.get('file_path')
    prompt = request.json.get('prompt')

    if not file_path:
        return jsonify({'error': 'file_path is required'}), 400

    try:
        print(f"Received prompt: {prompt}")
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
            file_path = file_path.replace(".csv", ".joblib")
            joblib.dump(df, file_path)

        upload_file(file_path)
        return jsonify({'message': 'File uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500