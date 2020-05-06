# -*- coding: utf-8 -*-
from LIBRARY import *

script_name = 'ALFATIMI'
menu_name='_FTM_'
website0a = WEBSITES[script_name][0]

moviesLIST = ['1239','1250','1245','20','1259','218','485','1238','1258','292']
englishLIST = ['3030','628']

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==60: results = MENU(url)
	elif mode==61: results = TITLES(url,text)
	elif mode==62: results = EPISODES(url)
	elif mode==63: results = PLAY(url)
	elif mode==64: results = MOSTS(text)
	elif mode==69: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	if website=='': addMenuItem('dir',menu_name+'بحث في الموقع','',69)
	addMenuItem('dir',website+'::'+menu_name+'ما يتم مشاهدته الان',website0a,64,'','','recent_viewed_vids')
	addMenuItem('dir',website+'::'+menu_name+'الاكثر مشاهدة',website0a,64,'','','most_viewed_vids')
	addMenuItem('dir',website+'::'+menu_name+'اضيفت مؤخرا',website0a,64,'','','recently_added_vids')
	addMenuItem('dir',website+'::'+menu_name+'فيديو عشوائي',website0a,64,'','','random_vids')
	addMenuItem('dir',website+'::'+menu_name+'افلام ومسلسلات',website0a,61,'','','-1')
	addMenuItem('dir',website+'::'+menu_name+'البرامج الدينية',website0a,61,'','','-2')
	addMenuItem('dir',website+'::'+menu_name+'English Videos',website0a,61,'','','-3')
	return

def TITLES(url,category):
	#xbmcgui.Dialog().ok('', category)
	cat = ''
	if category not in ['-1','-2','-3']: cat = '?cat='+category
	url2 = website0a+'/menu_level.php'+cat
	html = openURL_cached(REGULAR_CACHE,url2,'','','','ALFATIMI-TITLES-1st')
	items = re.findall('href=\'(.*?)\'.*?>(.*?)<.*?>(.*?)</span>',html,re.DOTALL)
	startAdd,found = False,False
	for link,title,count in items:
		title = unescapeHTML(title)
		title = title.strip(' ')
		if 'http' not in link: link = 'http:'+link
		cat = re.findall('cat=(.*?)&',link,re.DOTALL)[0]
		if category==cat: startAdd = True
		elif startAdd 	or (category=='-1' and cat in moviesLIST) \
						or (category=='-2' and cat not in englishLIST and cat not in moviesLIST) \
						or (category=='-3' and cat in englishLIST):
							if count=='1': addMenuItem('link',menu_name+title,link,63)
							else: addMenuItem('dir',menu_name+title,link,61,'','',cat)
							found = True
	if not found: EPISODES(url)
	return

def EPISODES(url):
	html = openURL_cached(REGULAR_CACHE,url,'','','','ALFATIMI-EPISODES-1st')
	#xbmcgui.Dialog().ok(url , html)
	html_blocks = re.findall('pagination(.*?)id="footer',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('grid_view.*?src="(.*?)".*?title="(.*?)".*?<h2.*?href="(.*?)"',block,re.DOTALL)
	link = ''
	for img,title,link in items:
		title = title.replace('Add','').replace('to Quicklist','').strip(' ')
		if 'http' not in link: link = 'http:'+link
		addMenuItem('link',menu_name+title,link,63,img)
	html_blocks=re.findall('(.*?)div',block,re.DOTALL)
	block=html_blocks[0]
	block=re.findall('pagination(.*?)</div>',html,re.DOTALL)[0]
	items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	url2 = url.split('?')[0]
	for link,page2 in items:
		link = url2 + link
		title = unescapeHTML(page2)
		title = 'صفحة ' + title
		addMenuItem('dir',menu_name+title,link,62)
	return link

def PLAY(url):
	if 'videos.php' in url: url = EPISODES(url)
	html = openURL_cached(LONG_CACHE,url,'','','','ALFATIMI-PLAY-1st')
	items = re.findall('playlistfile:"(.*?)"',html,re.DOTALL)
	url = items[0]
	if 'http' not in url: url = 'http:'+url
	#xbmcgui.Dialog().ok(url,'')
	PLAY_VIDEO(url,script_name)
	return

def MOSTS(category):
	payload = { 'mode' : category }
	url = 'http://alfatimi.tv/ajax.php'
	headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
	data = urllib.urlencode(payload)
	html = openURL_cached(SHORT_CACHE,url,data,headers,'','ALFATIMI-MOSTS-1st')
	items = re.findall('href="(.*?)".*?title="(.*?)".*?src="(.*?)".*?href',html,re.DOTALL)
	for link,title,img in items:
		title = title.strip(' ')
		if 'http' not in link: link = 'http:'+link
		addMenuItem('link',menu_name+title,link,63,img)
	return

def SEARCH(search):
	if '::' in search:
		search = search.split('::')[0]
		exit = False
	else: exit = True
	if search=='': search = KEYBOARD()
	if search == '': return
	#xbmcgui.Dialog().ok(search, website0a)
	new_search = search.replace(' ','+')
	url = website0a + '/search_result.php?query=' + new_search # + '&page=1'
	EPISODES(url)
	return


