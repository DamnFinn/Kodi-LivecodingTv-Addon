import xbmc


class Livestream(object):
	def __init__(self, json):
		self.api_url = json['url']
		self.user_name = self.api_url.split('/')[5]
		self.user_api_url = json['user']
		self.user_slug = json['user__slug']
		self.title = json['title']
		self.description = json['description']
		self.coding_category = json['coding_category']
		self.difficulty = json['difficulty']
		self.streaming_language = json['language']
		self.tags = json['tags']
		self.is_live = str(json['is_live']).lower() == "true"
		self.viewers = json['viewers_live']
		self.viewing_urls = json['viewing_urls']
		#additional properties
		self.display_title = '[%s] %s: %s' % (self.coding_category, self.user_name, self.title)
		self.thumbnail = 'https://www.livecoding.tv/video/livestream/' + self.user_name + '/thumbnail_250_140/'
		self.viewing_url = self.viewing_urls[0]


class Logger():
	def __init__(self, filename):
		self.filename = filename
	
	def __log(self, message, level):
		message += ' [%s]' % (self.filename)
		xbmc.log(message, level)
	
	def debug(self, message):
		self.__log(message, xbmc.LOGDEBUG)
	
	def error(self, message):
		self.__log(message, xbmc.LOGERROR)
	
	def info(self, message):
		self.__log(message, xbmc.LOGNOTICE)