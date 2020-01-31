class Drive:
	def __init__(self, WP):
		self.WP = WP
		self.client = WP.drive_client

	def deleteFile(self, id_):
		try:
			self.client.deleteFile(id_)
			return True
		except Exception as e:
			print(e)
			return None