import sys
sys.path.append('..')

import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SECRETS_FILE = 'credentials.json'

def loadCreds(scopes, token):
	creds = None

	if os.path.exists('{0}.pickle'.format(token)):
		with open('{0}.pickle'.format(token), 'rb') as my_token:
			creds = pickle.load(my_token)

	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(SECRETS_FILE, scopes)
			creds = flow.run_local_server(port=0)
		with open('{0}.pickle'.format(token), 'wb') as my_token:
			pickle.dump(creds, my_token)

	return creds