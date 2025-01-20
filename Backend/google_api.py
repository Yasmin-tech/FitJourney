#!/usr/bin/env python3
""" Access Google Drive API """
from google.oauth2 import service_account
from googleapiclient.discovery import build, MediaFileUpload
from googleapiclient.errors import HttpError, UnknownFileType
import os
import urllib.parse


# Path to the service account Json key file
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Create a service account credentials object
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive'])

# Build the service object
service = build('drive', 'v3', credentials=credentials)

# Test connection to the Google Drive API
def list_drive_files(service):
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

# Call the function to list files
# list_drive_files(service)

class ManageDrive:
    """ Manage Google Drive """
    def __init__(self):
        self.service = service
        self.root_folder_id = self.find_folder_id('FitJourney')
        self.users_folder_id = self.find_folder_id('Users', self.root_folder_id)
        self.default_exercises_folder = self.find_folder_id("default_exercises", self.root_folder_id)

    def find_folder_id(self, folder_name, parent_id=None):
        """ Find a folder by name and return the folder id """
        try:
            if parent_id:
                query = f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder'"
            else:
                query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
            
            results = self.service.files().list(q=query, spaces='drive', fields="files(id, name)").execute()
            items = results.get('files', [])
            if not items:
                # print(f"Folder '{folder_name}' not found.")
                return None
            return items[0]['id']
        except HttpError as e:
            print(f"An error occurred while finding folder '{folder_name}': {e}")
            return None 

    def create_folder(self, folder_name, parent_id=None):
        """ Create a folder """
        try:  
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                file_metadata['parents'] = [parent_id]

            folder = self.service.files().create(body=file_metadata, fields='id').execute()
            return folder.get('id')
        except HttpError as e:
            # print(f"An error occurred while creating folder '{folder_name}': {e}")
            return None

    def find_file_id(self, file_name, parent_id=None):
        """ Find a file by name and return the file id """
        try:
            if parent_id:
                query = f"name='{file_name}' and '{parent_id}' in parents"
            else:
                query = f"name='{file_name}'"
            
            results = self.service.files().list(q=query, spaces='drive', fields="files(id, name, webContentLink)").execute()
            items = results.get('files', [])
            if not items:
                # print(f"File '{file_name}' not found.")
                return None, None
            return items[0]['id'], items[0]['webContentLink']
        
        except HttpError as e:
            print(f"An error occurred while finding file '{file_name}': {e}")
            return None, None

    def upload_file(self, file_name, folder_id):
        """ Upload a file """
        try:
            file_metadata = {
                'name': os.path.basename(file_name),
                'parents': [folder_id]
            }
            media = MediaFileUpload(file_name, resumable=True)
            file = service.files().create(
                body=file_metadata,
                media_body=file_name,
                fields='id, webViewLink, webContentLink').execute()
            print(f"File '{file_name}' uploaded successfully with ID: {file.get('id')}")
    
            # Set file permissions to be accessible by anyone with the link
            permission = { 'type': 'anyone', 'role': 'reader' }
            self.service.permissions().create( fileId=file.get('id'), body=permission ).execute()
            # print(f"Permissions set for file ID: {file.get('id')}")
        
            return file.get('id'), True, file.get('webContentLink')
        except (HttpError, UnknownFileType) as e:
            print(f"An error occurred while uploading file '{file_name}': {e}")
            if isinstance(e, UnknownFileType):
                return None, False, None
            return None, True, None

    def list_files(self):
        """ List files in Google Drive """
        results = self.service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            return 'No files found.'
        files = []
        for item in items:
            files.append(f"{item['name']} ({item['id']})")
        return files

    def download_file(self, file_id):
        """ Download a file """
        request = self.service.files().get_media(fileId=file_id)
        fh = open(file_id, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return 'Downloaded'

    def delete_file(self, file_id=None, webContentLink=None):
        """ Delete a file """
        id = file_id
        try:
            if not id:
                if webContentLink:
                    # extract the file id from the webContentLink
                    url_parsed = urllib.parse.urlparse(webContentLink)
                    id = urllib.parse.parse_qs(url_parsed.query).get("id", None)
                    if not id:
                        return False, 'Invalid webContentLink provided'
                else:
                    return False, 'No file id or webContentLink provided'
            self.service.files().delete(fileId=id[0]).execute()
            return True, 'File deleted successfully'
        except HttpError as e:
            return False, f"An error occurred while deleting file: {e}"

    def delete_folder(self, folder_id):
        """ Delete a folder """
        try:
            self.service.files().delete(fileId=folder_id).execute()
            return True, 'Folder deleted successfully'
        except HttpError as e:
            return False, f"An error occurred while deleting folder: {e}"
