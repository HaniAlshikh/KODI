# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='SHAHID4U'
headers = { 'User-Agent' : '' }
menu_name='_SHA_'
website0a = WEBSITES[script_name][0]
ignoreLIST = ['مسلسلات انمي','الرئيسية','عروض مصارعة','الكل','افلام']

def MAIN(mode,url,text):
	LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==110: results = MENU(url)
	elif mode==111: results = TITLES(url)
	elif mode==112: results = PLAY(url)
	elif mode==113: results = EPISODES(url)
	elif mode==114: results = FILTERS_MENU(url,'FILTERS::'+text)
	elif mode==115: results = FILTERS_MENU(url,'CATEGORIES::'+text)
	elif mode==119: results = SEARCH(text)
	else: results = False
	return results

def MENU(website=''):
	if website=='': 
		addMenuItem('dir',menu_name+'بحث في الموقع','',119)
		addMenuItem('dir',menu_name+'فلتر محدد',website0a,115)
		addMenuItem('dir',menu_name+'فلتر كامل',website0a,114)
		addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
		#addMenuItem('dir',menu_name+'فلتر','',114,website0a)
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','SHAHID4U-MENU-1st')
	html_blocks = re.findall('categories-tabs(.*?)advanced-search',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('data-get="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
	for link,title in items:
		url = website0a+'/getposts?type=one&data='+link
		addMenuItem('dir',website+'::'+menu_name+title,url,111)
	if website=='': addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	html_blocks = re.findall('navigation-menu(.*?)</div>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	#keepLIST = ['مسلسلات ','افلام ','برامج','عروض','كليبات','اغانى']
	for link,title in items:
		if 'javascript' in link: continue
		if 'http' not in link: link = website0a+link
		"""
		if '%' in link:
			link = unquote(link)
			link = link.replace('ه','ة')
			link = link.replace('ى','ي')
		"""
		title = title.strip(' ')
		#if not any(value in title for value in ignoreLIST):
		#	if any(value in title for value in keepLIST):
		if title not in ignoreLIST:
			addMenuItem('dir',website+'::'+menu_name+title,link,111)
	return

def TITLES(url):
	#xbmcgui.Dialog().ok(url,url)
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','SHAHID4U-TITLES-1st')
	if 'getposts' in url: block = html
	else:
		html_blocks = re.findall('page-content(.*?)tags-cloud',html,re.DOTALL)
		block = html_blocks[0]
	items = re.findall('class="box.*?src="(.*?)".*?href="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
	allTitles = []
	itemLIST = ['مشاهدة','فيلم','اغنية','كليب','اعلان','هداف','مباراة','عرض','مهرجان','البوم']
	for img,link,title in items:
		if '/series/' in link: continue
		link = unquote(link).strip('/')
		title = unescapeHTML(title)
		title = title.strip(' ')
		if '/film/' in link or any(value in title for value in itemLIST):
			addMenuItem('link',menu_name+title,link,112,img)
		elif '/episode/' in link and 'الحلقة' in title:
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode:
				title = '_MOD_' + episode[0]
				if title not in allTitles:
					addMenuItem('dir',menu_name+title,link,113,img)
					allTitles.append(title)
		else: addMenuItem('dir',menu_name+title,link,113,img)
	html_blocks = re.findall('class="pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<a href=["\'](http.*?)["\'].*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			link = unescapeHTML(link)
			title = unescapeHTML(title)
			title = title.replace('الصفحة ','')
			if title!='': addMenuItem('dir',menu_name+'صفحة '+title,link,111)
	return

def EPISODES(url):
	episodesCount,items,itemsNEW = -1,[],[]
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','SHAHID4U-EPISODES-1st')
	html_blocks = re.findall('ti-list-numbered(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		itemsNEW = []
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
			if '/season/' in link: addMenuItem('dir',menu_name+title,link,113)
	else:
		for link,title,sequence in items:
			if '/season/' not in link: addMenuItem('link',menu_name+title,link,112)
	return

def PLAY(url):
	#LOG_THIS('NOTICE','EMAD 111')
	linkLIST = []
	parts = url.split('/')
	#xbmcgui.Dialog().ok(url,'PLAY-1st')
	#url = unquote(quote(url))
	html = openURL_cached(LONG_CACHE,url,'',headers,'','ARABLIONZ-PLAY-1st')
	id = re.findall('postId:"(.*?)"',html,re.DOTALL)
	if not id: id = re.findall('post_id=(.*?)"',html,re.DOTALL)
	id = id[0]
	if '/post/' in url and 'seed' in url: url = website0a+'/watch/'+id
	if True or '/watch/' in html:
		url2 = url.replace(parts[3],'watch')
		html2 = openURL_cached(LONG_CACHE,url2,'',headers,'','ARABLIONZ-PLAY-2nd')
		items1 = re.findall('data-embedd="(.*?)".*?alt="(.*?)"',html2,re.DOTALL)
		items2 = re.findall('data-embedd=".*?(http.*?)("|&quot;)',html2,re.DOTALL)
		items3 = re.findall('src=&quot;(.*?)&quot;.*?>(.*?)<',html2,re.DOTALL|re.IGNORECASE)
		items4 = re.findall('data-embedd="(.*?)">\n*.*?server_image">\n(.*?)\n',html2)
		items5 = re.findall('src=&quot;(.*?)&quot;.*?alt="(.*?)"',html2,re.DOTALL|re.IGNORECASE)
		items = items1+items2+items3+items4+items5
		for server,title in items:
			if '.png' in server: continue
			if '.jpg' in server: continue
			if '&quot;' in server: continue
			if server.isdigit():
				link = website0a+'/?postid='+id+'&serverid='+server+'?name='+title+'__watch'
			else:
				if 'http' not in server: server = 'http:'+server
				resolution = re.findall('\d\d\d+',title,re.DOTALL)
				if resolution: resolution = '__'+resolution[0]
				else: resolution = ''
				link = server+'?name=__watch'+resolution
			linkLIST.append(link)
	#selection = xbmcgui.Dialog().select('أختر البحث المناسب', linkLIST)
	#xbmcgui.Dialog().ok('watch 1',	str(len(items)))
	if True or '/download/' in html:
		headers2 = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
		url2 = website0a + '/ajaxCenter?_action=getdownloadlinks&postId='+id
		response = openURL_requests_cached(LONG_CACHE,'GET',url2,'',headers2,True,'','SHAHID4U-PLAY-3rd')
		html2 = response.text.encode('utf8')
		if 'download-btns' or 'DownloadTabel' in html2:
			items3 = re.findall('href="(.*?)"',html2,re.DOTALL)
			for url3 in items3:
				if '/page/' not in url3 and 'http' in url3:
					url3 = url3+'?name=__download'
					linkLIST.append(url3)
				elif '/page/' in url3:
					resolution4 = ''
					response = openURL_requests_cached(LONG_CACHE,'GET',url3,'',headers,True,'','SHAHID4U-PLAY-4th')
					html4 = response.text.encode('utf8')
					blocks = re.findall('(<strong>.*?)-----',html4,re.DOTALL)
					for block4 in blocks:
						server4 = ''
						items4 = re.findall('<strong>(.*?)</strong>',block4,re.DOTALL)
						for item4 in items4:
							item = re.findall('\d\d\d+',item4,re.DOTALL)
							if item:
								resolution4 = '____'+item[0]
								break
						for item4 in reversed(items4):
							item = re.findall('\w\w+',item4,re.DOTALL)
							if item:
								server4 = item[0]
								break
						items5 = re.findall('href="(.*?)"',block4,re.DOTALL)
						for link5 in items5:
							link5 = link5+'?name='+server4+'__download'+resolution4
							linkLIST.append(link5)
			#xbmcgui.Dialog().ok('download 1',	str(len(linkLIST))	)
		elif 'slow-motion' in html2:
			html3 = html2.replace('<h6 ','==END== ==START==')+'==END=='
			all_blocks = re.findall('==START==(.*?)==END==',html3,re.DOTALL)
			for block4 in all_blocks:
				resolution4 = ''
				items4 = re.findall('slow-motion">(.*?)<',block4,re.DOTALL)
				for item4 in items4:
					item = re.findall('\d\d\d+',item4,re.DOTALL)
					if item:
						resolution4 = '____'+item[0]
						break
				items4 = re.findall('<td>(.*?)</td>.*?href="(.*?)"',block4,re.DOTALL)
				for server4,link4 in items4:
					link4 = link4+'?name='+server4+'__download'+resolution4
					linkLIST.append(link4)
				items4 = re.findall('href="(.*?)".*?name">(.*?)<',block4,re.DOTALL)
				for link4,server4 in items4:
					link4 = link4+'?name='+server4+'__download'+resolution4
					linkLIST.append(link4)
	#LOG_THIS('NOTICE','EMAD 222')
	#xbmcgui.Dialog().ok('both: watch & download',	str(len(linkLIST))	)
	#selection = xbmcgui.Dialog().select('أختر البحث المناسب', linkLIST)
	if len(linkLIST)==0: xbmcgui.Dialog().ok('','الرابط ليس فيه فيديو')
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
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','SHAHID4U-SEARCH-1st')
	html_blocks = re.findall('chevron-select(.*?)</div>',html,re.DOTALL)
	if category and html_blocks:
		block = html_blocks[0]
		items = re.findall('value="(.*?)".*?>(.*?)<',block,re.DOTALL)
		categoryLIST,filterLIST = [],[]
		for category,title in items:
			if title in ['عروض مصارعة']: continue
			categoryLIST.append(category)
			filterLIST.append(title)
		selection = xbmcgui.Dialog().select('اختر الفلتر المناسب:', filterLIST)
		if selection == -1 : return
		category = categoryLIST[selection]
	else: category = ''
	url = website0a + '/search?s='+search+'&category='+category
	TITLES(url)
	return

def FILTERS_MENU(url,filter):
	#xbmcgui.Dialog().ok(filter,url)
	menu_list = ['category','genre','release-year']
	if '?' in url: url = url.split('/getposts?')[0]
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
		clean_filter = RECONSTRUCT_FILTER(filter_values,'modified_filters')
		url2 = url+'/getposts?'+clean_filter
	elif type=='FILTERS':
		filter_show = RECONSTRUCT_FILTER(filter_options,'modified_values')
		filter_show = unquote(filter_show)
		if filter_values!='': filter_values = RECONSTRUCT_FILTER(filter_values,'modified_filters')
		if filter_values=='': url2 = url
		else: url2 = url+'/getposts?'+filter_values
		addMenuItem('dir',menu_name+'أظهار قائمة الفيديو التي تم اختيارها ',url2,111)
		addMenuItem('dir',menu_name+' [[   '+filter_show+'   ]]',url2,111)
		addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	html = openURL_cached(LONG_CACHE,url,'',headers,'','SHAHID4U-FILTERS_MENU-1st')
	html_blocks = re.findall('<form class(.*?)</form>',html,re.DOTALL)
	block = html_blocks[0]
	select_blocks = re.findall('select.*?<a.*?>(.*?)</a>.*?data-tax="(.*?)"(.*?)</ul>',block,re.DOTALL)
	#xbmcgui.Dialog().ok('',str(select_blocks))
	dict = {}
	for name,category2,block in select_blocks:
		name = name.replace('--','')
		items = re.findall('data-cat="(.*?)".*?checkmark-bold">(.*?)<',block,re.DOTALL)
		if '=' not in url2: url2 = url
		if type=='CATEGORIES':
			if category!=category2: continue
			elif len(items)<=1:
				if category2==menu_list[-1]: TITLES(url2)
				else: FILTERS_MENU(url2,'CATEGORIES::'+new_filter)
				return
			else:
				if category2==menu_list[-1]: addMenuItem('dir',menu_name+'الجميع ',url2,111)
				else: addMenuItem('dir',menu_name+'الجميع ',url2,115,'','',new_filter)
		elif type=='FILTERS':
			new_options = filter_options+'&'+category2+'=0'
			new_values = filter_values+'&'+category2+'=0'
			new_filter = new_options+'::'+new_values
			addMenuItem('dir',menu_name+'الجميع :'+name,url2,114,'','',new_filter)
		dict[category2] = {}
		for value,option in items:
			if option in ignoreLIST: continue
			#if 'value' not in value: value = option
			#else: value = re.findall('"(.*?)"',value,re.DOTALL)[0]
			dict[category2][value] = option
			new_options = filter_options+'&'+category2+'='+option
			new_values = filter_values+'&'+category2+'='+value
			new_filter2 = new_options+'::'+new_values
			title = option+' :'#+dict[category2]['0']
			title = option+' :'+name
			if type=='FILTERS': addMenuItem('dir',menu_name+title,url,114,'','',new_filter2)
			elif type=='CATEGORIES' and menu_list[-2]+'=' in filter_options:
				clean_filter = RECONSTRUCT_FILTER(new_values,'modified_filters')
				url3 = url+'/getposts?'+clean_filter
				addMenuItem('dir',menu_name+title,url3,111)
			else: addMenuItem('dir',menu_name+title,url,115,'','',new_filter2)
	return

def RECONSTRUCT_FILTER(filters,mode):
	#xbmcgui.Dialog().ok(filters,'RECONSTRUCT_FILTER 11')
	# mode=='modified_values'		only non empty values
	# mode=='modified_filters'		only non empty filters
	# mode=='all'					all filters (includes empty filter)
	filters = filters.replace('=&','=0&')
	filters = filters.strip('&')
	filtersDICT = {}
	if '=' in filters:
		items = filters.split('&')
		for item in items:
			var,value = item.split('=')
			filtersDICT[var] = value
	new_filters = ''
	url_filter_list = ['quality','release-year','genre','category']
	for key in url_filter_list:
		if key in filtersDICT.keys(): value = filtersDICT[key]
		else: value = '0'
		if '%' not in value: value = quote(value)
		if mode=='modified_values' and value!='0': new_filters = new_filters+' + '+value
		elif mode=='modified_filters' and value!='0': new_filters = new_filters+'&'+key+'='+value
		elif mode=='all': new_filters = new_filters+'&'+key+'='+value
	new_filters = new_filters.strip(' + ')
	new_filters = new_filters.strip('&')
	new_filters = new_filters.replace('=0','=')
	#xbmcgui.Dialog().ok(filters,'RECONSTRUCT_FILTER 22')
	return new_filters