class Drive:
	def __init__(self, WP):
		self.WP = WP
		self.client = WP.drive_client

	def deleteFile(self, id_):
		self.client.deleteFile(id_)