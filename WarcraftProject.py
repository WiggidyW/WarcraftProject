from Google import Drive, AppsScript
from Firebase import Firebase
import Cfg

import WPAppsScript
import WPDrive
import WPFirebase

class WPObj:
	def __init__(self, dict_):
		self.id = None
		self.type = None
		for key, value in dict_.items():
			if key is not None and value is not None:
				setattr(self, key, value)
		if self.id is None:
			self.id = 'NoId'
		if self.type is None:
			self.type = 'NoType'

class WarcraftProject:
	def __init__(self, firebase=False, appsscript=False, drive=False):
		if firebase:
			self.firebase_client = Firebase.Firebase(Cfg.read('firebase_cert'))
			self.Firebase = WPFirebase.Firebase(self)
		if appsscript:
			self.appsscript_client = AppsScript.AppsScript(Cfg.read('appsscript_id'))
			self.AppsScript = WPAppsScript.AppsScript(self)
		if drive:
			self.drive_client = Drive.Drive()
			self.Drive = WPDrive.Drive(self)

	def WPObj(self, dict_):
		return WPObj(dict_)

	def characterId(self, name='NoName', server='NoServer', region='NoRegion'):
		return '{0}-{1}-{2}'.format(name, server, region)