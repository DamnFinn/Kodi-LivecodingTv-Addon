# this is necessary because livecoding.tv does not provide thumbnails right now
def get_thumbnail(user_name):
    thumbnail_url = 'https://www.livecoding.tv/video/livestream/%s/thumbnail_250_140/' % (user_name)
    return thumbnail_url



class Livestream(object):
    def __init__(self, json):
        self.api_url = json['url']
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
        self.user_name = self.api_url.split('/')[5]
        self.display_title = '[%s] %s: %s' % (self.coding_category, self.user_name, self.title)
        self.thumbnail = get_thumbnail(self.user_name)
        self.viewing_url = self.viewing_urls[0]


class Video(object):
    def __init__(self, json):
        self.api_url = json['url']
        self.slug = json['slug']
        self.user_api_url = json['user']
        self.title = json['title']
        self.description = json['description']
        self.coding_category = json['coding_category']
        self.difficulty = json['difficulty']
        self.streaming_language = json['language']
        self.product_type = json['product_type']
        self.creation_time = json['creation_time']
        self.duration = json['duration']
        self.region = json['region']
        self.viewers = json['viewers_overall']
        self.viewing_urls = json['viewing_urls']
        #additional properties
        self.user_name = self.user_api_url.split('/')[5]
        self.creation_date = self.creation_time.split('T')[0]
        creation_date_split = self.creation_date.split('-')
        self.creation_year = creation_date_split[0]
        self.creation_month = creation_date_split[1]
        self.creation_day = creation_date_split[2]
        self.display_title = '[%s, %s] %s: %s' % (self.coding_category, self.creation_date, self.user_name, self.title)
        self.thumbnail = get_thumbnail(self.user_name)
        self.viewing_url = self.viewing_urls[0]