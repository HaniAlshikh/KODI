# -*- coding: utf-8 -*-
from LIBRARY import *

headers = { 'User-Agent' : '' }
script_name='AKWAM'
menu_name='_AKW_'
website0a = WEBSITES[script_name][0]
#noEpisodesLIST = ['فيلم','كليب','العرض الاسبوعي','مسرحية','مسرحيه','اغنية','اعلان','لقاء']
#proxy = '||MyProxyUrl=https://159.203.87.130:3128'
#proxy = '||MyProxyUrl='+PROXIES[6][1]
proxy = ''

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==240: results = MENU(url)
	elif mode==241: results = TITLES(url+proxy,text)
	elif mode==242: results = EPISODES(url+proxy)
	elif mode==243: results = PLAY(url+proxy)
	elif mode==244: results = FILTERS_MENU(url+proxy,'FILTERS::'+text)
	elif mode==245: results = FILTERS_MENU(url+proxy,'CATEGORIES::'+text)
	elif mode==249: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	if website=='': addMenuItem('dir',website+'::'+menu_name+'بحث في الموقع','',249)
	addMenuItem('dir',website+'::'+menu_name+'المميزة',website0a+proxy,241,'','','featured')
	#addMenuItem('dir',website+'::'+menu_name+'المزيد',website0a+proxy,242,'','','more')
	#addMenuItem('dir',website+'::'+menu_name+'الاخبار',website0a+proxy,242,'','','news')
	if website=='': addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	html = openURL_cached(LONG_CACHE,website0a+proxy,'',headers,'','AKWAM-MENU-1st')
	html_blocks = re.findall('class="menu(.*?)<nav',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?text">(.*?)<',block,re.DOTALL)
		ignoreLIST = ['ألعاب','برامج']
		for link,title in items:
			if title not in ignoreLIST:
				title = title+' مصنفة'
				addMenuItem('dir',website+'::'+menu_name+title,link,245)
		if website=='': addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
		for link,title in items:
			if title not in ignoreLIST:
				title = title+' مفلترة'
				addMenuItem('dir',website+'::'+menu_name+title,link,244)
	return

def TITLES(url,type=''):
	#xbmcgui.Dialog().ok(url,'TITLES')
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','AKWAM-TITLES-1st')
	if type=='featured':
		html_blocks = re.findall('swiper-container(.*?)swiper-button-prev',html,re.DOTALL)
	else:
		html_blocks = re.findall('class="widget"(.*?)main-footer',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('src="(.*?)".*?href="(.*?)".*?text-white">(.*?)<',block,re.DOTALL)
		for img,link,title in items:
			if '/series/' in link or '/shows/' in link:
				addMenuItem('dir',menu_name+title,link,242,img)
			else: addMenuItem('link',menu_name+title,link,243,img)
	html_blocks = re.findall('pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			if title=='&lsaquo;': title = 'سابقة'
			if title=='&rsaquo;': title = 'لاحقة'
			link = unescapeHTML(link)
			addMenuItem('dir',menu_name+'صفحة '+title,link,241)
	return

def SEARCH(search):
	# https://akwam.net/search?q=%D8%A8%D8%AD%D8%AB
	if '::' in search: search = search.split('::')[0]
	if search=='': search = KEYBOARD()
	if search == '': return
	new_search = search.replace(' ','%20')
	url = website0a + '/search?q='+new_search
	#xbmcgui.Dialog().ok(url,'SEARCH_AKOAM')
	results = TITLES(url)
	return

def EPISODES(url):
	#xbmcgui.Dialog().ok(url,'EPISODES_AKWAM')
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','AKWAM-EPISODES-1st')
	if '-episodes' not in html:
		img = xbmc.getInfoLabel('ListItem.Icon')
		addMenuItem('link',menu_name+'رابط التشغيل',url,243,img)
	else:
		html_blocks = re.findall('-episodes">(.*?)col-lg-8',html,re.DOTALL)
		block = html_blocks[0]
		episodes = re.findall('href="(http.*?)".*?>(.*?)<.*?src="(.*?)"',block,re.DOTALL)
		for link,title,img in episodes:
			if 'الحلقات' in title or 'مواسم اخرى' in title: continue
			if '/series/' in link: addMenuItem('dir',menu_name+title,link,242,img)
			else: addMenuItem('link',menu_name+title,link,243,img)
	return

def PLAY(url):
	#xbmcgui.Dialog().ok(url,'PLAY')
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	#with open('S:\\emad.html', 'w') as f: f.write(html)
	html = openURL_cached(LONG_CACHE,url,'',headers,'','AKWAM-PLAY-1st')
	ratingLIST = re.findall('class="badge.*?>.*?(\w*).*?<',html,re.DOTALL)
	if RATING_CHECK(script_name,url,ratingLIST): return
	buttons = re.findall('li><a href="#(.*?)".*?>(.*?)<',html,re.DOTALL)
	#buttons = (['',''],['',''])
	linkLIST,titleLIST,blocks,qualities = [],[],[],[]
	if buttons:
		filename = '.mp4'
		for button,quality in buttons:
			#xbmcgui.Dialog().ok(quality,button)
			html_blocks = re.findall('tab-content" id="'+button+'".*?</div>.</div>',html,re.DOTALL)
			block = html_blocks[0]
			blocks.append(block)
			qualities.append(quality)
	else:
		html_blocks = re.findall('class="qualities(.*?)<h3.*?>(.*?)<',html,re.DOTALL)
		block,filename = html_blocks[0]
		notvideosLIST = ['zip','rar','txt','pdf','htm','tar','iso','html']
		file_extension = filename.rsplit('.',1)[1].strip(' ')
		if file_extension in notvideosLIST:
			xbmcgui.Dialog().ok('الملف ليس فيديو ولا صوت','')
			return
		blocks.append(block)
		qualities.append('')
	#xbmcgui.Dialog().ok(str(qualities),'')
	for i in range(len(blocks)):
		links = re.findall('href="(.*?)".*?icon-(.*?)"',blocks[i],re.DOTALL)
		#xbmcgui.Dialog().ok(str(links),'')
		for link,icon in links:
			if 'torrent' in icon: continue
			elif 'download' in icon: type = 'تحميل'
			elif 'play' in icon: type = 'مشاهدة'
			else: type = 'غير معروف'
			title = qualities[i]+' ملف '+type
			titleLIST.append(title)
			linkLIST.append(link)
	#selection = xbmcgui.Dialog().select('',titleLIST)
	#selection = xbmcgui.Dialog().select('',linkLIST)
	if len(titleLIST)==1: selection = 0
	else: selection = xbmcgui.Dialog().select('',titleLIST)
	if selection==-1: return
	link = linkLIST[selection]
	title = titleLIST[selection]
	if 'akwam' in link: url2 = link
	else:
		html2 = openURL_cached(LONG_CACHE,link,'',headers,'','AKWAM-PLAY-2nd')
		#xbmcgui.Dialog().ok(link,html2)
		url2 = re.findall('class="content.*?href="(.*?)"',html2,re.DOTALL)
		url2 = unquote(url2[0])
	url3 = ''
	if 'تحميل' in title:
		html3 = openURL_cached(SHORT_CACHE,url2,'',headers,'','AKWAM-PLAY-3rd')
		url3 = re.findall('btn-loader.*?href="(.*?)"',html3,re.DOTALL)
		url3 = unquote(url3[0])
	if 'مشاهدة' in title:
		html4 = openURL_cached(SHORT_CACHE,url2,'',headers,'','AKWAM-PLAY-4th')
		#xbmcgui.Dialog().ok(url2,html4)
		links = re.findall('<source.*?src="(.*?)".*?size="(.*?)"',html4,re.DOTALL)
		#xbmcgui.Dialog().ok(url2,str(links))
		for link,size in links:
			if size in title:
				url3 = link
				break
		if url3=='':
			linkLIST,titleLIST = [],[]
			for link,size in links:
				titleLIST.append(size)
				linkLIST.append(link)
			if len(titleLIST)==1: selection = 0
			else: selection = xbmcgui.Dialog().select('',titleLIST)
			if selection==-1: return
			url3 = linkLIST[selection]
	if url3=='': xbmcgui.Dialog().ok('','لا يوجد ملف تشغيل لهذا الفيديو')
	else: PLAY_VIDEO(url3,script_name,'yes')
	return

def FILTERS_MENU(url,filter):
	#xbmcgui.Dialog().ok(filter,url)
	menu_list = ['section','rating','category','year']
	if '?' in url: url = url.split('?')[0]
	type,filter = filter.split('::',1)
	if filter=='': filter_options,filter_values = '',''
	else: filter_options,filter_values = filter.split('::')
	if type=='CATEGORIES':
		if menu_list[0]+'=' not in filter_options: category = menu_list[0]
		for i in range(len(menu_list[0:-1])):
			if menu_list[i]+'=' in filter_options: category = menu_list[i+1]
		new_options = filter_options+'&'+category+'=0'
		new_values = filter_values+'&'+category+'=0'
		new_filter = new_options.strip('&')+'::'+new_values.strip('&')
		clean_filter = RECONSTRUCT_FILTER(filter_values,'all')
		url2 = url+'?'+clean_filter
	elif type=='FILTERS':
		filter_show = RECONSTRUCT_FILTER(filter_options,'modified_values')
		filter_show = unquote(filter_show)
		if filter_values!='': filter_values = RECONSTRUCT_FILTER(filter_values,'all')
		if filter_values=='': url2 = url
		else: url2 = url+'?'+filter_values
		addMenuItem('dir',menu_name+'أظهار قائمة الفيديو التي تم اختيارها',url2,241,'','1')
		addMenuItem('dir',menu_name+' [[   '+filter_show+'   ]]',url2,241,'','1')
		addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	html = openURL_cached(LONG_CACHE,url,'',headers,'','AKWAM-FILTERS_MENU-1st')
	html_blocks = re.findall('<form id(.*?)</form>',html,re.DOTALL)
	block = html_blocks[0]
	select_blocks = re.findall('<select.*?name="(.*?)".*?">(.*?)<(.*?)</select>',block,re.DOTALL)
	#xbmcgui.Dialog().ok('',str(select_blocks))
	dict = {}
	ignoreLIST = ['عروض مصارعة','الكل']
	for category2,name,block in select_blocks:
		#name = name.replace('--','')
		items = re.findall('<option(.*?)>(.*?)<',block,re.DOTALL)
		if '=' not in url2: url2 = url
		if type=='CATEGORIES':
			if category!=category2: continue
			elif len(items)<=1:
				if category2==menu_list[-1]: TITLES(url2)
				else: FILTERS_MENU(url2,'CATEGORIES::'+new_filter)
				return
			else:
				if category2==menu_list[-1]: addMenuItem('dir',menu_name+'الجميع',url2,241,'','1')
				else: addMenuItem('dir',menu_name+'الجميع',url2,245,'','',new_filter)
		elif type=='FILTERS':
			new_options = filter_options+'&'+category2+'=0'
			new_values = filter_values+'&'+category2+'=0'
			new_filter = new_options+'::'+new_values
			addMenuItem('dir',menu_name+'الجميع : '+name,url2,244,'','',new_filter)
		dict[category2] = {}
		for value,option in items:
			if option in ignoreLIST: continue
			if 'value' not in value: value = option
			else: value = re.findall('"(.*?)"',value,re.DOTALL)[0]
			dict[category2][value] = option
			new_options = filter_options+'&'+category2+'='+option
			new_values = filter_values+'&'+category2+'='+value
			new_filter2 = new_options+'::'+new_values
			title = option+' : '#+dict[category2]['0']
			title = option+' : '+name
			if type=='FILTERS': addMenuItem('dir',menu_name+title,url,244,'','',new_filter2)
			elif type=='CATEGORIES' and menu_list[-2]+'=' in filter_options:
				clean_filter = RECONSTRUCT_FILTER(new_values,'all')
				url3 = url+'?'+clean_filter
				addMenuItem('dir',menu_name+title,url3,241,'','1')
			else: addMenuItem('dir',menu_name+title,url,245,'','',new_filter2)
	return

def RECONSTRUCT_FILTER(filters,mode):
	#xbmcgui.Dialog().ok(filters,'RECONSTRUCT_FILTER 11')
	# mode=='modified_values'		only non empty values
	# mode=='modified_filters'		only non empty filters
	# mode=='all'					all filters (includes empty filter)
	#filters = filters.replace('=&','=0&')
	filters = filters.strip('&')
	filtersDICT = {}
	if '=' in filters:
		items = filters.split('&')
		for item in items:
			var,value = item.split('=')
			filtersDICT[var] = value
	new_filters = ''
	url_filter_list = ['section','category','rating','year','language','formats','quality']
	for key in url_filter_list:
		if key in filtersDICT.keys(): value = filtersDICT[key]
		else: value = '0'
		#if '%' not in value: value = quote(value)
		if mode=='modified_values' and value!='0': new_filters = new_filters+' + '+value
		elif mode=='modified_filters' and value!='0': new_filters = new_filters+'&'+key+'='+value
		elif mode=='all': new_filters = new_filters+'&'+key+'='+value
	new_filters = new_filters.strip(' + ')
	new_filters = new_filters.strip('&')
	#new_filters = new_filters.replace('=0','=')
	#xbmcgui.Dialog().ok(filters,'RECONSTRUCT_FILTER 22')
	return new_filters



