# -*- coding: utf-8 -*-
from LIBRARY import *

script_name = 'IFILM'
menu_name='_IFL_'
website0a = WEBSITES[script_name][0]
website0b = WEBSITES[script_name][1]
website0c = WEBSITES[script_name][2]
website0d = WEBSITES[script_name][3]
website1  = 'http://93.190.24.122'

def MAIN(mode,url,page,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==20: results = LANGUAGE_MENU()
	elif mode==21: results = MENU(url)
	elif mode==22: results = TITLES(url,page)
	elif mode==23: results = EPISODES(url,page)
	elif mode==24: results = PLAY(url)
	elif mode==25: results = MUSIC_MENU(url)
	elif mode==27: results = LIVE(url)
	elif mode==28: results = LIVE_MENU()
	elif mode==29: results = SEARCH(url,text)
	else: results = False
	return results

def LANGUAGE_MENU():
	addMenuItem('dir',menu_name+'عربي',website0a,21,'','101')
	addMenuItem('dir',menu_name+'English',website0b,21,'','101')
	addMenuItem('dir',menu_name+'فارسى',website0c,21,'','101')
	addMenuItem('dir',menu_name+'فارسى 2',website0d,21,'','101')
	return

def LIVE_MENU():
	addMenuItem('dir',menu_name+'عربي',website0a,27)
	addMenuItem('dir',menu_name+'English',website0b,27)
	addMenuItem('dir',menu_name+'فارسى',website0c,27)
	addMenuItem('dir',menu_name+'فارسى 2',website0d,27)
	return

def MENU(website0):
	website = website0
	if website0=='IFILM_ARABIC': website0 = website0a
	elif website0=='IFILM_ENGLISH': website0 = website0b
	else: website = ''
	lang = LANG(website0)
	if lang=='ar' or website!='':
		name0 = 'بحث في الموقع'
		name1 = 'المسلسلات الحالية'
		name2 = 'المسلسلات مرتبة حسب الاحدث'
		name3 = 'المسلسلات مرتبة حسب الابجدية'
		name4 = 'البث الحي لقناة اي فيلم'
	elif lang=='en':
		name0 = 'Search in site'
		name1 = 'Current Series'
		name2 = 'Series sorted by Latest'
		name3 = 'Series sorted by Alphabet'
		name4 = 'Live broadcast of iFilm channel'
	elif lang in ['fa','fa2']:
		name0 = 'جستجو در سایت'
		name1 = 'سريال ها جاری'
		name2 = 'سريال ها مرتب سازى براساس'
		name3 = 'سريال ها مرتب حروف الفبا'
		name4 = 'پخش زنده از اي فيلم كانال'
	if website=='':
		addMenuItem('dir',menu_name+name4,website0,27,'','','IsPlayable=False')
		addMenuItem('dir',menu_name+name0,website0,29)
	html = openURL_cached(LONG_CACHE,website0+'/home','','','','IFILM-MAIN_MENU-1st')
	#html = openURL_cached(LONG_CACHE,website0+'/home/index','','','','IFILM-MAIN_MENU-1st')
	html_blocks=re.findall('button-menu(.*?)nav',html,re.DOTALL)
	menu = ['Series', 'Program', 'Music']
	block = html_blocks[0]
	items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		if any(value in link for value in menu):
			#xbmcgui.Dialog().ok(link,str(title))
			url = website0+link
			if 'Series' in link:
				addMenuItem('dir',website+'::'+menu_name+name1,url,22,'','100')
				addMenuItem('dir',website+'::'+menu_name+name2,url,22,'','101')
				addMenuItem('dir',website+'::'+menu_name+name3,url,22,'','201')
			elif 'Music' in link:
				if website!='': title = 'موسيقى'
				addMenuItem('dir',website+'::'+menu_name+title,url,25,'','101')
			elif 'Program':
				if website!='': title = 'برامج'
				addMenuItem('dir',website+'::'+menu_name+title,url,22,'','101')
	return

def MUSIC_MENU(url):
	website0 = SITE(url)
	html = openURL_cached(LONG_CACHE,url,'','','','IFILM-MUSIC_MENU-1st')
	html_blocks = re.findall('Music-tools-header(.*?)Music-body',html,re.DOTALL)
	block = html_blocks[0]
	title = re.findall('<p>(.*?)</p>',block,re.DOTALL)[0]
	addMenuItem('dir',menu_name+title,url,22,'','101')
	items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		link = website0 + link
		addMenuItem('dir',menu_name+title,link,23,'','101')
	return

def TITLES(url,page):
	website0 = SITE(url)
	lang = LANG(url)
	type = url.split('/')[-1]
	order = str(int(page)/100)
	page = str(int(page)%100)
	#xbmcgui.Dialog().ok(url, type)
	if type=='Series' and page=='0':
		html = openURL_cached(REGULAR_CACHE,url,'','','','IFILM-TITLES-1st')
		html_blocks = re.findall('serial-body(.*?)class="row',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?src=(.*?)>.*?h3>(.*?)<',block,re.DOTALL)
		for link,img,title in items:
			title = escapeUNICODE(title)
			title = unescapeHTML(title)
			link = website0 + link
			img = website0 + quote(img)
			addMenuItem('dir',menu_name+title,link,23,img,order+'01')
	count_items=0
	if type=='Series': category='3'
	if type=='Program': category='7'
	if (type=='Series' or type=='Program') and page!='0':
		url2 = website0+'/Home/PageingItem?category='+category+'&page='+page+'&size=30&orderby='+order
		html = openURL_cached(REGULAR_CACHE,url2,'','','','IFILM-TITLES-2nd')
		#xbmcgui.Dialog().ok(url2, html)
		items = re.findall('"Id":(.*?),"Title":(.*?),.+?"ImageAddress_S":"(.*?)"',html,re.DOTALL)
		for id,title,img in items:
			title = escapeUNICODE(title)
			title = title.replace('\\','')
			title = title.replace('"','')
			count_items += 1
			link = website0 + '/' + type + '/Content/' + id
			img = website0 + quote(img)
			addMenuItem('dir',menu_name+title,link,23,img,order+'01')
	if type=='Music':
		html = openURL_cached(REGULAR_CACHE,website0+'/Music/Index?page='+page,'','','','IFILM-TITLES-3rd')
		html_blocks = re.findall('pagination-demo(.*?)pagination-demo',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>',block,re.DOTALL)
		for link,img,title in items:
			count_items += 1
			img = website0 + img
			link = website0 + link
			addMenuItem('dir',menu_name+title,link,23,img,'101')
	if count_items>20:
		title='صفحة '
		if lang=='en': title = 'Page '
		if lang=='fa': title = 'صفحه '
		if lang=='fa2': title = 'صفحه '
		for count_page in range(1,11) :
			if not page==str(count_page):
				counter = '0'+str(count_page)
				addMenuItem('dir',menu_name+title+str(count_page),url,22,'',order+counter[-2:])
	return

def EPISODES(url,page):
	website0 = SITE(url)
	lang = LANG(url)
	parts = url.split('/')
	id,type = parts[-1],parts[3]
	order = str(int(page)/100)
	page = str(int(page)%100)
	count_items=0
	#xbmcgui.Dialog().ok(url, type)
	if type=='Series':
		html = openURL_cached(REGULAR_CACHE,url,'','','','IFILM-EPISODES-1st')
		items = re.findall('Comment_panel_Item.*?p>(.*?)<i.+?var inter_ = (.*?);.*?src="(.*?)\'.*?data-url="(.*?)\'',html,re.DOTALL)
		title = ' - الحلقة '
		if lang=='en': title = ' - Episode '
		if lang=='fa': title = ' - قسمت '
		if lang=='fa2': title = ' - قسمت '
		if lang=='fa': linklang = ''
		else: linklang = lang
		for name,count,img,link in items:
			for episode in range(int(count),0,-1):
				img1 = img + linklang + id + '/' + str(episode) + '.png' 
				link1 = link + linklang + id + '/' + str(episode) + '.mp4' 
				name1 = name + title + str(episode)
				name1 = unescapeHTML(name1)
				addMenuItem('link',menu_name+name1,link1,24,img1)
	if type=='Program':
		url2 = website0+'/Home/PageingAttachmentItem?id='+str(id)+'&page='+page+'&size=30&orderby=1'
		html = openURL_cached(REGULAR_CACHE,url2,'','','','IFILM-EPISODES-2nd')
		items = re.findall('Episode":(.*?),.*?ImageAddress_S":"(.*?)".*?VideoAddress":"(.*?)".*?Discription":"(.*?)".*?Caption":"(.*?)"',html,re.DOTALL)
		title = ' - الحلقة '
		if lang=='en': title = ' - Episode '
		if lang=='fa': title = ' - قسمت '
		if lang=='fa2': title = ' - قسمت '
		for episode,img,link,desc,name in items:
			count_items += 1
			img1 = website1 + quote(img)
			link1 = website1 + quote(link)
			name = escapeUNICODE(name)
			name1 = name + title + str(episode)
			addMenuItem('link',menu_name+name1,link1,24,img1)
	if type=='Music':
		if 'Content' in url and 'category' not in url:
			url2 = website0+'/Music/GetTracksBy?id='+str(id)+'&page='+page+'&size=30&type=0'
			html = openURL_cached(REGULAR_CACHE,url2,'','','','IFILM-EPISODES-3rd')
			items = re.findall('ImageAddress_S":"(.*?)".*?VoiceAddress":"(.*?)".*?Caption":"(.*?)","Title":"(.*?)"',html,re.DOTALL)
			for img,link,name,title in items:
				count_items += 1
				img1 = website1 + quote(img)
				link1 = website1 + quote(link)
				name1 = name + ' - ' + title
				name1 = name1.strip(' ')
				name1 = escapeUNICODE(name1)
				addMenuItem('link',menu_name+name1,link1,24,img1)
		elif 'Clips' in url:
			url2 = website0+'/Music/GetTracksBy?id=0&page='+page+'&size=30&type=15'
			html = openURL_cached(REGULAR_CACHE,url2,'','','','IFILM-EPISODES-4th')
			items = re.findall('ImageAddress_S":"(.*?)".*?Caption":"(.*?)".*?VideoAddress":"(.*?)"',html,re.DOTALL)
			for img,title,link in items:
				count_items += 1
				img1 = website1 + quote(img)
				link1 = website1 + quote(link)
				name1 = title.strip(' ')
				name1 = escapeUNICODE(name1)
				addMenuItem('link',menu_name+name1,link1,24,img1)
		elif 'category' in url:
			if 'category=6' in url:
				html = openURL_cached(REGULAR_CACHE,website0+'/Music/GetTracksBy?id=0&page='+page+'&size=30&type=6','','','','IFILM-EPISODES-5th')
			elif 'category=4' in url:
				html = openURL_cached(REGULAR_CACHE,website0+'/Music/GetTracksBy?id=0&page='+page+'&size=30&type=4','','','','IFILM-EPISODES-6th')
			items = re.findall('ImageAddress_S":"(.*?)".*?VoiceAddress":"(.*?)".*?Caption":"(.*?)","Title":"(.*?)"',html,re.DOTALL)
			for img,link,name,title in items:
				count_items += 1
				img1 = website1 + quote(img)
				link1 = website1 + quote(link)
				name1 = name + ' - ' + title
				name1 = name1.strip(' ')
				name1 = escapeUNICODE(name1)
				addMenuItem('link',menu_name+name1,link1,24,img1)
	if type=='Music' or type=='Program':
		if count_items>25:
			title='صفحة '
			if lang=='en': title = ' Page '
			if lang=='fa': title = ' صفحه '
			if lang=='fa2': title = ' صفحه '
			for count_page in range(1,11):
				if not page==str(count_page):
					counter = '0'+str(count_page)
					addMenuItem('dir',menu_name+title+str(count_page),url,23,'',order+counter[-2:])
	return

def PLAY(url):
	#logging.warning('emad2:  '+ url)
	PLAY_VIDEO(url,script_name,'yes')
	return
	
def SITE(url):
	if website0a in url: site = website0a
	elif website0b in url: site = website0b
	elif website0c in url: site = website0c
	elif website0d in url: site = website0d
	return site

def LANG(url):
	lang = ''
	if   website0a in url: lang = 'ar'
	elif website0b in url: lang = 'en'
	elif website0c in url: lang = 'fa'
	elif website0d in url: lang = 'fa2'
	return lang

def LIVE(url):
	lang = LANG(url)
	url2 = url + '/Home/Live'
	html = openURL_cached(LONG_CACHE,url2,'','','','IFILM-LIVE-1st')
	items = re.findall('source src="(.*?)"',html,re.DOTALL)
	url3 = items[0]
	PLAY_VIDEO(url3,script_name,'no')
	return

def SEARCH(url,search=''):
	if '::' in search:
		search = search.split('::')[0]
		category = False
	else: category = True
	if search=='': search = KEYBOARD()
	if search == '': return
	if url=='' and category:
		urlLIST = [ website0a , website0b , website0c , website0d ]
		nameLIST = [ 'عربي' , 'English' , 'فارسى' , 'فارسى 2' ]
		selection = xbmcgui.Dialog().select('اختر اللغة المناسبة:', nameLIST)
		if selection == -1 : return ''
		url = urlLIST[selection]
	else: url = website0a
	new_search = search.replace(' ','+')
	lang = LANG(url)
	url2 = url + "/Home/Search?searchstring=" + new_search
	#xbmcgui.Dialog().ok(lang,url2)
	html = openURL_cached(REGULAR_CACHE,url2,'','','','IFILM-SEARCH-1st')
	items = re.findall('"ImageAddress_S":"(.*?)".*?"CategoryId":(.*?),"Id":(.*?),"Title":(.*?),',html,re.DOTALL)
	if items:
		for img,category,id,title in items:
			if category=='3' or category=='7':
				title = title.replace('\\','')
				title = title.replace('"','')
				if category=='3':
					type = 'Series'
					if lang=='ar': name = 'مسلسل : '
					elif lang=='en': name = 'Series : '
					elif lang=='fa': name = 'سريال ها : '
					elif lang=='fa2': name = 'سريال ها : '
				if category=='7':
					type = 'Program'
					if lang=='ar': name = 'برنامج : '
					elif lang=='en': name = 'Program : '
					elif lang=='fa': name = 'برنامه ها : '
					elif lang=='fa2': name = 'برنامه ها : '
				title = name + title
				link = url + '/' + type + '/Content/' + id
				img = url + quote(img)
				addMenuItem('dir',menu_name+title,link,23,img,'101')
	#else: xbmcgui.Dialog().ok('no results','لا توجد نتائج للبحث')
	return


