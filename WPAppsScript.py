class AppsScript:
	def __init__(self, WP):
		self.WP = WP
		self.client = WP.appsscript_client
		self.Forms = Forms(self)

class Forms:
	def __init__(self, AppsScript):
		self.AppsScript = AppsScript
		self.client = AppsScript.client

	def create(self, wpobj, question_list):
		try:
			list_ = self.client.Forms.create(wpobj.id, question_list)
			form_dict = {
				'id': list_[0],
				'url': list_[1],
				'edit_url': list_[2]
			}
			return form_dict
		except Exception as e:
			print(e)
			return None

	def read(self, form_id):
		try:
			formResponses = self.client.Forms.read(form_id)
			return formResponses
		except Exception as e:
			print(e)
			return None

	def mostRecentResponse(self, formResponses):
		try:
			if formResponses is not None:
				return formResponses[len(formResponses)-1]
		except Exception as e:
			print(e)
			return None

	def WPObjFromFormResponse(self, formResponse, fields):
		try:
			dict_ = {}
			if formResponse is not None:
				for i in range(0, len(fields)):
					if formResponse[i+2] != '':
						dict_.update({fields[i]: formResponse[i+2]})
			WPObj = self.AppsScript.WP.WPObj(dict_)
			return WPObj
		except Exception as e:
			print(e)
			return None