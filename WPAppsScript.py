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
		list_ = self.client.Forms.create(wpobj.id, question_list)
		form_dict = {
			'id': list_[0],
			'url': list_[1],
			'edit_url': list_[2]
		}
		return form_dict

	def read(self, form_id):
		formResponses = self.client.Forms.read(form_id)
		return formResponses

	def mostRecentResponse(self, formResponses):
		if formResponses is not None:
			return formResponses[len(formResponses)-1]

	def WPObjFromFormResponse(self, formResponse, fields):
		dict_ = {}
		if formResponse is not None:
			for i in range(0, len(fields)):
				if formResponse[i+2] != '':
					dict_.update({fields[i]: formResponse[i+2]})
		WPObj = self.AppsScript.WP.WPObj(dict_)
		return WPObj