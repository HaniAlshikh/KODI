# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='ARABSEED'
headers = { 'User-Agent' : '' }
menu_name='_ARS_'
website0a = WEBSITES[script_name][0]
ignoreLIST = ['الرئيسية','مصارعه']

def MAIN(mode,url,text):
	LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if mode==250: MENU()
	elif mode==251: TITLES(url)
	elif mode==252: PLAY(url)
	elif mode==253: EPISODES(url)
	elif mode==254: FILTERS_MENU(url,'FILTERS::'+text)
	elif mode==255: FILTERS_MENU(url,'CATEGORIES::'+text)
	elif mode==259: SEARCH(text)
	return

def MENU():
	addDir(menu_name+'بحث في الموقع','',259)
	addDir(menu_name+'فلتر محدد',website0a,255)
	addDir(menu_name+'فلتر كامل',website0a,254)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	#addDir(menu_name+'فلتر','',254,website0a)
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','ARABSEED-MENU-1st')
	html_blocks = re.findall('navigation-menu(.*?)</header>',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	"""
	for link,title in items:
		url = website0a+'/getposts?type=one&data='+link
		addDir(menu_name+title,url,251)
	addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	html_blocks = re.findall('navigation-menu(.*?)div',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(\/.*?)">(.*?)<',block,re.DOTALL)
	"""
	#keepLIST = ['مسلسلات ','افلام ','برامج','عروض','كليبات','اغانى']
	for link,title in items:
		if 'javascript' in link: continue
		#title = title.strip(' ')
		if not any(value in title for value in ignoreLIST):
		#	if any(value in title for value in keepLIST):
			url = website0a+link
			addDir(menu_name+title,link,251)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def TITLES(url):
	#xbmcgui.Dialog().ok(url,url)
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','ARABSEED-TITLES-1st')
	html_blocks = re.findall('class="row(.*?)class="pagination',html+'class="pagination',re.DOTALL)
	block = html_blocks[0]
	items = re.findall('data-src="(.*?)".*?href="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
	allTitles = []
	itemLIST = ['مشاهدة','فيلم','اغنية','كليب','اعلان','هداف','مباراة','عرض','مهرجان','البوم']
	for img,link,title in items:
		#if '/series/' in link: continue
		#link = unquote(link).strip('/')
		#title = title.strip(' ')
		#if '/film/' in link or any(value in title for value in itemLIST):
		#	addLink(menu_name+title,link,252,img)
		#elif '/episode/' in link and 'الحلقة' in title:
		title = unescapeHTML(title)
		if any(value in title for value in itemLIST):
			addLink(menu_name+title,link,252,img)
		else:
			mod = ''
			episode = re.findall('(.*?) الحلقة \d+',title,re.DOTALL)
			if episode:
				title = episode[0]
				mod = '_MOD_'
			if title not in allTitles:
				allTitles.append(title)
				title = mod+title
				addDir(menu_name+title,link,253,img)
	html_blocks = re.findall('class="pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(http.*?)">(.*?)<',block,re.DOTALL)
		for link,title in items:
			#link = unescapeHTML(link)
			#title = unescapeHTML(title)
			#title = title.replace('الصفحة ','')
			if title!='': addDir(menu_name+'صفحة '+title,link,251)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def EPISODES(url):
	episodesCount,items,itemsNEW = -1,[],[]
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','ARABSEED-EPISODES-1st')
	items = re.findall('<td style="display.*?<td>(.*?)<.*?href="(.*?)"',html,re.DOTALL)
	name = xbmc.getInfoLabel('ListItem.Label')
	for episode,link in items:
		title = 'الحلقة '+episode
		addLink(menu_name+title,link,252)
	xbmcplugin.endOfDirectory(addon_handle)
	return
	"""
	items.append(url)
	items = set(items)
	name = xbmc.getInfoLabel('ListItem.Label')
	for link in items:
		#link = link.strip('/')
		#title = '_MOD_' + link.split('/')[-1].replace('-',' ')
		sequence = re.findall('الحلقة-(\d+)',link.split('/')[-1],re.DOTALL)
		if sequence: sequence = sequence[0]
		else: sequence = '0'
		itemsNEW.append([link,title,sequence])
	items = sorted(itemsNEW, reverse=False, key=lambda key: int(key[2]))
	seasonsCount = str(items).count('/season/')
	episodesCount = str(items).count('/episode/')
	if seasonsCount>1 and episodesCount>0 and '/season/' not in url:
		for link,title,sequence in items:
			if '/season/' in link: addDir(menu_name+title,link,253)
	else:
		for link,title,sequence in items:
			if '/season/' not in link: addLink(menu_name+title,link,252)
	"""

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
		items4 = re.findall('data-embedd="(.*?)">\n.*?server_image">\n(.*?)\n',html2,re.DOTALL)
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
		html2 = openURL_cached(LONG_CACHE,url2,'',headers2,'','ARABLIONZ-PLAY-3rd')
		if 'download-btns' in html2:
			items3 = re.findall('href="(.*?)"',html2,re.DOTALL)
			for url3 in items3:
				if '/page/' not in url3 and 'http' in url3:
					url3 = url3+'?name=__download'
					linkLIST.append(url3)
				elif '/page/' in url3:
					resolution4 = ''
					html4 = openURL_cached(LONG_CACHE,url3,'',headers,'','ARABLIONZ-PLAY-4th')
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
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.replace(' ','+')
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','ARABSEED-SEARCH-1st')
	html_blocks = re.findall('name="category(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('value="(.*?)".*?>(.*?)<',block,re.DOTALL)
		categoryLIST,filterLIST = [''],['الكل']
		for category,title in items:
			if title in ['مصارعه']: continue
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
		addDir(menu_name+'أظهار قائمة الفيديو التي تم اختيارها ',url2,251)
		addDir(menu_name+' [[   '+filter_show+'   ]]',url2,251)
		addLink('[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	html = openURL_cached(LONG_CACHE,url,'',headers,'','ARABSEED-FILTERS_MENU-1st')
	html_blocks = re.findall('class="Filters(.*?)hideTilteHome',html,re.DOTALL)
	#xbmcgui.Dialog().ok('',str(html_blocks))
	block = html_blocks[0]
	select_blocks = re.findall('class="ti-arrow-down.*?span>(.*?)</span>.*?data-tax="(.*?)"(.*?)</ul>',block,re.DOTALL)
	#xbmcgui.Dialog().ok('',str(select_blocks))
	dict = {}
	for name,category2,block in select_blocks:
		name = name.replace('--','')
		items = re.findall('data-cat="(.*?)".*?</div>(.*?)\n',block,re.DOTALL)
		if '=' not in url2: url2 = url
		if type=='CATEGORIES':
			if category!=category2: continue
			elif len(items)<=1:
				if category2==menu_list[-1]: TITLES(url2)
				else: FILTERS_MENU(url2,'CATEGORIES::'+new_filter)
				return
			else:
				if category2==menu_list[-1]: addDir(menu_name+'الجميع ',url2,251)
				else: addDir(menu_name+'الجميع ',url2,255,'','',new_filter)
		elif type=='FILTERS':
			new_options = filter_options+'&'+category2+'=0'
			new_values = filter_values+'&'+category2+'=0'
			new_filter = new_options+'::'+new_values
			addDir(menu_name+'الجميع :'+name,url2,254,'','',new_filter)
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
			if type=='FILTERS': addDir(menu_name+title,url,254,'','',new_filter2)
			elif type=='CATEGORIES' and menu_list[-2]+'=' in filter_options:
				clean_filter = RECONSTRUCT_FILTER(new_values,'modified_filters')
				url3 = url+'/getposts?'+clean_filter
				addDir(menu_name+title,url3,251)
			else: addDir(menu_name+title,url,255,'','',new_filter2)
	xbmcplugin.endOfDirectory(addon_handle)
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
	url_filter_list = ['category','genre','release-year']
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

