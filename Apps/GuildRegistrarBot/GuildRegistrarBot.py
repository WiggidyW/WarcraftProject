import sys
sys.path.append('../..')

import discord
from datetime import datetime

from WarcraftProject import WarcraftProject
from Discord import Message
from Apps.GuildRegistrarBot import Forms
import Time
import Cfg

COMMANDS = ['!register', '!finished', '!self', '!character', '!professions']

class Bot(discord.Client):
	def __init__(self, WP, guild_name, server, region):
		discord.Client.__init__(self)
		self.WP = WP
		self.guild_name = guild_name
		self.server = server
		self.region = region
		self.commands = COMMANDS

	def discordName(self, user):
		return '{0}#{1}'.format(user.name, user.discriminator)

	def clearForms(self, DiscordUser):
		if getattr(DiscordUser, 'RegistrarForm', None) is not None:
			self.WP.Firebase.delete(DiscordUser, 'RegistrarForm')
			self.WP.Drive.deleteFile(DiscordUser.RegistrarForm.get('id'))
		if getattr(DiscordUser, 'CharacterForm', None) is not None:
			self.WP.Firebase.delete(DiscordUser, 'CharacterForm')
			self.WP.Drive.deleteFile(DiscordUser.CharacterForm.get('id'))
		if getattr(DiscordUser, 'ProfessionsForm', None) is not None:
			self.WP.Firebase.delete(DiscordUser, 'ProfessionsForm')
			self.WP.Drive.deleteFile(DiscordUser.ProfessionsForm.get('id'))

	async def on_ready(self):
		print('We have logged on.\nUser: {0}'.format(self.user))

	async def on_message(self, message):

		if message.author == self.user:
			return

		if message.content in self.commands:
			
			if message.guild is not None:
				await Message.message(message.channel, 'That command can only be used when it is sent as a direct message to me!')
				return

			discord_name = self.discordName(message.author)
			discord_id = str(message.author.id)
			DiscordUser = self.WP.Firebase.fetch(self.WP.WPObj({'type': 'DiscordUser', 'id': discord_id}))

			if message.content == self.commands[1]:
				if getattr(DiscordUser, 'RegistrarForm', None) is not None:
					formResponses = Forms.getForm(WP=self.WP, form_dict=DiscordUser.RegistrarForm)
					if formResponses is not None:
						self.clearForms(DiscordUser)
						DiscordUser = Forms.formToDiscordUser(WP=self.WP, response=formResponses, guild_name=self.guild_name, discord_id=discord_id)
						self.WP.Firebase.set(DiscordUser)
						await Message.message(message.author, 'You have been successfully registered!')
					else:
						await Message.message(message.author, 'Your submission was empty!')

				elif getattr(DiscordUser, 'CharacterForm', None) is not None:
					formResponses = Forms.getForm(WP=self.WP, form_dict=DiscordUser.CharacterForm)
					if formResponses is not None:
						self.clearForms(DiscordUser)
						Character = Forms.formToCharacter(WP=self.WP, response=formResponses, discord_name=discord_name, server=self.server, region=self.region, discord_id=discord_id)
						self.WP.Firebase.set(Character)
						await Message.message(message.author, 'Your character has been successfully registered!')
					else:
						await Message.message(message.author, 'Your submission was empty!')

				elif getattr(DiscordUser, 'ProfessionsForm', None) is not None:
					formResponses = Forms.getForm(WP=self.WP, form_dict=DiscordUser.ProfessionsForm)
					if formResponses is not None:
						self.clearForms(DiscordUser)
						Professions = Forms.formToProfessions(WP=self.WP, response=formResponses, discord_id=discord_id)
						self.WP.Firebase.set(Professions)
						await Message.message(message.author, 'Your professions have been successfully registered!')
					else:
						await Message.message(message.author, 'Your submission was empty!')

				else:
					await Message.message(message.author, 'You have no active forms to be finished with!')

				return

			self.clearForms(DiscordUser)

			if message.content == self.commands[2]:
				form_dict = Forms.createDiscordForm(WP=self.WP, guild_name=self.guild_name, discord_name=discord_name)
				DiscordUser = self.WP.WPObj({'type': 'DiscordUser', 'id': discord_id, 'name': discord_name, 'RegistrarForm': form_dict})
				self.WP.Firebase.set(DiscordUser)
				await Message.message(message.author, 'Please visit the following link and submit your response. When you have submitted, please message me with **`{command}`**.\n{url}'.format(command=self.commands[1], url=form_dict.get('url')))
				return

			elif message.content == self.commands[3]:
				if getattr(DiscordUser, 'registeredOn', None) is None:
					await Message.message(message.author, 'You must first register yourself with **`{command}`** before you can register any characters!'.format(command=self.commands[2]))
				else:
					form_dict = Forms.createCharacterForm(WP=self.WP, guild_name=self.guild_name, discord_name=discord_name)
					DiscordUser = self.WP.WPObj({'type': 'DiscordUser', 'id': discord_id, 'name': discord_name, 'CharacterForm': form_dict})
					self.WP.Firebase.set(DiscordUser)
					await Message.message(message.author, 'Please visit the following link and submit your response. When you have submitted, please message me with **`{command}`**.\n{url}'.format(command=self.commands[1], url=form_dict.get('url')))
				return

			elif message.content == self.commands[4]:
				if getattr(DiscordUser, 'registeredOn', None) is None:
					await Message.message(message.author, 'You must first register yourself with **`{command}`** before you can register professions!'.format(command=self.commands[2]))
				else:
					form_dict = Forms.createProfessionsForm(WP=self.WP, guild_name=self.guild_name, discord_name=discord_name, discord_id=discord_id)

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