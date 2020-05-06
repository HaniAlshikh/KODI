# -*- coding: utf-8 -*-
from LIBRARY import *

script_name='IPTV'
menu_name='_IPT_'

def MAIN(mode,url,text):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==230: results = MAIN_MENU()
	elif mode==231: results = ADD_ACCOUNT()
	elif mode==232: results = CREATE_STREAMS()
	elif mode==233: results = GROUPS(url,text,'')
	elif mode==234: results = ITEMS(url,text)
	elif mode==235: results = PLAY(url,'LIVE')
	elif mode==236: results = PLAY(url,'VOD')
	elif mode==237: results = DELETE_ALL_OLD_FILES([],True)
	elif mode==239: results = SEARCH(text)
	else: results = False
	return results

def MAIN_MENU():
	addMenuItem('dir','  1.  [COLOR FFC89008]IPT  [/COLOR]'+'بحث في ملفات IPTV','',239)
	addMenuItem('dir','  2.  [COLOR FFC89008]IPT  [/COLOR]'+'اضافة اشتراك IPTV','',231)
	addMenuItem('dir','  3.  [COLOR FFC89008]IPT  [/COLOR]'+'جلب ملفات IPTV','',232)
	addMenuItem('dir','  4.  [COLOR FFC89008]IPT  [/COLOR]'+'مسح ملفات IPTV','',237)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addMenuItem('dir','  5.  [COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة ومرتبة','LIVE_GROUPED',233)
	addMenuItem('dir','  6.  [COLOR FFC89008]IPT  [/COLOR]'+'أفلام مصنفة ومرتبة','VOD_MOVIES',233)
	addMenuItem('dir','  7.  [COLOR FFC89008]IPT  [/COLOR]'+'مسلسلات مصنفة ومرتبة','VOD_SERIES',233)
	addMenuItem('dir','  8.  [COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مجهولة','VOD_UNKNOWN',233)
	#addMenuItem('dir',menu_name+'قنوات مجهولة','LIVE_UNKNOWN',233)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addMenuItem('dir','  9.  [COLOR FFC89008]IPT  [/COLOR]'+'قنوات مصنفة من أسمائها','LIVE_FROM_NAME',233)
	addMenuItem('dir','10.  [COLOR FFC89008]IPT  [/COLOR]'+'فيديوهات مصنفة من أسمائها','VOD_FROM_NAME',233)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addMenuItem('dir','11.  [COLOR FFC89008]IPT  [/COLOR]'+'القنوات الاصلية بدون تغيير','LIVE_ORIGINAL',233)
	addMenuItem('dir','12.  [COLOR FFC89008]IPT  [/COLOR]'+'الفيديوهات الاصلية بدون تغيير','VOD_ORIGINAL',233)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	return

def GROUPS(TYPE,GROUP,website=''):
	#LOG_THIS('NOTICE','EMAD START GROUPS')
	results = READ_FROM_SQL3([TYPE,GROUP,website],'iptv_groups')
	#LOG_THIS('NOTICE','EMAD 000')
	if results:
		for i1,i2,i3,i4,i5,i6,i7 in results:
			addMenuItem(i1,i2,i3,i4,i5,i6,i7)
		#LOG_THIS('NOTICE','EMAD 111')
		return
	else: results = []
	if website=='': show = True
	else: show = False
	if not isIPTVFiles(show): return
	#LOG_THIS('NOTICE','EMAD 222')
	streams = GET_STREAMS_FROM_SQL3(TYPE)
	#LOG_THIS('NOTICE','EMAD 333')
	groups,unique,logos = [],[],[]
	for dict in streams:
		groups.append(dict['group'])
		logos.append(dict['img'])
	z = zip(groups,logos)
	z = sorted(z, reverse=False, key=lambda key: key[0])
	name = ''
	if website!='': name = '[COLOR FFC89008]'+website+':[/COLOR]  '
	for group,img in z:
		if '____' in group: title2,group2 = group.split('____')
		else: title2,group2 = '',group
		if TYPE=='VOD_SERIES' and GROUP=='':
			title = title2
			if title in unique: continue
			unique.append(title)
			addMenuItem('dir',website+'::'+menu_name+name+title,TYPE,233,'','',group)
			results.append(('dir',website+'::'+menu_name+name+title,TYPE,233,'','',group))
		else:
			title = group2
			if title in unique: continue
			unique.append(title)
			if GROUP=='' and TYPE!='VOD_ORIGINAL': img = ''
			if title=='!!__UNKNOWN__!!': img = ''
			if TYPE!='VOD_SERIES' or GROUP=='' or title2 in GROUP:
				addMenuItem('dir',website+'::'+menu_name+name+title,TYPE,234,img,'',group)
				results.append(('dir',website+'::'+menu_name+name+title,TYPE,234,img,'',group))
	WRITE_TO_SQL3([TYPE,GROUP,website],'iptv_groups',results)
	LOG_THIS('NOTICE','EMAD FINISHED GROUPS')
	return

def ITEMS(TYPE,GROUP):
	#xbmcgui.Dialog().ok(TYPE,GROUP)
	results = READ_FROM_SQL3([TYPE,GROUP],'iptv_items')
	if results:
		for i1,i2,i3,i4,i5,i6,i7 in results:
			addMenuItem(i1,i2,i3,i4,i5,i6,i7)
		return
	else: results = []
	streams = GET_STREAMS_FROM_SQL3(TYPE)
	for dict in streams:
		group = dict['group']
		if group==GROUP:
			title = dict['title']
			url = dict['url']
			img = dict['img']
			if 'LIVE' in TYPE: addMenuItem('link',menu_name+title,url,235,img,'','IsPlayable=no')
			else:
				addMenuItem('link',menu_name+title,url,236,img,'','IsPlayable=yes')
				results.append(('link',menu_name+title,url,236,img,'','IsPlayable=yes'))
	WRITE_TO_SQL3([TYPE,GROUP],'iptv_items',results)
	return

def PLAY(url,type):
	#xbmcgui.Dialog().ok(url,'')
	if 'LIVE' in type: PLAY_VIDEO(url,script_name,'no')
	else: PLAY_VIDEO(url,script_name,'yes')
	return

def ADD_ACCOUNT():
	settings = xbmcaddon.Addon(id=addon_id)
	xbmcgui.Dialog().ok('IPTV','البرنامج يحتاج اشتراك IPTV من نوع رابط التحميل m3u من اي شركة IPTV والافضل ان يحتوي الرابط في نهايته على هذه الكلمات','&type=m3u_plus')
	iptvURL = settings.getSetting('iptv.url')
	if iptvURL!='':
		answer = xbmcgui.Dialog().yesno(iptvURL,'هذا هو رابط IPTV المسجل في البرنامج ... هل تريد تعديله أم تريد كتابة رابط جديد ؟!','','','كتابة جديد','تعديل القديم')
		if not answer: iptvURL = ''
	iptvURL = KEYBOARD('اكتب رابط IPTV كاملا',iptvURL)
	iptvURL = iptvURL.strip(' ')
	if iptvURL=='': return
	else:
		answer = xbmcgui.Dialog().yesno(iptvURL,'هل تريد استخدام هذا الرابط بدلا من الرابط القديم ؟','','','كلا','نعم')
		if not answer: return
	settings.setSetting('iptv.url',iptvURL)
	xbmcgui.Dialog().ok(iptvURL,'تم تغير رابط اشتراك IPTV الى هذا الرابط الجديد')
	CREATE_STREAMS()
	return

def SEARCH(search=''):
	if '::' in search:
		if not isIPTVFiles(False): return
		search = search.split('::')[0]
		exit = False
		TYPE = 'VOD_FROM_NAME'
	else:
		if not isIPTVFiles(True): return
		exit = True
		searchTitle = ['الكل','قنوات','فيديوهات']
		typeList = ['ALL','LIVE_FROM_NAME','VOD_FROM_NAME']
		selection = xbmcgui.Dialog().select('أختر البحث المناسب', searchTitle)
		if selection == -1: return
		TYPE = typeList[selection]
	if search=='': search = KEYBOARD()
	if search == '': return
	streams = GET_STREAMS_FROM_SQL3(TYPE)
	searchLower = search.lower()
	for dict in streams:
		title = dict['title']
		if searchLower in title.lower():
			url = dict['url']
			img = dict['img']
			if '.mp4' in url or '.mkv' in url or '.avi' in url or '.mp3' in url:
				addMenuItem('link',menu_name+title,url,236,img,'','IsPlayable=yes')
			else: addMenuItem('link',menu_name+title,url,235,img,'','IsPlayable=no')
	return

def CREATE_STREAMS():
	#LOG_THIS('NOTICE','EMAD 111')
	answer = xbmcgui.Dialog().yesno('IPTV','هل تريد أن تجلب الان ملفات IPTV جديدة ؟','','','كلا','نعم')
	if not answer: return
	settings = xbmcaddon.Addon(id=addon_id)
	iptvURL = settings.getSetting('iptv.url')
	headers = { 'User-Agent' : '' }
	try: m3u_text = openURL_cached(REGULAR_CACHE,iptvURL,'',headers,'','IPTV-CREATE_STREAMS-1st')
	except:
		xbmcgui.Dialog().ok('فشل في جلب ملفات IPTV','يجب عليك: اولا الضغط على رابط اضافة حسابك ثم ثانيا الضغط على رابط جلب الملفات')
		LOG_THIS('ERROR',LOGGING(script_name)+'   No IPTV files')
		return
	m3u_filename = 'iptv_'+str(int(now))+'_.m3u'
	iptvFile = os.path.join(addoncachefolder,m3u_filename)
	file = open(iptvFile, 'wb')
	file.write(m3u_text)
	file.close()
	m3u_text = m3u_text.replace('"tvg-','" tvg-')
	m3u_text = m3u_text.replace('َ','').replace('ً','').replace('ُ','').replace('ٌ','')
	m3u_text = m3u_text.replace('ّ','').replace('ِ','').replace('ٍ','').replace('ْ','')
	m3u_text = m3u_text.replace('group-title=','group=')
	m3u_text = m3u_text.replace('tvg-','')
	username = re.findall('username=(.*?)&',iptvURL+'&',re.DOTALL)
	password = re.findall('password=(.*?)&',iptvURL+'&',re.DOTALL)
	if username and password: 
		username = username[0]
		password = password[0]
		url_parts = iptvURL.split('/')
		server = url_parts[0]+'//'+url_parts[2]
		seriesCategoriesURL = server+'/player_api.php?username='+username+'&password='+password+'&action=get_series_categories'
		series_groups = openURL_cached(REGULAR_CACHE,seriesCategoriesURL,'',headers,'','IPTV-CREATE_STREAMS-2nd')
		series_groups = re.findall('category_name":"(.*?)"',series_groups,re.DOTALL)
		if series_groups:
			#xbmcgui.Dialog().ok('','')
			for group in series_groups:
				group = group.replace('\/','/').decode('unicode_escape').encode('utf8')
				m3u_text = m3u_text.replace('group="'+group+'"','group="__SERIES__'+group+'"')
		vodCategoriesURL = server+'/player_api.php?username='+username+'&password='+password+'&action=get_vod_categories'
		vod_groups = openURL_cached(REGULAR_CACHE,vodCategoriesURL,'',headers,'','IPTV-CREATE_STREAMS-3rd')
		vod_groups = re.findall('category_name":"(.*?)"',vod_groups,re.DOTALL)
		if vod_groups:
			for group in vod_groups:
				group = group.replace('\/','/').decode('unicode_escape').encode('utf8')
				m3u_text = m3u_text.replace('group="'+group+'"','group="__MOVIES__'+group+'"')
	#LOG_THIS('NOTICE','EMAD 222')
	lines = re.findall('#EXTINF(.*?)[\n\r]+(.*?)[\n\r]+',m3u_text+'\n',re.DOTALL)
	#LOG_THIS('NOTICE','EMAD 333')
	streams_not_sorted = []
	for line,url in lines:
		dict = {}
		dict['url'] = url
		if '",' in line:
			line,title = line.rsplit('",',1)
			line = line+'"'
		else: line,title = line.rsplit('1,',1)
		params = re.findall(' (.*?)="(.*?)"',line,re.DOTALL)
		for key,value in params:
			key = key.replace('"','').strip(' ')
			dict[key] = value.strip(' ')
		dict['org_title'] = title
		if title=='':
			if 'name' in dict.keys(): title = dict['name']
			else: title = '!!__UNKNOWN__!!'
		dict['title'] = title.strip(' ').replace('  ',' ').replace('  ',' ')
		if 'logo' in dict.keys():
			dict['img'] = dict['logo']
			del dict['logo']
		else: dict['img'] = ''
		group = ''
		if 'group' in dict.keys(): group = dict['group']
		if group=='': group = '!!__UNKNOWN__!!'
		dict['org_group'] = group
		if '.mp4' in url or '.mkv' in url or '.avi' in url or '.mp3' in url or '__SERIES__' in group or '__MOVIES__' in group:
			if '__SERIES__' in group: type = 'VOD_SERIES'
			elif '__MOVIES__' in group: type = 'VOD_MOVIES'
			else: type = 'VOD_UNKNOWN'
			group = group.replace('__SERIES__','').replace('__MOVIES__','')
		else:
			if group=='': type = 'LIVE_UNKNOWN'
			else: type = 'LIVE_GROUPED'
		dict['type'] = type
		if group=='': group = type
		if dict['type']=='VOD_SERIES':
			series_title = re.findall('(.*?) [Ss]\d+ +[Ee]\d+',dict['title'],re.DOTALL)
			group = group+'____'
			if series_title: group = group+series_title[0]
			else: group = group+'!!__UNKNOWN__!!'
		dict['group'] = group.strip(' ').replace('  ',' ').replace('  ',' ').upper()
		if 'id' in dict.keys(): del dict['id']
		if 'ID' in dict.keys(): del dict['ID']
		if 'name' in dict.keys(): del dict['name']
		if '\u' in dict['title'].lower(): dict['title'] = dict['title'].decode('unicode_escape')
		title = dict['title']
		title = title.replace('  ',' ').replace('  ',' ').replace('  ',' ')
		title = title.replace('||','|').replace('::',':').replace('--','-')
		title = title.replace('[[','[').replace(']]',']')
		title = title.replace('((','(').replace('))',')')
		title = title.replace('<<','<').replace('>>','>')
		#title = title.strip(' ').strip('|').strip('-').strip(':').strip('(').strip('[')
		lowest,lang = 9999,''
		first = title[0:2]
		separators = [' ',':','-','|',']',')','#','.',',','$',"'",'!','@','%','&','*','^']
		if   first[0]=='(': separators = [')']
		elif first[0]=='[': separators = [']']
		elif first[0]=='<': separators = ['>']
		for i in separators:
			position = title[2:].find(i)
			#position = title[1:].replace(' ','').find(i)
			if position>=0 and position<=lowest:
				lowest = position
				sep = i
		if lowest==9999: lang = '!!__UNKNOWN__!!'
		#if   ' ' in title and lowest==9999: sep = ' '
		#elif ' ' in title and lowest<9999:
		#	spacePos = title.find(' ')
		#	sepPos = title.find(sep)
		#	if sep in [')',']','>'] and first not in ['(','[','<']: sep = ' '
		#	elif sep not in [')',']','>'] and (sepPos-spacePos)!=1 and sepPos>=spacePos: sep = ' '
		#else: lang = '!!__UNKNOWN__!!'
		"""
		elif lowest<9999 and ' ' in title and sep not in [')',']','|'] and (sepPos-spacePos)!=1 and sepPos>=spacePos:
			sep = ' '
		elif lowest<9999 and ' ' in title and sep in [')',']','|'] and first not in ['(','[','|']:
			sep = ' '
		elif lowest<9999: sep = sep
		else: lang = '!!__UNKNOWN__!!'
			#if (sepPos-spacePos)!=1 or sepPos>=spacePos: sep = ' '
			#if (sepPos-spacePos)==1: sep = sep
			#elif sepPos<spacePos: sep = sep
			#else: sep = ' '
			#if (sepPos-spacePos)==1 or sepPos<spacePos: sep = sep
			#else: sep = ' '
			#if (sepPos-spacePos)!=1 and sepPos>=spacePos: sep = ' '
		"""
		if lang=='': lang = first+title[2:].split(sep,1)[0]+sep.strip(' ')
		dict['lang'] = lang.upper()
		dict['title'] = title.upper()
		#if 'AL - ' in dict['title']: dict['title'] = dict['title'].replace('AL - ','AL ')
		#if 'EL - ' in dict['title']: dict['title'] = dict['title'].replace('EL - ','EL ')
		streams_not_sorted.append(dict)
	#LOG_THIS('NOTICE','EMAD 444')
	streams_sorted = sorted(streams_not_sorted, reverse=False, key=lambda key: key['title'].lower())
	grouped_streams = {}
	types = ['ALL','LIVE_ORIGINAL','VOD_ORIGINAL','LIVE_FROM_NAME','VOD_FROM_NAME','LIVE_GROUPED','LIVE_UNKNOWN','VOD_MOVIES','VOD_SERIES','VOD_UNKNOWN','DUMMY']
	for type in types: grouped_streams[type] = []
	#LOG_THIS('NOTICE','EMAD 444 CREATE STREAMS START creating 1st STREAMS dictionary')
	for dict in streams_sorted:
		grouped_streams['ALL'].append(dict)
		type = dict['type']
		dict2 = dict.copy()
		del dict2['type']
		del dict2['org_title']
		del dict2['org_group']
		dict3 = dict2.copy()
		dict4 = dict2.copy()
		del dict3['lang']
		grouped_streams[type].append(dict3)
		dict4['group'] = dict4['lang']
		del dict4['lang']
		if 'LIVE' in type: grouped_streams['LIVE_FROM_NAME'].append(dict4)
		elif 'VOD' in type: grouped_streams['VOD_FROM_NAME'].append(dict4)
	#LOG_THIS('NOTICE','EMAD 555 CREATE STREAMS finished 1st and START creating 2nd STREAMS dictionary')
	for dict in streams_not_sorted:
		type = dict['type']
		dict2 = dict.copy()
		dict2['title'] = dict2['org_title']
		dict2['group'] = dict2['org_group'].replace('__MOVIES__','').replace('__SERIES__','')
		del dict2['type']
		del dict2['org_title']
		del dict2['org_group']
		del dict2['lang']
		if 'LIVE' in type: grouped_streams['LIVE_ORIGINAL'].append(dict2)
		elif 'VOD' in type: grouped_streams['VOD_ORIGINAL'].append(dict2)
	grouped_streams['DUMMY'].append('')
	#LOG_THIS('NOTICE','EMAD 666 CREATE STREAMS FINISHED')
	"""
	for dict in streams_sorted:
		dict3 = dict.copy()
		del dict3['group2']
		if dict3['type']=='VOD_SERIES':
			title = dict3['title']
			series_title = re.findall('(.*?) [Ss]\d+ +[Ee]\d+',title,re.DOTALL)
			if series_title: dict3['group'] = series_title[0]
			else: dict3['group'] = '!!__UNKNOWN__!!'
			dict3['type'] = 'VOD_EPISODES'
			grouped_streams['VOD_EPISODES'].append(dict3)
	"""
	DELETE_ALL_OLD_FILES([m3u_filename],False)
	SAVE_STREAMS_TO_SQL3(grouped_streams,types)
	#SAVE_STREAMS_TO_DISK(grouped_streams,types)
	return

def isIPTVFiles(show_msg=True):
	streams = GET_STREAMS_FROM_SQL3('DUMMY')
	#xbmcgui.Dialog().ok('DUMMY',str(streams))
	if streams: return True
	if show_msg: xbmcgui.Dialog().ok('جهازك لا يحتوي على ملفات IPTV','انت بحاجة الى:','اولا اضافة اشتراكك المدفوع مع أي شركة IPTV','ثم ثانيا جلب ملفات IPTV')
	return False

def isIPTVFiles_Disk(show_msg=True):
	settings = xbmcaddon.Addon(id=addon_id)
	filename = settings.getSetting('iptv.file')
	list = str(os.listdir(addoncachefolder))
	if filename in list: return True
	if show_msg: xbmcgui.Dialog().ok('جهازك لا يحتوي على ملفات IPTV','انت بحاجة الى:','اولا اضافة اشتراكك المدفوع مع أي شركة IPTV','ثم ثانيا جلب ملفات IPTV')
	return False

def SAVE_STREAMS_TO_DISK(grouped_streams,types):
	filesLIST = []
	filesLIST.append('iptv_'+str(int(now))+'_.m3u')
	filename = 'iptv_'+str(int(now))+'__TYPE__.streams'
	settings = xbmcaddon.Addon(id=addon_id)
	settings.setSetting('iptv.file',filename)
	for TYPE in types:
		new_streams = str(grouped_streams[TYPE])
		new_streams = new_streams.replace('},','},\n')
		new_filename = filename.replace('__TYPE__','_'+TYPE+'_')
		iptvFile = os.path.join(addoncachefolder,new_filename)
		file = open(iptvFile, 'wb')
		file.write(new_streams)
		file.close()
		filesLIST.append(new_filename)
	xbmcgui.Dialog().ok('IPTV','تم جلب ملفات IPTV جديدة')
	return

def SAVE_STREAMS_TO_SQL3(grouped_streams,types):
	for TYPE in types:
		WRITE_TO_SQL3([TYPE],'iptv_streams',grouped_streams[TYPE])
	xbmcgui.Dialog().ok('IPTV','تم جلب ملفات IPTV جديدة')
	return

def GET_STREAMS_FROM_DISK(TYPE):
	settings = xbmcaddon.Addon(id=addon_id)
	filename = settings.getSetting('iptv.file')
	filename = filename.replace('__TYPE__','_'+TYPE+'_')
	iptvFile = os.path.join(addoncachefolder,filename)
	f = open(iptvFile,'rb')
	streams_text = f.read()
	streams_text = streams_text.replace('u\'','\'')
	streams = eval(streams_text)
	return streams

def GET_STREAMS_FROM_SQL3(TYPE):
	streams = READ_FROM_SQL3([TYPE],'iptv_streams')
	return streams

def DELETE_ALL_OLD_FILES(exceptionLIST=[],show=True):
	if show:
		yes = xbmcgui.Dialog().yesno('مسح ملفات IPTV','تستطيع في أي وقت الدخول إلى قائمة IPTV وجلب ملفات IPTV جديدة .. هل تريد الآن مسح الملفات القديمة المخزنة في البرنامج ؟!','','','كلا','نعم')
		if not yes: return
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	c.execute('DROP TABLE IF EXISTS iptv_streams')
	c.execute('DROP TABLE IF EXISTS iptv_groups')
	c.execute('DROP TABLE IF EXISTS iptv_items')
	conn.commit()
	conn.close()
	for filename in os.listdir(addoncachefolder):
		cond1 = ('_.streams' in filename or '_.m3u' in filename)
		if 'iptv_' in filename and cond1 and filename not in exceptionLIST:
			iptvOldFile = os.path.join(addoncachefolder,filename)
			os.remove(iptvOldFile)
	if show: xbmcgui.Dialog().ok('IPTV','تم مسح جميع ملفات IPTV')
	return

def WRITE_TO_SQL3(inputLIST,tableNAME,dataLIST):
	#xbmcgui.Dialog().ok(filename,'')
	#LOG_THIS('NOTICE','EMAD START SAVE')
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	conn.text_factory = str
	c.execute('create table if not exists '+tableNAME+' (input,data)')
	data = str(dataLIST)
	data = data.replace('},','},\n')
	text = cPickle.dumps(data)
	compressed = zlib.compress(text)
	t = (str(inputLIST),sqlite3.Binary(compressed))
	c.execute('INSERT INTO '+tableNAME+' VALUES (?,?)',t)
	conn.commit()
	conn.close()
	return

def READ_FROM_SQL3(inputLIST,tableNAME):
	#LOG_THIS('NOTICE','EMAD START')
	#LOG_THIS('NOTICE',str(inputLIST))
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	conn.text_factory = str
	conn.commit()
	t = (str(inputLIST),)
	try:
		c.execute('SELECT data FROM '+tableNAME+' WHERE input=?', t)
		rows = c.fetchall()
	except: rows = None
	conn.close()
	if rows:
		#message = 'found in cache'
		compressed = rows[0][0]
		text = zlib.decompress(compressed)
		results2 = cPickle.loads(text)
		results = eval(results2)
		#LOG_THIS('NOTICE','EMAD 444')
	else:
		#message = 'not found in cache'
		results = []
	#LOG_THIS('NOTICE','EMAD END')
	return results
