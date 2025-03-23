import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
test_file_path = 'persistance/microsoft.joblib'

folder_ids = {
    'joblib': ['1Yr4Q81G-xlvsJinw685W2DgREMj1LZuq'],
    'models': ['1vLuyS9c-r_kYkN_NZVLLbckdGGiXNOKi']
}

def get_drive_folder(file_path):
    ext = os.path.splitext(file_path)[1].lstrip('.').lower()
    return folder_ids.get(ext, folder_ids['models'])

def upload_file(file_path=test_file_path):
    file_name = os.path.basename(file_path)
    folder_id = get_drive_folder(file_path)

    file_metadata = {
        'name': file_name,
        'parents': folder_id
    }

    media = MediaFileUpload(file_path, mimetype='application/octet-stream')

    # Authenticate using the service account key
    creds = service_account.Credentials.from_service_account_file(
        'service_account.json', scopes=SCOPES)

    # Build the Drive service
    service = build('drive', 'v3', credentials=creds)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"Uploaded file ID: {file.get('id')}")

# Run upload for test file
upload_file()