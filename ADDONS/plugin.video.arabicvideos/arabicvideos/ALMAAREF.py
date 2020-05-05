# -*- coding: utf-8 -*-
from LIBRARY import *

script_name = 'ALMAAREF'
headers = { 'User-Agent' : '' }
menu_name='_MRF_'
website0a = WEBSITES[script_name][0]
website0b = WEBSITES[script_name][1]

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==40: results = MENU(url)
	elif mode==41: results = LIVE()
	elif mode==42: results = EPISODES(url)
	elif mode==43: results = PLAY(url)
	elif mode==44: results = CATEGORIES(url,text)
	elif mode==45: results = TITLES(url,text)
	elif mode==46: results = PROGRAMS()
	elif mode==47: results = PLAY_NEWWEBSITE(url)
	elif mode==49: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	if website=='':
		addMenuItem('link',menu_name+'البث الحي لقناة المعارف','',41,'','','IsPlayable=no')
		addMenuItem('dir',menu_name+'بحث في الموقع','',49)
	addMenuItem('dir',website+'::'+menu_name+'البرامج الحالية','',46)
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','ALMAAREF-MENU-1st')
	items = re.findall('<h2><a href="(.*?)">(.*?)</a></h2>',html,re.DOTALL)
	for link,name in items:
		addMenuItem('dir',website+'::'+menu_name+name,link,45,'','','3')
	name = re.findall('recent-default.*?<h2>(.*?)</h2>',html,re.DOTALL)
	if name:
		addMenuItem('dir',website+'::'+menu_name+name[0],website0a,45,'','','2')
	name = ['ارشيف البرامج']
	#name = re.findall('categories"><div class="widget-top"><h4>(.*?)</h4>',html,re.DOTALL)
	if name:
		addMenuItem('dir',website+'::'+menu_name+name[0],website0a,44,'','','0')
	return

def TITLES(url,select):
	notvideosLIST = ['تطبيقات الاجهزة الذكية','جدول البرامج','اوقات برامجنا']
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','ALMAAREF-TITLES-1st')
	if select=='2':
		html_blocks2=re.findall('recent-default(.*?)class="clear"',html,re.DOTALL)
		if html_blocks2:
			block = html_blocks2[0]
			items=re.findall('src="(.*?)".*?href="(.*?)" rel="bookmark">(.*?)<',block,re.DOTALL)
			for img,url,title in items:
				if not any(value in title for value in notvideosLIST):
					title = unescapeHTML(title)
					addMenuItem('dir',menu_name+title,url,42,img)
	elif select=='3':
		html_blocks3=re.findall('archive-box(.*?)script',html,re.DOTALL)
		if html_blocks3:
			block = html_blocks3[0]
			items=re.findall('h2.*?href="(.*?)">(.*?)<.*?src="(.*?)"',block,re.DOTALL)
			for url,title,img in items:
				if not any(value in title for value in notvideosLIST):
					title = unescapeHTML(title)
					addMenuItem('dir',menu_name+title,url,42,img)
	html_blocks4=re.findall('class="pagination"(.*?)<h',html,re.DOTALL)
	if html_blocks4:
		block = html_blocks4[0]
		items=re.findall('href="(.*?)".*?title="(.*?)"',block,re.DOTALL)
		for url,title in items:
			title = unescapeHTML(title)
			title = 'صفحة ' + title
			addMenuItem('dir',menu_name+title,url,45,'','',select)
	return

def EPISODES(url):
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','ALMAAREF-EPISODES-1st')
	html_blocks=re.findall('entry-title"><span itemprop="name">(.*?)<',html,re.DOTALL)
	if html_blocks:
		name = html_blocks[0]
		name = unescapeHTML(name)
		html_blocks=re.findall('wp-playlist-script(.*?).entry',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items=re.findall('src":"(.*?)".*?title":"(.*?)".*?meta":(.*?),.*?image":{"src":"(.*?)".*?thumb":{"src":"(.*?)"',block,re.DOTALL)
			for link,title,meta,img1,img2 in items:
				img1 = img1.replace('\/','/')
				img2 = img2.replace('\/','/')
				link = link.replace('\/','/')
				title = escapeUNICODE(title)
				link = escapeUNICODE(link)
				title = title.split(' ')[-1]
				title = '_MOD_' + name + ' - ' + title
				duration = re.findall('length_formatted":"(.*?)"',meta,re.DOTALL)
				if duration: addMenuItem('link',menu_name+title,link,43,img2,duration[0])
				else: addMenuItem('link',menu_name+title,link,43,img2)
		else:
			items=re.findall('itemprop="name">(.*?)<.*?contentUrl" content="(.*?)".*?image.*?url":"(.*?)"',html,re.DOTALL)
			for title,link,img in items:
				img = img.replace('\/','/')
				title = escapeUNICODE(title)
				link = escapeUNICODE(link)
				addMenuItem('link',menu_name+title,link,43,img)
			#PLAY_FROM_DIRECTORY(url)
	else:
		html_blocks=re.findall('id="dropdown-menu-series"(.*?)</ul>',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			#xbmcgui.Dialog().ok(url, block)
			items=re.findall('href="(.*?)" title="(.*?)"',block,re.DOTALL)
			for link,title in items:
				title = unescapeHTML(title)
				addMenuItem('link',menu_name+title,link,47)
	return

def PLAY(url):
	url = url.replace(' ','%20')
	PLAY_VIDEO(url,script_name)
	return

def PLAY_NEWWEBSITE(url):
	html = openURL_cached(LONG_CACHE,url,'',headers,'','ALMAAREF-PLAY_NEWWEBSITE-1st')
	link = re.findall('itemprop="contentURL" content="(.*?)"',html,re.DOTALL)
	PLAY(link[0])
	return

def CATEGORIES(url,category):
	#xbmcgui.Dialog().ok(type, url)
	html = openURL_cached(LONG_CACHE,url,'',headers,'','ALMAAREF-CATEGORIES-1st')
	html_blocks=re.findall('cat1.a\(0,(.*?)document.write',html,re.DOTALL)
	block= html_blocks[0]
	items=re.findall('cat1.a\((.*?),(.*?),\'(.*?)\',\'\',\'(.*?)\'',block,re.DOTALL)
	exist=False
	notvideosLIST = ['-399','5643','2306','5654','10716','10277','7946']
	for cat,parent,title,link in items:
		if parent == category and cat not in notvideosLIST:
			title = unescapeHTML(title)
			if 'وقات برامج' in title: continue
			if '(' in title:
				title = '_MOD_' + title.replace(re.findall(' \(.*?\)',title)[0],'')
			url = website0a + '/' + link
			if cat == '-165': title = '_MOD_' + 'السيد صباح شبر (60)'
			if '-' in cat: addMenuItem('dir',menu_name+title,url,44,'','',cat)
			else: addMenuItem('dir',menu_name+title,url,42)
			exist=True
	if not exist: TITLES(url,'3')
	return

def PROGRAMS():
	#xbmcgui.Dialog().ok(type, url)
	html = openURL_cached(REGULAR_CACHE,website0a,'',headers,'','ALMAAREF-PROGRAMS-1st')
	html_blocks = re.findall('mega-menu-block(.*?)mega-menu',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		addMenuItem('dir',menu_name+title,link,44)
	return

def LIVE():
	html = openURL_cached(LONG_CACHE,'http://live.almaaref.tv','',headers,'','ALMAAREF-LIVE-1st')
	items = re.findall('sourceURL":"(.*?)"',html,re.DOTALL)
	url = unquote(items[0])
	#xbmcgui.Dialog().ok(url,str(html))
	PLAY_VIDEO(url,script_name,'no')
	return

def SEARCH(search):
	if '::' in search:
		search = search.split('::')[0]
		exit = False
	else: exit = True
	if search=='': search = KEYBOARD()
	if search == '': return
	new_search = search.replace(' ','%20')
	url = website0b + '/?s=' + new_search
	TITLES(url,'3')
	return

