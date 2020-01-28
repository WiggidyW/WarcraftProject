import yaml

FILENAME = 'config.yml'

def read(key_, type_=None):
	with open(FILENAME) as ymlfile:
		data = yaml.full_load(ymlfile)
		if data is None:
			data = {}
	if type_ is not None:
		data = data.get(type_, {})
	return data.get(key_, None)