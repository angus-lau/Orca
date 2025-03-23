from flask import Blueprint, jsonify, request
from download import download_file, list_files_in_folder
from app import get_service, FOLDER_IDS
import joblib
import os

data_bp = Blueprint('data', __name__)

@data_bp.route('/list/<folder_key>', methods=['GET'])
def list_files(folder_key):
    folder_id = FOLDER_IDS.get(folder_key)
    if not folder_id:
        return jsonify({'error': 'Invalid folder key'}), 400
    service = get_service()
    return jsonify(list_files_in_folder(service, folder_id))

@data_bp.route('/folders', methods=['GET'])
def list_folder_keys():
    return jsonify(list(FOLDER_IDS.keys()))

@data_bp.route('/download', methods=['POST'])
def handle_download():
    file_id = request.json.get('file_id')
    file_name = request.json.get('file_name')
    if not file_id or not file_name:
        return jsonify({'error': 'file_id and file_name are required'}), 400

    try:
        os.makedirs('downloads', exist_ok=True)
        download_file(file_id, f"downloads/{file_name}")
        return jsonify({'message': 'File downloaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@data_bp.route('/load_data', methods=['POST'])
def load_data():
    try:
        data_path = request.json.get('data_path')
        dataset = joblib.load(data_path)
        return jsonify({"message": "Dataset loaded successfully", "columns": dataset.columns.tolist()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400