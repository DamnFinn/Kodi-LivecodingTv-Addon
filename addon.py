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

__mainmenu = [
        [30010, 'livestreams', providers. \
            LivestreamDataProvider().getInformation()],
        [30011, 'videos', providers.VideoDataProvider().getInformation()]
        #,[30019, 'settings']
    ]

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
    requested_routing_uri = '%s%s' % (__addon_uri, uri_params)
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
        menu_item_name = __addon.getLocalizedString(menu_item[0])
        # create a list item with a text label and a thumbnail image
        if len(menu_item) == 3:
            list_item = xbmcgui.ListItem(label=menu_item_name, \
                thumbnailImage=menu_item[2].thumbnail)
        else:
            list_item = xbmcgui.ListItem(label=menu_item_name)
        url = get_routing_uri([[__action, menu_item[1]]])
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
        list_item.setProperty('fanart_image', livestream.thumbnail)
        # set additional info for the list item
        list_item.setInfo('video', {'title': livestream.display_title, \
            'genre': livestream.coding_category})
        list_item.setArt({'landscape': livestream.thumbnail})
        list_item.setProperty('IsPlayable', 'true')
        # create a URL for the plugin recursive callback
        uri = get_routing_uri([[__action, __mainmenu[0][1]], \
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
        list_item.setProperty('fanart_image', video.thumbnail)
        # set additional info for the list item
        list_item.setInfo('video', {'title': video.display_title, \
            'genre': video.coding_category})
        list_item.setArt({'landscape': video.thumbnail})
        list_item.setProperty('IsPlayable', 'true')
        # create a URL for the plugin recursive callback
        uri = get_routing_uri([[__action, __mainmenu[0][1]], \
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
        elif params[__action] == __mainmenu[0][1]:
            list_livestreams()
        elif params[__action] == __mainmenu[1][1]:
            list_videos()
    else:
        # default, without any parameters
        list_mainmenu()


if __name__ == '__main__':
    # call the router function and pass the plugin call parameters to it
    # we use string slicing to trim the leading '?'
    # from the plugin call paramstring
    router(sys.argv[2][1:])
