import sys
sys.path.append('..')

from googleapiclient import errors
from googleapiclient.discovery import build
from Google import Auth

SCOPES = ['https://www.googleapis.com/auth/script.projects', 'https://www.googleapis.com/auth/forms']
FUNCTION = 'myFunction'

class AppsScript:
	def __init__(self, script_id):
		creds = Auth.loadCreds(SCOPES, 'appsscript')
		self.service = build('script', 'v1', credentials=creds)
		self.script_id = script_id
		self.function = FUNCTION
		self.Forms = self.Forms(self)

	def run(self, code):
		try:
			request = {
				'function': self.function,
				'parameters': [code]
			}
			response = self.service.scripts().run(body=request, scriptId=self.script_id).execute()
			return response
		except errors.HttpError as error:
			print('Error running Function:\n{0}'.format(error))
			return None

	class Forms:
		def __init__(self, AppsScript):
			self.run = AppsScript.run
			self.script_id = AppsScript.script_id
			self.service = AppsScript.service
			self.function = AppsScript.function

		def create(self, id_, list_):
			def multipleChoice(code, type_, title, choices):
				formatted_choices = []
				for value in choices:
					formatted_choices.append('"{0}"'.format(value))
				code.append('var item = form.add{0}Item();'.format(type_))
				code.append('item.setTitle("{0}");'.format(title))
				code.append('item.setChoiceValues({0});'.format(choices))

			def text(code, type_, title):
				code.append('var item = form.add{0}Item();'.format(type_))
				code.append('item.setTitle("{0}");'.format(title))

			code = ['var form = FormApp.create("{0}");'.format(id_)]
			for dict_ in list_:
				type_ = dict_.get('type')
				if type_ == 'Checkbox' or type_ == 'MultipleChoice':
					multipleChoice(code, type_, dict_.get('title'), dict_.get('choices'))
				elif type_ == 'Text' or type_ == 'ParagraphText':
					text(code, type_, dict_.get('title'))
				code.append('returnVal = [form.getId(), form.getPublishedUrl(), form.getEditUrl()];')

			response = self.run(code)
			try:
				return response['response']['result']
			except KeyError:
				return None

		# Returns 2D Array of following rows:
		# [ResponseID, Timestamp, QuestionAnswer1, ..., QuestionAnswerN]
		def read(self, id_):
			code = []
			code.append('returnVal = [];')
			code.append('var form = FormApp.openById("{0}");'.format(id_))
			code.append('returnVal[0] = form.getResponses().length;')
			code.append('returnVal[1] = form.getItems().length;')
			response = self.run(code)
			try:
				response_count = response['response']['result']
			except KeyError:
				return None

			code = []
			code.append('returnVal = [];')
			code.append('var form = FormApp.openById("{0}");'.format(id_))
			code.append('var formResponses = form.getResponses();')
			for i in range(0, response_count[0]):
				code.append('var tempArr = [formResponses[{i}].getId(), formResponses[{i}].getTimestamp().toString()];'.format(i=i))
				code.append('var itemResponses = formResponses[{i}].getItemResponses();'.format(i=i))
				for j in range(0, response_count[1]):
					code.append('try {{tempArr[{jPlus}] = itemResponses[{j}].getResponse();}}'.format(jPlus=j+2, j=j) +
						'catch (e) {{tempArr[{jPlus}] = "";}}'.format(jPlus=j+2))
				code.append('returnVal[{i}] = tempArr;'.format(i=i))
			response = self.run(code)
			try:
				return response['response']['result']
			except KeyError:
				return None