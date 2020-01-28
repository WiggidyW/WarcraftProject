import sys
sys.path.append('..')

from googleapiclient import errors
from googleapiclient.discovery import build
from Google import Auth

SCOPES = ['https://www.googleapis.com/auth/drive']

class Drive:
	def __init__(self):
		creds = Auth.loadCreds(SCOPES, 'drive')
		self.service = build('drive', 'v3', credentials=creds)

	def deleteFile(self, id_):
		self.service.files().delete(fileId=id_).execute()