# -*- coding: utf-8 -*-
from LIBRARY import *

#website0a = 'http://m.panet.co.il'
headers = { 'User-Agent' : '' }
script_name = 'PANET'
menu_name='_PNT_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,page,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==30: results = MENU(url)
	elif mode==31: results = CATEGORIES(url,'3')
	elif mode==32: results = ITEMS(url)
	elif mode==33: results = PLAY(url)
	elif mode==35: results = CATEGORIES(url,'1')
	elif mode==36: results = CATEGORIES(url,'2')
	elif mode==37: results = CATEGORIES(url,'4')
	elif mode==39: results = SEARCH(text,page)
	else: results = False
	return results

def MENU(website=''):
	#if website=='': addMenuItem('dir',menu_name+'بحث في الموقع','',39)
	addMenuItem('dir',website+'::'+menu_name+'مسلسلات وبرامج',website0a+'/series',31)
	addMenuItem('dir',website+'::'+menu_name+'المسلسلات الاكثر مشاهدة',website0a+'/series',37)
	addMenuItem('dir',website+'::'+menu_name+'افلام حسب النوع',website0a+'/movies',35)
	addMenuItem('dir',website+'::'+menu_name+'افلام حسب الممثل',website0a+'/movies',36)
	addMenuItem('dir',website+'::'+menu_name+'احدث الافلام',website0a+'/movies',32)
	addMenuItem('dir',website+'::'+menu_name+'مسرحيات',website0a+'/movies/genre/4/1',32)
	return

def CATEGORIES(url,select=''):
	type = url.split('/')[3]
	#xbmcgui.Dialog().ok(type, url)
	if type=='series':
		html = openURL_cached(LONG_CACHE,url,'',headers,'','PANET-CATEGORIES-1st')
		if select=='3':
			html_blocks=re.findall('categoriesMenu(.*?)seriesForm',html,re.DOTALL)
			block= html_blocks[0]
			items=re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
			for link,name in items:
				if 'كليبات مضحكة' in name: continue
				url = website0a + link
				name = name.strip(' ')
				addMenuItem('dir',menu_name+name,url,32)
		if select=='4':
			html_blocks=re.findall('video-details-panel(.*?)v></a></div>',html,re.DOTALL)
			block= html_blocks[0]
			items=re.findall('panet-thumbnail" href="(.*?)".*?src="(.*?)".*?panet-info">(.*?)<',block,re.DOTALL)
			for link,img,title in items:
				url = website0a + link
				title = title.strip(' ')
				addMenuItem('dir',menu_name+title,url,32,img)
		#xbmcgui.Dialog().ok(url,'')
	if type=='movies':
		html = openURL_cached(LONG_CACHE,url,'',headers,'','PANET-CATEGORIES-2nd')
		if select=='1':
			html_blocks=re.findall('moviesGender(.*?)select',html,re.DOTALL)
			block = html_blocks[0]
			items=re.findall('option><option value="(.*?)">(.*?)<',block,re.DOTALL)
			for value,name in items:
				url = website0a + '/movies/genre/' + value
				name = name.strip(' ')
				addMenuItem('dir',menu_name+name,url,32)
		elif select=='2':
			html_blocks=re.findall('moviesActor(.*?)select',html,re.DOTALL)
			block = html_blocks[0]
			items=re.findall('option><option value="(.*?)">(.*?)<',block,re.DOTALL)
			for value,name in items:
				name = name.strip(' ')
				url = website0a + '/movies/actor/' + value
				addMenuItem('dir',menu_name+name,url,32)
	return

def ITEMS(url):
	#xbmcgui.Dialog().ok(url,'')
	type = url.split('/')[3]
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','PANET-ITEMS-1st')
	if 'home' in url: type='episodes'
	if type=='series':
		html_blocks = re.findall('panet-thumbnails(.*?)panet-pagination',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)""><img src="(.*?)".*?h2>(.*?)<',block,re.DOTALL)
		for link,img,name in items:
			url = website0a + link 
			name = name.strip(' ')
			addMenuItem('dir',menu_name+name,url,32,img)
	if type=='movies':
		html_blocks = re.findall('advBarMars(.+?)panet-pagination',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('panet-thumbnail.*?href="(.*?)"><img src="(.*?)" alt="(.+?)"',block,re.DOTALL)
		for link,img,name in items:
			name = name.strip(' ')
			url = website0a + link
			addMenuItem('link',menu_name+name,url,33,img)
	if type=='episodes':
		page = url.split('/')[-1]
		#xbmcgui.Dialog().ok(url,'')
		if page=='1':
			html_blocks = re.findall('advBarMars(.+?)advBarMars',html,re.DOTALL)
			block = html_blocks[0]
			items = re.findall('panet-thumbnail.*?href="(.*?)"><img src="(.*?)".*?panet-title">(.*?)</div.*?panet-info">(.*?)</div',block,re.DOTALL)
			count = 0
			for link,img,episode,title in items:
				count += 1
				if count==10: break
				name = title + ' - ' + episode
				url = website0a + link
				addMenuItem('link',menu_name+name,url,33,img)
		html_blocks = re.findall('advBarMars.*?advBarMars(.+?)panet-pagination',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('panet-thumbnail.*?href="(.*?)""><img src="(.*?)".*?panet-title"><h2>(.*?)</h2.*?panet-info"><h2>(.*?)</h2',block,re.DOTALL)
		for link,img,title,episode in items:
			episode = episode.strip(' ')
			title = title.strip(' ')
			name = title + ' - ' + episode
			url = website0a + link
			addMenuItem('link',menu_name+name,url,33,img)
	html_blocks = re.findall('glyphicon-chevron-right(.+?)data-revive-zoneid="4"',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('<li><a href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,page in items:
		url = website0a + link 
		name = 'صفحة ' + page
		addMenuItem('dir',menu_name+name,url,32)
	return

def PLAY(url):
	#xbmcgui.Dialog().ok(url,'')
	if 'series' in url:
		url = website0a + '/series/v1/seriesLink/' + url.split('/')[-1]
		html = openURL_cached(SHORT_CACHE,url,'',headers,'','PANET-PLAY-1st')
		items = re.findall('url":"(.*?)"',html,re.DOTALL)
		url = items[0]
		url = url.replace('\/','/')
	else:
		html = openURL_cached(SHORT_CACHE,url,'',headers,'','PANET-PLAY-2nd')
		items = re.findall('contentURL" content="(.*?)"',html,re.DOTALL)
		url = items[0]
	PLAY_VIDEO(url,script_name)
	return

def SEARCH(search,page):
	#xbmcgui.Dialog().ok(search,page)
	if '::' in search:
		search = search.split('::')[0]
		category = False
	else: category = True
	if search=='': search = KEYBOARD()
	if search == '': return
	new_search = search.replace(' ','%20')
	typeLIST = [ 'movies' , 'series']
	if category:
		if page=='':
			page = '1'
			nameLIST = [ 'بحث عن افلام' , 'بحث عن مسلسلات']
			selection = xbmcgui.Dialog().select('اختر النوع المناسب:', nameLIST)
			if selection == -1 : return
			type = typeLIST[selection]
		else: page,type = page.split('/')
	else: page,type = '1',random.sample(typeLIST,1)
	payload = { 'query':new_search , 'searchDomain':type }
	if page!='1': payload['from'] = page
	data = urllib.urlencode(payload)
	html = openURL_cached(REGULAR_CACHE,website0a+'/search',data,headers,'','PANET-SEARCH-1st')
	#xbmc.log(str(html), level=xbmc.LOGNOTICE)
	items=re.findall('title":"(.*?)".*?link":"(.*?)"',html,re.DOTALL)
	if items:
		for title,link in items:
			url = website0a + link.replace('\/','/')
			if '/movies/' in url: addMenuItem('link',menu_name+'فيلم '+title,url,33)
			elif '/series/' in url: addMenuItem('dir',menu_name+'مسلسل '+title,url+'/1',32)
	count=re.findall('"total":(.*?)}',html,re.DOTALL)
	if count:
		pages = int(  (int(count[0])+9)   /10 )+1
		for page2 in range(1,pages):
			page2 = str(page2)
			if page2!=page:
				addMenuItem('dir','صفحة '+page2,'',39,'',page2+'/'+type,search)
	#else: xbmcgui.Dialog().ok('no results','لا توجد نتائج للبحث')
	return


