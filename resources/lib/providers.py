# -*- coding: utf-8 -*-

import xbmc, xbmcaddon
import json
import models


class Logger:
    def __init__(self, filename):
        self.filename = filename

    def __log(self, message, level):
        message = '{m} [module: {n}]'.format(m=message, n=self.filename)
        xbmc.log(message, level)

    def debug(self, message):
        self.__log(message, xbmc.LOGDEBUG)

    def error(self, message):
        self.__log(message, xbmc.LOGERROR)

    def info(self, message):
        self.__log(message, xbmc.LOGNOTICE)


__addon = xbmcaddon.Addon()


def request_json(uri):
    # authentification with oauth2 needed for that currently:
    #data = requests.get(uri)
    #data_json = data.json()
    log = Logger(__name__)
    addon_path = __addon.getAddonInfo('path')
    data_path = '{p}/testdata/{f}.json'.format(p=addon_path, f=uri)
    log.debug('Requesting document from {p}'.format(p=data_path))
    fp = open(data_path, 'r')
    data_json = json.load(fp)
    fp.close()
    log.debug('Answer to request from {path}: {answer}' \
        .format(path=data_path, answer=data_json))
    return data_json


class MainMenuProvider:
    def __init__(self):
        # TODO
        pass

class LivestreamDataProvider:
    def __init__(self):
        self.__log = Logger(__name__)
        self.thumbnail = ''
        self.total = 0

    def get(self, limit = 20, offset = 0):
        # TODO: request Livecoding's API with limit and offset
        livestreams = []
        livestreams_json = request_json('livestreams')
        self.total = int(livestreams_json['count'])
        index = -1
        for livestream_json in livestreams_json['results']:
            # workaround for not requesting Livecoding's API
            index += 1
            if index < offset:
                continue
            livestream = models.Livestream(livestream_json)
            if len(livestreams) == 0:
                self.thumbnail = livestream.thumbnail
            livestreams.append(livestream)
            # workaround for not requesting Livecoding's API
            if len(livestreams) >= limit:
                break
        if len(livestreams) == 0 and limit != 0:
            message = '{num} livestreams returned while limit={limit}, ' \
                'offset={offset}' \
                .format(num=len(livestreams), limit=limit, offset=offset)
            self.__log.debug(message)
        return livestreams

    def getInformation(self):
        self.get(1)
        return self


class VideoDataProvider:
    def __init__(self):
        self.__log = Logger(__name__)
        self.thumbnail = ''
        self.total = 0

    def get(self, limit = 20, offset = 0):
        # TODO: request Livecoding's API with limit and offset
        # TODO: should be dependend on coding_category / broadcaster
        videos = []
        videos_json = request_json('videos')
        self.total = int(videos_json['count'])
        index = -1
        for video_json in videos_json['results']:
            # workaround for not requesting Livecoding's API
            index += 1
            if index < offset:
                continue
            video = models.Video(video_json)
            if len(videos) == 0:
                self.thumbnail = video.thumbnail
            videos.append(video)
            # workaround for not requesting Livecoding's API
            if len(videos) >= limit:
                break
        if len(videos) == 0 and limit != 0:
            message = '{num} videos returned while limit={limit}, ' \
                'offset={offset}' \
                .format(num=len(videos), limit=limit, offset=offset)
            self.__log.debug(message)
        videos = sorted(videos, key=lambda video: video.creation_date, reverse=True)
        return videos

    def getInformation(self):
        self.get(1)
        return self
