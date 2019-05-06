# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'https://www.4helal.tv'
script_name='4HELAL'
headers = { 'User-Agent' : '' }
menu_name='[COLOR FFC89008]HEL [/COLOR]'

def MAIN(mode,url,text):
	if mode==90: MENU()
	elif mode==91: ITEMS(url)
	elif mode==92: PLAY(url)
	elif mode==94: LATEST()
	elif mode==99: SEARCH(text)
	return

def MENU():
	addDir(menu_name+'بحث في الموقع','',99)
	addDir(menu_name+'المضاف حديثا','',94)
	addDir(menu_name+'جديد الموقع',website0a,91)
	html = openURL(website0a,'',headers,'','4HELAL-MENU-1st')
	html_blocks = re.findall('mainmenu(.*?)nav',html,re.DOTALL)
	block1 = html_blocks[0]
	html_blocks = re.findall('class="f-cats(.*?)div',html,re.DOTALL)
	block2 = html_blocks[0].replace('</a></li>',' اخرى</a></li>')
	block = block1 + block2
	items = re.findall('<li><a href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	#xbmcgui.Dialog().ok(block,str(items))
	ignoreLIST = ['افلام للكبار فقط']
	for link,title in items:
		title = title.strip(' ')
		if not any(value in title for value in ignoreLIST):
			addDir(menu_name+title,link,91)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def ITEMS(url,html=''):
	if html=='': html = openURL(url,'',headers,'','4HELAL-ITEMS-1st')
	html_blocks = re.findall('movies-items(.*?)class="clear',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('background-image:url\((.*?)\).*?href="(.*?)".*?movie-title">(.*?)<',block,re.DOTALL)
	for img,link,title in items:
		if '/video/' in link:
			addDir(menu_name+title,link,92,img)
		else:
			addDir(menu_name+title,link,91,img)
	html_blocks = re.findall('pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<a href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			title = unescapeHTML(title)
			title = title.replace('الصفحة ','')
			addDir(menu_name+'صفحة '+title,link,91)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	import xbmcaddon
	settings = xbmcaddon.Addon(id=addon_id)
	previous_url = settings.getSetting('previous.url')
	if url==previous_url:
		linkLIST = settings.getSetting('previous.linkLIST')
		linkLIST = linkLIST[1:-1].replace('&apos;','').replace(' ','').replace("'",'')
		linkLIST = linkLIST.split(',')
		#xbmcgui.Dialog().ok(url,str(linkLIST))
	else:
		linkLIST = []
		urlLIST = []
		adultLIST = ['R - للكبار فقط','PG-18','PG-16','TV-MA']
		html = openURL(url,'',headers,'','4HELAL-PLAY-1st')
		if any(value in html for value in adultLIST):
			xbmcgui.Dialog().notification('قم بتشغيل فيديو غيره','هذا الفيديو للكبار فقط ولا يعمل هنا')
			return
		html_blocks = re.findall('links-panel(.*?)div',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('href="(.*?)"',block,re.DOTALL)
			for link in items:
				linkLIST.append(link)
		html_blocks = re.findall('nav-tabs(.*?)video-panel-more',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('ajax-file-id.*?value="(.*?)"',block,re.DOTALL)
		id = items[0]
		#xbmcgui.Dialog().ok('',id)
		items = re.findall('data-server-src="(.*?)"',block,re.DOTALL)
		for link in items:
			link = unquote(link)
			linkLIST.append(link)
		"""
		items = re.findall('data-server="(.*?)"',block,re.DOTALL)
		for link in items:
			url2 = website0a + '/ajax.php?id='+id+'&ajax=true&server='+link
			#link = openURL(url2,'',headers,'','4HELAL-PLAY-2nd')
			#linkLIST.append(link)
			urlLIST.append(url2)
			html = openURL(url2,'',headers,'','4HELAL-PLAY-2nd')
			#xbmcgui.Dialog().ok(url2,html)
		count = len(urlLIST)
		import concurrent.futures
		with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
			responcesDICT = dict( (executor.submit(openURL, urlLIST[i], '', headers,'','4HELAL-PLAY-2nd'), i) for i in range(0,count) )
		for response in concurrent.futures.as_completed(responcesDICT):
			linkLIST.append( response.result() )
		"""
		settings.setSetting('previous.url',url)
		settings.setSetting('previous.linkLIST',str(linkLIST))
	from RESOLVERS import PLAY as RESOLVERS_PLAY
	RESOLVERS_PLAY(linkLIST,script_name)
	return

def LATEST():
	html = openURL(website0a,'',headers,'','4HELAL-LATEST-1st')
	html_blocks = re.findall('index-last-movie(.*?)index-slider-movie',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('src="(.*?)".*?href="(.*?)" title="(.*?)"',block,re.DOTALL)
	for img,link,title in items:
		if '/video/' in link:
			addDir(menu_name+title,link,92,img)
		else:
			addDir(menu_name+title,link,91,img)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def SEARCH(search=''):
	if search=='': search = KEYBOARD()
	if search == '': return
	#search = search.replace(' ','+')
	url = website0a + '/search.php'
	headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { 't' : search }
	data = urllib.urlencode(payload)
	html = openURL(url,data,headers,'','4HELAL-SEARCH-1st')
	if 'movies-items' in html: ITEMS('',html)
	else: xbmcgui.Dialog().ok('no results','لا توجد نتائج للبحث')
	return



