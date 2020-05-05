# -*- coding: utf-8 -*-
from LIBRARY import *

script_name = 'ALKAWTHAR'
menu_name='_KWT_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,page,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==130: results = MENU(url)
	#elif mode==131: results = TITLES(url)
	elif mode==132: results = CATEGORIES(url)
	elif mode==133: results = EPISODES(url,page)
	elif mode==134: results = PLAY(url)
	elif mode==135: results = LIVE()
	elif mode==139: results = SEARCH(text,url)
	else: results = False
	return results

def MENU(website=''):
	if website=='':
		addMenuItem('link',menu_name+'البث الحي لقناة الكوثر','',135,'','','IsPlayable=no')
		addMenuItem('dir',menu_name+'بحث في الموقع','',139)
	addMenuItem('dir',website+'::'+menu_name+'المسلسلات',website0a+'/category/543',132,'','1')
	addMenuItem('dir',website+'::'+menu_name+'الافلام',website0a+'/category/628',132,'','1')
	addMenuItem('dir',website+'::'+menu_name+'برامج الصغار والشباب',website0a+'/category/517',132,'','1')
	addMenuItem('dir',website+'::'+menu_name+'ابرز البرامج',website0a+'/category/1763',132,'','1')
	addMenuItem('dir',website+'::'+menu_name+'المحاضرات',website0a+'/category/943',132,'','1')
	addMenuItem('dir',website+'::'+menu_name+'عاشوراء',website0a+'/category/1353',132,'','1')
	addMenuItem('dir',website+'::'+menu_name+'البرامج الاجتماعية',website0a+'/category/501',132,'','1')
	addMenuItem('dir',website+'::'+menu_name+'البرامج الدينية',website0a+'/category/509',132,'','1')
	addMenuItem('dir',website+'::'+menu_name+'البرامج الوثائقية',website0a+'/category/553',132,'','1')
	addMenuItem('dir',website+'::'+menu_name+'البرامج السياسية',website0a+'/category/545',132,'','1')
	addMenuItem('dir',website+'::'+menu_name+'كتب',website0a+'/category/291',132,'','1')
	addMenuItem('dir',website+'::'+menu_name+'تعلم الفارسية',website0a+'/category/88',132,'','1')
	addMenuItem('dir',website+'::'+menu_name+'ارشيف البرامج',website0a+'/category/1279',132,'','1')
	return
	"""
	html = openURL_cached(REGULAR_CACHE,website0a,'','','','ALKAWTHAR-MENU-1st')
	html_blocks=re.findall('dropdown-menu(.*?)dropdown-toggle',html,re.DOTALL)
	block = html_blocks[1]
	items=re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		title = title.strip(' ')
		typeLIST = ['/religious','/social','/political']
		if any(value in link for value in typeLIST):
			title = 'البرامج ' + title
		url = website0a + link
		if '/category' in url:
			addMenuItem('dir',menu_name+title,url,132,'','1')
		elif '/conductor' not in url:
			addMenuItem('dir',menu_name+title,url,131,'','1')
	"""

"""
def TITLES(url):
	typeLIST = ['/religious','/social','/political','/films','/series']
	html = openURL_cached(REGULAR_CACHE,url,'','','','ALKAWTHAR-TITLES-1st')
	html_blocks = re.findall('titlebar(.*?)titlebar',html,re.DOTALL)
	block = html_blocks[0]
	if any(value in url for value in typeLIST):
		items = re.findall("src='(.*?)'.*?href='(.*?)'.*?>(.*?)<",block,re.DOTALL)
		for img,link,title in items:
			title = title.strip(' ')
			link = website0a + link
			addMenuItem('dir',menu_name+title,link,133,img,'1')
	elif '/docs' in url:
		items = re.findall("src='(.*?)'.*?<h2>(.*?)</h2>.*?href='(.*?)'",block,re.DOTALL)
		for img,title,link in items:
			title = title.strip(' ')
			link = website0a + link
			addMenuItem('dir',menu_name+title,link,133,img,'1')
	return
"""

def CATEGORIES(url):
	category = url.split('/')[-1]
	html = openURL_cached(LONG_CACHE,url,'','','','ALKAWTHAR-CATEGORIES-1st')
	html_blocks = re.findall('parentcat(.*?)</div>',html,re.DOTALL)
	if not html_blocks:
		EPISODES(url,'1')
		return
	block = html_blocks[0]
	items = re.findall("href='(.*?)'.*?>(.*?)<",block,re.DOTALL)
	for link,title in items:
		#categoryNew = url.split('/')[-1]
		#if category==categoryNew: continue
		title = title.strip(' ')
		link = website0a + link
		addMenuItem('dir',menu_name+title,link,132,'','1')
	return

def EPISODES(url,page):
	#xbmcgui.Dialog().ok(url, page)
	html = openURL_cached(REGULAR_CACHE,url,'','','','ALKAWTHAR-EPISODES-1st')
	items = re.findall('totalpagecount=[\'"](.*?)[\'"]',html,re.DOTALL)
	if items[0]=='':
		xbmcgui.Dialog().ok('فرع فارغ','لا يوجد حاليا ملفات فيديو في هذا الفرع')
		return
	totalpages = int(items[0])
	name = re.findall('main-title.*?</a> >(.*?)<',html,re.DOTALL)
	if name: name = name[0].replace('\n','').strip(' ')
	else: name = xbmc.getInfoLabel('ListItem.Label')
	#xbmcgui.Dialog().ok(name, str(''))
	if '/category/' in url:
		category = url.split('/')[-1]
		url2 = website0a + '/category/' + category + '/' + page
		html = openURL_cached(REGULAR_CACHE,url2,'','','','ALKAWTHAR-EPISODES-2nd')
		html_blocks = re.findall('currentpagenumber(.*?)javascript',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('src="(.*?)".*?full(.*?)>.*?href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for img,type,link,title in items:
			if 'video' not in type: continue
			if 'مسلسل' in title and 'حلقة' not in title: continue
			title = title.replace('\r\n','')
			title = title.strip(' ')
			if 'مسلسل' in name and 'حلقة' in title and 'مسلسل' not in title:
				title = '_MOD_' + name + ' - ' + title
			link = website0a + link
			if category=='628':
				addMenuItem('dir',menu_name+title,link,133,img,'1')
			else:
				addMenuItem('link',menu_name+title,link,134,img)
	elif '/episode/' in url:
		html_blocks = re.findall('playlist(.*?)col-md-12',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall("video-track-text.*?loadVideo\('(.*?)','(.*?)'.*?>(.*?)<",block,re.DOTALL)
			for link,img,title in items:
				title = title.strip(' ')
				addMenuItem('link',menu_name+title,link,134,img)
		elif '/category/628' in html:
				title = '_MOD_' + 'ملف التشغيل - ' + name
				addMenuItem('link',menu_name+title,url,134)
		else:
			items = re.findall('id="Categories.*?href=\'(.*?)\'',html,re.DOTALL)
			category = items[0].split('/')[-1]
			url = website0a + '/category/' + category
			CATEGORIES(url)
			return
		totalpages = 0
		"""
			episodeID = url.split('/')[-1]
			items = re.findall('id="Categories.*?href=\'(.*?)\'',html,re.DOTALL)
			category = items[0].split('/')[-1]
			url2 = website0a + '/ajax/category/' + category + '/' + page
			html = openURL_cached(REGULAR_CACHE,url2,'','','','ALKAWTHAR-EPISODES-3rd')
			items = re.findall('src="(.*?)".*?href="(.*?)"> <h5>(.*?)<',html,re.DOTALL)
			for img,link,title in items:
				link = website0a + link
				episodeIDnew = link.split('/')[-1]
				if episodeIDnew==episodeID: continue
				title = title.strip(' ')
				addMenuItem('link',menu_name+title,link,134,img)
		"""
	title = 'صفحة '
	for i in range(1,1+totalpages):
		if page!=str(i):
			addMenuItem('dir',menu_name+title+str(i),url,133,'',str(i))
	return

def PLAY(url):
	#xbmcgui.Dialog().ok(url, '')
	if '/news/' in url or '/episode/' in url:
		html = openURL_cached(LONG_CACHE,url,'','','','ALKAWTHAR-PLAY-1st')
		items = re.findall("mobilevideopath.*?value='(.*?)'",html,re.DOTALL)
		if items: url = items[0]
		else:
			xbmcgui.Dialog().ok('','لا يوجد ملف فيديو')
			return
	PLAY_VIDEO(url,script_name,'yes')
	return

def LIVE():
	xbmcgui.Dialog().notification('جاري تشغيل القناة','')
	url = website0a+'/live'
	html = openURL_cached(LONG_CACHE,url,'','','','ALKAWTHAR-LIVE-1st')
	items = re.findall('live-container.*?src="(.*?)"',html,re.DOTALL)
	url = items[0]
	html = openURL_cached(NO_CACHE,url,'','','','ALKAWTHAR-LIVE-2nd')
	token = re.findall('csrf-token" content="(.*?)"',html,re.DOTALL)
	token = token[0]
	server = SERVER(url)
	url = re.findall("playUrl = '(.*?)'",html,re.DOTALL)
	url = server+url[0]
	headers2 = { 'Content-Type':'application/x-www-form-urlencoded' , 'X-CSRF-TOKEN':token }
	response = openURL_requests_cached(NO_CACHE,'POST',url,'',headers2,False,'','ALKAWTHAR-LIVE-3rd')
	html = response.text
	url = re.findall('"(.*?)"',html,re.DOTALL)
	url = url[0].replace('\/','/')
	#xbmcgui.Dialog().ok(url,html)
	PLAY_VIDEO(url,script_name,'no')
	return

def SEARCH(search,url=''):
	if '::' in search: search = search.split('::')[0]
	if url=='':
		#search = 'man'
		if search=='': search = KEYBOARD()
		if search=='': return
		#search = search.replace(' ','+')
		#search = '-tag docs OR films OR series OR episode OR episodes OR category OR news mp4 '+search
		search = '"mp4" '+search
		search = quote(search)
		url = website0a+'/search?q='+search
		html = openURL_cached(NO_CACHE,url,'','','','ALKAWTHAR-SEARCH-1st')
		#with open('S:\\emad1.html', 'w') as f: f.write(html)
		cx = re.findall("var cx = '(.*?)'",html,re.DOTALL)[0]
		url = re.findall("gcse.src = '(.*?)'",html,re.DOTALL)[0]
		url = url+cx
		html = openURL_cached(NO_CACHE,url,'','','','ALKAWTHAR-SEARCH-2nd')
		#with open('S:\\emad2.html', 'w') as f: f.write(html)
		cse_token = re.findall('cse_token": "(.*?)"',html,re.DOTALL)[0]
		cselibVersion = re.findall('cselibVersion": "(.*?)"',html,re.DOTALL)[0]
		randomAPI = str(random.randint(1111,9999))
		url = 'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=ar&source=gcsc&gss=.com&cselibv='+cselibVersion+'&cx='+cx+'&q='+search+'&safe=off&cse_tok='+cse_token+'&sort=&exp=csqr,cc&callback=google.search.cse.api'+randomAPI+'&start=0'
	html = openURL_cached(NO_CACHE,url,'','','','ALKAWTHAR-SEARCH-3rd')
	#with open('S:\\emad3.html', 'w') as f: f.write(html)
	#LOG_THIS('NOTICE','EMAD  '+url)
	items = re.findall('cacheUrl":.*?"title": "(.*?)".*?"url": "(.*?)".*?"metatags": {(.*?)}',html,re.DOTALL)
	for title,link,tags in items:
		if 'video' not in tags: continue
		title = unescapeHTML(title)
		title = title.replace('\u003c','<').replace('\u003e','>')
		title = title.replace('<b>','').replace('</b>','').replace('  ',' ')
		if '/category/' in link:	# or '/program/' in link:
			vars = link.split('/')
			category = vars[4]
			url = website0a + '/category/' + category
			if len(vars)>5:
				page1 = vars[5]
				addMenuItem('dir',menu_name+title,url,133,'',page1)
			else:
				addMenuItem('dir',menu_name+title,url,132)
		elif '/episode/' in link:
			addMenuItem('dir',menu_name+title,link,133,'','1')
		else:
			addMenuItem('link',menu_name+title,link,134)
	items = re.findall('"label": (.*?),.*?"start": "(.*?)"',html,re.DOTALL)
	if items:
		currentPage = re.findall('"currentPageIndex": (.*?),',html,re.DOTALL)
		currentPage = str(int(currentPage[0])+1)
		for title,start in items:
			if title==currentPage: continue
			url = url.split('start=')[0]+'start='+start
			addMenuItem('dir',menu_name+'صفحة '+title,url,139)
	return


