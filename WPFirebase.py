class Firebase:
	def __init__(self, WP):
		self.WP = WP
		self.client = WP.firebase_client

	def fetch(self, wpobj):
		try:
			dict_ = wpobj.__dict__
			type_ = dict_.get('type')
			if type_ is not 'NoType':
				id_ = dict_.get('id')
				if id_ is not 'NoId':
					db = self.client.fetchById(dict_.get('type'), dict_.get('id'))
					if db is not None:
						return self.WP.WPObj(db)
				else:
					db_list = self.client.fetchByKeys(type_, dict_)
					if db_list:
						WPObj_list = []
						for val in db_list:
							WPObj_list.append(self.WP.WPObj(val))
							return WPObj_list
		except Exception as e:
			print(e)
			return None

	def set(self, wpobj, update=True):
		try:
			self.client.set(wpobj.__dict__, update)
			return True
		except Exception as e:
			print(e)
			return None

	def delete(self, wpobj, key):
		try:
			type_ = wpobj.type
			id_ = wpobj.id
			if type_ is not 'NoType' and id_ is not 'NoId':
				self.client.deleteField(type_, id_, key)
				return True
		except Exception as e:
			print(e)
			return None