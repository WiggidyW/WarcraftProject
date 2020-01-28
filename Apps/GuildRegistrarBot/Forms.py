import sys
sys.path.append('../..')

import Time

def createDiscordForm(WP, guild_name, discord_name):

	def friends():
		guildUsers = WP.Firebase.fetch(WP.WPObj({'type': 'DiscordUser', 'guild': guild_name}))
		friend_name_list = []
		if guildUsers:
			for guildUser in guildUsers:
				if getattr(guildUser, 'moniker', None) is not None:
					friend_name_list.append(guildUser.moniker)
		if friend_name_list == []:
			friend_name_list.append('')
		return friend_name_list

	questions = [{
		'type': 'Text',
		'title': 'What is your preferred online moniker? (e.g. Steve, xSlayer48, NodeVampire, etc.)'
		}, {
		'type': 'Checkbox',
		'title': 'What is your availability for raiding? (please base this on your evening availability)',
		'choices': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
		}, {
		'type': 'Checkbox',
		'title': 'Who were you friends with before joining the Guild?',
		'choices': friends()
		}]

	WPObj = WP.WPObj({'type': 'DiscordUser', 'id': discord_name})
	form_dict = WP.AppsScript.Forms.create(WPObj, questions)
	return form_dict

def createCharacterForm(WP, guild_name, discord_name):

	questions = [{
		'type': 'Text',
		'title': 'What is the name of your character?'
		}, {
		'type': 'MultipleChoice',
		'title': 'What is your character\'s class?',
		'choices': ['Druid', 'Hunter', 'Mage', 'Priest', 'Rogue', 'Shaman', 'Warlock', 'Warrior']
		}, {
		'type': 'MultipleChoice',
		'title': 'What is your character\'s role?',
		'choices': ['DPS', 'Tank', 'Healer']
		}, {
		'type': 'Text',
		'title': 'What guild is your character in?'
		}]

	WPObj = WP.WPObj({'type': 'DiscordUser', 'id': discord_name})
	form_dict = WP.AppsScript.Forms.create(WPObj, questions)
	return form_dict

def getForm(WP, form_dict):
	responses = WP.AppsScript.Forms.read(form_dict.get('id'))
	return WP.AppsScript.Forms.mostRecentResponse(responses)

def formToDiscordUser(WP, response, guild_name, discord_name, discord_id):
	fields = ['moniker', 'availability', 'friends']
	DiscordUser = WP.AppsScript.Forms.WPObjFromFormResponse(response, fields)
	updateDict = {'type': 'DiscordUser', 'name': discord_name, 'id': discord_id, 'guild': guild_name, 'registeredOn': Time.dateTime()}
	for key, value in updateDict.items():
		setattr(DiscordUser, key, value)
	return DiscordUser

def formToCharacter(WP, response, discord_name, server, region, discord_id):
	fields = ['name', 'class', 'role', 'guild']
	Character = WP.AppsScript.Forms.WPObjFromFormResponse(response, fields)
	updateDict = {'type': 'Character', 'name': getattr(Character, 'name', 'NoName'),
		'discordId': discord_id, 'discordName': discord_name, 'server': server,
		'region': region, 'registeredOn': Time.dateTime(),
		'id': WP.characterId(name=getattr(Character, 'name', 'NoName'), server=server, region=region)}
	for key, value in updateDict.items():
		setattr(Character, key, value)
	return Character

def deleteForm(WP, form_dict):
	WP.Drive.deleteFile(form_dict.get('id'))