# -*- coding: utf-8 -*-

# REMARK: Livecoding's API does not provide thumbnails right now...


class MenuItem:
    def __init__(self, label, routing_action, elements=-1, thumbnail=''):
        if elements > 0:
            self.label = '{label} [{num}]' \
                .format(label=label, num=elements)
        else:
            self.label = label
        self.routing_action = routing_action
        self.elements = elements
        self.thumbnail = thumbnail


class Stream:
    def __init__(self, json):
        self.api_url = json['url'].encode('utf8')
        self.user_api_url = json['user'].encode('utf8')
        self.title = json['title'].encode('utf8')
        self.description = json['description'].encode('utf8')
        self.coding_category = json['coding_category'].encode('utf8')
        self.difficulty = json['difficulty'].encode('utf8')
        self.streaming_language = json['language'].encode('utf8')
        self.viewing_urls = json['viewing_urls']
        #additional properties
        self.user_name = self.user_api_url.split('/')[5]
        if len(self.viewing_urls) > 0:
            self.viewing_url = self.viewing_urls[0]


class Livestream(Stream):
    def __init__(self, json):
        Stream.__init__(self, json)
        self.user_slug = json['user__slug'].encode('utf8')
        self.tags = json['tags'].encode('utf8')
        self.is_live = bool(json['is_live'])
        self.viewers = json['viewers_live']
        #additional properties
        self.display_title = '[{c}] {s}: {t}'.format \
            (c=self.coding_category, s=self.user_name, t=self.title)
        self.thumbnail = '{p}/video/livestream/{u}/thumbnail_250_140/' \
            .format(p='https://www.livecoding.tv', u=self.user_name)


class Video(Stream):
    def __init__(self, json):
        Stream.__init__(self, json)
        self.slug = json['slug'].encode('utf8')
        self.product_type = json['product_type'].encode('utf8')
        self.creation_time = json['creation_time']
        self.duration = json['duration']
        self.region = json['region'].encode('utf8')
        self.viewers = json['viewers_overall']
        #additional properties
        self.creation_date = self.creation_time.split('T')[0]
        creation_date_split = self.creation_date.split('-')
        self.creation_year = creation_date_split[0]
        self.creation_month = creation_date_split[1]
        self.creation_day = creation_date_split[2]
        self.display_title = '[{c}, {d}] {s}: {t}'.format \
            (c=self.coding_category, d=self.creation_date, \
             s=self.user_name, t=self.title)
        self.thumbnail = '{p}/video/video/{s}/thumbnail_250_140/' \
            .format(p='https://www.livecoding.tv', s=self.slug)
