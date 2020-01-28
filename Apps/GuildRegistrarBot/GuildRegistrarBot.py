import sys
sys.path.append('../..')

import discord
from datetime import datetime

from WarcraftProject import WarcraftProject
from Discord import Message
from Apps.GuildRegistrarBot import Forms
import Time
import Cfg

COMMANDS = ['!register', '!character', '!finished']

class Bot(discord.Client):
	def __init__(self, WP, guild_name, server, region):
		discord.Client.__init__(self)
		self.WP = WP
		self.guild_name = guild_name
		self.server = server
		self.region = region

	def discordName(self, user):
		return '{0}#{1}'.format(user.name, user.discriminator)

	def clearForms(self, DiscordUser):
		if getattr(DiscordUser, 'RegistrarForm', None) is not None:
			self.WP.Firebase.delete(DiscordUser, 'RegistrarForm')
			self.WP.Drive.deleteFile(DiscordUser.RegistrarForm.get('id'))
		if getattr(DiscordUser, 'CharacterForm', None) is not None:
			self.WP.Firebase.delete(DiscordUser, 'CharacterForm')
			self.WP.Drive.deleteFile(DiscordUser.CharacterForm.get('id'))

	async def on_ready(self):
		print('We have logged on.\nUser: {0}'.format(self.user))

	async def on_message(self, message):

		if message.author == self.user:
			return

		if message.content == COMMANDS[0]:
			discord_name = self.discordName(message.author)
			discord_id = str(message.author.id)
			DiscordUser = self.WP.Firebase.fetch(self.WP.WPObj({'type': 'DiscordUser', 'id': discord_id}))
			self.clearForms(DiscordUser)
			form_dict = Forms.createDiscordForm(WP=self.WP, guild_name=self.guild_name, discord_name=discord_name)
			DiscordUser = self.WP.WPObj({'type': 'DiscordUser', 'id': discord_id, 'name': discord_name, 'RegistrarForm': form_dict})
			self.WP.Firebase.set(DiscordUser)
			await Message.message(message.author, 'Please visit the following link and submit your response. When you have submitted, please message me with **`{command}`**.\n{url}'.format(command=COMMANDS[2], url=form_dict.get('url')))
			return

		if message.content == COMMANDS[1]:
			discord_name = self.discordName(message.author)
			discord_id = str(message.author.id)
			DiscordUser = self.WP.Firebase.fetch(self.WP.WPObj({'type': 'DiscordUser', 'id': discord_id}))
			self.clearForms(DiscordUser)
			if getattr(DiscordUser, 'registeredOn', None) is None:
				await Message.message(message.author, 'You must first register yourself with **`{command}`** before you can register any characters!'.format(command=COMMANDS[0]))
			else:
				form_dict = Forms.createCharacterForm(WP=self.WP, guild_name=self.guild_name, discord_name=discord_name)
				DiscordUser = self.WP.WPObj({'type': 'DiscordUser', 'id': discord_id, 'name': discord_name, 'CharacterForm': form_dict})
				self.WP.Firebase.set(DiscordUser)
				await Message.message(message.author, 'Please visit the following link and submit your response. When you have submitted, please message me with **`{command}`**.\n{url}'.format(command=COMMANDS[2], url=form_dict.get('url')))
			return

		if message.content == COMMANDS[2]:
			discord_name = self.discordName(message.author)
			discord_id = str(message.author.id)
			DiscordUser = self.WP.Firebase.fetch(self.WP.WPObj({'type': 'DiscordUser', 'id': discord_id}))

			if getattr(DiscordUser, 'RegistrarForm', None) is None and getattr(DiscordUser, 'CharacterForm', None) is None:
				await Message.message(message.author, 'You have no active forms to be finished with!')

			if getattr(DiscordUser, 'RegistrarForm', None) is not None:
				formResponses = Forms.getForm(WP=self.WP, form_dict=DiscordUser.RegistrarForm)
				if formResponses is not None:
					self.clearForms(DiscordUser)
					DiscordUser = Forms.formToDiscordUser(WP=self.WP, response=formResponses, guild_name=self.guild_name, discord_name=discord_name, discord_id=discord_id)
					self.WP.Firebase.set(DiscordUser)
					await Message.message(message.author, 'You have been successfully registered! You may now register characters with **`{command}`**'.format(command=COMMANDS[1]))
				else:
					await Message.message(message.author, 'Your submission was empty!')

			if getattr(DiscordUser, 'CharacterForm', None) is not None:
				formResponses = Forms.getForm(WP=self.WP, form_dict=DiscordUser.CharacterForm)
				if formResponses is not None:
					self.clearForms(DiscordUser)
					Character = Forms.formToCharacter(WP=self.WP, response=formResponses, discord_name=discord_name, server=self.server, region=self.region, discord_id=discord_id)
					self.WP.Firebase.set(Character)
					await Message.message(message.author, 'Your character has been successfully registered!')
				else:
					await Message.message(message.author, 'Your submission was empty!')

			return

def main():
	MyWP = WarcraftProject(firebase=True, drive=True, appsscript=True)

	guild_name = Cfg.read('guild_name')
	server = Cfg.read('server')
	region = Cfg.read('region')
	MyBot = Bot(WP=MyWP, guild_name=guild_name, server=server, region=region)

	id_ = Cfg.read('id')
	MyBot.run(id_)

if __name__ == '__main__':
	main()