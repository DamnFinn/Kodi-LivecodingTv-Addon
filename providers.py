import xbmc, xbmcaddon
import json
from models import Livestream, Video


class Logger():
    def __init__(self, filename):
        self.filename = filename
    
    def __log(self, message, level):
        message += ' [module: %s]' % (self.filename)
        xbmc.log(message, level)
    
    def debug(self, message):
        self.__log(message, xbmc.LOGDEBUG)
    
    def error(self, message):
        self.__log(message, xbmc.LOGERROR)
    
    def info(self, message):
        self.__log(message, xbmc.LOGNOTICE)


_addon = xbmcaddon.Addon()

_log = Logger(__name__)


def request_json(uri):
    #data = requests.get(uri)   # authentification needed for that currently...
    #data_json = data.json()	
    data_path = '%s/testdata/%s.json' % (_addon.getAddonInfo('path'), uri)
    _log.debug('Requesting document from %s' % (data_path))
    fp = open(data_path, 'r')
    data_json = json.load(fp)
    fp.close()
    _log.debug('Answer to request from %s: %s' % (data_path, data_json))
    return data_json


class LivestreamDataProvider:
    def get(self):
        livestreams_json = request_json('livestreams')
        livestreams = []
        for livestream_json in livestreams_json['results']:
            livestream = Livestream(livestream_json)
            livestreams.append(livestream)
        return livestreams


class VideoDataProvider:
    def get(self):    # TODO: should be dependend on coding_category
        videos_json = request_json('videos')
        videos = []
        for video_json in videos_json['results']:
            video = Video(video_json)
            videos.append(video)
        videos = sorted(videos, key=lambda video: video.creation_date, reverse=True)
        return videos
