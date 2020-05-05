# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='MOVIZLAND'
headers = { 'User-Agent' : '' }
menu_name='_MVZ_'
website0a = WEBSITES[script_name][0]
website0b = WEBSITES[script_name][1]

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==180: results = MENU(url)
	elif mode==181: results = TITLES(url,text)
	elif mode==182: results = PLAY(url)
	elif mode==183: results = EPISODES(url)
	elif mode==188: results = TERMINATED_CHANGED()
	elif mode==189: results = SEARCH(text)
	else: results = False
	return results

def TERMINATED_CHANGED():
	message = 'هذا الموقع تغير بالكامل ... وبحاجة الى اعادة برمجة من الصفر ... والمبرمج حاليا مشغول ويعاني من وعكة صحية ... ولهذا سوف يبقى الموقع مغلق الى ما شاء الله'
	xbmcgui.Dialog().ok('الموقع تغير بالكامل',message)
	return

def MENU(website=''):
	if website=='': addMenuItem('dir',menu_name+'بحث في الموقع','',189)
	addMenuItem('dir',website+'::'+menu_name+'بوكس اوفيس موفيز لاند',website0a,181,'','','box-office')
	addMenuItem('dir',website+'::'+menu_name+'أحدث الافلام',website0a,181,'','','latest-movies')
	addMenuItem('dir',website+'::'+menu_name+'تليفزيون موفيز لاند',website0a,181,'','','tv')
	addMenuItem('dir',website+'::'+menu_name+'الاكثر مشاهدة',website0a,181,'','','top-views')
	addMenuItem('dir',website+'::'+menu_name+'أقوى الافلام الحالية',website0a,181,'','','top-movies')
	html = openURL_cached(LONG_CACHE,website0a,'',headers,'','MOVIZLAND-MENU-1st')
	items = re.findall('<h2><a href="(.*?)".*?">(.*?)<',html,re.DOTALL)
	for link,title in items:
		addMenuItem('dir',website+'::'+menu_name+title,link,181)
	#xbmcgui.Dialog().ok(html,html)
	return

def TITLES(url,type=''):
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','MOVIZLAND-ITEMS-1st')
	#xbmc.log(html, level=xbmc.LOGNOTICE)
	if type=='latest-movies': block = re.findall('class="titleSection">أحدث الأفلام</h1>(.*?)<h1',html,re.DOTALL)[0]
	elif type=='box-office': block = re.findall('class="titleSection">بوكس اوفيس موفيز لاند</h1>(.*?)<h1',html,re.DOTALL)[0]
	elif type=='top-movies': block = re.findall('btn-2-overlay(.*?)<style>',html,re.DOTALL)[0]
	elif type=='top-views': block = re.findall('btn-1 btn-absoly(.*?)btn-2 btn-absoly',html,re.DOTALL)[0]
	elif type=='tv': block = re.findall('class="titleSection">تليفزيون موفيز لاند</h1>(.*?)class="paging"',html,re.DOTALL)[0]
	else: block = html
	if type in ['top-views','top-movies']:
		items = re.findall('style="background-image:url\(\'(.*?)\'.*?href="(.*?)".*?href="(.*?)".*?bottom-title.*?>(.*?)<',block,re.DOTALL)
	else: items = re.findall('height="3[0-9]+" src="(.*?)".*?bottom-title.*?href=.*?>(.*?)<.*?href="(.*?)".*?href="(.*?)"',block,re.DOTALL)
	allTitles = []
	itemLIST = ['فيلم','الحلقة','الحلقه','عرض','Raw','SmackDown','اعلان','اجزاء']
	for img,var1,var2,var3 in items:
		if type in ['top-views','top-movies']:
			img,link,link2,title = img,var1,var2,var3
		else: img,title,link,link2 = img,var1,var2,var3
		link = unquote(link)
		link = link.replace('?view=true','')
		#xbmcgui.Dialog().ok(link,link2)
		title = unescapeHTML(title)
		#title2 = re.findall('(.*?)(بجودة|بجوده)',title,re.DOTALL)
		#if title2: title = title2[0][0]
		if 'بجودة ' in title or 'بجوده ' in title:
			title = '_MOD_' + title.replace('بجودة ','').replace('بجوده ','')
		title = title.strip(' ')
		if 'الحلقة' in title or 'الحلقه' in title:
			episode = re.findall('(.*?) (الحلقة|الحلقه) \d+',title,re.DOTALL)
			if episode:
				title = '_MOD_' + episode[0][0]
				if title not in allTitles:
					addMenuItem('dir',menu_name+title,link,183,img)
					allTitles.append(title)
		elif any(value in title for value in itemLIST):
			link = link + '?servers=' + link2
			addMenuItem('link',menu_name+title,link,182,img)
		else:
			link = link + '?servers=' + link2
			addMenuItem('dir',menu_name+title,link,183,img)
	if type=='':
		items = re.findall('\n<li><a href="(.*?)".*?>(.*?)<',html,re.DOTALL)
		for link,title in items:
			title = unescapeHTML(title)
			title = title.replace('الصفحة ','')
			if title!='':
				addMenuItem('dir',menu_name+'صفحة '+title,link,181)
	return

def EPISODES(url):
	url2 = url.split('?servers=')[0]
	html = openURL_cached(REGULAR_CACHE,url2,'',headers,'','MOVIZLAND-EPISODES-1st')
	block = re.findall('<title>(.*?)</title>.*?height="([0-9]+)" src="(.*?)"',html,re.DOTALL)
	title,dummy,img = block[0]
	name = re.findall('(.*?) (الحلقة|الحلقه) [0-9]+',title,re.DOTALL)
	if name: name = '_MOD_' + name[0][0]
	else: name = title
	items = []
	html_blocks = re.findall('class="episodesNumbers"(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		#xbmcgui.Dialog().ok(url2,str(html_blocks))
		block = html_blocks[0]
		items = re.findall('href="(.*?)"',block,re.DOTALL)
		for link in items:
			link = unquote(link)
			title = re.findall('(الحلقة|الحلقه)-([0-9]+)',link.split('/')[-2],re.DOTALL)
			if not title: title = re.findall('()-([0-9]+)',link.split('/')[-2],re.DOTALL)
			if title: title = ' ' + title[0][1]
			else: title = ''
			title = name + ' - ' + 'الحلقة' + title
			title = unescapeHTML(title)
			addMenuItem('link',menu_name+title,link,182,img)
	if not items:
		title = unescapeHTML(title)
		if 'بجودة ' in title or 'بجوده ' in title:
			title = '_MOD_' + title.replace('بجودة ','').replace('بجوده ','')
		addMenuItem('link',menu_name+title,url,182,img)
	return

def PLAY(url):
	urls = url.split('?servers=')
	url2 = urls[0]
	del urls[0]
	html = openURL_cached(LONG_CACHE,url2,'',headers,'','MOVIZLAND-PLAY-1st')
	link = re.findall('font-size: 25px;" href="(.*?)"',html,re.DOTALL)[0]
	if link not in urls: urls.append(link)
	linkLIST = []
	# main_watch_link
	for link in urls:
		if '://moshahda.' in link:
			main_watch_link = link
			linkLIST.append(main_watch_link+'?name=Main')
	# all_vb_links
	for link in urls:
		if '://vb.movizland.' in link:
			html = openURL_cached(LONG_CACHE,link,'',headers,'','MOVIZLAND-PLAY-2nd')
			html = html.decode('windows-1256').encode('utf8')
			#xbmc.log(html, level=xbmc.LOGNOTICE)
			#</a></div><br /><div align="center">(\*\*\*\*\*\*\*\*|13721411411.png|)
			html = html.replace('src="http://up.movizland.com/uploads/13721411411.png"','src="/uploads/13721411411.png"  \n  src="/uploads/13721411411.png"')
			html = html.replace('src="http://up.movizland.online/uploads/13721411411.png"','src="/uploads/13721411411.png"  \n  src="/uploads/13721411411.png"')
			html = html.replace('</a></div><br /><div align="center">','src="/uploads/13721411411.png"')
			html = html.replace('class="tborder" align="center"','src="/uploads/13721411411.png"')
			html_blocks = re.findall('(src="/uploads/13721411411.png".*?href="http://moshahda\..*?/\w+.html".*?src="/uploads/13721411411.png")',html,re.DOTALL)
			if html_blocks:
				#xbmcgui.Dialog().ok(url,str(len(html_blocks)))
				titleLIST2,linkLIST2 = [],[]
				if len(html_blocks)==1:
					title = ''
					block = html
				else:
					for block in html_blocks:
						block2 = re.findall('src="/uploads/13721411411.png".*?http://up.movizland.(online|com)/uploads/.*?\*\*\*\*\*\*\*+(.*?src="/uploads/13721411411.png")',block,re.DOTALL)
						if block2: block = 'src="/uploads/13721411411.png"  \n  ' + block2[0][1]
						block2 = re.findall('src="/uploads/13721411411.png".*?<hr size="1" style="color:#333; background-color:#333" />(.*?href="http://moshahda\..*?/\w+.html".*?src="/uploads/13721411411.png")',block,re.DOTALL)
						if block2: block = 'src="/uploads/13721411411.png"  \n  ' + block2[0]
						block2 = re.findall('(src="/uploads/13721411411.png".*?href="http://moshahda\..*?/\w+.html".*?)<hr size="1" style="color:#333; background-color:#333" />.*?src="/uploads/13721411411.png"',block,re.DOTALL)
						if block2: block = block2[0] + '  \n  src="/uploads/13721411411.png"'
						title_blocks = re.findall('<(.*?)http://up.movizland.(online|com)/uploads/',block,re.DOTALL)
						title = re.findall('> *([^<>]+) *<',title_blocks[0][0],re.DOTALL)
						title = ' '.join(title)
						title = title.replace('\n','').strip(' ')
						title = title.replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ')
						titleLIST2.append(title)
					selection = xbmcgui.Dialog().select('أختر الفيديو المطلوب:', titleLIST2)
					if selection == -1 : return
					title = titleLIST2[selection]
					block = html_blocks[selection]
				link = re.findall('href="(http://moshahda\..*?/\w+.html)"',block,re.DOTALL)
				forum_watch_link = link[0]
				linkLIST.append(forum_watch_link+'?name=Forum')
				block = block.replace('ـ','')
				block = block.replace('src="http://up.movizland.online/uploads/1517412175296.png"','src="/uploads/13721411411.png"  \n  src="/uploads/13721411411.png"  \n  typetype="both"  \n  ')
				block = block.replace('src="http://up.movizland.com/uploads/1517412175296.png"','src="/uploads/13721411411.png"  \n  src="/uploads/13721411411.png"  \n  typetype="both"  \n  ')
				block = block.replace('سيرفرات التحميل','src="/uploads/13721411411.png"  \n  src="/uploads/13721411411.png"  \n  typetype="download"  \n  ')
				block = block.replace('روابط التحميل','src="/uploads/13721411411.png"  \n  src="/uploads/13721411411.png"  \n  typetype="download"  \n  ')
				block = block.replace('سيرفرات المشاهد','src="/uploads/13721411411.png"  \n  src="/uploads/13721411411.png"  \n  typetype="watch"  \n  ')
				block = block.replace('روابط المشاهد','src="/uploads/13721411411.png"  \n  src="/uploads/13721411411.png"  \n  typetype="watch"  \n  ')
				links_blocks = re.findall('(src="/uploads/13721411411.png".*?href="http://e5tsar.com/\d+".*?src="/uploads/13721411411.png")',block,re.DOTALL)
				for link_block in links_blocks:
					#xbmcgui.Dialog().ok('',str(link_block))
					type = re.findall(' typetype="(.*?)" ',link_block)
					if type:
						if type[0]!='both': type = '__'+type[0]
						else: type = ''
					items = re.findall('(?<!http://e5tsar.com/)(\w+[ \w]*</font>.*?|\w+[ \w]*<br />.*?)href="(http://e5tsar.com/.*?)"',link_block,re.DOTALL)
					for title_block,link in items:
						title = re.findall('(\w+[ \w]*)<',title_block)
						title = title[-1]
						link = link + '?name=' + title + type
						linkLIST.append(link)
	# mobile_watch_link
	url3 = url2.replace(website0a,website0b)
	html = openURL_cached(LONG_CACHE,url3,'',headers,'','MOVIZLAND-PLAY-3rd')
	items = re.findall('" href="(.*?)"',html,re.DOTALL)
	#id2 = re.findall('" href="(http://moshahda\..*?/embedM-(\w+)-.*?.html)',html,re.DOTALL)
	#if id2:
	if items:
		#mobile_watch_link = 'http://moshahda.online/' + id2[-1] + '.html'
		mobile_watch_link = items[-1]
		linkLIST.append(mobile_watch_link+'?name=Mobile')
	link2LIST,name2LIST = [],[]
	for link in linkLIST:
		link2,name2 = link.split('?name=')
		link2LIST.append(link2)
		name2LIST.append(name2)
	#z = 


	if len(linkLIST)==0:
		xbmcgui.Dialog().ok('مشكلة','غير قادر على ايجاد ملف الفيديو المناسب')
	else:
		#selection = xbmcgui.Dialog().select('اختر الفلتر المناسب:', linkLIST)
		#if selection == -1 : return
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
	html = openURL_cached(REGULAR_CACHE,website0a,'',headers,'','MOVIZLAND-SEARCH-1st')
	items = re.findall('<option value="(.*?)">(.*?)</option>',html,re.DOTALL)
	categoryLIST = [ '' ]
	filterLIST = [ 'الكل وبدون فلتر' ]
	for category,title in items:
		categoryLIST.append(category)
		filterLIST.append(title)
	if category:
		selection = xbmcgui.Dialog().select('اختر الفلتر المناسب:', filterLIST)
		if selection == -1 : return
		category = categoryLIST[selection]
	else: category = ''
	url = website0a + '/?s='+search+'&mcat='+category
	#xbmcgui.Dialog().ok(url,url)
	TITLES(url)
	return

