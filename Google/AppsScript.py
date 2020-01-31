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
		request = {
			'function': self.function,
			'parameters': [code]
		}
		response = self.service.scripts().run(body=request, scriptId=self.script_id).execute()
		return response

	class Forms:
		def __init__(self, AppsScript):
			self.AppsScript = AppsScript

		# Creates a new form. ID is the title of the form, and list is a list of dictionaries that define questions for the form.
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

			response = self.AppsScript.run(code)
			return response['response']['result']

		# Returns 2D Array of following rows:
		# [ResponseID, Timestamp, QuestionAnswer1, ..., QuestionAnswerN]
		def read(self, id_):
			code = []
			code.append('returnVal = [];')
			code.append('var form = FormApp.openById("{0}");'.format(id_))
			code.append('returnVal[0] = form.getResponses().length;')
			code.append('returnVal[1] = form.getItems().length;')
			response = self.AppsScript.run(code)
			response_count = response['response']['result']

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
			response = self.AppsScript.run(code)
			return response['response']['result']

		# Takes a form dictionary returned by create() and sets default responses, and then returns the URL for that form.
		def createFormResponse(self, formArr, answers):
			code = []
			code.append('var form = FormApp.openById("{0}");'.format(formArr[0]))
			code.append('var items = form.getItems();')
			code.append('var formResponse = form.createResponse();')
			i = 0
			for answer in answers:
				if answer:
					if answer != '':
						code.append('var item = items[{i}];'.format(i=i))
						code.append('if (item.getType() == FormApp.ItemType.CHECKBOX) {item = item.asCheckboxItem();}')
						code.append('if (item.getType() == FormApp.ItemType.TEXT) {item = item.asTextItem();}')
						code.append('if (item.getType() == FormApp.ItemType.PARAGRAPH_TEXT) {item = item.asParagraphTextItem();}')
						code.append('if (item.getType() == FormApp.ItemType.MULTIPLE_CHOICE) {item = item.asMultipleChoiceItem();}')
						if isinstance(answer, list):
							for item in answer:
								item = '"{0}"'.format(item)
							code.append('var itemResponse = item.createResponse({answer});'.format(answer=answer))
						elif isinstance(answer, str):
							code.append('var itemResponse = item.createResponse("{answer}");'.format(answer=answer))
						code.append('formResponse.withItemResponse(itemResponse);')
				i += 1
			code.append('returnVal = formResponse.toPrefilledUrl();')
			response = self.AppsScript.run(code)
			return response['response']['result']