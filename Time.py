import datetime
import pytz
import Cfg

def timezone():
	timezone = Cfg.read('timezone')
	return timezone
def date():
	timezone = Cfg.read('timezone')
	utc_now = pytz.utc.localize(datetime.datetime.utcnow())
	now = utc_now.astimezone(pytz.timezone(timezone))
	return utc_now.strftime('%m-%d-%y')
def time():
	timezone = Cfg.read('timezone')
	utc_now = pytz.utc.localize(datetime.datetime.utcnow())
	now = utc_now.astimezone(pytz.timezone(timezone))
	return now.strftime('%I:%M %p')
def dateTime():
	return date() + ' ' + time()