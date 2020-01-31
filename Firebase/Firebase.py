import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class Firebase:
	def __init__(self, cert):
		cred = credentials.Certificate(cert)
		firebase_admin.initialize_app(cred)
		self.client = firestore.client()

	# Retrieves a specific document by its ID.
	def fetchById(self, base, id_):
		ref = self.client.collection(base).document(id_)
		doc_snapshot = ref.get()
		if doc_snapshot:
			dict_ = doc_snapshot.to_dict()
			return dict_

	# Retrieves all documents that match the key:value pairs in the dictionary.
	def fetchByKeys(self, base, dict_):
		ref = self.client.collection(base)
		for key, value in dict_.items():
			if key is not None and value is not None:
				ref.where(key, '==', value)
		doc_stream = ref.get()
		if doc_stream:
			dict_list = []
			for doc_snapshot in doc_stream:
				dict_list.append(doc_snapshot.to_dict())
			return dict_list

	# Inputs a document into the Firestore. Only key:values that already exist will be replaced.
	def set(self, dict_, update=True):
		id_ = dict_.get('id')
		type_ = dict_.get('type')
		ref = self.client.collection(type_).document(id_)
		ref.set(dict_, merge=update)

	# Deletes a key:value pair for a specific document located by its ID.
	def deleteField(self, base, id_, key):
		ref = self.client.collection(base).document(id_)
		ref.update({key: firestore.DELETE_FIELD})