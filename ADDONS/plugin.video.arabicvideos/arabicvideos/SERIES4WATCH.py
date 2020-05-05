# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='SERIES4WATCH'
headers = { 'User-Agent' : '' }
menu_name='_SFW_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==210: results = MENU(url)
	elif mode==211: results = TITLES(url)
	elif mode==212: results = PLAY(url)
	elif mode==213: results = EPISODES(url)
	elif mode==214: results = FILTER_MENU(url)
	elif mode==215: results = FILTER_SELECT(url)
	elif mode==218: results = TERMINATED_CHANGED()
	elif mode==219: results = SEARCH(text)
	else: results = False
	return results

def TERMINATED_CHANGED():
	message = 'هذا الموقع تغير بالكامل ... وبحاجة الى اعادة برمجة من الصفر ... والمبرمج حاليا مشغول ويعاني من وعكة صحية ... ولهذا سوف يبقى الموقع مغلق الى ما شاء الله'
	xbmcgui.Dialog().ok('الموقع تغير بالكامل',message)
	return

def MENU(website=''):
	if website=='':
		addMenuItem('dir',menu_name+'بحث في الموقع','',219)
		#addMenuItem('dir',menu_name+'فلتر','',114,website0a)
	url = website0a+'/getpostsPin?type=one&data=pin&limit=25'
	addMenuItem('dir',website+'::'+menu_name+'المميزة',url,211)
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','SERIES4WATCH-MENU-1st')
	html_blocks = re.findall('FiltersButtons(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('data-get="(.*?)".*?</i>(.*?)<',block,re.DOTALL)
	for link,title in items:#[1:-1]:
		url = website0a+'/getposts?type=one&data='+link
		addMenuItem('dir',website+'::'+menu_name+title,url,211)
	html_blocks = re.findall('navigation-menu(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(http.*?)">(.*?)<',block,re.DOTALL)
	ignoreLIST = ['مسلسلات انمي','الرئيسية']
	#keepLIST = ['مسلسلات ','افلام ','برامج','عروض','كليبات','اغانى']
	for link,title in items:
		title = title.strip(' ')
		if not any(value in title for value in ignoreLIST):
		#	if any(value in title for value in keepLIST):
			addMenuItem('dir',website+'::'+menu_name+title,link,211)
	return

def TITLES(url):
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','SERIES4WATCH-TITLES-1st')
	#xbmcgui.Dialog().ok(url,html)
	if 'getposts' in url or '/search?s=' in url: block = html
	else:
		html_blocks = re.findall('MediaGrid"(.*?)class="pagination"',html,re.DOTALL)
		if html_blocks: block = html_blocks[0]
		else: return
	items = re.findall('src="(.*?)".*?href="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
	allTitles = []
	itemLIST = ['مشاهدة','فيلم','اغنية','كليب','اعلان','هداف','مباراة','عرض','مهرجان','البوم']
	for img,link,title in items:
		if '/series/' in link: continue
		link = unquote(link).strip('/')
		title = unescapeHTML(title)
		title = title.strip(' ')
		if '/film/' in link or any(value in title for value in itemLIST):
			addMenuItem('link',menu_name+title,link,212,img)
		elif '/episode/' in link and 'الحلقة' in title:
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode:
				title = '_MOD_' + episode[0]
				if title not in allTitles:
					addMenuItem('dir',menu_name+title,link,213,img)
					allTitles.append(title)
		else: addMenuItem('dir',menu_name+title,link,213,img)
	html_blocks = re.findall('class="pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<a href=["\'](http.*?)["\'].*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			link = unescapeHTML(link)
			title = unescapeHTML(title)
			title = title.replace('الصفحة ','')
			if title!='': addMenuItem('dir',menu_name+'صفحة '+title,link,211)
	return

def EPISODES(url):
	episodesCount,items,itemsNEW = -1,[],[]
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','SERIES4WATCH-EPISODES-1st')
	html_blocks = re.findall('ti-list-numbered(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		blocks = ''.join(html_blocks)
		items = re.findall('href="(.*?)"',blocks,re.DOTALL)
	items.append(url)
	items = set(items)
	#name = xbmc.getInfoLabel('ListItem.Label')
	for link in items:
		link = link.strip('/')
		title = '_MOD_' + link.split('/')[-1].replace('-',' ')
		sequence = re.findall('الحلقة-(\d+)',link.split('/')[-1],re.DOTALL)
		if sequence: sequence = sequence[0]
		else: sequence = '0'
		itemsNEW.append([link,title,sequence])
	items = sorted(itemsNEW, reverse=False, key=lambda key: int(key[2]))
	seasonsCount = str(items).count('/season/')
	episodesCount = str(items).count('/episode/')
	if seasonsCount>1 and episodesCount>0 and '/season/' not in url:
		for link,title,sequence in items:
			if '/season/' in link: addMenuItem('dir',menu_name+title,link,213)
	else:
		for link,title,sequence in items:
			if '/season/' not in link: addMenuItem('link',menu_name+title,link,212)
	return

def PLAY(url):
	linkLIST = []
	parts = url.split('/')
	html = openURL_cached(LONG_CACHE,url,'',headers,'','SERIES4WATCH-PLAY-1st')
	# watch links
	if '/watch/' in html:
		url2 = url.replace(parts[3],'watch')
		html2 = openURL_cached(LONG_CACHE,url2,'',headers,'','SERIES4WATCH-PLAY-2nd')
		html_blocks = re.findall('class="servers-list(.*?)</div>',html2,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('data-embedd="(.*?)".*?server_image">\n(.*?)\n',block,re.DOTALL)
			if items:
				id = re.findall('post_id=(.*?)"',html2,re.DOTALL)
				if id:
					id2 = id[0]
					for link,title in items:
						link = website0a+'/?postid='+id2+'&serverid='+link+'&name='+title+'__watch'
						linkLIST.append(link)
			else:
				# https://shahd4u.tv/watch/مشاهدة-برنامج-نفسنة-تقديم-انتصار-وهيدى-وشيماء-حلقة-1
				items = re.findall('data-embedd=".*?(http.*?)("|&quot;)',block,re.DOTALL)
				for link,dummy in items:
					linkLIST.append(link)
	# download links
	if '/download/' in html:
		url2 = url.replace(parts[3],'download')
		html2 = openURL_cached(LONG_CACHE,url2,'',headers,'','SERIES4WATCH-PLAY-3rd')
		id = re.findall('postId:"(.*?)"',html2,re.DOTALL)
		if id:
			id2 = id[0]
			headers2 = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
			url2 = website0a + '/ajaxCenter?_action=getdownloadlinks&postId='+id2
			html2 = openURL_cached(LONG_CACHE,url2,'',headers2,'','SERIES4WATCH-PLAY-4th')
			html_blocks = re.findall('<h3.*?(\d+)(.*?)</div>',html2,re.DOTALL)
			if html_blocks:
				for resolution,block in html_blocks:
					items = re.findall('<td>(.*?)<.*?href="(.*?)"',block,re.DOTALL)
					for name,link in items:
						linkLIST.append(link+'?name='+name+' '+resolution+'__download')
			else:
				html_blocks = re.findall('<h6(.*?)</table>',html2,re.DOTALL)
				if not html_blocks: html_blocks = [html2]
				for block in html_blocks:
					"""
					name = re.findall('serversTitle.*?>(.*?)<',block,re.DOTALL)
					if name:
						name = name[-1].replace('الدقة ','').replace('\n','')
						if name!='': name = name + ' ـ '
					else: name = ''
					"""
					name = ''
					items = re.findall('href="(http.*?)"',block,re.DOTALL)
					for link in items:
						server = '&&' + link.split('/')[2].lower() + '&&'
						server = server.replace('.com&&','').replace('.co&&','')
						server = server.replace('.net&&','').replace('.org&&','')
						server = server.replace('.live&&','').replace('.online&&','')
						server = server.replace('&&hd.','').replace('&&www.','')
						server = server.replace('&&','')
						link = link + '?name=' + name + server + '__download'
						linkLIST.append(link)
	if len(linkLIST)==0:
		xbmcgui.Dialog().ok('','الرابط ليس فيه فيديو')
	else:
		import RESOLVERS
		RESOLVERS.PLAY(linkLIST,script_name)
	return

def SEARCH(search):
	if '::' in search:
		search = search.split('::')[0]
		category = False
	else: category = True
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.replace(' ','+')
	url = website0a + '/search?s='+search
	TITLES(url)
	return
	"""
	html = openURL_cached(REGULAR_CACHE,website0a,'',headers,'','SERIES4WATCH-SEARCH-1st')
	html_blocks = re.findall('advanced-search secondary(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('data-cat="(.*?)".*?checkmark-bold">(.*?)</span>',block,re.DOTALL)
		categoryLIST,filterLIST = [],[]
		for category,title in items:
			categoryLIST.append(category)
			filterLIST.append(title)
		selection = xbmcgui.Dialog().select('اختر الفلتر المناسب:', filterLIST)
		if selection == -1 : return
		category = categoryLIST[selection]
		url = website0a + '/search?s='+search+'&category='+category
		TITLES(url)
	return
	"""



