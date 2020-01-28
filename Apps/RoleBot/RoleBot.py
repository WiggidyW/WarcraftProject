import sys
sys.path.append('../..')

import discord

import Cfg
from Discord import Message

COMMANDS = ['!setrole']

class Bot(discord.Client):
	async def on_ready(self):
		print('We have logged on.\nUser: {0}'.format(self.user))

	async def on_message(self, message):
		if message.author == self.user:
			return
		if message.guild is None:
			return
		if message.content.startswith(COMMANDS[0]):
			if not message.mentions and not message.role_mentions:
				await Message.message(message.channel, 'You didn\'t mention any Users or Roles!')
			elif not message.mentions:
				await Message.message(message.channel, 'You didn\'t mention any Users!')
			elif not message.role_mentions:
				await Message.message(message.channel, 'You didn\'t mention any Roles!')
			else:
				for member in message.mentions:
					for role in message.role_mentions:
						try:
							if role in member.roles:
								await Message.message(message.channel, '{0} was already {1}.'.format(member.name, role.name))
							else:
								await member.add_roles(role)
								await Message.message(message.channel, '{0} is now {1}.'.format(member.name, role.name))
						except discord.errors.DiscordException as error:
							await Message.message(message.channel, str(error))
							return

def main():
	MyBot = Bot()
	id_ = Cfg.read('id')
	MyBot.run(id_)

if __name__ == '__main__':
	main()