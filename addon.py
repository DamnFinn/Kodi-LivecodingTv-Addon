import sys
from urlparse import parse_qsl
import xbmcaddon, xbmcgui, xbmcplugin
import requests
from classes import Livestream, Logger
from client import LivecodingTvApp

# Get the plugin url in plugin:// notation.
_plugin_url = sys.argv[0]
# Get the plugin handle as an integer number.
_plugin_handle = int(sys.argv[1])

_addon = xbmcaddon.Addon()
_app_shortname = 'LCTV'

_lctv_app = LivecodingTvApp()
_log = Logger('addon.py')

_mainmenu = [[30010, 'livestreams']]
_action = 'action'
_user = 'user'


def get_plugin_url(params):
	url_params = ''
	for param in params:
		if len(url_params) == 0:
			url_params = '?'
		else:
			url_params += '&'
		url_params += '%s=%s' % (param[0], param[1])
	requested_plugin_url = '%s%s' % (_plugin_url, url_params)
	# logging
	message = 'Requested plugin url: ' + requested_plugin_url
	_log.debug(message)
	return requested_plugin_url


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
		url = get_plugin_url([[_action, menu_item[1]]])
		# is_folder = True means that this item opens a sub-list of lower level items.
		is_folder = True
		# Add our item to the listing as a 3-element tuple.
		listing.append((url, list_item, is_folder))
	# Add our listing to Kodi.
	# Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
	# instead of adding one by ove via addDirectoryItem.
	xbmcplugin.addDirectoryItems(_plugin_handle, listing, len(listing))
	# Add a sort method for the virtual folder items (alphabetically, ignore articles)
	#xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	# Finish creating a virtual folder.
	xbmcplugin.endOfDirectory(_plugin_handle)


def request_json(url):
	data = requests.get(url, auth=(_lctv_app.client_id, _lctv_app.client_secret))
	json = data.json()	
	_log.debug('Answer to request from %s: %s' % (url, json))
	return json


def get_livestreams():
	livestreams_json = request_json('https://www.livecoding.tv:443/api/livestreams/onair/')
	#iteratore through livestreams
	livestreams = []
	for livestream_json in livestreams_json['results']:
		livestream = Livestream(livestream_json)
		livestreams.append(livestream)
	return livestreams


def list_livestreams():
	# Get the list of videos in the category.
	#videos = get_videos(category)
	# Create a list for our items.
	listing = []
	# Iterate through videos.
	for livestream in get_livestreams():
		# Create a list item with a text label and a thumbnail image.
		list_item = xbmcgui.ListItem(label=livestream.display_title, thumbnailImage=livestream.thumbnail)
		# Set a fanart image for the list item.
		list_item.setProperty('fanart_image', livestream.thumbnail)
		# Set additional info for the list item.
		list_item.setInfo('video', {'title': livestream.title, 'genre': livestream.coding_category})
		# Set additional graphics (banner, poster, landscape etc.) for the list item.
		list_item.setArt({'landscape': livestream.thumbnail})
		# Set 'IsPlayable' property to 'true'.
		# This is mandatory for playable items!
		list_item.setProperty('IsPlayable', 'true')
		# Create a URL for the plugin recursive callback
		# Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
		url = get_plugin_url([[_action, _mainmenu[0][1]], [_user, livestream.user_slug]])
		# Add the list item to a virtual Kodi folder.
		# is_folder = False means that this item won't open any sub-list.
		is_folder = False
		# Add our item to the listing as a 3-element tuple.
		listing.append((url, list_item, is_folder))
	# Add our listing to Kodi.
	# Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
	# instead of adding one by ove via addDirectoryItem.
	xbmcplugin.addDirectoryItems(_plugin_handle, listing, len(listing))
	# Add a sort method for the virtual folder items (alphabetically, ignore articles)
	#xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	# Finish creating a virtual folder.
	xbmcplugin.endOfDirectory(_plugin_handle)


def watch_livestream(user_slug):
	# Create a playable item with a path to play.
	#play_item = xbmcgui.ListItem(path=path)
	# Pass the item to the Kodi player.
	#xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
	message = 'Livestreams cannot be watched right now'
	_log.info(message)

"""
def show_notification_error(message):
	_log.error(message)
	xbmcgui.Dialog().notification(_app_shortname, message, xbmcgui.NOTIFICATION_ERROR, 15000)
"""

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
		if params[_action] == _mainmenu[0][1]:
			if _user in params:
				watch_livestream(params[_user])
			else:
				list_livestreams()
	else:
		# default, without any parameters
		list_mainmenu()


if __name__ == '__main__':
	#message = 'Starting app %s' % (_app_shortname)
	#xbmcgui.Dialog().notification(_app_shortname, message, xbmcgui.NOTIFICATION_INFO, 10000)
	# Call the router function and pass the plugin call parameters to it.
	# We use string slicing to trim the leading '?' from the plugin call paramstring
	router(sys.argv[2][1:])