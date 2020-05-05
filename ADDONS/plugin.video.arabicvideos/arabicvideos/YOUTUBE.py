# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='YOUTUBE'
menu_name='_YUT_'
website0a = WEBSITES[script_name][0]

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==140: results = MENU()
	elif mode==141: results = TITLES(url)
	elif mode==142: results = PLAYLIST_ITEMS(url)
	elif mode==143: results = PLAY(url,text)
	#elif mode==144: results = SETTINGS()
	elif mode==145: results = CHANNEL_MENU(url)
	elif mode==146: results = CHANNEL_ITEMS(url)
	elif mode==147: results = LIVE_ARABIC()
	elif mode==148: results = LIVE_ENGLISH()
	elif mode==149: results = SEARCH(text)
	else: results = False
	return results

def MENU():
	addMenuItem('dir',menu_name+'بحث في الموقع','',149)
	addMenuItem('dir',menu_name+'العراق خطبة المرجعية',website0a+'/playlist?list=PL4jUq6pnG36QjuXDhNnIlriuzroTFtmfr',142)
	addMenuItem('dir',menu_name+'قناة كربلاء الفضائية',website0a+'/user/karbalatvchannel',145)
	addMenuItem('dir',menu_name+'العتبة الحسينية المقدسة',website0a+'/user/ImamHussaindotorg',145)
	addMenuItem('dir',menu_name+'بحث عن خطبة المرجعية',website0a+'/results?search_query=قناة+كربلاء+الفضائية+خطبة+الجمعة&sp=CAISAhAB',141)
	addMenuItem('dir',menu_name+'بحث عن قنوات عربية بث مباشر','',147)
	addMenuItem('dir',menu_name+'بحث عن قنوات أجنبية بث مباشر','',148)
	addMenuItem('dir',menu_name+'بحث عن مسلسلات عربية',website0a+'/results?search_query=مسلسل&sp=EgIQAw==',141)
	addMenuItem('dir',menu_name+'بحث عن افلام عربية',website0a+'/results?search_query=فيلم',141)
	addMenuItem('dir',menu_name+'بحث عن مسرحيات عربية',website0a+'/results?search_query=مسرحية',141)
	addMenuItem('dir',menu_name+'بحث عن مسلسلات اجنبية',website0a+'/results?search_query=series&sp=EgIQAw==',141)
	addMenuItem('dir',menu_name+'بحث عن افلام اجنبية',website0a+'/results?search_query=movie',141)
	addMenuItem('dir',menu_name+'بحث عن مسلسلات كارتون',website0a+'/results?search_query=كارتون&sp=EgIQAw==',141)
	addMenuItem('dir',menu_name+'شوف دراما الاولى',website0a+'/channel/UCgd_tWU4X7s10DKdgt-XDNQ',145)
	addMenuItem('dir',menu_name+'شوف دراما الثانية',website0a+'/channel/UC25ZB5ZMqLQwxFDV9FHvF8g',145)
	addMenuItem('dir',menu_name+'شوف دراما الثالثة',website0a+'/channel/UCQOz2_AhxeHUbNMYan-6ZQQ',145)
	addMenuItem('dir',menu_name+'شبكة وطن',website0a+'/user/WatanNetwork',145)
	#addMenuItem('dir',menu_name+'اعدادات اضافة يوتيوب','',144)
	#yes = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','هذا الاختيار سوف يخرجك من البرنامج','لأنه سوف يقوم بتشغيل برنامج يوتيوب')
	#if yes:
	#	url = 'plugin://plugin.video.youtube'
	#	xbmc.executebuiltin('Dialog.Close(busydialog)')
	#	xbmc.executebuiltin('ReplaceWindow(videos,'+url+')')
	#	#xbmc.executebuiltin('RunAddon(plugin.video.youtube)')
	return

def LIVE_ARABIC():
	TITLES(website0a+'/results?search_query=قناة+بث&sp=EgJAAQ==')
	return

def LIVE_ENGLISH():
	TITLES(website0a+'/results?search_query=tv&sp=EgJAAQ==')
	return

def CHANNEL_MENU(url):
	addMenuItem('dir',menu_name+'فيديوهات',url+'/videos',146)
	addMenuItem('dir',menu_name+'قوائم',url+'/playlists',146)
	addMenuItem('dir',menu_name+'قنوات',url+'/channels',146)
	return

def PLAY(url,text):
	#url = url+'&'
	#items = re.findall('v=(.*?)&',url,re.DOTALL)
	#id = items[0]
	#xbmcgui.Dialog().ok(url,'')
	#link = 'plugin://plugin.video.youtube/play/?video_id='+id
	#PLAY_VIDEO(link,script_name)
	linkLIST = [url]
	import RESOLVERS
	RESOLVERS.PLAY(linkLIST,script_name,text)
	return

def PLAYLIST_ITEMS(url):
	html_blocks = []
	if 'browse_ajax' in url:
		html = openURL_cached(REGULAR_CACHE,url,'','','','YOUTUBE-PLAYLIST_ITEMS-1st')
		html = CLEAN_AJAX(html)
		html_blocks = [html]
	elif 'list=' in url and 'index=' not in url:
		id = url.split('list=')[1].split('&')[0]
		url2 = website0a+'/playlist?list='+id
		html = openURL_cached(REGULAR_CACHE,url2,'','','','YOUTUBE-PLAYLIST_ITEMS-2nd')
		html_blocks = re.findall('class="pl-video-table(.*?)footer-container',html,re.DOTALL)
	#xbmcgui.Dialog().ok(url2,id)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('data-title="(.*?)".*?href="(.*?)".*?data-thumb="(.*?)".*?video-time(.*?)</div></td></tr>',block,re.DOTALL)
		for title,link,img,duration in items:
			if 'timestamp' in duration: duration = re.findall('timestamp.*?><.*?>(.*?)<',duration,re.DOTALL)[0]
			else: duration=''
			if '.' in duration: duration = duration.replace('.',':')
			title = title.replace('\n','')
			title = unescapeHTML(title)
			link = website0a+link
			addMenuItem('link',menu_name+title,link,143,img,duration)
		html_blocks = re.findall('items-load-more-button(.*?)load-more-loading',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('href="(.*?)"',block,re.DOTALL)
			for link in items:
				addMenuItem('dir',menu_name+'صفحة اخرى',website0a+link,142)
	else: PLAYLIST_ITEMS_PLAYER(url)
	return

def PLAYLIST_ITEMS_PLAYER(url):
	#url = 'https://www.youtube.com/watch?v=qCO4suk-pUY&list=RDQMvzOL1FJ97vc&start_radio=1'
	#xbmcgui.Dialog().ok(url,'')
	html = openURL_cached(REGULAR_CACHE,url,'','','','YOUTUBE-PLAYLIST_ITEMS_PLAYER-1st')
	html_blocks = re.findall('playlist-videos-container(.*?)watch7-container',html,re.DOTALL)
	block = html_blocks[0]
	items1 = re.findall('data-video-title="(.*?)".*?href="(.*?)"',block,re.DOTALL)
	items2 = re.findall('data-thumbnail-url="(.*?)"',block,re.DOTALL)
	i = 0
	for title,link in items1:
		title = title.replace('\n','')
		title = unescapeHTML(title)
		img = items2[i]
		link = website0a+link
		addMenuItem('link',menu_name+title,link,143,img)
		i = i+1
	addMenuItem('dir',menu_name+'صفحة اخرى',link,142)
	return

def CHANNEL_ITEMS(url):
	html = openURL_cached(REGULAR_CACHE,url,'','','','YOUTUBE-CHANNEL_ITEMS-1st')
	if 'browse_ajax' in url:
		html = CLEAN_AJAX(html)
		html_blocks = [html]
	else: html_blocks = re.findall('branded-page-v2-subnav-container(.*?)footer-container',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('yt-lockup-thumbnail.*?href="(.*?)".*?src="(.*?)"(.*?)sessionlink.*?title="(.*?)"(.*?)container',block,re.DOTALL)
		for link,img,count,title,live in items:
			if '>Live now<' in live: live = 'LIVE:  '
			else: live = ''
			if 'video-time' in count: duration = re.findall('video-time.*?><.*?>(.*?)<',count,re.DOTALL)[0]
			else: duration=''
			if '.' in duration: duration = duration.replace('.',':')
			if 'video-count-label' in count: count = ' '+re.findall('video-count-label.*?(\d+).*?</',count,re.DOTALL)[0]
			else: count=''
			title = title.replace('\n','')
			link = website0a+link
			title = unescapeHTML(title)
			if 'list=' in link: addMenuItem('dir',menu_name+'LIST'+count+':  '+title,link,142,img)
			elif '/channel/' in link: addMenuItem('dir',menu_name+'CHNL:  '+title,link,145,img)
			elif live!='': addMenuItem('link',menu_name+live+title,link,143,img,'','IsPlayable=no')
			else: addMenuItem('link',menu_name+title,link,143,img,duration)
		html_blocks = re.findall('items-load-more-button(.*?)load-more-loading',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('href="(.*?)"',block,re.DOTALL)
			for link in items:
				addMenuItem('dir',menu_name+'صفحة اخرى',website0a+link,146)
	return

def TITLES(url):
	html = openURL_cached(REGULAR_CACHE,url,'','','','YOUTUBE-TITLES-1st')
	html_blocks = re.findall('(yt-lockup-tile.*?)footer-container',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('yt-lockup-tile.*?(src|thumb)="(.*?)"(.*?)href="(.*?)".*?title="(.*?)"(.*?)</div></div></div>(.*?)</li>',block,re.DOTALL)
	else: items = []
	#xbmcgui.Dialog().ok(str(block.count('yt-lockup-tile')),str(len(items)))
	#with open('S:\emad3.html', 'w') as f: f.write(block)
	for dummy,img,count,link,title,count2,paid in items:
		if 'Watch later' in title: continue
		if 'adurl=' in link:
			#title = 'AD:  '+title
			#link = re.findall('adurl=(.*?)&amp;',link+'&amp;',re.DOTALL)
			#link = unquote(link[0])
			continue
		img2 = re.findall('thumb="(.*?)"',count,re.DOTALL)
		if img2: img = img2[0]
		counts = ''
		if '\n' in paid: title = '$$:  '+title
		if 'video-time' in count: duration = re.findall('video-time.*?>(.*?)<',count,re.DOTALL)[0]
		else: duration = ''
		if '.' in duration: duration = duration.replace('.',':')
		if '>Live now<' in count2: live = 'LIVE:  '
		else: live = ''
		if 'video-count-label' in count:
			count = re.findall('video-count-label.*?(\d+).*?</',count,re.DOTALL)
			if count: counts = ' ' + count[0]
		else:
			count2 = re.findall('<li>(\d+) video',count2,re.DOTALL)
			if count2: counts = ' ' + count2[0]
		if 'http' not in img: img = 'https:'+img
		if 'http' not in link: link = website0a+link
		title = title.replace('\n','')
		title = unescapeHTML(title)
		if 'list=' in link: addMenuItem('dir',menu_name+'LIST'+counts+':  '+title,link,142,img)
		elif '/channel/' in link: addMenuItem('dir',menu_name+'CHNL'+counts+':  '+title,link,145,img)
		elif '/user/' in link: addMenuItem('dir',menu_name+'USER'+counts+':  '+title,link,145,img)
		elif live!='': addMenuItem('link',menu_name+live+title,link,143,img,'','IsPlayable=no')
		else: addMenuItem('link',menu_name+title,link,143,img,duration)
	html_blocks = re.findall('search-pager(.*?)footer-container',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?button-content">(.*?)<',block,re.DOTALL)
		for link,title in items:
			addMenuItem('dir',menu_name+'صفحة '+title,website0a+link,141)
	return

"""
def SETTINGS():
	text1 = 'هذا الموقع يستخدم اضافة يوتيوب ولا يعمل بدونه'
	text2 = 'لعرض فيدوهات يوتيوب تحتاج ان تتأكد ان تضبيطات واعدادت يوتويب صحيحة'
	xbmcgui.Dialog().ok(text1,text2)
	xbmc.executebuiltin('Addon.OpenSettings(plugin.video.youtube)', True)
	return
"""

def SEARCH(search):
	if '::' in search:
		search = search.split('::')[0]
		category = False
	else: category = True
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.replace(' ','%20')
	url2 = website0a + '/results?search_query='+search
	#url2 = 'plugin://plugin.video.youtube/kodion/search/query/?q='+search
	#xbmc.executebuiltin('Dialog.Close(busydialog)')
	#xbmc.executebuiltin('ActivateWindow(videos,'+url2+',return)')
	html = openURL_cached(REGULAR_CACHE,url2,'','','','YOUTUBE-SEARCH-1st')
	html_blocks = re.findall('filter-dropdown(.*?)class="item-section',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('href="(.*?)".*?title="(.*?)"',block,re.DOTALL)
	fileterLIST = ['بدون فلتر وبدون ترتيب']
	linkLIST = [url2]
	for link,title in items:
		if 'Remove' in title: continue
		title = title.replace('Search for','Search for:  ')
		title = title.replace('Sort by','Sort by:  ')
		if 'Playlist' in title: title = 'جيد للمسلسلات '+title
		fileterLIST.append(unescapeHTML(title))
		linkLIST.append(website0a+link)
	fileterLIST.append(unescapeHTML('Sort by:   relevance'))
	linkLIST.append(url2)
	if category:
		selection = xbmcgui.Dialog().select('اختر الفلتر او الترتيب المناسب:', fileterLIST)
		if selection == -1: return
		url3 = linkLIST[selection]
	else: url3 = linkLIST[0]
	TITLES(url3)
	return

def CLEAN_AJAX(text):
	text = text.replace('\\u003c','<')
	text = text.replace('\\u003e','>')
	text = text.replace('\\u0026','&')
	text = text.replace('\\"','"')
	text = text.replace('\\/','/')
	text = text.replace('\\n','\n')
	#text = text.encode('utf8')
	#text = text.decode('unicode_escape')
	#text = escapeUNICODE(text)
	#file = open('s:\emad.txt', 'w')
	#file.write(text)
	#file.close()
	return text


