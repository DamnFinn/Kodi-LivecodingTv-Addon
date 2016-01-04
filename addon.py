# -*- coding: utf-8 -*-

import sys
from urlparse import parse_qsl
import xbmcaddon, xbmcgui, xbmcplugin
import resources.lib.providers as providers


__addon_uri = sys.argv[0]
__addon_handle = int(sys.argv[1])

__addon = xbmcaddon.Addon()
__addon_shortname = 'LCTV'

__log = providers.Logger(__name__)
__mainmenu = providers.get_mainmenu()

__action = 'action'
__video = 'video'


def get_routing_uri(params):
    uri_params = ''
    for param in params:
        if len(uri_params) == 0:
            uri_params = '?'
        else:
            uri_params = '{t}&'.format(t=uri_params)
        uri_params = '{t}{n}={v}' \
            .format(t=uri_params, n=param[0], v=param[1])
    requested_routing_uri = ''.join([__addon_uri, uri_params])
    # logging
    message = 'Requested routing uri: {u}'.format(u=requested_routing_uri)
    __log.debug(message)
    return requested_routing_uri


def show_notification_error(message):
    __log.error(message)
    xbmcgui.Dialog().notification \
        (__addon_shortname, message, xbmcgui.NOTIFICATION_ERROR, 15000)


def list_mainmenu():
    listing = []
    for menu_item in __mainmenu:
        list_item = xbmcgui.ListItem(label=menu_item.label)
        if len(menu_item.thumbnail) > 0:
            list_item.setThumbnailImage(menu_item.thumbnail)
        url = get_routing_uri([[__action, menu_item.routing_action]])
        is_folder = True
        # add our item to the listing as a 3-element tuple
        listing.append((url, list_item, is_folder))
    # add our listing to Kodi
    xbmcplugin.addDirectoryItems(__addon_handle, listing, len(listing))
    # finish creating a virtual folder
    xbmcplugin.endOfDirectory(__addon_handle)


def list_livestreams():
    limit = int(__addon.getSetting('max_entries'))
    listing = []
    for livestream in providers.LivestreamDataProvider().get(limit):
        # create a list item with a text label and a thumbnail image
        list_item = xbmcgui.ListItem(label=livestream.display_title, \
            thumbnailImage=livestream.thumbnail)
        list_item.setArt({'landscape': livestream.thumbnail})
        list_item.setProperty('fanart_image', livestream.thumbnail)
        list_item.setProperty('IsPlayable', 'true')
        # set additional info for the list item
        list_item.setInfo('video', { \
            'artist': [livestream.user_name], \
            'genre': livestream.coding_category, \
            'originaltitle': livestream.title, \
            'playcount': livestream.viewers, \
            'plot': livestream.description, \
            'title': livestream.display_title})
        # create a URL for the plugin recursive callback
        uri = get_routing_uri([[__action, __mainmenu[0].routing_action], \
            [__video, livestream.viewing_url]])
        # add the list item to a virtual Kodi folder
        is_folder = False
        # add our item to the listing as a 3-element tuple
        listing.append((uri, list_item, is_folder))
    # add our listing to Kodi
    xbmcplugin.addDirectoryItems(__addon_handle, listing, len(listing))
    # add a sort method for the virtual folder items
    # (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(__addon_handle, \
        xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder
    xbmcplugin.endOfDirectory(__addon_handle)


def list_videos():
    limit = int(__addon.getSetting('max_entries'))
    listing = []
    for video in providers.VideoDataProvider().get(limit):
        # create a list item with a text label and a thumbnail image
        list_item = xbmcgui.ListItem(label=video.display_title, \
            thumbnailImage=video.thumbnail)
        list_item.setArt({'landscape': video.thumbnail})
        list_item.setProperty('fanart_image', video.thumbnail)
        list_item.setProperty('IsPlayable', 'true')
        if len(video.coding_category) > 0 and len(video.product_type) > 0:
            genre = '{category}, {type}'.format( \
                category=video.coding_category, type=video.product_type)
        elif len(video.product_type) > 0:
            genre = video.product_type
        else:
            genre = video.coding_category
        # set additional info for the list item
        list_item.setInfo('video', { \
            'aired': video.creation_date, \
            'artist': [video.user_name], \
            'duration': video.duration, \
            'genre': genre, \
            'originaltitle': video.title, \
            'playcount': video.viewers, \
            'plot': video.description, \
            'premiered': video.creation_date, \
            'title': video.display_title, \
            'year': video.creation_year})
        # create a URL for the plugin recursive callback
        uri = get_routing_uri([[__action, __mainmenu[1].routing_action], \
            [__video, video.viewing_url]])
        # add the list item to a virtual Kodi folder
        is_folder = False
        # add our item to the listing as a 3-element tuple.
        listing.append((uri, list_item, is_folder))
    # add our listing to Kodi
    xbmcplugin.addDirectoryItems(__addon_handle, listing, len(listing))
    # add a sort method for the virtual folder items (alphabetically,
    # ignore articles)
    #xbmcplugin.addSortMethod(_addon_handle, \
    #   xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder
    xbmcplugin.endOfDirectory(__addon_handle)


def watch_video(url):
    message = 'Livestreams/videos cannot be watched right now'
    __log.info(message)
    show_notification_error(message)
    # replace url with a playable video - not from Livecoding.tv
    url = 'http://cdn.media.ccc.de/congress/2015/h264-hd-web/' \
        '32c3-7528-en-Lets_Encrypt_--_' \
        'What_launching_a_free_CA_looks_like.mp4'
    # create a playable item with a path to play
    play_item = xbmcgui.ListItem(path=url)
    # pass the item to the Kodi player
    xbmcplugin.setResolvedUrl(__addon_handle, True, listitem=play_item)


def show_settings():
    __addon.openSettings()


def router(paramstring):
    """
    Router function that calls other functions depending on the provided
    paramstring
    :param paramstring:
    :return:
    """
    # parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # check the parameters passed to the plugin
    if params:
        if __video in params:
            watch_video(params[__video])
        elif params[__action] == __mainmenu[0].routing_action:
            list_livestreams()
        elif params[__action] == __mainmenu[1].routing_action:
            list_videos()
        elif params[__action] == __mainmenu[2].routing_action:
            show_settings()
    else:
        # default, without any parameters
        list_mainmenu()


if __name__ == '__main__':
    # call the router function and pass the plugin call parameters to it
    # we use string slicing to trim the leading '?'
    # from the plugin call paramstring
    router(sys.argv[2][1:])
