# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'https://www.halacima.net'
script_name='HALACIMA'
headers = { 'User-Agent' : '' }
menu_name='[COLOR FFC89008]HLA [/COLOR]'

def MAIN(mode,url,page,text):
	if mode==80: MENU()
	elif mode==81: ITEMS(url)
	elif mode==82: PLAY(url)
	elif mode==84: ITEMS('','','lastRecent',page)
	elif mode==85: ITEMS('','','pin',page)
	elif mode==86: ITEMS('','','views',page)
	elif mode==89: SEARCH(text)
	return

def MENU():
	addDir(menu_name+'بحث في الموقع','',89)
	addDir(menu_name+'جديد المسلسلات','',84,icon,0)
	addDir(menu_name+'افلام ومسلسلات مميزة','',85,icon,0)
	addDir(menu_name+'الاكثر مشاهدة','',86,icon,0)
	html = openURL(website0a,'',headers,'','HALACIMA-MENU-1st')
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	html_blocks = re.findall('dropdown(.*?)nav',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('<a href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	#xbmcgui.Dialog().ok(block,str(items))
	ignoreLIST = ['مسلسلات انمي']
	for link,title in items:
		title = title.strip(' ')
		if not any(value in title for value in ignoreLIST):
			addDir(menu_name+title,link,81)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def ITEMS(url,html='',type='',page=0):
	headers = { 'User-Agent' : '' }
	if type=='':
		if html=='':
			html = openURL(url,'',headers,'','HALACIMA-ITEMS-1st')
		html_blocks = re.findall('art_list(.*?)col-md-12',html,re.DOTALL)
		block = html_blocks[0]
	else:
		if page==0: url = website0a + '/ajax/getItem'
		else: url = website0a + '/ajax/loadMore'
		headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'Ajax' : '1' , 'item' : type , 'offset' : page*50 }
		data = urllib.urlencode(payload)
		block = openURL(url,data,headers,'','HALACIMA-ITEMS-2nd')
	items = re.findall('href="(.*?)".*?data-src="(.*?)".*?class="desc">(.*?)<',block,re.DOTALL)
	allTitles = []
	for link,img,title in items:
		title = title.replace('\n','')
		title = title.strip(' ')
		if 'الحلقة' in title and '/article/' not in link:
			episode = re.findall(' الحلقة [0-9]+',title,re.DOTALL)
			if episode:
				title = title.replace(episode[0],'')
		title = unescapeHTML(title)
		if title not in allTitles:
			allTitles.append(title)
			if '/article/' in link:
				addLink(menu_name+title,link,82,img)
			else:
				addDir(menu_name+title,link,81,img)
	html_blocks = re.findall('pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<li><a href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			title = title.replace('الصفحة ','')
			addDir(menu_name+'صفحة '+title,link,81)
	if type=='lastRecent': addDir(menu_name+'صفحة المزيد','',84,icon,page+1)
	elif type=='pin': addDir(menu_name+'صفحة المزيد','',85,icon,page+1)
	elif type=='views': addDir(menu_name+'صفحة المزيد','',86,icon,page+1)
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
		urlLIST = []
		dataLIST = []
		linkLIST = []
		headers = { 'User-Agent' : '' }
		html = openURL(url,'',headers,'','HALACIMA-PLAY-1st')
		html_blocks = re.findall('class="download(.*?)div',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)"',block,re.DOTALL)
		for link in items:
			if 'http' not in link: link = 'http:' + link
			linkLIST.append(link)
		url2 = url.replace('/article/','/online/')
		html = openURL(url2,'',headers,'','HALACIMA-PLAY-2nd')
		html_blocks = re.findall('artId.*?(.*?)col-sm-12',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall(' = \'(.*?)\'',block,re.DOTALL)
		artID = items[0]
		url2 = website0a + '/ajax/getVideoPlayer'
		headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
		items = re.findall('getVideoPlayer\(\'(.*?)\'',block,re.DOTALL)
		for server in items:
			payload = { 'Ajax' : '1' , 'art' : artID , 'server' : server }
			data = urllib.urlencode(payload)
			#html = openURL(url2,data,headers,'','HALACIMA-PLAY-3rd')
			urlLIST.append(url2)
			dataLIST.append(data)
		count = len(urlLIST)
		import concurrent.futures
		with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
			responcesDICT = dict( (executor.submit(openURL, urlLIST[i], dataLIST[i], headers,'','HALACIMA-PLAY-3rd'), i) for i in range(0,count) )
		for response in concurrent.futures.as_completed(responcesDICT):
			html = response.result()
			html = html.replace('SRC=','src=')
			links = re.findall('src=\'(.*?)\'',html,re.DOTALL)
			#if 'http' not in link: link = 'http:' + link
			linkLIST.append(links[0])
		settings.setSetting('previous.url',url)
		settings.setSetting('previous.linkLIST',str(linkLIST))
	from RESOLVERS import PLAY as RESOLVERS_PLAY
	RESOLVERS_PLAY(linkLIST,script_name,'yes')
	return

def SEARCH(search=''):
	if search=='': search = KEYBOARD()
	if search == '': return
	#search = search.replace(' ','+')
	url = website0a + '/search.html'
	headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { 'name' : search , 'search' : 'البحث' }
	data = urllib.urlencode(payload)
	html = openURL(url,data,headers,'','HALACIMA-SEARCH-1st')
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	if 'art_list' in html: ITEMS('',html)
	else: xbmcgui.Dialog().ok('no results','لا توجد نتائج للبحث')
	return



