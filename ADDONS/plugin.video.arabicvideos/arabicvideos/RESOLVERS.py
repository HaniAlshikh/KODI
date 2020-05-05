# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from LIBRARY import *

script_name='RESOLVERS'
#doNOTresolveMElist = [ 'mystream','vimple','vidbom','gounlimited' ]
doNOTresolveMElist = []

def PLAY(linkLIST,script_name,text=''):
	linkLIST = list(set(linkLIST))
	count_watch = str(linkLIST).count('__watch')
	count_download = str(linkLIST).count('__download')
	count_others = len(linkLIST)-count_watch-count_download
	select_header = 'مشاهدة:'+str(count_watch)+'    تحميل:'+str(count_download)+'    أخرى:'+str(count_others)
	#xbmcgui.Dialog().ok(str(count_watch),str(count_download))
	#selection = xbmcgui.Dialog().select(select_header, linkLIST)
	titleLIST,linkLIST = SERVERS_cached(linkLIST,script_name)
	if len(linkLIST)==0:
		result = 'unresolved'
		errormsg = ''
	else:
		while True:
			errormsg = ''
			if len(linkLIST)==1: selection = 0
			else: selection = xbmcgui.Dialog().select(select_header, titleLIST)
			if selection == -1: result = 'canceled1'
			else:
				title = titleLIST[selection]
				url = linkLIST[selection]
				#xbmcgui.Dialog().ok(str(urlLIST[selection]),str(urlLIST[selection]))
				if 'سيرفر' in title and '2مجهول2' in title:
					LOG_THIS('ERROR',LOGGING(script_name)+'   Unknown Selected Server   Server: [ '+title+' ]   URL: [ '+url+' ]')
					import SERVICES
					SERVICES.MAIN(156)
					result = 'unresolved'
				else:
					LOG_THIS('NOTICE',LOGGING(script_name)+'   Playing Selected Server   Server: [ '+title+' ]   URL: [ '+url+' ]')
					result,errormsg = PLAY_LINK(url,script_name,text)
			if '\n' not in errormsg: error1,error2 = errormsg,''
			else: error1,error2 = errormsg.split('\n',1)
			if result in ['playing','canceled1'] or len(linkLIST)==1: break
			elif result in ['failed','timeout','tried']: break
			elif result not in ['canceled2','https']: xbmcgui.Dialog().ok('السيرفر لم يعمل','جرب سيرفر غيره',error1,error2)
	if result=='unresolved' and len(titleLIST)>0: xbmcgui.Dialog().ok('سيرفر هذا الفيديو لم يعمل','جرب فيديو غيره',errormsg)
	elif result in ['failed','timeout']: xbmcgui.Dialog().ok('الفيديو لم يعمل',errormsg)
	"""
	elif result in ['Canceled1','Canceled2']:
		#LOG_THIS('NOTICE',LOGGING(script_name)+'   Test:   '+sys.argv[0]+sys.argv[2])
		xbmcplugin.setResolvedUrl(addon_handle, False, xbmcgui.ListItem())
		play_item = xbmcgui.ListItem(path='plugin://plugin.video.arabicvideos/?mode=143&url=https://www.youtube.com/watch%3Fv%3Dgwb1pxVtw9Q')
		xbmc.Player().play('https://flv1.alarab.com/iphone/123447.mp4',play_item)
		#xbmcgui.Dialog().ok('تم الالغاء','')
	"""
	return result
	#if script_name=='HALACIMA': menu_name='HLA [/COLOR]'
	#elif script_name=='4HELAL': menu_name='[COLOR FFC89008]HEL [/COLOR]'
	#elif script_name=='AKOAM': menu_name='[COLOR FFC89008]AKM [/COLOR]'
	#elif script_name=='SHAHID4U': menu_name='[COLOR FFC89008]SHA '
	#size = len(urlLIST)
	#for i in range(0,size):
	#	title = serversLIST[i]
	#	link = urlLIST[i]
	#	addMenuItem('link',menu_name+title,link,160,'','',script_name)

def PLAY_LINK(url,script_name,text=''):
	#xbmcgui.Dialog().ok('',titleLIST[0])
	url = url.strip(' ').strip('&').strip('?').strip('/')
	errormsg,titleLIST,linkLIST = RESOLVE(url)
	if 'IsPlayable=no' in text: IsPlayable = 'no'
	else: IsPlayable='yes'
	if linkLIST:
		while True:
			if len(linkLIST)==1: selection = 0
			else: selection = xbmcgui.Dialog().select('اختر الملف المناسب:', titleLIST)
			if selection == -1: result = 'canceled2'
			else:
				videoURL = linkLIST[selection]
				title = titleLIST[selection]
				LOG_THIS('NOTICE',LOGGING(script_name)+'   Playing Selected Video   Selected: [ '+title+' ]   URL: [ '+str(videoURL)+' ]')
				if 'moshahda.' in videoURL and 'download_orig' in videoURL:
					errormsg2,titleLIST2,linkLIST2 = MOVIZLAND(videoURL)
					if linkLIST2: videoURL = linkLIST2[0]
					else: videoURL = ''
				if videoURL=='': result = 'unresolved'
				else: result = PLAY_VIDEO(videoURL,script_name,IsPlayable)
			if result in ['playing','canceled2'] or len(linkLIST)==1: break
			elif result in ['failed','timeout','tried']: break
			else: xbmcgui.Dialog().ok('الملف لم يعمل','جرب ملف غيره')
		"""
		if 'youtube.mpd' in linkLIST[0]:
			xbmcgui.Dialog().ok('click ok to shutdown the http server','')
			#html = openURL_cached(NO_CACHE,'http://localhost:55055/shutdown','','','','RESOLVERS-PLAY_LINK-1st')
			titleLIST[0].shutdown()
		"""
	else:
		result = 'unresolved'
		videofiletype = re.findall('(\.ts|\.mp4|\.m3u|\.m3u8|\.mpd|\.mkv|\.flv|\.mp3)(|\?.*?|/\?.*?|\|.*?)&&',url+'&&',re.DOTALL)
		if videofiletype: result = PLAY_VIDEO(url,script_name,IsPlayable)
	return result,errormsg
	#title = xbmc.getInfoLabel( "ListItem.Label" )
	#if 'سيرفر عام مجهول' in title:
	#	import SERVICES
	#	SERVICES.MAIN(156)
	#	return ''

def RESOLVABLE(url):
	# private	: سيرفر خاص
	# known		: سيرفر عام معروف
	# external	: سيرفر عام خارجي
	# named		: سيرفر عام محدد
	private,known,external,named = None,None,None,None
	result1,result2,result3,result4,result5 = '','','','',''
	#xbmcgui.Dialog().ok(url,'')
	url2,server = url,url.lower().split('/')[2]
	if 'name=' in url:
		url2,named = url.split('name=',1)
		named = named+'__'+'__'+'__'
		server2,type,filetype,quality = named.lower().split('__')[:4]
		#xbmcgui.Dialog().ok(server,server2)
		if server2!='': server = server2
		if type=='watch': result3 = ' '+'مشاهدة'
		elif type=='download': result3 = ' '+'%%تحميل'
		else: result3 = ' '+'%مشاهدة وتحميل'
		if filetype!='':
			#if '360p'==quality: filetype = 'm3u8'
			if 'mp4' not in filetype: filetype = '%'+filetype
			result4 = ' '+filetype
		if quality!='':
			#if '360p'==quality: quality = '1080p'
			quality = '%%%%%%%%%'+quality
			result5 = ' '+quality[-9:]
	url2 = url2.strip('?').strip('/').strip('&')
	#if any(value in server for value in doNOTresolveMElist): return ''
	#xbmcgui.Dialog().ok(server,named)
	if   'akoam'		in server: private = 'akoam'
	elif 'arabseed'		in server: private = 'arabseed'
	elif 'youtu'	 	in server: private = 'youtube'
	elif 'y2u.be'	 	in server: private = 'youtube'
	elif 'd.egybest.d'	in server: private = 'egybestvip'
	elif 'moshahda'		in server: private = 'movizland'
	elif 'facultybooks'	in server: private = 'facultybooks'
	elif 'inflam.cc'	in server: private = 'inflam'
	elif 'buzzvrl'		in server: private = 'buzzvrl'
	elif 'arabloads'	in server: known = 'arabloads'
	elif 'archive'		in server: known = 'archive'
	elif 'catch.is'	 	in server: known = 'catch'
	elif 'filerio'		in server: known = 'filerio'
	elif 'vidbm'		in server: known = 'vidbm'
	elif 'vidhd'		in server: known = 'vidhd'
	elif 'videobin'		in server: known = 'videobin'
	elif 'govid'		in server: known = 'govid'
	elif 'liivideo' 	in server: known = 'liivideo'
	elif 'mp4upload'	in server: known = 'mp4upload'
	elif 'publicvideo'	in server: known = 'publicvideo'
	elif 'rapidvideo' 	in server: known = 'rapidvideo'
	elif 'top4top'		in server: known = 'top4top'
	elif 'upbom' 		in server: known = 'upbom'
	elif 'uppom' 		in server: known = 'uppom'
	elif 'uptobox' 		in server: known = 'uptobox'
	elif 'uptostream'	in server: known = 'uptostream'
	elif 'uqload' 		in server: known = 'uqload'
	elif 'vcstream' 	in server: known = 'vcstream'
	elif 'vidbob'		in server: known = 'vidbob'
	elif 'vidoza' 		in server: known = 'vidoza'
	elif 'watchvideo' 	in server: known = 'watchvideo'
	elif 'wintv.live'	in server: known = 'wintv.live'
	elif 'zippyshare'	in server: known = 'zippyshare'
	else:
		import resolveurl
		external = resolveurl.HostedMediaFile(url2).valid_url()
		if not external:
			#LOG_THIS('NOTICE','1111 ==========================')
			external = False
			list_url = 'https://ytdl-org.github.io/youtube-dl/supportedsites.html'
			html = openURL_cached(LONG_CACHE,list_url,'','','','RESOLVERS-RESOLVABLE-1st')
			html = re.findall('<ul>(.*?)</ul>',html,re.DOTALL)
			html = html[0].lower()
			html = html.replace('<li>','').replace('<b>','')
			html = html.replace('</li>','').replace('</b>','')
			#LOG_THIS('NOTICE','2222 ==========================')
			parts = server.split('.')
			for part in parts:
				if len(part)<4: continue
				elif part in html:
					external = True
					break
	#xbmcgui.Dialog().ok(url,url2)
	if   private:  result1,result2 = 'خاص',private
	elif known:    result1,result2 = '%عام معروف',known
	elif named:    result1,result2 = '%%عام محدد',server
	elif external: result1,result2 = '%%%عام خارجي',server
	else:          result1,result2 = '%%%%عام مجهول',server
	result1 = ' '+result1
	result2 = ' '+result2	
	result = 'سيرفر'+result3+result1+result2+result4+result5
	#xbmc.log(result)
	return result
	"""
	elif 'playr.4helal'	in server2:	private = 'helal'
	elif 'estream'	 	in server2:	known = 'estream'
	elif 'gounlimited'	in server2:	known = 'gounlimited'
	elif 'intoupload' 	in server2:	known = 'intoupload'
	elif 'thevideo'		in server2:	known = 'thevideo'
	elif 'vev.io'	 	in server2:	known = 'vev'
	elif 'vidbom'		in server2:	known = 'vidbom'
	elif 'vidhd' 		in server2:	known = 'vidhd'
	elif 'vidshare' 	in server2:	known = 'vidshare'
	"""

def INTERNAL_RESOLVERS(url):
	url2,server = url,url.lower().split('/')[2]
	if 'name=' in url:
		url2,named = url.split('name=',1)
		named = named.lower()
	else: named = ''
	url2 = url2.strip('?').strip('/').strip('&')
	#if 'gounlimited'	in server: url2 = url2.replace('https:','http:')
	#if any(value in server for value in doNOTresolveMElist): titleLIST,linkLIST = ['Error: RESOLVE does not resolve this server'],[]
	if   'akoam'		in server: errormsg,titleLIST,linkLIST = AKOAM(url2,named)
	elif 'shahid4u'		in server: errormsg,titleLIST,linkLIST = SHAHID4U(url2)
	elif 'arabseed'		in server: errormsg,titleLIST,linkLIST = ARABSEED(url2)
	elif 'arblionz'		in server: errormsg,titleLIST,linkLIST = ARABLIONZ(url2)
	elif 'arablionz'	in server: errormsg,titleLIST,linkLIST = ARABLIONZ(url2)
	elif 'youtu'		in server: errormsg,titleLIST,linkLIST = YOUTUBE(url2)
	elif 'y2u.be'		in server: errormsg,titleLIST,linkLIST = YOUTUBE(url2)
	elif 'd.egybest.d'	in server: errormsg,titleLIST,linkLIST = '',[''],[url2]
	elif 'egy.best'		in server: errormsg,titleLIST,linkLIST = EGYBEST(url)
	elif 'series4watch'	in server: errormsg,titleLIST,linkLIST = SERIES4WATCH(url2)
	elif 'moshahda'		in server: errormsg,titleLIST,linkLIST = MOVIZLAND(url)
	else: errormsg,titleLIST,linkLIST = 'NEED_EXTERNAL_RESOLVERS',[''],[url2]
	#xbmcgui.Dialog().ok('INTERNAL_RESOLVERS 1',str(url2))
	#xbmcgui.Dialog().ok('INTERNAL_RESOLVERS 2',str(linkLIST))
	return errormsg,titleLIST,linkLIST

def EXTERNAL_RESOLVER_1(url):
	server = url.lower().split('/')[2]
	#if 'gounlimited'	in server: url2 = url2.replace('https:','http:')
	#if any(value in server for value in doNOTresolveMElist): titleLIST,linkLIST = ['Error: RESOLVE does not resolve this server'],[]
	if   'arabloads'	in server: errormsg,titleLIST,linkLIST = ARABLOADS(url)
	elif 'archive'		in server: errormsg,titleLIST,linkLIST = ARCHIVE(url)
	elif 'buzzvrl'		in server: errormsg,titleLIST,linkLIST = BUZZVRL(url)
	elif 'e5tsar'		in server: errormsg,titleLIST,linkLIST = E5TSAR(url)
	elif 'facultybooks'	in server: errormsg,titleLIST,linkLIST = FACULTYBOOKS(url)
	elif 'inflam.cc'	in server: errormsg,titleLIST,linkLIST = FACULTYBOOKS(url)
	elif 'catch.is'	 	in server: errormsg,titleLIST,linkLIST = XFILESHARING(url)
	elif 'filerio'		in server: errormsg,titleLIST,linkLIST = XFILESHARING(url)
	elif 'vidbm'		in server: errormsg,titleLIST,linkLIST = XFILESHARING(url)
	elif 'vidhd'		in server: errormsg,titleLIST,linkLIST = XFILESHARING(url)
	elif 'videobin'		in server: errormsg,titleLIST,linkLIST = XFILESHARING(url)
	elif 'govid'		in server: errormsg,titleLIST,linkLIST = GOVID(url)
	elif 'liivideo' 	in server: errormsg,titleLIST,linkLIST = LIIVIDEO(url)
	elif 'mp4upload'	in server: errormsg,titleLIST,linkLIST = MP4UPLOAD(url)
	elif 'publicvideohos'	in server: errormsg,titleLIST,linkLIST = PUBLICVIDEOHOST(url)
	elif 'rapidvideo' 	in server: errormsg,titleLIST,linkLIST = RAPIDVIDEO(url)
	elif 'top4top'		in server: errormsg,titleLIST,linkLIST = TOP4TOP(url)
	elif 'upbom' 		in server: errormsg,titleLIST,linkLIST = UPBOM(url)
	elif 'uppom' 		in server: errormsg,titleLIST,linkLIST = UPBOM(url)
	elif 'uptobox' 		in server: errormsg,titleLIST,linkLIST = UPTO(url)
	elif 'uptostream'	in server: errormsg,titleLIST,linkLIST = UPTO(url)
	elif 'uqload' 		in server: errormsg,titleLIST,linkLIST = UQLOAD(url)
	elif 'vcstream' 	in server: errormsg,titleLIST,linkLIST = VCSTREAM(url)
	elif 'vidbob'		in server: errormsg,titleLIST,linkLIST = VIDBOB(url)
	elif 'vidoza' 		in server: errormsg,titleLIST,linkLIST = VIDOZA(url)
	elif 'watchvideo' 	in server: errormsg,titleLIST,linkLIST = WATCHVIDEO(url)
	elif 'wintv.live'	in server: errormsg,titleLIST,linkLIST = WINTVLIVE(url)
	elif 'zippyshare'	in server: errormsg,titleLIST,linkLIST = ZIPPYSHARE(url)
	else: errormsg,titleLIST,linkLIST = 'Error: EXTERNAL_RESOLVER_1 Failed',[],[]
	return errormsg,titleLIST,linkLIST
	"""
	elif 'estream'	 	in server: errormsg,titleLIST,linkLIST = ESTREAM(url)
	elif 'gounlimited'	in server: errormsg,titleLIST,linkLIST = GOUNLIMITED(url)
	elif 'intoupload' 	in server: errormsg,titleLIST,linkLIST = INTOUPLOAD(url)
	elif 'thevideo'		in server: errormsg,titleLIST,linkLIST = THEVIDEO(url)
	elif 'vev.io'	 	in server: errormsg,titleLIST,linkLIST = VEVIO(url)
	elif 'playr.4helal'	in server: errormsg,titleLIST,linkLIST = HELAL(url)
	elif 'vidbom'		in server: errormsg,titleLIST,linkLIST = VIDBOM(url)
	elif 'vidhd' 		in server: errormsg,titleLIST,linkLIST = VIDHD(url)
	elif 'vidshare' 	in server: errormsg,titleLIST,linkLIST = VIDSHARE(url)
	"""

def	CLEAN_URLS(urls):
	if 'list' in str(type(urls)):
		links = []
		for link in urls:
			if 'str' in str(type(link)):
				link = link.replace('\r','').replace('\n','').strip(' ')
			links.append(link)
	else: links = urls.replace('\r','').replace('\n','').strip(' ')
	return links

def RESOLVE(url):
	LOG_THIS('NOTICE',LOGGING(script_name)+'   Resolving Started   For: [ '+url+' ]')
	resolver,link,allerrors = 'INTERNAL_RESOLVER','',''
	errormsg,titleLIST,linkLIST = INTERNAL_RESOLVERS(url)
	linkLIST = CLEAN_URLS(linkLIST)
	if errormsg=='NEED_EXTERNAL_RESOLVERS':
		#errormsg = errormsg.replace('NEED_EXTERNAL_RESOLVERS','')
		link = linkLIST[0]
		resolver = 'EXTERNAL_RESOLVER_1'
		errormsg,titleLIST,linkLIST = EXTERNAL_RESOLVER_1(link)
		linkLIST = CLEAN_URLS(linkLIST)
		if errormsg!='':
			allerrors = allerrors+'\nResolver 1: '+errormsg
			resolver = 'EXTERNAL_RESOLVER_2'
			errormsg,titleLIST,linkLIST = EXTERNAL_RESOLVER_2(link)
			linkLIST = CLEAN_URLS(linkLIST)
			if errormsg!='':
				allerrors = allerrors+'\nResolver 2: '+errormsg
				resolver = 'EXTERNAL_RESOLVER_3'
				errormsg,titleLIST,linkLIST = EXTERNAL_RESOLVER_3(link)
				linkLIST = CLEAN_URLS(linkLIST)
				if errormsg!='':
					allerrors = allerrors+'\nResolver 3: '+errormsg
					#LOG_THIS('ERROR',LOGGING(script_name)+'   All External Resolvers Failed   Messages: [ '+allerrors+' ]   For: [ '+url+' ]   Link: [ '+link+' ]')
	elif errormsg!='':
		allerrors = 'Resolver 0: '+errormsg
	allerrors = allerrors.strip('\n')
	if len(linkLIST)>0:
		LOG_THIS('NOTICE',LOGGING(script_name)+'   Resolving Succeeded   Resolver: [ '+resolver+' ]   Result: [ '+str(linkLIST)+' ]   Messages: [ '+allerrors+' ]   For: [ '+url+' ]   Link: [ '+link+' ]')
	else:
		LOG_THIS('ERROR',LOGGING(script_name)+'   Resolving Failed   Resolver: [ '+resolver+' ]   Messages: [ '+allerrors+' ]   For: [ '+url+' ]   Link: [ '+link+' ]')
	#allerrors = allerrors.replace('\n',' ... ')
	return allerrors,titleLIST,linkLIST

def SERVERS_cached(linkLIST,script_name=''):
	#t1 = time.time()
	cacheperiod = LONG_CACHE
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	conn.text_factory = str
	c.execute('SELECT serversLIST,urlLIST FROM serverscache WHERE linkLIST="'+str(linkLIST)+'"')
	rows = c.fetchall()
	if rows:
		#message = 'found in cache'
		serversLIST,urlLIST = eval(rows[0][0]),eval(rows[0][1])
	else:
		#message = 'not found in cache'
		serversLIST,urlLIST = SERVERS(linkLIST)
		t = (now+cacheperiod,str(linkLIST),str(serversLIST),str(urlLIST))
		c.execute("INSERT INTO serverscache VALUES (?,?,?,?)",t)
		conn.commit()
	conn.close()
	#t2 = time.time()
	#xbmcgui.Dialog().notification(message,str(int(t2-t1))+' ms')
	return serversLIST,urlLIST

def SERVERS(linkLIST,script_name=''):
	serversLIST,urlLIST,unknownLIST,serversDICT = [],[],[],[]
	#linkLIST = list(set(linkLIST))
	#selection = xbmcgui.Dialog().select('اختر الفلتر المناسب:', linkLIST)
	#if selection == -1 : return ''
	for link in linkLIST:
		if link=='': continue
		serverNAME = RESOLVABLE(link)
		serversDICT.append( [serverNAME,link] )
	sortedDICT = sorted(serversDICT, reverse=True, key=lambda key: key[0])
	for server,link in sortedDICT:
		server = server.replace('%','')
		serversLIST.append(server)
		urlLIST.append(link)
	#lines = len(unknownLIST)
	#if lines>0:
	#	message = '\\n'
	#	for link in unknownLIST:
	#		message += link + '\\n'
	#	subject = 'Unknown Resolvers = ' + str(lines)
	#	result = SEND_EMAIL(subject,message,'no','','FROM-RESOLVERS-'+script_name)
	return serversLIST,urlLIST

def	EXTERNAL_RESOLVER_2(url):
	#url = 'http://www.youtube.com/watch?v=BaW_jenozKc'
	try:
		import resolveurl
		result = resolveurl.HostedMediaFile(url).resolve()
	except: result = False
	# resolveurl might fail either with an error or returns value False
	if result==False:
		errortrace = traceback.format_exc()
		sys.stderr.write(errortrace)
		if 'Error: ' in errortrace: errormsg = errortrace.splitlines()[-1]
		else: errormsg = 'Error: EXTERNAL_RESOLVER_2 Failed'
		#xbmcgui.Dialog().ok(errormsg,str(result))
		return errormsg,[],[]
	return '',[''],[result]

def	EXTERNAL_RESOLVER_3(url):
	#url = 'http://www.youtube.com/watch?v=BaW_jenozKc'
	try:
		import youtube_dl
		ydl = youtube_dl.YoutubeDL({})
		#ydl = youtube_dl.YoutubeDL({'outtmpl': u'%(id)s%(ext)s'})
		with ydl:
			results = ydl.extract_info(url,download=False) # We just want to extract the info
	except: results = False
	# youtube_dl might fail either with an error or returns value False
	if results==False or 'formats' not in results.keys():
		errortrace = traceback.format_exc()
		sys.stderr.write(errortrace)
		if 'Error: ' in errortrace: errormsg = errortrace.splitlines()[-1]
		else: errormsg = 'Error: EXTERNAL_RESOLVER_3 Failed'
		return errormsg,[],[]
	else:
		titleLIST,linkLIST = [],[]
		for link in results['formats']:
			titleLIST.append(link['format'])
			linkLIST.append(link['url'])
		return '',titleLIST,linkLIST

def MOVIZLAND(link):
	# http://moshahda.online/hj4ihfwvu3rl.html?name=Main
	# http://moshahda.online/dl?op=download_orig&id=hj4ihfwvu3rl&mode=o&hash=62516-107-159-1560654817-4fa63debbd8f3714289ad753ebf598ae
	headers = { 'User-Agent' : '' }
	if 'op=download_orig' in link:
		html = openURL_cached(SHORT_CACHE,link,'',headers,'','RESOLVERS-MOSHAHDA_ONLINE-1st')
		#xbmc.log(html)
		#xbmcgui.Dialog().ok(link,html)
		items = re.findall('direct link.*?href="(.*?)"',html,re.DOTALL)
		if items: return '',[''],[ items[0] ]
		else:
			message = re.findall('class="err">(.*?)<',html,re.DOTALL)
			if message:
				xbmcgui.Dialog().ok('رسالة من الموقع الاصلي',message[0])
				return message[0],[],[]
	else:
		#xbmcgui.Dialog().ok(link,'')
		parts = link.split('?')
		url = parts[0]
		name2 = parts[1].replace('name=','').lower()
		# watch links
		html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-MOSHAHDA_ONLINE-2nd')
		html_blocks = re.findall('Form method="POST" action=\'(.*?)\'(.*?)div',html,re.DOTALL)
		if not html_blocks: return 'Error: Resolver MOVIZLAND Failed',[],[]
		link2 = html_blocks[0][0]
		block = html_blocks[0][1]
		if '.rar' in block or '.zip' in block: return 'Error: MOVIZLAND Not a video file',[],[]
		items = re.findall('name="(.*?)".*?value="(.*?)"',block,re.DOTALL)
		payload = {}
		for name,value in items:
			payload[name] = value
		data = urllib.urlencode(payload)
		html = openURL_cached(SHORT_CACHE,link2,data,headers,'','RESOLVERS-MOSHAHDA_ONLINE-3rd')
		html_blocks = re.findall('Download Video.*?get\(\'(.*?)\'.*?sources:(.*?)image:',html,re.DOTALL)
		if not html_blocks: return 'Error: Resolver MOVIZLAND Failed',[],[]
		download = html_blocks[0][0]
		block = html_blocks[0][1]
		items = re.findall('file:"(.*?)"(,label:".*?"|)',block,re.DOTALL)
		titleLISTtemp,titleLIST,linkLISTtemp,linkLIST,resolutionLIST = [],[],[],[],[]
		for link,title in items:
			if '.m3u8' in link:
				titleLISTtemp,linkLISTtemp = EXTRACT_M3U8(link)
				linkLIST = linkLIST + linkLISTtemp
				if titleLISTtemp[0]=='-1': titleLIST.append(' سيرفر خاص '+'m3u8 '+name2)
				else:
					for title in titleLISTtemp:
						titleLIST.append(' سيرفر خاص '+'m3u8 '+name2+' '+title)
			else:
				title = title.replace(',label:"','')
				title = title.strip('"')
				#xbmcgui.Dialog().ok(title,str(resolutionLIST))
				title = ' سيرفر  خاص '+' mp4 '+name2+' '+title
				titleLIST.append(title)
				linkLIST.append(link)
		# download links
		link = 'http://moshahda.online' + download
		html = openURL_cached(SHORT_CACHE,link,'',headers,'','RESOLVERS-MOSHAHDA_ONLINE-5th')
		items = re.findall("download_video\('(.*?)','(.*?)','(.*?)'.*?<td>(.*?),",html,re.DOTALL)
		for id,mode,hash,resolution in items:
			title = ' سيرفر تحميل خاص '+' mp4 '+name2+' '+resolution.split('x')[1]
			link = 'http://moshahda.online/dl?op=download_orig&id='+id+'&mode='+mode+'&hash='+hash
			resolutionLIST.append(resolution)
			titleLIST.append(title)
			linkLIST.append(link)
		resolutionLIST = set(resolutionLIST)
		titleLISTnew,sortingDICT = [],[]
		for title in titleLIST:
			#xbmcgui.Dialog().ok(title,'')
			res = re.findall(" (\d*x|\d*)&&",title+'&&',re.DOTALL)
			for resolution in resolutionLIST:
				if res[0] in resolution:
					title = title.replace(res[0],resolution.split('x')[1])
			titleLISTnew.append(title)
		#xbmc.log(items[0][0])
		for i in range(len(linkLIST)):
			items = re.findall("&&(.*?)(\d*)&&",'&&'+titleLISTnew[i]+'&&',re.DOTALL)
			sortingDICT.append( [titleLISTnew[i],linkLIST[i],items[0][0],items[0][1]] )
		sortingDICT = sorted(sortingDICT, key=lambda x: x[3], reverse=True)
		sortingDICT = sorted(sortingDICT, key=lambda x: x[2], reverse=False)
		titleLIST,linkLIST = [],[]
		for i in range(len(sortingDICT)):
			titleLIST.append(sortingDICT[i][0])
			linkLIST.append(sortingDICT[i][1])
	if len(linkLIST)==0: return 'Error: MOVIZLAND Resolver Failed',[],[]
	else: return '',titleLIST,linkLIST

def E5TSAR(url):
	# http://e5tsar.com/717254
	parts = url.split('?')
	url2 = parts[0]
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url2,'',headers,'','RESOLVERS-E5TSAR-1st')
	items = re.findall('Please wait.*?href=\'(.*?)\'',html,re.DOTALL)
	url = items[0]
	#errormsg,titleLIST,linkLIST = EXTERNAL_RESOLVERS(url)
	#return errormsg,titleLIST,linkLIST
	return 'NEED_EXTERNAL_RESOLVERS',[''],[url]

def BUZZVRL(url):
	# https://facultybooks.org/VLO1NNdGuy
	# https://inflam.cc/VLO1NNdGuy
	titleLIST,linkLIST = [],[]
	headers = { 'User-Agent' : '' }
	html = openURL_cached(LONG_CACHE,url,'',headers,'','RESOLVERS-FACULTYBOOKS-1st')
	url2 = re.findall('redirect_url.*?href="(.*?)"',html,re.DOTALL)
	if url2: return '',[''],[url2[0]]
	else: return 'Error: Resolver BUZZVRL Failed',[],[]

def FACULTYBOOKS(url):
	# https://facultybooks.org/VLO1NNdGuy
	# https://inflam.cc/VLO1NNdGuy
	titleLIST,linkLIST = [],[]
	headers = { 'User-Agent' : '' }
	html = openURL_cached(LONG_CACHE,url,'',headers,'','RESOLVERS-FACULTYBOOKS-1st')
	url2 = re.findall('href","(htt.*?)"',html,re.DOTALL)
	if url2: return '',[''],[url2[0]]
	else: return 'Error: Resolver FACULTYBOOKS Failed',[],[]

def EGYBEST(url):
	# https://egy.best/api?call=nAAAUceAUAlAUNbbbbbbbaUlUAUbFQAUAlAUGkmPMsfPyNBUlUAUSReUAlAUuReRSRBpElzAUlUAUguGdPRbgBUAlNhANdNANdNdNbbdNUlUAUPRSAUAlAUNhhlNhNNdAUlUAUPRyAUAlAUNhbUAzhAlfzhlAvfUAd&auth=874ded32a2e3b91d6ae55186274469e2?name=vidstream__watch
	# https://egy.best/api?call=nAAAUceAUAlAUNbbbbbbbaUlUAUbFQAUAlAUGkmPMsfPyNBUlUAUSReUAlAUuReRSRBpElzAUlUAUguGdPRbgBUAlNhANdNANdNdNbbdNUlUAUPRSAUAlAUNhhlNhNNdAUlUAUPRyAUAlAUNhbUAzhAlfzhlAvfUAd&auth=874ded32a2e3b91d6ae55186274469e2?name=vidstream__download
	url2 = url.split('name=',1)[0].strip('?').strip('/').strip('&')
	titleLIST,linkLIST,items,url3 = [],[],[],''
	headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }
	response = openURL_requests_cached(SHORT_CACHE,'GET',url2,'',headers,False,'','RESOLVERS-EGYBEST-1st')
	if 'Location' in response.headers:
		url3 = response.headers['Location']
		response = openURL_requests_cached(SHORT_CACHE,'GET',url3,'',headers,False,'','RESOLVERS-EGYBEST-2nd')
	if 'Location' in response.headers:
		url3 = response.headers['Location']
	xbmcgui.Dialog().ok(url3,response.html)
	if 'http' in url3:
		# https://vidstream.top/f/KcLxaW7twB/?vclid=e4f9c370b562664b276ba926964e62cc87d0ae5f1f08bd0c6f427dc5ZLLLZaruvLZLnLZXnXnnTLnrXHsZnZLZoruvLZLnLZXvZfEATHZXomqrgXinfHuqoAqFvnCXLXGHUsZnZLZoBVLZLnLZeeeLRtrrZLcWifpLZnZLZavrlZLnLZrfdwGEzAHRXNdWfeWrXNLZnZLZBUjLZLnLZrXuqEsrmSpfifpLZLN
		# https://vidstream.top/v/KcLxaW7twB/?vclid=58888a3c0b432423a217819ac7b6b5ebdc5fe250434aec29a2321f5bSVVVXrSGTVXViVXtTXpagMmXtruoSHtOipmGorgoDTijtVtEmQeXiXVXWSGTVXViVXtitiiMViStmeXiXVXWTSCXViVXSpAvEawgmBtLAzpszStLVXiXVXrPYVXViVXsssVBNSSXVRzOpfVXiXVXPQcVXViVXStGoaeSuxfpOpfVXVL
		if '__watch' in url: url3 = url3.replace('/f/','/v/')
		PHPSID = url2.split('?PHPSID=')[1]
		headers = { 'User-Agent':headers['User-Agent'] , 'Cookie':'PHPSID='+PHPSID }
		response = openURL_requests_cached(SHORT_CACHE,'GET',url3,'',headers,False,'','EGYBEST-PLAY-3rd')
		html = response.text
		#xbmc.log(html)
		#html = openURL_cached(SHORT_CACHE,url3,'',headers,'','RESOLVERS-EGYBEST-3rd')
		if '/f/' in url3: items = re.findall('<h2>.*?href="(.*?)"',html,re.DOTALL)
		elif '/v/' in url3: items = re.findall('id="video".*?src="(.*?)"',html,re.DOTALL)
		if items: return [],[''],[ items[0] ]
		elif '<h1>404</h1>' in html:
			return 'سيرفر الفيديو فيه حجب ضد كودي ومصدره من الانترنيت الخاصة بك',[],[]
	else: return 'Error: Resolver EGYBEST Failed',[],[]
	#xbmc.log(html)

def SERIES4WATCH(link):
	# https://series4watch.net/?postid=147043&serverid=5
	parts = re.findall('postid=(.*?)&serverid=(.*?)&&',link+'&&',re.DOTALL|re.IGNORECASE)
	postid,serverid = parts[0]
	url = 'https://series4watch.net/ajaxCenter?_action=getserver&_post_id='+postid+'&serverid='+serverid
	headers = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
	url2 = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-SERIES4WATCH-1st')
	#xbmcgui.Dialog().ok(url,url2)
	#errormsg,titleLIST,linkLIST = EXTERNAL_RESOLVERS(url2)
	#return errormsg,titleLIST,linkLIST
	return 'NEED_EXTERNAL_RESOLVERS',[''],[url2]

def ARABLIONZ(link):
	# http://arablionz.tv/?postid=159485&serverid=0
	if 'postid' in link:
		parts = re.findall('postid=(.*?)&serverid=(.*?)&&',link+'&&',re.DOTALL|re.IGNORECASE)
		postid,serverid = parts[0]
		url = 'https://arblionz.tv/ajaxCenter?_action=getserver&_post_id='+postid+'&serverid='+serverid
		headers = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
		url2 = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-ARABLIONZ-1st')
		url2 = url2.replace('\n','').replace('\r','')
		#xbmcgui.Dialog().ok(url,url2)
		#errormsg,titleLIST,linkLIST = EXTERNAL_RESOLVERS(url2)
		#return errormsg,titleLIST,linkLIST
		return 'NEED_EXTERNAL_RESOLVERS',[''],[url2]
	elif '/redirect/' in link:
		counts = 0
		while '/redirect/' in link and counts<5:
			response = openURL_requests_cached(LONG_CACHE,'GET',link,'','',False,'','RESOLVERS-ARABLIONZ-2nd')
			if 'Location' in response.headers.keys():
				link = response.headers['Location']
			counts += 1
		return '',[''],[link]
	else: return 'Error: Resolver ARABLIONZ Failed',[],[]

def ARABSEED(url):
	#xbmcgui.Dialog().ok(url,url)
	if '.mp4.html' in url:
		errormsg,titleLIST,linkLIST = XFILESHARING(url)
		return errormsg,titleLIST,linkLIST
	else:
		html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-ARABLIONZ-1st')
		links = re.findall('<source src="(.*?)"',html,re.DOTALL)
		if links: return '',[''],[ links[0] ]
		return 'Error: Resolver ARABSEED Failed',[],[]

def SHAHID4U(link):
	# https://shahid4u.net/?postid=142302&serverid=4
	parts = re.findall('postid=(.*?)&serverid=(.*?)&&',link+'&&',re.DOTALL|re.IGNORECASE)
	postid,serverid = parts[0]
	url = 'https://on.shahid4u.net/ajaxCenter?_action=getserver&_post_id='+postid+'&serverid='+serverid
	headers = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
	url2 = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-SHAHID4U-1st')
	return 'NEED_EXTERNAL_RESOLVERS',[''],[url2]

def AKOAM(url,named):
	#xbmcgui.Dialog().ok(url,named)
	# http://go.akoam.net/5cf68c23e6e79
	response = openURL_requests_cached(REGULAR_CACHE,'GET',url,'','',True,'','RESOLVERS-AKOAM-1st')
	html = response.text
	cookies = response.cookies.get_dict()
	cookie = cookies['golink']
	cookie = unquote(escapeUNICODE(cookie))
	items = re.findall('route":"(.*?)"',cookie,re.DOTALL)
	url2 = items[0].replace('\/','/')
	url2 = escapeUNICODE(url2)
	if 'catch.is' in url2:
		id = url2.split('%2F')[-1]
		url2 = 'http://catch.is/'+id
		return 'NEED_EXTERNAL_RESOLVERS',[''],[url2]
	else:
		website = WEBSITES['AKOAM'][0]
		response = openURL_requests_cached(REGULAR_CACHE,'GET',website,'','',True,'','RESOLVERS-AKOAM-2nd')
		relocateURL = response.url
		#relocateURL = response.headers['Location']
		#xbmcgui.Dialog().ok(response.url,website)
		serverOLD = url2.split('/')[2]
		serverNEW = relocateURL.split('/')[2]
		url3 = url2.replace(serverOLD,serverNEW.encode('utf8'))
		headers = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' , 'Referer':url3 }
		response = openURL_requests_cached(SHORT_CACHE,'POST', url3, '', headers, False,'','RESOLVERS-AKOAM-3rd')
		html = response.text
		#xbmc.log(str(url3), level=xbmc.LOGERROR)
		items = re.findall('direct_link":"(.*?)"',html,re.DOTALL|re.IGNORECASE)
		if not items:
			items = re.findall('<iframe.*?src="(.*?)"',html,re.DOTALL|re.IGNORECASE)
			if not items:
				items = re.findall('<embed.*?src="(.*?)"',html,re.DOTALL|re.IGNORECASE)
		#xbmcgui.Dialog().ok(str(items),html)
		if items:
			link = items[0].replace('\/','/')
			link = link.rstrip('/')
			if 'http' not in link: link = 'http:' + link
			if named=='': errormsg,titleLIST,linkLIST = '',[''],[link]
			else: errormsg,titleLIST,linkLIST = 'NEED_EXTERNAL_RESOLVERS',[''],[link]
		else: errormsg,titleLIST,linkLIST = 'Error: Resolver AKOAM Failed',[],[]
		#xbmcgui.Dialog().ok(linkLIST[0],errormsg)
		return errormsg,titleLIST,linkLIST

def RAPIDVIDEO(url):
	# https://www.rapidvideo.com/e/FZSQ3R0XHZ
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-RAPIDVIDEO-1st')
	#xbmcgui.Dialog().ok(url,html)
	items = re.findall('<source src="(.*?)".*?label="(.*?)"',html,re.DOTALL)
	titleLIST,linkLIST,errno = [],[],''
	if items:
		for link,label in items:
			titleLIST.append(label)
			linkLIST.append(link)
	if len(linkLIST)==0: return 'Error: Resolver RAPIDVIDEO Failed',[],[]
	else: return '',titleLIST,linkLIST

def UQLOAD(url):
	# https://uqload.com/embed-iaj1zudyf89v.html
	url = url.replace('embed-','')
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-UQLOAD-1st')
	items = re.findall('sources: \["(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(url,items[0])
	if items:
		url = items[0]+'|Referer='+url
		return '',[''],[url]
	else: return 'Error: Resolver UQLOAD Failed',[],[]

def VCSTREAM(url):
	# https://vcstream.to/embed/5c83f14297d62
	url = url.strip('/')
	if '/embed/' in url: id = url.split('/')[4]
	else: id = url.split('/')[-1]
	url = 'https://vcstream.to/player?fid=' + id
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VCSTREAM-1st')
	html = html.replace('\\','')
	#xbmcgui.Dialog().ok(url,html)
	items = re.findall('file":"(.*?)"',html,re.DOTALL)
	if items: return '',[''],[ items[0] ]
	else: return 'Error: Resolver VCSTREAM Failed',[],[]

def VIDOZA(url):
	# https://vidoza.net/embed-pkqq5ljvckb7.html
	url = url.replace('embed-','')
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-VIDOZA-1st')
	items = re.findall('src: "(.*?)".*?label:"(.*?)", res:"(.*?)"',html,re.DOTALL)
	titleLIST,linkLIST = [],[]
	for link,label,res in items:
		titleLIST.append(label+' '+res)
		linkLIST.append(link)
	if len(linkLIST)==0: return 'Error: Resolver VIDOZA Failed',[],[]
	else: return '',titleLIST,linkLIST

def WATCHVIDEO(url):
	# https://watchvideo.us/embed-rpvwb9ns8i73.html
	url = url.replace('embed-','')
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-WATCHVIDEO-1st')
	items = re.findall("download_video\('(.*?)','(.*?)','(.*?)'\)\">(.*?)</a>.*?<td>(.*?),.*?</td>",html,re.DOTALL)
	items = set(items)
	titleLIST,linkLIST = [],[]
	for id,mode,hash,label,res in items:
		url = 'https://watchvideo.us/dl?op=download_orig&id='+id+'&mode='+mode+'&hash='+hash
		html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-WATCHVIDEO-2nd')
		items = re.findall('direct link.*?href="(.*?)"',html,re.DOTALL)
		for link in items:
			titleLIST.append(label+' '+res)
			linkLIST.append(link)
	if len(linkLIST)==0: return 'Error: Resolver WATCHVIDEO Failed',[],[]
	else: return '',titleLIST,linkLIST

def UPBOM(url):
	# http://upbom.live/hm9opje7okqm/TGQSDA001.The.Vanishing.2018.1080p.WEB-DL.Cima4U.mp4.html
	url = url.replace('upbom.live','uppom.live')
	url = url.split('/')
	id = url[3]
	url = '/'.join(url[0:4])
	headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { 'id' : id  , 'op' : 'download2' , 'method_free':'Free+Download+%3E%3E' }
	data = urllib.urlencode(payload)
	html = openURL_cached(SHORT_CACHE,url,data,headers,'','RESOLVERS-UPBOM-1st')
	#xbmcgui.Dialog().ok(url,html)
	#xbmc.log(html)
	items = re.findall('direct_link.*?href="(.*?)"',html,re.DOTALL)
	if items: return '',[''],[ items[0] ]
	else: return 'Error: Resolver UPBOM Failed',[],[]

def LIIVIDEO(url):
	# https://www.liivideo.com/012ocyw9li6g.html
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-LIIVIDEO-1st')
	items = re.findall('sources:.*?"(.*?)","(.*?)"',html,re.DOTALL)
	titleLIST,linkLIST = [],[]
	if items:
		titleLIST.append('mp4')
		linkLIST.append(items[0][1])
		titleLIST.append('m3u8')
		linkLIST.append(items[0][0])
		return '',titleLIST,linkLIST
	else: return 'Error: Resolver LIIVIDEO Failed',[],[]

def UPTO(url):
	#xbmcgui.Dialog().ok(url,'')
	errormsg1,titleLIST1,linkLIST1 = '',[],[]
	errormsg2,titleLIST2,linkLIST2 = '',[],[]
	titleLIST = ['uptostream','uptobox (delay 30sec)','both']
	selection = xbmcgui.Dialog().select('اختر السيرفر:', titleLIST)
	if selection == -1: return 'Error: UPTO Resolver failed',[],[]
	elif selection==0 or selection==2:
		url2 = url.replace('://uptobox.','://uptostream.')
		errormsg1,titleLIST1,linkLIST1 = UPTOSTREAM(url2)
	elif selection==1 or selection==2:
		url2 = url.replace('://uptostream','://uptobox.')
		errormsg2,titleLIST2,linkLIST2 = UPTOBOX(url2)
	errormsg = errormsg1+'\n'+errormsg2
	titleLIST = titleLIST1 + titleLIST2
	linkLIST = linkLIST1 + linkLIST2
	errormsg = errormsg.strip('\n')
	if len(linkLIST)==0: return 'Error: Resolver UPTO Failed',[],[]
	else: return errormsg,titleLIST,linkLIST

def UPTOSTREAM(url):
	#xbmcgui.Dialog().ok(url,'')
	headers = { 'User-Agent' : '' }
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','RESOLVERS-UPTOSTREAM-1st')
	items = re.findall('src":"(.*?)".*?label":"(.*?)"',html,re.DOTALL)
	titleLIST,linkLIST = [],[]
	if items:
		for link,title in items:
			link = link.replace('\/','/')
			titleLIST.append(title)
			linkLIST.append(link)
		return '',titleLIST,linkLIST
	else: return 'Error: Resolver UPTOSTREAM Failed',[],[]

def UPTOBOX(url):
	#xbmcgui.Dialog().ok(url,'')
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-UPTOBOX-1st')
	titleLIST,linkLIST = [],[]
	if 'waitingToken' in html:
		token = re.findall('waitingToken\' value=\'(.*?)\'',html,re.DOTALL)
		token = token[0]
		headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
		payload = { 'waitingToken' : token }
		data = urllib.urlencode(payload)
		progress = xbmcgui.DialogProgress()
		progress.create('Waiting 35 seconds ...')
		for i in range(0,35):
			progress.update(i*100/35,str(35-i)+' seconds left')
			xbmc.sleep(1000)
			if progress.iscanceled(): break
		progress.close()
		html = openURL_cached(SHORT_CACHE,url,data,headers,'','RESOLVERS-UPTOBOX-2nd')
	items = re.findall('class=\'file-title\'>(.*?)<.*?comparison-table.*?href="(.*?)"',html,re.DOTALL)
	if items:
		title,url = items[0]
		return '',[title],[url]
	else: return 'Error: Resolver UPTOBOX Failed',[],[]
	#xbmcgui.Dialog().ok(str(html),html)
	#file = open('S:\emad3.html', 'w')
	#file.write(token)
	#file.write('\n\n\n')
	#file.write(html)
	#file.close()

def YOUTUBE(url):
	# subtitles example		url = 'https://www.youtube.com/watch?v=eDlZ5vANQUg'
	# mpddash .mpd example		url = 'https://www.youtube.com/watch?v=XvmSNAyeyFI'
	# hls ts .m3u8 example			url = 'https://www.youtube.com/watch?v=Gf2-NStSsNw'
	# signature example		url = 'https://www.youtube.com/watch?v=e_S9VvJM1PI'
	# url = 'https://youtu.be/eDlZ5vANQUg'
	# url = 'http://y2u.be/eDlZ5vANQUg'
	# url = 'https://www.youtube.com/embed/eDlZ5vANQUg'
	# youtube unofficial details   https://tyrrrz.me/Blog/Reverse-engineering-YouTube
	"""
	youtubeID = url.split('/watch?v=')[-1]
	#xbmcgui.Dialog().ok(url,youtubeID)
	#id = url.split('/')[-1]
	#youtubeID = id.split('?')[0]
	url = 'plugin://plugin.video.youtube/play/?video_id='+youtubeID
	return '',[''],[url]
	"""
	id = url.split('/')[-1]
	id = id.replace('watch?v=','')
	if 'embed' in url: url = WEBSITES['YOUTUBE'][0]+'/watch?v='+id
	#html = openURL_cached(SHORT_CACHE,'http://localhost:55055/shutdown','','','','RESOLVERS-YOUTUBE-1st')
	subtitleURL,dashURL,hlsURL,finalURL = '','','',''
	#headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-YOUTUBE-2nd')
	#xbmc.log('===========================================',level=xbmc.LOGNOTICE)
	html = html.replace('\\u0026','&&').replace('\\','')
	#xbmc.log(html,level=xbmc.LOGNOTICE)
	#xbmcgui.Dialog().ok(str(message),html)
	#xbmc.log('===========================================',level=xbmc.LOGNOTICE)
	#xbmc.log(html,level=xbmc.LOGNOTICE)
	html_blocks = re.findall('playerCaptionsTracklistRenderer(.*?)defaultAudioTrackIndex',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0].replace('u0026','&&')
		items = re.findall('{"languageCode":"(.*?)".*?simpleText":"(.*?)"',block,re.DOTALL)
		titleLIST,linkLIST = ['بدون اضافة الترجمة الاضافية'],['']
		for lang,title in items:
			titleLIST.append(title)
			linkLIST.append(lang)
		selection = xbmcgui.Dialog().select('اختر الترجمة المناسبة:', titleLIST)
		if selection not in [0,-1]:
			subtitleURL = re.findall('baseUrl":"(.*?)"',block,re.DOTALL)
			subtitleURL = subtitleURL[0]+'&fmt=vtt&type=track&tlang='+linkLIST[selection]
	titleLIST,linkLIST = [],[]
	html_blocks = re.findall('dashManifestUrl":"(.*?)"',html,re.DOTALL)
	if html_blocks:
		if '/signature/' in html_blocks[0]: dashURL = html_blocks[0]
		else: dashURL = html_blocks[0].replace('/s/','/signature/')
	html_blocks = re.findall('hlsManifestUrl":"(.*?)"',html,re.DOTALL)
	if html_blocks:
		hlsURL = html_blocks[0]
		#html2 = openURL_cached(SHORT_CACHE,hlsURL,'','','','RESOLVERS-YOUTUBE-3rd')
		#items = re.findall('X-MEDIA:URI="(.*?)",TYPE=SUBTITLES,GROUP-ID="vtt',html2,re.DOTALL)
		#if items: subtitleURL = items[0]#+'&fmt=vtt&type=track&tlang='
	blocks,streams_type1,fmt_size_dict = [],[],{}
	html_blocks = re.findall('url_encoded_fmt_stream_map":"(.*?)"',html,re.DOTALL)
	if html_blocks: blocks.append(html_blocks[0])
	html_blocks = re.findall('adaptive_fmts":"(.*?)"',html,re.DOTALL)
	if html_blocks: blocks.append(html_blocks[0])
	if blocks:
		html_blocks = re.findall('fmt_list":"(.*?)"',html,re.DOTALL)
		if html_blocks and html_blocks!=['']:
			fmt_list = html_blocks[0]
			fmt_itags = fmt_list.split(',')
			for item in fmt_itags:
				#xbmcgui.Dialog().ok(str(html_blocks),item)
				itag,size = item.split('/')
				fmt_size_dict[itag] = size
	#xbmcgui.Dialog().ok(str(len(blocks)),'')
	for block in blocks:
		if block=='': continue
		lines = block.split(',')
		for line in lines:
			#xbmc.log('===========================================',level=xbmc.LOGNOTICE)
			#xbmc.log(line,level=xbmc.LOGNOTICE)
			line = unquote(line)
			dict = {}
			items = line.split('&&')
			for item in items:
				key,value = item.split('=',1)
				dict[key] = value
			if 'size' not in dict.keys() and dict['itag'] in fmt_size_dict.keys():
				#xbmcgui.Dialog().ok(fmt_size_dict[dict['itag']],'')
				dict['size'] = fmt_size_dict[dict['itag']]
			streams_type1.append(dict)
	blocks,streams_type2 = [],[]
	html_blocks = re.findall('"formats":\[(.*?)\]',html,re.DOTALL)
	if html_blocks: blocks.append(html_blocks[0])
	html_blocks = re.findall('"adaptiveFormats":\[(.*?)\]',html,re.DOTALL)
	#xbmcgui.Dialog().ok(str(html_blocks),'')
	#xbmc.log(html_blocks[0], level=xbmc.LOGNOTICE)
	if html_blocks: blocks.append(html_blocks[0])
	for block in blocks:
		block = block.replace('&&','&')
		block = block.replace('="','=').replace('""','"')
		block = block.replace(':true',':True').replace(':false',':False')
		if '[' not in block: block = '['+block+']'
		block = eval(block)
		#xbmcgui.Dialog().ok(str(type(block)),'')
		#xbmc.log(str(block), level=xbmc.LOGNOTICE)
		#xbmcgui.Dialog().ok(str(block['url']),str(block['itag']))
		for dict in block:
			dict['itag'] = str(dict['itag'])
			dict['type'] = dict['mimeType'].replace('=','="')+'"'
			if 'fps' in dict.keys(): dict['fps'] = str(dict['fps'])
			if 'audioSampleRate' in dict.keys(): dict['audio_sample_rate'] = str(dict['audioSampleRate'])
			if 'audioChannels' in dict.keys(): dict['audio_channels'] = str(dict['audioChannels'])
			if 'width' in dict.keys(): dict['size'] = str(dict['width'])+'x'+str(dict['height'])
			if 'initRange' in dict.keys(): dict['init'] = dict['initRange']['start']+'-'+dict['initRange']['end']
			if 'indexRange' in dict.keys(): dict['index'] = dict['indexRange']['start']+'-'+dict['indexRange']['end']
			if 'averageBitrate' in dict.keys(): dict['bitrate'] = dict['averageBitrate']
			if 'bitrate' in dict.keys() and dict['bitrate']>111222333: del dict['bitrate']
			if 'cipher' in dict.keys():
				cipher = dict['cipher'].split('&')
				for item in cipher:
					key,value = item.split('=',1)
					dict[key] = unquote(value)
			#if 'url' in dict.keys(): dict['url'] = unquote(dict['url'])
			streams_type2.append(dict)
	url_list,streams0,streams1,streams2 = [],[],[],[]
	if streams_type1 and streams_type2:
		for dict1 in streams_type1:
			url1 = dict1['url'][:300]
			#url1 = unquote(unquote(dict1['url']))[:300]
			for dict2 in streams_type2:
				url2 = dict2['url'][:300]
				#url2 = unquote(unquote(dict2['url']))[:300]
				if url1==url2 and url1 not in url_list:
					url_list.append(url1)
					dict1.update(dict2)
					streams0.append(dict1)
	else: streams0 = streams_type1+streams_type2
	jshtml = ''
	#xbmc.log(str(streams_type1),level=xbmc.LOGNOTICE)
	#xbmc.log(str(streams_type2),level=xbmc.LOGNOTICE)
	#xbmc.log(str(streams0),level=xbmc.LOGNOTICE)
	if 'sp=sig' in html:
		#xbmcgui.Dialog().ok('cipher','')
		html_blocks = re.findall('src="(/yts/jsbin/player_.*?)"',html,re.DOTALL)
		if html_blocks:
			jsfile = WEBSITES['YOUTUBE'][0]+html_blocks[0]
			jshtml = openURL_cached(REGULAR_CACHE,jsfile,'','','','RESOLVERS-YOUTUBE-3rd')
			import youtube_signature.cipher
			import youtube_signature.json_script_engine
			cipher = youtube_signature.cipher.Cipher()
			cipher._object_cache = {}
			#xbmcgui.Dialog().ok('',jshtml)
			json_script = cipher._load_javascript(jshtml)
			json_script_cached = str(json_script)
	#xbmc.log(jsfile,level=xbmc.LOGNOTICE)
	for dict in streams0:
		url = dict['url']
		if 'signature=' in url or url.count('sig=')>1:
			streams1.append(dict)
		elif jshtml!='' and 's' in dict.keys() and 'sp' in dict.keys():
			json_script = eval(json_script_cached)
			json_script_engine = youtube_signature.json_script_engine.JsonScriptEngine(json_script)
			signature = json_script_engine.execute(dict['s'])
			if signature!=dict['s']:
				dict['url'] = url+'&'+dict['sp']+'='+signature
				streams1.append(dict)
	for dict in streams1:
		filetype,codec,quality2,type2,codecs,bitrate = 'unknown','unknown','unknown','Unknown','',0
		try:
			type0 = dict['type']
			#LOG_THIS('NOTICE',LOGGING(script_name)+'   Type:['+type0+']')
			type0 = type0.replace('+','')
			items = re.findall('(.*?)/(.*?);.*?"(.*?)"',type0,re.DOTALL)
			type2,filetype,codecs = items[0]
			codecs2 = codecs.split(',')
			codec = ''
			for item in codecs2: codec += item.split('.')[0]+','
			codec = codec.strip(',')
			if 'bitrate' in dict.keys(): bitrate = str(int(dict['bitrate'])/1024)+'kbps  '
			else: bitrate = ''
			if type2=='text': continue
			elif ',' in type0:
				type2 = 'A+V'
				quality2 = filetype+'  '+bitrate+dict['size'].split('x')[1]
			elif type2=='video':
				type2 = 'Video'
				quality2 = bitrate+dict['size'].split('x')[1]+'  '+dict['fps']+'fps'+'  '+filetype
			elif type2=='audio':
				type2 = 'Audio'
				quality2 = bitrate+str(int(dict['audio_sample_rate'])/1000)+'khz  '+dict['audio_channels']+'ch'+'  '+filetype
		except:
			errortrace = traceback.format_exc()
			sys.stderr.write(errortrace)
			#pass
		if 'dur=' in dict['url']: duration = round(0.5+float(dict['url'].split('dur=',1)[1].split('&',1)[0]))
		elif 'approxDurationMs' in dict.keys(): duration = round(0.5+float(dict['approxDurationMs'])/1000)
		else: duration = '0'
		if 'bitrate' not in dict.keys(): bitrate = int(dict['size'].split('x')[1])
		else: bitrate = int(dict['bitrate'])
		if 'init' not in dict.keys(): dict['init'] = '0-0'
		dict['title'] = type2+':  '+quality2+'  ('+codec+','+dict['itag']+')'
		dict['quality'] = quality2.split(' ')[0].split('kbps')[0]
		dict['type2'] = type2
		dict['filetype'] = filetype
		dict['codecs'] = codecs
		dict['duration'] = duration
		dict['bitrate'] = bitrate
		streams2.append(dict)
	videoTitleLIST,audioTitleLIST,muxedTitleLIST,mpdaudioTitleLIST,mpdvideoTitleLIST = [],[],[],[],[]
	videoDictLIST,audioDictLIST,muxedDictLIST,mpdaudioDictLIST,mpdvideoDictLIST = [],[],[],[],[]
	if dashURL!='':
		dict = {}
		dict['type2'] = 'A+V'
		dict['filetype'] = 'mpd'
		dict['title'] = dict['type2']+':  '+dict['filetype']+'  '+'دقة اوتوماتيكية'
		dict['url'] = dashURL
		dict['quality'] = '0' # for single dashURL any number will produce same sort order
		dict['bitrate'] = 20
		streams2.append(dict)
	if hlsURL!='':
		titleLISTtemp,linkLISTtemp = EXTRACT_M3U8(hlsURL)
		zippedLIST = zip(titleLISTtemp,linkLISTtemp)
		for title,link in zippedLIST:
			dict = {}
			dict['type2'] = 'A+V'
			dict['filetype'] = 'm3u8'
			dict['url'] = link
			#if 'BW: ' in title: dict['bitrate'] = title.split(' ')[1].split('kbps')[0]
			#if 'Res: ' in title: dict['quality'] = title.split('Res: ')[1]
			if 'kbps' in title: dict['bitrate'] = title.split('kbps')[0].rsplit(' ')[-1]
			else: dict['bitrate'] = 10
			quality = title.rsplit(' ')[-1]
			if quality.isdigit(): dict['quality'] = quality
			else: dict['quality'] = '0000'
			if title=='-1': dict['title'] = dict['type2']+':  '+dict['filetype']+'  '+'دقة اوتوماتيكية'
			else: dict['title'] = dict['type2']+':  '+dict['filetype']+'  '+dict['bitrate']+'kbps  '+dict['quality']
			streams2.append(dict)
	streams2 = sorted(streams2, reverse=True, key=lambda key: int(key['bitrate']))
	if not streams2:
		message = re.findall('class="message">(.*?)<',html,re.DOTALL)
		if 'Content Warning' in html:
			xbmcgui.Dialog().ok('رسالة من الموقع','تحذير بشأن المحتوى','ربما يكون هذا الفيديو غير ملائم لبعض المستخدمين')
			return 'Error: Resolver YOUTUBE Failed: '+'تحذير بشأن المحتوى',[],[]
		elif message:
			# 'The uploader has not made this video available in your country.'
			# 'This video is unavailable.'
			message = message[0].replace('\n','').strip(' ')
			xbmcgui.Dialog().ok('رسالة من الموقع',message)
			return 'Error: Resolver YOUTUBE Failed: '+message,[],[]
		else: return 'Error: Resolver YOUTUBE Failed',[],[]
	allStreams,highestStreams,firstLIST = [],[],[]
	for dict in streams2:
		#xbmcgui.Dialog().ok(dict['codecs'],'')
		if dict['type2']=='Video':
			videoTitleLIST.append(dict['title'])
			videoDictLIST.append(dict)
		elif dict['type2']=='Audio':
			audioTitleLIST.append(dict['title'])
			audioDictLIST.append(dict)
		elif dict['filetype']=='mpd':
			title = dict['title'].replace('A+V:  ','')
			if 'bitrate' not in dict.keys(): bitrate = 0
			else: bitrate = dict['bitrate']
			allStreams.append([dict,{},title,bitrate])
		else:
			title = dict['title'].replace('A+V:  ','')
			if 'bitrate' not in dict.keys(): bitrate = 0
			else: bitrate = dict['bitrate']
			allStreams.append([dict,{},title,bitrate])
			muxedTitleLIST.append(title)
			muxedDictLIST.append(dict)
		allowMPD = True
		if 'codecs' in dict.keys():
			if 'av0' in dict['codecs']: allowMPD = False
			elif kodi_version<18:
				if 'avc' not in dict['codecs'] and 'mp4a' not in dict['codecs']: allowMPD = False
		if dict['type2']=='Video' and dict['init']!='0-0' and allowMPD==True:
			mpdvideoTitleLIST.append(dict['title'])
			mpdvideoDictLIST.append(dict)
		elif dict['type2']=='Audio' and dict['init']!='0-0' and allowMPD==True:
			mpdaudioTitleLIST.append(dict['title'])
			mpdaudioDictLIST.append(dict)
	for audiodict in mpdaudioDictLIST:
		audioBitrate = audiodict['bitrate']
		for videodict in mpdvideoDictLIST:
			videoBitrate = videodict['bitrate']
			bitrate = videoBitrate+audioBitrate
			title = videodict['title'].replace('Video:  ','mpd  ')
			title = title.replace(videodict['filetype']+'  ','')
			title = title.replace(str(int(videoBitrate/1024))+'kbps',str(int(bitrate/1024))+'kbps')
			title = title+'('+audiodict['title'].split('(',1)[1]
			allStreams.append([videodict,audiodict,title,bitrate])
	allStreams = sorted(allStreams, reverse=True, key=lambda key: int(key[3]))
	for videodict,audiodict,title,bitrate in allStreams:
		typeAV = videodict['filetype']
		if 'filetype' in audiodict.keys():
			typeAV = 'mpd'
			#typeAV = typeAV+audiodict['filetype']
		if typeAV not in firstLIST:
			firstLIST.append(typeAV)
			highestStreams.append([videodict,audiodict,title,bitrate])
	#highestStreams = sorted(highestStreams, reverse=True, key=lambda key: int(key[3]))
	selectMenu,choiceMenu,shift = [],[],0
	#if dashURL!='':
	#	selectMenu.append('mpd صورة وصوت دقة اوتوماتيكية') ; choiceMenu.append('dash')
	#	shift = 1
	for videodict,audiodict,title,bitrate in highestStreams:
		selectMenu.append(title) ; choiceMenu.append('highest')
	if allStreams: selectMenu.append('صورة وصوت جميع المتوفر') ; choiceMenu.append('all')
	if muxedTitleLIST: selectMenu.append('صورة وصوت محدودة الدقة') ; choiceMenu.append('muxed')
	if mpdvideoTitleLIST: selectMenu.append('mpd انت تختار دقة الصورة ودقة الصوت') ; choiceMenu.append('mpd')
	if videoTitleLIST: selectMenu.append('صورة فقط بدون صوت') ; choiceMenu.append('video')
	if audioTitleLIST: selectMenu.append('صوت فقط بدون صورة') ; choiceMenu.append('audio')
	need_mpd_server = False
	while True:
		selection = xbmcgui.Dialog().select('اختر النوع المناسب:', selectMenu)
		if selection==-1: return 'تم الغاء تشغيل الفيديو',[],[]
		choice = choiceMenu[selection]
		logTitle = selectMenu[selection]
		if choice=='dash':
			finalURL = dashURL
			break
		elif choice in ['audio','video','muxed']:
			if choice=='muxed': titleLIST,dictLIST = muxedTitleLIST,muxedDictLIST
			elif choice=='video': titleLIST,dictLIST = videoTitleLIST,videoDictLIST
			elif choice=='audio': titleLIST,dictLIST = audioTitleLIST,audioDictLIST
			selection = xbmcgui.Dialog().select('اختر الملف المناسب:', titleLIST)
			if selection!=-1:
				finalURL = dictLIST[selection]['url']
				logTitle = titleLIST[selection]
				break
		elif choice=='mpd':
			selection = xbmcgui.Dialog().select('اختر دقة الصورة المناسبة:', mpdvideoTitleLIST)
			if selection!=-1:
				logTitle = mpdvideoTitleLIST[selection]
				videoDICT = videoDictLIST[selection]
				selection = xbmcgui.Dialog().select('اختر دقة الصوت المناسبة:', mpdaudioTitleLIST)
				if selection!=-1:
					logTitle += ' + '+mpdaudioTitleLIST[selection]
					audioDICT = audioDictLIST[selection]
					need_mpd_server = True
					break
		elif choice=='all':
			allVideo,allAudio,allTitle,allBitrate = zip(*allStreams)
			selection = xbmcgui.Dialog().select('اختر الملف المناسب:', allTitle)
			if selection!=-1:
				logTitle = allTitle[selection]
				videoDICT = allVideo[selection]
				if 'mpd' in allTitle[selection] and videoDICT['url']!=dashURL:
					audioDICT = allAudio[selection]
					need_mpd_server = True
				else: finalURL = videoDICT['url']
				break
		elif choice=='highest':
			allVideo,allAudio,allTitle,allBitrate = zip(*highestStreams)
			videoDICT = allVideo[selection-shift]
			if 'mpd' in allTitle[selection-shift] and videoDICT['url']!=dashURL:
				audioDICT = allAudio[selection-shift]
				need_mpd_server = True
			else: finalURL = videoDICT['url']
			logTitle = allTitle[selection-shift]
			break
	if not need_mpd_server: logURL = finalURL
	else: logURL = 'Video: '+videoDICT['url']+' + Audio: '+audioDICT['url']
	#xbmcgui.Dialog().ok(logURL,logTitle)
	#LOG_THIS('NOTICE',LOGGING(script_name)+'   Playing Selected   File: [ '+logTitle+' ]   URL: [ '+logURL+' ]')
	if need_mpd_server:
		#xbmc.log(videoDICT['url'],level=xbmc.LOGNOTICE)
		#xbmc.log(audioDICT['url'],level=xbmc.LOGNOTICE)
		videoDuration = int(videoDICT['duration'])
		audioDuration = int(audioDICT['duration'])
		if videoDuration>audioDuration: duration = str(videoDuration)
		else: duration = str(audioDuration)
		#duration = str(videoDuration) if videoDuration>audioDuration else str(audioDuration)
		mpd = '<?xml version="1.0" encoding="UTF-8"?>\n'
		mpd += '<MPD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:mpeg:dash:schema:mpd:2011" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="urn:mpeg:dash:schema:mpd:2011 http://standards.iso.org/ittf/PubliclyAvailableStandards/MPEG-DASH_schema_files/DASH-MPD.xsd" minBufferTime="PT1.5S" mediaPresentationDuration="PT'+duration+'S" type="static" profiles="urn:mpeg:dash:profile:isoff-main:2011">\n'
		mpd += '<Period>\n'
		mpd += '<AdaptationSet id="0" mimeType="video/'+videoDICT['filetype']+'" subsegmentAlignment="true">\n'# subsegmentStartsWithSAP="1" bitstreamSwitching="true" default="true">\n'
		mpd += '<Role schemeIdUri="urn:mpeg:DASH:role:2011" value="main"/>\n'
		mpd += '<Representation id="'+videoDICT['itag']+'" codecs="'+videoDICT['codecs']+'" startWithSAP="1" bandwidth="'+str(videoDICT['bitrate'])+'" width="'+videoDICT['size'].split('x')[0]+'" height="'+videoDICT['size'].split('x')[1]+'" frameRate="'+videoDICT['fps']+'">\n'
		mpd += '<BaseURL>'+videoDICT['url'].replace('&','&amp;')+'</BaseURL>\n'
		mpd += '<SegmentBase indexRange="'+videoDICT['index']+'">\n'# indexRangeExact="true">\n'
		mpd += '<Initialization range="'+videoDICT['init']+'" />\n'
		mpd += '</SegmentBase>\n'
		mpd += '</Representation>\n'
		mpd += '</AdaptationSet>\n'
		mpd += '<AdaptationSet id="1" mimeType="audio/'+audioDICT['filetype']+'" subsegmentAlignment="true">\n'# subsegmentStartsWithSAP="1" bitstreamSwitching="true" default="true">\n'
		mpd += '<Role schemeIdUri="urn:mpeg:DASH:role:2011" value="main"/>\n'
		mpd += '<Representation id="'+audioDICT['itag']+'" codecs="'+audioDICT['codecs']+'" bandwidth="130475">\n'
		mpd += '<AudioChannelConfiguration schemeIdUri="urn:mpeg:dash:23003:3:audio_channel_configuration:2011" value="'+audioDICT['audio_channels']+'"/>\n'
		mpd += '<BaseURL>'+audioDICT['url'].replace('&','&amp;')+'</BaseURL>\n'
		mpd += '<SegmentBase indexRange="'+audioDICT['index']+'">\n'# indexRangeExact="true">\n'
		mpd += '<Initialization range="'+audioDICT['init']+'" />\n'
		mpd += '</SegmentBase>\n'
		mpd += '</Representation>\n'
		mpd += '</AdaptationSet>\n'
		mpd += '</Period>\n'
		mpd += '</MPD>\n'
		#xbmc.log(mpd,level=xbmc.LOGNOTICE)
		"""
		mpdfolder = os.path.join(xbmc.translatePath('special://temp'),addon_id)
		if not os.path.exists(mpdfolder):
			#xbmcgui.Dialog().ok('folder does not exsit','')
			import xbmcvfs
			xbmcvfs.mkdir(mpdfolder)
		mpdfile = os.path.join(mpdfolder,id+'.mpd')
		#xbmcgui.Dialog().ok(mpdfile,mpd)
		#with open(mpdfile,'w') as file: file.write(mpd)
		#mpdfile = 'http://localhost:55055/'+id+'.mpd'
		"""
		import BaseHTTPServer
		class HTTP_SERVER(BaseHTTPServer.HTTPServer):
			#mpd = 'mpd = used when not using __init__'
			def __init__(self,port='55055',mpd='mpd = from __init__'):
				BaseHTTPServer.HTTPServer.__init__(self,('localhost',port), HTTP_HANDLER)
				self.port = port
				self.mpd = mpd
				#print('server is up now listening on port: '+str(port))
			def start(self):
				self.threads = CustomThread(False)
				self.threads.start_new_thread(1,self.serve)
			def serve(self):
				#print('serving requests started')
				self.keeprunning = True
				#counter = 0
				while self.keeprunning:
					#counter += 1
					#print('running a single handle_request() now: '+str(counter)+'')
					#settimeout does not work due to error message if it kills an http request
					#self.socket.settimeout(10) # default is 60 seconds (it will serve one request within 60 seconds)
					self.handle_request()
				#print('serving requests stopped\n')
			def stop(self):
				self.keeprunning = False
				self.send_dummy_http()	# needed to force self.handle_request() to serve its last request
			def shutdown(self):
				self.stop()
				self.socket.close()
				self.server_close()
				time.sleep(1)
				#print('server is down now\n')
			def load(self,mpd):
				self.mpd = mpd
			def send_dummy_http(self):
				conn = httplib.HTTPConnection('localhost:'+str(self.port))
				conn.request("HEAD", "/")
		class HTTP_HANDLER(BaseHTTPServer.BaseHTTPRequestHandler):
			def do_GET(self):
				#print('doing GET  '+self.path)
				self.send_response(200)
				self.send_header('Content-type', 'text/plain')
				self.end_headers()
				#self.wfile.write(self.path+'\n')
				self.wfile.write(self.server.mpd)
				if self.path=='/shutdown': self.server.shutdown()
			def do_HEAD(s):
				#print('doing HEAD  '+self.path)
				s.send_response(200)
				s.end_headers()
		httpd = HTTP_SERVER(55055,mpd)
		#httpd.load(mpd)
		httpd.start()
		# http://localhost:55055/shutdown
		finalURL = 'http://localhost:55055/youtube.mpd'
	else: httpd = ''
	if finalURL!='': return '',[''],[ [finalURL,subtitleURL,httpd] ]
	else: return 'Error: Resolver YOUTUBE Failed',[],[]

def VIDBOB(url):
	# https://vidbob.com/v6rnlgmrwgqu
	headers = { 'User-Agent' : '' }
	#url = url.replace('http:','https:')
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VIDBOB-1st')
	items = re.findall('file:"(.*?)"(,label:"(.*?)"|)\}',html,re.DOTALL)
	items = set(items)
	items = sorted(items, reverse=True, key=lambda key: key[2])
	titleLISTtemp,titleLIST,linkLISTtemp,linkLIST = [],[],[],[]
	if items:
		for link,dummy,label in items:
			link = link.replace('https:','http:')
			if '.m3u8' in link:
				titleLISTtemp,linkLISTtemp = EXTRACT_M3U8(link)
				#xbmcgui.Dialog().ok(str(linkLIST),str(linkLISTtemp))
				linkLIST = linkLIST + linkLISTtemp
				if titleLISTtemp[0]=='-1': titleLIST.append('سيرفر خاص'+'   m3u8')
				else:
					for title in titleLISTtemp:
						titleLIST.append('سيرفر خاص'+'   '+title)
			else:
				title = 'سيرفر خاص'+'   mp4   '+label
				linkLIST.append(link)
				titleLIST.append(title)
		return '',titleLIST,linkLIST
	else: return 'Error: Resolver VIDBOB Failed',[],[]

def	XFILESHARING(url):
	# https://filerio.in/dmntn4rjquns
	#xbmc.log(url)
	url = url.replace('embed-','')
	url = url.replace('.html','')
	id = url.split('/')[3]
	#xbmcgui.Dialog().ok(url,id)
	headers = { 'User-Agent':'' , 'Content-Type':'application/x-www-form-urlencoded' }
	payload = { 'id':id , 'op':'download2' }
	data = urllib.urlencode(payload)
	html = openURL_cached(SHORT_CACHE,url,data,headers,'','RESOLVERS-XFILESHARING-1st')
	#xbmcgui.Dialog().ok(url,html)
	#LOG_THIS('NOTICE','----------------------------------')
	#LOG_THIS('NOTICE',html)
	#LOG_THIS('NOTICE','----------------------------------')
	items = re.findall('direct_link.*?href="(.*?)"',html,re.DOTALL)
	if items: return '',[''],[ items[0] ]
	else: return 'Error: Resolver XFILESHARING Failed',[],[]

def GOVID(url):
	# https://govid.co/video/play/AAVENd
	headers = { 'User-Agent' : '' }
	html = openURL_cached(REGULAR_CACHE,url,'',headers,'','RESOLVERS-GOVID-1st')
	items = re.findall('source src="(.*?)"',html,re.DOTALL)
	titleLISTtemp,titleLIST,linkLIST = [],[],[],[]
	if items:
		link = items[0]
		if '.m3u8' in link:
			titleLISTtemp,linkLIST = EXTRACT_M3U8(link)
			if titleLISTtemp[0]=='-1': titleLIST.append('سيرفر خاص'+'   m3u8')
			else:
				for title in titleLISTtemp:
					titleLIST.append('سيرفر خاص'+'   '+title)
		else:
			title = 'سيرفر خاص'+'   mp4'
			titleLIST.append(title)
			linkLIST.append(link)
		return '',titleLIST,linkLIST
	else: return 'Error: Resolver GOVID Failed',[],[]
	# https://s1m.govid.co/stream/229.m3u8









#####################################################
#    NOT YET VERIFIED
#    16-06-2019
#####################################################

def ARABLOADS(url):
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-ARABLOADS-1st')
	items = re.findall('color="red">(.*?)<',html,re.DOTALL)
	if items: return '',[''],[ items[0] ]
	else: return 'Error: Resolver ARABLOADS Failed',[],[]

def TOP4TOP(url):
	return '',[''],[ url ]

def ZIPPYSHARE(url):
	#xbmcgui.Dialog().ok(url,'')
	server = url.split('/')
	basename = '/'.join(server[0:3])
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-ZIPPYSHARE-1st')
	items = re.findall('dlbutton\'\).href = "(.*?)" \+ \((.*?) \% (.*?) \+ (.*?) \% (.*?)\) \+ "(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(url,str(var))
	if items:
		var1,var2,var3,var4,var5,var6 = items[0]
		var = int(var2) % int(var3) + int(var4) % int(var5)
		url = basename + var1 + str(var) + var6
		return '',[''],[ url ]
	else: return 'Error: ZIPPYSHARE Resolver Failed',[],[]

def MP4UPLOAD(url):
	url = url.replace('embed-','')
	url = url.replace('.html','')
	id = url.split('/')[-1]
	headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { "id":id , "op":"download2" }
	request = openURL_requests_cached(SHORT_CACHE,'POST', url, payload, headers, False,'','RESOLVERS-MP4UPLOAD-1st')
	url = request.headers['Location']
	if url!='': return '',[''],[ url ]
	else: return 'Error: Resolver MP4UPLOAD Failed',[],[]

def WINTVLIVE(url):
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-WINTVLIVE-1st')
	items = re.findall('mp4: \[\'(.*?)\'',html,re.DOTALL)
	if items: return '',[''],[ items[0] ]
	else: return 'Error: Resolver WINTVLIVE Failed',[],[]

def ARCHIVE(url):
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-ARCHIVE-1st')
	items = re.findall('source src="(.*?)"',html,re.DOTALL)
	#logging.warning('https://archive.org' + items[0])
	if items:
		url = url = 'https://archive.org' + items[0]
		return '',[''],[ url ]
	else: return 'Error: Resolver ARCHIVE Failed',[],[]

def PUBLICVIDEOHOST(url):
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-PUBLICVIDEOHOST-1st')
	items = re.findall('file: "(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(str(items),html)
	if items: return '',[''],[ items[0] ]
	else: return 'Error: Resolver PUBLICVIDEOHOST Failed',[],[]

def ESTREAM(url):
	#url = url.replace('embed-','')
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-ESTREAM-1st')
	items = re.findall('video preload.*?src=.*?src="(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(items[0],items[0])
	if items: return '',[''],[ items[0] ]
	else: return 'Error: Resolver ESTREAM Failed',[],[]








#####################################################
#         FAILED
#	NOT WORKING ANYMORE
#####################################################
"""
def THEVIDEO_PROBLEM(url):
	# https://thevideo.me/embed-xldtqj5deiyj-780x439.html
	url = url.replace('embed-','')
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-THEVIDEO-1st')
	items = re.findall('direct link" value="(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(str(items),html)
	if items:
		link = items[0].rstrip('/')
		title,url = VEVIO(link)
		return title,url
	else: return ['Error: ESTREAM Resolver failed'],[]

def HELAL_PROBLEM(url):
	# https://playr.4helal.tv/4qlqt9d3813e
	headers = { 'User-Agent' : '' }
	#url = url.replace('http:','https:')
	html = openURL_cached(NO_CACHE,url,'',headers,'','RESOLVERS-VIDBOB-1st')
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	#xbmcgui.Dialog().ok(items[0].rstrip('/'),'')
	if items:
		url = items[0].replace('https:','http:')
		return [url],[url]
	else: return ['Error: ESTREAM Resolver failed'],[]

def VIMPLE_PROBLEM(link):
	id = link.split('id=')[1]
	headers = { 'User-Agent' : '' }
	url = 'http://player.vimple.ru/iframe/' + id
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VIMPLE-1st')
	items = re.findall('true,"url":"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0].replace('\/','/')
		return [url],[url]
	else: return ['Error: ESTREAM Resolver failed'],[]

def VIDSHARE_PROBLEM(url):
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VIDSHARE-1st')
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return ['Error: ESTREAM Resolver failed'],[]

def INTOUPLOAD_PROBLEM(url):
	# https://intoupload.net/w2j4lomvzopd
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-INTOUPLOAD-1st')
	html_blocks = re.findall('POST.*?(.*?)clearfix',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('op" value="(.*?)".*?id" value="(.*?)".*?rand" value="(.*?)".*?left:(.*?)px;.*?&#(.*?);.*?left:(.*?)px;.*?&#(.*?);.*?left:(.*?)px;.*?&#(.*?);.*?left:(.*?)px;.*?&#(.*?);',block,re.DOTALL)
	op,id,rand,pos1,num1,pos2,num2,pos3,num3,pos4,num4 = items
	captcha = { int(pos1):chr(int(num1)) , int(pos2):chr(int(num2)) , int(pos3):chr(int(num3)) , int(pos4):chr(int(num4)) }
	code = ''
	for char in sorted(captcha):
		code += captcha[char]
	#xbmcgui.Dialog().ok(code,str(captcha))
	headers = { 'User-Agent' : '' , 'Content-Type' : 'application/x-www-form-urlencoded' }
	payload = { 'id':id , 'op':op , 'code':code , 'rand':rand }
	data = urllib.urlencode(payload)
	progress = xbmcgui.DialogProgress()
	progress.create('Waiting 15 seconds ...')
	for i in range(0,15):
		progress.update(i*100/15,str(15-i))
		xbmc.sleep(1000)
		if progress.iscanceled(): return
	progress.close()
	html = openURL_cached(SHORT_CACHE,url,data,headers,'','RESOLVERS-INTOUPLOAD-2nd')
	items = re.findall('target_type.*?href="(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return ['Error: ESTREAM Resolver failed'],[]

def VIDBOM_PROBLEM(url):
	# https://www.vidbom.com/embed-05ycj7325jae.html
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-VIDBOM-1st')
	xbmc.sleep(1500)
	items = re.findall('file: "(.*?)"',html,re.DOTALL)
	slidesURL = items[0].rstrip('/')
	html2 = openURL_cached(SHORT_CACHE,slidesURL,'','','','RESOLVERS-VIDBOM-2nd')
	xbmc.sleep(1500)
	items = re.findall('file:"(.*?)"',html,re.DOTALL)
	if items:
		url = items[0]
		return [url],[url]
	else: return ['Error: ESTREAM Resolver failed'],[]

def GOUNLIMITED_OLD(url):
	url = url.replace('embed-','')
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-GOUNLIMITED-1st')
	items = re.findall('data(.*?)hide.*?embed(.*?)hash',html,re.DOTALL)
	id = items[0][0].replace('|','')
	hash = items[0][1].split('|')
	newhash = ''
	for i in reversed(hash):
		newhash += i + '-'
	newhash = newhash.strip('-')
	#url = 'https://gounlimited.to/dl?op=view&file_code='+id+'&hash='+newhash+'&embed=&adb=1'
	#html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-GOUNLIMITED-1st')
	url = "https://gounlimited.to/dl"
	querystring = { "op":"view","file_code":"o1yo2xwdmk0l","hash":newhash,"embed":"","adb":"1" }
	headers = {
		'accept': "*/*",
		'dnt': "1",
		'x-requested-with': "XMLHttpRequest",
		'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
		'referer': "https://gounlimited.to/o1yo2xwdmk0l.html",
		'accept-encoding': "gzip, deflate, br",
		'accept-language': "en-US,en;q=0.9,ar;q=0.8"
		}
	import requests
	html = requests.request('GET', url, headers=headers, params=querystring)
	items = re.findall('video="" src="(.*?)"',html.text,re.DOTALL)
	#xbmcgui.Dialog().ok(str(html.content),str(len(html.content)))
	if items:
		url = items[0]
		return [url],[url]
	else: return ['Error: ESTREAM Resolver failed'],[]

def VEVIO_PROBLEM(url):
	# https://vev.io/qnoxd4yqyy30
	id = url.split('/')[-1]
	url = 'https://vev.io/api/serve/video/' + id
	headers = { 'User-Agent' : '' }
	titleLIST,linkLIST = [],[]
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-VEVIO-1st')
	html_blocks = re.findall('qualities":\{(.*?)\}',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('"(.*?)":"(.*?)"',block,re.DOTALL)
		for label,link in items:
			titleLIST.append(label)
			linkLIST.append(link)
	return titleLIST,linkLIST

def GOUNLIMITED_PROBLEM(url):
	# https://gounlimited.to/embed-wqsi313vbpua.html
	# http://gounlimited.to/embed-bhczqclxokgq.html
	url = url.replace('https:','http:')
	headers = { 'User-Agent' : '' }
	html = openURL_cached(SHORT_CACHE,url,'',headers,'','RESOLVERS-GOUNLIMITED-1st')
	html_blocks = re.findall('function\(p,a,c,k,e,d\)(.*?)split',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall(",'(.*?)'",block,re.DOTALL)
		items = items[-1].split('|')
		link = items[12]+'://'+items[85]+'.'+items[11]+'.'+items[10]+'/'+items[84]+'/v.mp4'
		return [link],[link]
	else: return ['Error: ESTREAM Resolver failed'],[]
	#link = 'https://shuwaikh.gounlimited.to/'+id+'/v.mp4'
	#link = 'https://fs67.gounlimited.to/'+id+'/v.mp4'

def VIDHD_PROBLEM(url):
	# https://vidhd.net/562ghl3hr1cw.html
	html = openURL_cached(SHORT_CACHE,url,'','','','RESOLVERS-LIIVIDEO-1st')
	items = re.findall('file:"(.*?)",label:"(.*?)"',html,re.DOTALL)
	titleLIST,linkLIST = [],[]
	for link,label in items:
		titleLIST.append(label)
		linkLIST.append(link)
	html_blocks = re.findall('function\(p,a,c,k,e,d\)(.*?)split',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall(",'(.*?)'",block,re.DOTALL)
		items = items[-1].split('|')
		server = items[7]+'://'+items[19]+'.'+items[6]+'.'+items[4]
		html_blocks = re.findall('\|image(\|.*?\|)sources\|',block,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('\|(\w+)\|(\w+)',block,re.DOTALL)
			for label,id in items:
				link = server+'/'+id+'/v.mp4'
				titleLIST.append(label)
				linkLIST.append(link)
	return titleLIST,linkLIST
	#link = https://s2.vidhd.net/kmxsuzrepjumwmesrluuynfphmbrrpofmbwknihn4l6rdua3pwajpcxqvboq/v.mp4
"""


"""
def CHECK(url):
	result = 'unknown'
	if   '1fichier'		in url: result = 'known'
	elif '4helal'		in url: result = 'known'
	elif 'allmyvideos'	in url: result = 'known'
	elif 'allvid'		in url: result = 'known'
	elif 'bestcima'		in url: result = 'known'
	elif 'cloudy.ec'	in url: result = 'known'
	elif 'dailymotion'	in url: result = 'known'
	elif 'downace'		in url: result = 'known'
	#elif 'estream'		in url: result = 'known'
	elif 'filerio'		in url: result = 'known'
	elif 'firedrive'	in url: result = 'known'
	elif 'flashx'		in url: result = 'known'
	elif 'govid'		in url: result = 'known'
	elif 'hqq'			in url: result = 'known'
	elif 'media4up'		in url: result = 'known'
	#elif 'mystream'		in url: result = 'known'
	elif 'nitroflare'	in url: result = 'known'
	elif 'nowvideo'		in url: result = 'known'
	elif 'ok.ru'		in url: result = 'known'
	elif 'oload'		in url: result = 'known'
	elif 'openload'		in url: result = 'known'
	elif 'streamango'	in url: result = 'known'
	elif 'streamin'		in url: result = 'known'
	elif 'streammango'	in url: result = 'known'
	elif 'thevid.net'	in url: result = 'known'
	elif 'upload'		in url: result = 'known'
	elif 'uptobox'		in url: result = 'known'
	elif 'videobam'		in url: result = 'known'
	elif 'videorev'		in url: result = 'known'
	elif 'vidfast'		in url: result = 'known'
	elif 'vidgg'		in url: result = 'known'
	elif 'vidlox'		in url: result = 'known'
	elif 'vidzi'		in url: result = 'known'
	elif 'watchers'		in url: result = 'known'
	elif 'watchers.to'	in url: result = 'known'
	elif 'wintv.live'	in url: result = 'known'
	elif 'youwatch'		in url: result = 'known'
	elif 'vidto.me'		in url: result = 'known'
	elif 'archive'		in url: result = 'known'
	elif 'publicvideohost' in url: result = 'known'
	#elif 'vidbom'		in url: result = 'known'
	else:
		link = 'http://emadmahdi.pythonanywhere.com/check?url=' + url
		result = openURL_cached(SHORT_CACHE,link,'','','','RESOLVERS-CHECK-1st')
	return result
"""


