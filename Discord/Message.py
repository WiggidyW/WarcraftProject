from discord import errors

DISCORD_MAX_CHARACTERS = 2000

async def message(channel, str_):
	try:
		await channel.send(str_)
	except discord.errors.HTTPException:
		i = 0
		j = DISCORD_MAX_CHARACTERS
		while i < len(str_):
			if i+j > len(str):
				await channel.send(str_[i:len(str)-1])
				break
			else:
				cut_str = str_[i:i+j-1]
				for k in range(j-1, -1, -1):
					if cut_str[k] == '\n':
						await channel.send(str_[i:k-1])
						i = k+1
						break
				await channel.send(cut_str)
	except discord.errors.DiscordException as error:
		print(error)