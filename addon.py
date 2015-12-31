import sys
from urlparse import parse_qsl
import xbmcaddon, xbmcgui, xbmcplugin
#import requests
from providers import LivestreamDataProvider, VideoDataProvider, Logger


_addon_uri = sys.argv[0]
_addon_handle = int(sys.argv[1])

_addon = xbmcaddon.Addon()
_app_shortname = 'LCTV'

_log = Logger(__name__)

_mainmenu = [
        [30010, 'livestreams'],
        [30011, 'videos']
    ]

_action = 'action'
_video = 'video'


def get_routing_uri(params):
	uri_params = ''
	for param in params:
		if len(uri_params) == 0:
			uri_params = '?'
		else:
			uri_params += '&'
		uri_params += '%s=%s' % (param[0], param[1])
	requested_routing_uri = '%s%s' % (_addon_uri, uri_params)
	# logging
	message = 'Requested plugin uri: ' + requested_routing_uri
	_log.debug(message)
	return requested_routing_uri


def show_notification_error(message):
	_log.error(message)
	xbmcgui.Dialog().notification(_app_shortname, message, xbmcgui.NOTIFICATION_ERROR, 15000)


def list_mainmenu():
	# Create a list for our items.
	listing = []
	# Iterate through categories
	for menu_item in _mainmenu:
		menu_item_name = _addon.getLocalizedString(menu_item[0])
		# Create a list item with a text label and a thumbnail image, if applicable
		list_item = xbmcgui.ListItem(label=menu_item_name)
		# Set a fanart image for the list item.
		#list_item.setProperty('fanart_image', _mainmenu[category][0]['thumb'])
		# Set additional info for the list item.
		# For available properties see the following link:
		# http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
		#list_item.setInfo('video', {'title': category, 'genre': category})
		# Create a URL for the plugin recursive callback.
		# Example: plugin://plugin.video.example/?action=listing&category=Animals
		url = get_routing_uri([[_action, menu_item[1]]])
		# is_folder = True means that this item opens a sub-list of lower level items.
		is_folder = True
		# Add our item to the listing as a 3-element tuple.
		listing.append((url, list_item, is_folder))
	# Add our listing to Kodi.
	# Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
	# instead of adding one by ove via addDirectoryItem.
	xbmcplugin.addDirectoryItems(_addon_handle, listing, len(listing))
	# Add a sort method for the virtual folder items (alphabetically, ignore articles)
	#xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	# Finish creating a virtual folder.
	xbmcplugin.endOfDirectory(_addon_handle)


def list_livestreams():
	# Get the list of videos in the category.
	#videos = get_videos(category)
	# Create a list for our items.
	listing = []
	# Iterate through videos.
	for livestream in LivestreamDataProvider().get():
		# create a list item with a text label and a thumbnail image
		list_item = xbmcgui.ListItem(label=livestream.display_title, thumbnailImage=livestream.thumbnail)
		list_item.setProperty('fanart_image', livestream.thumbnail)
		# set additional info for the list item
		list_item.setInfo('video', {'title': livestream.display_title, 'genre': livestream.coding_category})
		list_item.setArt({'landscape': livestream.thumbnail})
		list_item.setProperty('IsPlayable', 'true')
		# create a URL for the plugin recursive callback
		uri = get_routing_uri([[_action, _mainmenu[0][1]], [_video, livestream.viewing_url]])
		# add the list item to a virtual Kodi folder.
		# is_folder = False means that this item won't open any sub-list.
		is_folder = False
		# add our item to the listing as a 3-element tuple.
		listing.append((uri, list_item, is_folder))
	# add our listing to Kodi.
	# Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
	# instead of adding one by ove via addDirectoryItem.
	xbmcplugin.addDirectoryItems(_addon_handle, listing, len(listing))
	# add a sort method for the virtual folder items (alphabetically, ignore articles)
	xbmcplugin.addSortMethod(_addon_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	# Finish creating a virtual folder.
	xbmcplugin.endOfDirectory(_addon_handle)


def list_videos():
	# Get the list of videos in the category.
	#videos = get_videos(category)
	# Create a list for our items.
	listing = []
	# Iterate through videos.
	for video in VideoDataProvider().get():
		# create a list item with a text label and a thumbnail image
		list_item = xbmcgui.ListItem(label=video.display_title, thumbnailImage=video.thumbnail)
		list_item.setProperty('fanart_image', video.thumbnail)
		# set additional info for the list item
		list_item.setInfo('video', {'title': video.display_title, 'genre': video.coding_category})
		list_item.setArt({'landscape': video.thumbnail})
		list_item.setProperty('IsPlayable', 'true')
		# create a URL for the plugin recursive callback
		uri = get_routing_uri([[_action, _mainmenu[0][1]], [_video, video.viewing_url]])
		# add the list item to a virtual Kodi folder.
		# is_folder = False means that this item won't open any sub-list.
		is_folder = False
		# add our item to the listing as a 3-element tuple.
		listing.append((uri, list_item, is_folder))
	# add our listing to Kodi.
	# Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
	# instead of adding one by ove via addDirectoryItem.
	xbmcplugin.addDirectoryItems(_addon_handle, listing, len(listing))
	# add a sort method for the virtual folder items (alphabetically, ignore articles)
	#xbmcplugin.addSortMethod(_addon_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	# Finish creating a virtual folder.
	xbmcplugin.endOfDirectory(_addon_handle)


def watch_video(url):
    message = 'Livestreams cannot be watched right now'
    _log.info(message)
    show_notification_error(message)
    # create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=url)
    # pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_addon_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions depending on the provided paramstring
    :param paramstring:
    :return:
    """
    # Parse a URL-encoded paramstring to the dictionary of {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if _video in params:
            watch_video(params[_video])
        elif params[_action] == _mainmenu[0][1]:
            list_livestreams()
        elif params[_action] == _mainmenu[1][1]:
            list_videos()
    else:
        # default, without any parameters
        list_mainmenu()


if __name__ == '__main__':
    #message = 'Starting app %s' % (_app_shortname)
    #xbmcgui.Dialog().notification(_app_shortname, message, xbmcgui.NOTIFICATION_INFO, 10000)
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])