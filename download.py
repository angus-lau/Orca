from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io

SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_IDS = {
    'models': '1vLuyS9c-r_kYkN_NZVLLbckdGGiXNOKi',
    'joblib': '1Yr4Q81G-xlvsJinw685W2DgREMj1LZuq'
}

def prompt_folder_choice():
    print("\n📁 Available folders:")
    for i, name in enumerate(FOLDER_IDS):
        print(f"[{i}] {name}")
    
    choice = input("Select a folder by number: ")
    try:
        idx = int(choice)
        folder_name = list(FOLDER_IDS.keys())[idx]
        return folder_name, FOLDER_IDS[folder_name]
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        return None, None

def prompt_user_for_file(files):
    choice = input("\nEnter the number of the file to download: ")
    try:
        index = int(choice)
        return files[index]
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        return None

def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
        pageSize=100
    ).execute()

    files = results.get('files', [])
    if not files:
        print("No files found in folder.")
        return []

    print("\n📂 Files in Folder:")
    for i, file in enumerate(files):
        print(f"[{i}] {file['name']} (ID: {file['id']})")
    return files

def download_file(file_id, destination_path):
    # Authenticate using the service account key
    creds = service_account.Credentials.from_service_account_file(
        'service_account.json', scopes=SCOPES)

    # Build the Drive service
    service = build('drive', 'v3', credentials=creds)

    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download progress: {int(status.progress() * 100)}%")

    print(f"File downloaded to: {destination_path}")

def main():
    creds = service_account.Credentials.from_service_account_file(
        'service_account.json', scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    folder_name, folder_id = prompt_folder_choice()
    if not folder_id:
        return

    files = list_files_in_folder(service, folder_id)
    if not files:
        return

    selected = prompt_user_for_file(files)
    if selected:
        file_id = selected['id']
        download_path = f"downloads/{selected['name']}"
        download_file(file_id, download_path)