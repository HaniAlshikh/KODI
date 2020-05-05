# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from LIBRARY import *

script_name='SERVICES'

def MAIN(mode,text=''):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	#if mode in [0,1]: FIX_SKIN_KEYBOARD(mode,text)
	if   mode==  2: SEND_MESSAGE(text)
	elif mode==  3: DMCA()
	elif mode==  4: HTTPS_TEST()
	elif mode==  7: VERSIONS()
	elif mode==  9: DELETE_CACHE()
	elif mode==151: NO_ARABIC_FONTS()
	elif mode==152: HTTPS_FAILED()
	elif mode==153: LINKS_NOT_WORKING()
	elif mode==154: NO_FORIGN_LANGUAGE_VIDEOS()
	elif mode==155: SLOW_LINKS()
	elif mode==156: UNKNOWN_SERVERS()
	elif mode==157: PRIVATE_PUBLIC_SERVERS()
	elif mode==158: SLOW_VIDES()
	elif mode==159: CHECK_FOR_ADDONS_UPDATES()
	elif mode==171: SSL_WARNING()
	elif mode==172: INSTALL_REPOSITORY(True)
	elif mode==173: ENABLE_MPD()
	elif mode==174: ENABLE_RTMP()
	elif mode==175: TEST_ALL_WEBSITES()
	elif mode==176: ANALYTICS_REPORT()
	elif mode==177: RESOLVEURL_SETTINGS()
	elif mode==178: YOUTUBE_DL_SETTINGS()
	elif mode==179: TESTINGS()
	elif mode==190: WHAT_IS_CACHE()
	elif mode==191: WHAT_DOT_COMMA_MEANS()
	elif mode==192: SOLVE_TEMP_PROBLEM()
	elif mode==193: WHY_IGNORE_SSL_CERTIFICATE()
	elif mode==194: MPD_NOT_WORKING()
	elif mode==195: WEBSITES_BLOCKED()
	elif mode==196: CONTACT_ME()
	elif mode==197: KODI_SKIN()
	return

def SEND_EMAIL(subject,message,showDialogs='yes',url='',source='',text=''):
	if 'problem=yes' in text: problem='yes'
	else: problem='no'
	sendit,html = 1,''
	if showDialogs=='yes':
		sendit = xbmcgui.Dialog().yesno('هل ترسل هذه الرسالة الى المبرمج',message.replace('\\n','\n'),'','','كلا','نعم')
		if sendit==0: 
			xbmcgui.Dialog().ok('تم الغاء الارسال','تم الغاء الارسال بناء على طلبك')
			return ''
	if sendit==1:
		#addon_version = xbmc.getInfoLabel( "System.AddonVersion("+addon_id+")" )
		kodiName = xbmc.getInfoLabel( "System.FriendlyName" )
		message = message+' \\n\\n==== ==== ==== \\nAddon Version: '+addon_version+' :\\nEmail Sender: '+dummyClientID(32)+' :\\nKodi Version: '+kodi_release+' :\\nKodi Name: '+kodiName
		#xbmc.sleep(4000)
		#playerTitle = xbmc.getInfoLabel( "Player.Title" )
		#playerPath = xbmc.getInfoLabel( "Player.Filenameandpath" )
		#if playerTitle != '': message += ' :\\nPlayer Title: '+playerTitle
		#if playerPath != '': message += ' :\\nPlayer Path: '+playerPath
		#xbmcgui.Dialog().ok(playerTitle,playerPath)
		if url != '': message += ' :\\nURL: ' + url
		if source != '': message += ' :\\nSource: ' + source
		message += ' :\\n'
		if showDialogs=='yes': xbmcgui.Dialog().notification('جاري ألإرسال','الرجاء الانتظار')
		logfileNEW = ''
		if problem=='yes':
			dataNEW,counts = [],0
			logfile = xbmc.translatePath('special://logpath')+'kodi.log'
			#logfile = 'S://DOWNLOADS/6ac26462c99fc35816f3532bb17608f4-5.8.1.log'
			f = open(logfile,'rb')
			size = os.path.getsize(logfile)
			if size>600000: f.seek(-600000, os.SEEK_END)
			data = f.readlines()
			for line in reversed(data):
				if "extension '' is not currently supported" in line: continue
				if 'Checking for Malicious scripts' in line: continue
				if 'Previous line repeats' in line: continue
				if 'PVR IPTV Simple Client' in line: continue
				if 'this hash function is broken' in line: continue
				if 'uses plain HTTP for add-on downloads' in line: continue
				if 'NOTICE: ADDON:' in line and line.endswith('installed\n'): continue
				dataNEW.append(line)
				counts += 1
				if counts==1000: break
			dataNEW = reversed(dataNEW)
			logfileNEW = ''.join(dataNEW)
			#logfileNEW = ''.join(dataNEW[-1000:])
			logfileNEW = base64.b64encode(logfileNEW)
		url = 'http://emadmahdi.pythonanywhere.com/sendemail'
		payload = { 'subject' : quote(subject) , 'message' : quote(message) , 'logfile' : logfileNEW }
		data = urllib.urlencode(payload)
		html = openURL_cached(NO_CACHE,url,data,'','','SERVICES-SEND_EMAIL-1st')
		result = html[0:6]
		if showDialogs=='yes':
			if result == 'Error ':
				xbmcgui.Dialog().notification('للأسف','فشل في الإرسال')
				xbmcgui.Dialog().ok('Failed sending the message','خطأ وفشل في إرسال الرسالة')
			else:
				xbmcgui.Dialog().notification('تم الإرسال','بنجاح')
				xbmcgui.Dialog().ok('Message sent','تم إرسال الرسالة بنجاح')
	return html

def NO_ARABIC_FONTS():
	message1 = '1.   If you can\'t see Arabic Letters then go to "Kodi Interface Settings" and change the font to "Arial"'
	message2 = '1.   إذا لم تستطع رؤية الأحرف العربية فغير الخط المستخدم إلى "Arial" من إعدادات واجهة كودي'
	xbmcgui.Dialog().ok('Arabic Problem',message1,message2)
	message1 = '2.   If you don\'t find "Arial" font in kodi skin then change skin in "Kodi Interface Settings"'
	message2 = '2.   إذا لم تجد الخط "Arial" فإدن عليك أن تذهب إلى إعدادات كودي وتغير واجهة كودي المستخدمة'
	xbmcgui.Dialog().ok('Font Problem',message1,message2)
	yes = xbmcgui.Dialog().yesno('Font settings','Do you want to go to "Kodi Interface Settings" now?','هل تريد الذهاب إلى لوحة إعدادات واجهة كودي ألآن؟')
	if yes==1: xbmc.executebuiltin("ActivateWindow(InterfaceSettings)")
	return

def HTTPS_FAILED():
	message1 = 'بعض المواقع تحتاج ربط مشفر وقد يكون جهازك غير قادر على الربط المشفر أو هناك مشكلة في شهادة التشفير الخاصة بكودي عندك علما انه تم فحص البرنامج على كودي الإصدارات'
	message2 = '17.6  &  18.[0-3]'
	xbmcgui.Dialog().ok('المواقع المشفرة',message1,message2)
	#message2 = 'شهادة التشفير هي ملف يحتوي على شفرة خاصة أو تواقيع خاصة لشركات معروفة وله تاريخ صلاحية ونفاذ والغرض منه هو تبادل المعلومات بطريقة مشفرة يصعب اختراقها وفهمها'
	#xbmcgui.Dialog().ok('شهادة التشفير - SSL Certificate',message2)
	LATEST_KODI()
	return

def LINKS_NOT_WORKING():
	xbmcgui.Dialog().ok('روابط لا تعمل','غالبا السبب هو من الموقع الأصلي المغذي للبرنامج وللتأكد قم بتشغيل الرابط الذي لا يعمل ثم قم بإرسال مشكلة إلى المبرمج من القائمة الرئيسية للبرنامج')
	return

def NO_FORIGN_LANGUAGE_VIDEOS():
	message = 'هذا البرنامج مخصص فقط للغة العربية ولكن هذا لا يمنع وجود مواقع فيها أفلام ومسلسلات مترجمة أو مدبلجة إلى اللغة العربية والى لغات اخرى ولا يوجد سبب للتكرار'
	xbmcgui.Dialog().ok('مواقع أجنبية',message)
	return

def SLOW_LINKS():
	message = 'الروابط البطيئة لا علاقة لها بالبرنامج وغالبا السبب هو من الموقع الأصلي المغذي للبرنامج'
	xbmcgui.Dialog().ok('روابط بطيئة',message)
	return

def UNKNOWN_SERVERS():
	message = 'هي سيرفرات لا يستطيع البرنامج استخدامها بسبب كونها محمية من المصدر أو بحاجة إلى اشتراك رسمي أو جديدة أو لا يعرفها البرنامج'
	xbmcgui.Dialog().ok('سيرفرات سيئة أو مجهولة',message)
	return

def PRIVATE_PUBLIC_SERVERS():
	message = 'السيرفرات العامة هي سيرفرات خارجية وغير جيدة لان الكثير منها ممنوع أو محذوف أو خطأ بسبب حقوق الطبع وحقوق الألفية الرقمية ولا توجد طريقة لفحصها أو إصلاحها \n\n السيرفرات الخاصة هي سيرفرات يتحكم فيها الموقع الأصلي وهي جيدة نسبيا ولا توجد طريقة لفحصها أو إصلاحها \n\n الرجاء قبل الإبلاغ عن مشكلة وقبل مراسلة المبرمج افحص نفس الفيديو وافحص نفس السيرفر على الموقع الأصلي'
	xbmcgui.Dialog().textviewer('مواقع تستخدم سيرفرات عامة',message)
	return

def SLOW_VIDES():
	message1 = 'ابتعد عن ملفات الدقة العالية'
	message2 = 'ابتعد عن ملفات أل m3u8'
	message3 = 'ابتعد عن ملفات التحميل والداونلود download'
	xbmcgui.Dialog().ok('لتسريع عمل الفيديوهات',message1,message2,message3)
	return

def WHAT_IS_CACHE():
	message2 = 'الكاش هو مخزن مؤقت للمعلومات يستخدمه البرنامج لخزن صفحات الإنترنيت وروابط الفيديوهات'
	message2 += ' ' + 'للوصول إليها بسرعة وبدون إنترنيت والبرنامج يمسحها أوتوماتيكيا بعد انتهاء وقتها وأيضا عند تحديث البرنامج والكاش في البرنامج هو ثلاثة أنواع'
	message2 += '\n\n' + 'طويل المدى للصفحات التي لا تتغير ومدته ' + str(LONG_CACHE/60/60) + ' ساعة'
	message2 += '\n\n' + 'متوسط المدى للصفحات التي قد تتغير ومدته ' + str(REGULAR_CACHE/60/60) + ' ساعة'
	message2 += '\n\n' + 'قصير المدى للصفحات التي تتغير دائما ومدته ' + str(SHORT_CACHE/60/60) + ' ساعة'
	xbmcgui.Dialog().textviewer('ما هو الكاش المستخدم في البرنامج',message2)
	return

def WHAT_DOT_COMMA_MEANS():
	message = 'الفاصلة تعني مجلد بنفس اسمه الأصلي والنقطة تعني أن الاسم الأصلي تم تعديله وفاصلة ونقطة تعنى مجلد وتم تعديل اسمه وبدون علامة تعني ملف بنفس اسمه الأصلي'
	xbmcgui.Dialog().ok('ما معنى هذه العلامات ,'+escapeUNICODE('\u02d1')+';',message)
	return

def SOLVE_TEMP_PROBLEM():
	message = 'إذا واجهتك مشكلة في الشبكة وتم حلها ... أو انك تظن أن الموقع الأصلي كان فيه مشكلة مؤقته وتم حلها ... فإذن جرب مسح كاش البرنامج لكي يقوم البرنامج بطلب الصفحة الصحيحة وتخزينها بدلا من الصفحة القديمة'
	xbmcgui.Dialog().ok('كيف تحل مشكلة مؤقته',message)
	return

def WHY_IGNORE_SSL_CERTIFICATE():
	message = 'الغرض من شهادة التشفير هو ضمان صحة وسرية المعلومات المتبادلة بين البرنامج والموقع المشفر وهذا الضمان غير مطلوب ولا حاجة له عند الاتصال او الربط مع مواقع الفيديوهات المشفرة'
	xbmcgui.Dialog().ok('لماذا لا نفحص شهادة التشفير',message)
	return

def MPD_NOT_WORKING():
	message1 = 'يجب تفعيل إضافة اسمها inputstream.adaptive لكي يعمل هذا النوع من الفيديوهات'
	message2 = 'InputStream Adaptive'
	message3 = 'وبعدها سوف تعمل هذه الفيديوهات'
	xbmcgui.Dialog().ok('الفيديوهات نوع mpd لا تعمل',message1)
	ENABLE_MPD()
	return

def WEBSITES_BLOCKED():
	message  = 'مؤخرا قامت بعض شركات الأنترنيت الدولي بوضع عائق ضد البرامج مثل كودي لتسمح فقط لبعض مستخدمي المتصفح بالدخول لمواقع الفيديو'
	#message += '\n[COLOR FFC89008]وهذا العائق هو reCAPTCHA الخاص بشركة جوجل[/COLOR]\n'
	#message += 'والذي صنعته شركة جوجل خصيصا لمنع برامج مثل كودي من تصفح الأنترنيت'
	message += '\n\ونتيجة لهذا العائق فانه تقريبا جميع مستخدمي برنامج كودي لا يستطيعون الدخول لجميع مواقع البرنامج حتى مع استخدام'
	message += '\n[COLOR FFC89008]ـ  VPN  أو  Proxy  أو  DNS  أو أي حل بسيط آخر[/COLOR]\n'
	message += '\nلان هذا لن يحل المشكلة وإنما فقط سيقوم بإصلاح بعض المواقع وإعاقة مواقع اخرى كانت تعمل سابقا بدون مشاكل'
	xbmcgui.Dialog().textviewer('عائق ضد كودي والبرامج الأخرى عدا المتصفح',message)
	message = 'المواقع التي تأثرت بالعائق عند بعض الناس هي:'
	message += '\n'+'[COLOR FFC89008]akoam  egybest  egybestvip  movizland  series4watch  shahid4u[/COLOR]'
	message += '\n\n'+'الدول التي تأثرت بالعائق عند بعض الناس هي:'
	message += '\n'+'[COLOR FFC89008]مصر  الكويت  أميركا  كندا  فرنسا  اليونان  بريطانيا الإمارات ألمانيا روسيا اليابان السعودية رومانيا هولندا[/COLOR]'
	message += '\n\n'+'المبرمج وجد طريقة لتجاوز العائق ولكنها تحتاج جهد كبير والمبرمج يظن المشكلة صغيرة ولا تستحق التعب فإذا لديك مشكلة بالدخول لبعض المواقع وأيضا لكي يتضح حجم المشكلة '
	message += '[COLOR FFC89008]ارسل رسالة مؤدبة إلى المبرمج واكتب فيها اسم بلدك وأسماء المواقع التي لا تستطيع دخولها[/COLOR]'
	xbmcgui.Dialog().textviewer('المواقع والدول التي تأثرت بالعائق',message)
	#SEND_MESSAGE('IsPlayable=no,problem=no')
	#message = '\n\n'+'ولقد لاحظنا ايضا أن المواقع المعاقة تختلف باختلاف البلد وتختلف باختلاف شركة الانترنيت في ذلك البلد وهذا معناه انه حتى لو تم استخدام VPN أو Proxy أو أي وسيلة اخرى فان المواقع المعاقة سوف تختلف ولكنها لن تعمل جميعها'
	#message += 'لحل المشكلة قم بعملين:    الأول: أرسل سجل الأخطاء والاستخدام إلى المبرمج (من قائمة خدمات البرنامج) واكتب معه اسم بلدك واسم شركة الإنترنيت وأسماء المواقع التي لا تعمل عندك'
	#message += '\n\n'+'والثاني: جرب استخدام VPN وعند البعض قد تحتاج فقط تغيير DNS والأحسن أن يكون في بلد اخر علما ان استخدام Proxy قد يحل مشكلة بعض المواقع ولكن ليس في جميع الدول'
	#xbmcgui.Dialog().textviewer('مشكلة عند بعض الناس',message)
	#yes = xbmcgui.Dialog().yesno('فحص جميع مواقع البرنامج','هذا الفحص هو لمعرفة هل المشكلة من عندك ام من البرنامج. سيقوم البرنامج الآن بفحص مواقعه مرتين الأولى بوضعك الطبيعي والثانية باستخدام بروكسي مجاني انت تختاره من القائمة التي ستظهر لاحقا. هل تريد الاستمرار؟','','','كلا','نعم')
	#if yes==1:
	#TEST_ALL_WEBSITES()
	return

def CONTACT_ME():
	xbmcgui.Dialog().ok('ثلاث طرق للتواصل مع المبرمج','إما باستخدام الفيسبوك "الحاج عماد مهدي" أو إرسال رسالة أو مشكلة من قائمة خدمات البرنامج أو فتح موضوع للنقاش بهذا الرابط','https://github.com/emadmahdi/KODI/issues')
	return

def DELETE_CACHE():
	#WHAT_IS_CACHE()
	yes = xbmcgui.Dialog().yesno('هل تريد مسح جميع الكاش ؟','الكاش يعمل على تسريع عمل البرنامج ومسحه يسبب إعادة طلب جميع الصفحات من الأنترنيت عند الحاجة إليها والمسح ليس فيه أي ضرر وبالعكس فان المسح ممكن أن يحل بعض مشاكل البرنامج','','','كلا','نعم')
	if yes==1: 
		DELETE_DATABASE_FILES()
		xbmcgui.Dialog().ok('تم مسح كاش البرنامج بالكامل','إذا كانت عندك مشكلة في احد المواقع فجرب الموقع الآن ... وأدا المشكلة مستمرة فإذن ارسل المشكلة إلى المبرمج')
	return yes

def HTTPS_TEST():
	working = HTTPS(True)
	if not working: HTTPS_FAILED()
	return

def FIX_SKIN_KEYBOARD(mode,text):
	import xbmc,unicodedata,email.charset
	import xbmcgui
	#import simplejson as json
	#from LIBRARY import *
	#xbmcgui.Dialog().ok(str(mode),text)
	keyboard = text
	if keyboard=='': return
	if mode==1:
		try:
			window_id = xbmcgui.getCurrentWindowDialogId()
			window = xbmcgui.Window(window_id)
			keyboard = mixARABIC(keyboard)
			window.getControl(311).setLabel(keyboard)
		except:
			traceback.print_exc(file=sys.stderr)
			pass
	elif mode==0:
		ttype = 'X'
		check = isinstance(keyboard, unicode)
		if check==True: ttype = 'U'
		new1 = str(type(keyboard))+' '+keyboard+' '+ttype+' '
		for i in range(0,len(keyboard),1):
			new1 += hex(ord(keyboard[i])).replace('0x','')+' '
		keyboard = mixARABIC(keyboard)
		ttype = 'X'
		check = isinstance(keyboard, unicode)
		if check==True: ttype='U'
		new2 = str(type(keyboard))+' '+keyboard+' '+ttype+' '
		for i in range(0,len(keyboard),1):
			new2 += hex(ord(keyboard[i])).replace('0x','')+' '
		#xbmcgui.Dialog().ok(new1,new2)
	return

def SEND_MESSAGE(text=''):
	if 'problem=yes' in text: problem='yes'
	else:
		problem='no'
		yes = xbmcgui.Dialog().yesno('','هل لديك مشكلة تريد أبلاغ المبرمج عنها ؟','','','كلا','نعم')
		if yes==1: problem='yes'
	if problem=='yes':
		#yes = DELETE_CACHE()
		#if yes==1: return ''
		logs = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','سيقوم البرنامج بإرسال سجل الأخطاء والاستخدام إلى المبرمج لكي يستطيع المبرمج معرفة المشكلة وإصلاحها','','','كلا','نعم')
		if logs==0:
			xbmcgui.Dialog().ok('تم إلغاء الإرسال','للأسف بدون سجل الأخطاء والاستخدام المبرمج لا يستطيع معرفة المشكلة ولا حلها لان المبرمج لا يعلم الغيب')
			return ''
		logs2 = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','هل قمت قبل قليل بتشغيل الفيديو أو الرابط الذي أعطاك المشكلة لكي يتم تسجيل هذه المشكلة في سجل الأخطاء والاستخدام قبل إرساله للمبرمج','','','كلا','نعم')
		if logs2==0:
			xbmcgui.Dialog().ok('تم إلغاء الإرسال','للأسف بدون تسجيل المشكلة في سجل الأخطاء والاستخدام فان المبرمج لا يستطيع معرفة المشكلة ولا حلها لان المبرمج لا يعلم الغيب')
			return ''
		"""
		else:
			text += 'logs=yes'
			yes = xbmcgui.Dialog().yesno('هل تريد الاستمرار ؟','قبل ارسال سجل الاخطاء والاستخدام إلى المبرمج عليك ان تقوم بتشغيل الفيديو او الرابط الذي يعطيك المشكلة لكي يتم تسجيل المشكلة في سجل الاخطاء والاستخدام. هل تريد الارسال الان ؟','','','كلا','نعم')
			if yes==0:
				xbmcgui.Dialog().ok('','تم الغاء الارسال')
				return ''
		xbmcgui.Dialog().ok('المبرمج لا يعلم الغيب','اذا كانت لديك مشكلة فالرجاء قراءة قسم المشاكل والاسئلة واذا لم تجد الحل هناك فحاول كتابة جميع تفاصيل المشكلة لان المبرمج لا يعلم الغيب')
		"""
	xbmcgui.Dialog().ok('ملاحظة مهمة','اكتب الآن رسالة إلى المبرمج واكتب فيها عنوان بريدك ألإلكتروني ... والأفضل أن تراسل المبرمج على الفيسبوك وأسمه "الحاج عماد مهدي"')
	search = KEYBOARD('Write a message   اكتب رسالة')
	if search == '':
		xbmcgui.Dialog().ok('تم إلغاء الإرسال','تم إلغاء الإرسال لأنك لم تكتب أي شيء')
		return ''
	message = search
	subject = 'Message: From Arabic Videos'
	text = 'problem='+problem
	result = SEND_EMAIL(subject,message,'yes','','EMAIL-FROM-USERS',text)
	#	url = 'my API and/or SMTP server'
	#	payload = '{"api_key":"MY API KEY","to":["me@email.com"],"sender":"me@email.com","subject":"From Arabic Videos","text_body":"'+message+'"}'
	#	#auth=("api", "my personal api key"),
	#	import requests
	#	response = requests.request('POST',url, data=payload, headers='', auth='')
	#	response = requests.post(url, data=payload, headers='', auth='')
	#	if response.status_code == 200:
	#		xbmcgui.Dialog().ok('','تم الإرسال بنجاح')
	#	else:
	#		xbmcgui.Dialog().ok('خطأ في الإرسال','Error {}: {!r}'.format(response.status_code, response.content))
	#	FROMemailAddress = 'me@email.com'
	#	TOemailAddress = 'me@email.com'
	#	header = ''
	#	#header += 'From: ' + FROMemailAddress
	#	#header += '\nTo: ' + emailAddress
	#	#header += '\nCc: ' + emailAddress
	#	header += '\nSubject: من كودي الفيديو العربي'
	#	server = smtplib.SMTP('smtp-server',25)
	#	#server.starttls()
	#	server.login('username','password')
	#	response = server.sendmail(FROMemailAddress,TOemailAddress, header + '\n' + message)
	#	server.quit()
	#	xbmcgui.Dialog().ok('Response',str(response))
	return ''

def DMCA():
	text = 'هذا البرنامج لا يوجد له أي سيرفر يستضيف أي محتويات. البرنامج يستخدم روابط وتضمين لمحتويات مرفوعة على سيرفرات خارجية. البرنامج غير مسؤول عن أي محتويات تم تحميلها على سيرفرات ومواقع خارجية "مواقع طرف ثالث". جميع الأسماء والماركات والصور والمنشورات هي خاصة باصحابها. البرنامج لا ينتهك حقوق الطبع والنشر وقانون الألفية للملكية الرقمية DMCA إذا كان لديك شكوى خاصة بالروابط والتضامين الخارجية فالرجاء التواصل مع إدارة هذه السيرفرات والمواقع الخارجية. هذا البرنامج هو ببساطة متصفح لمواقع الويب'
	xbmcgui.Dialog().textviewer('حقوق الطبع والنشر وقانون الألفية للملكية الرقمية',text)
	text = 'This program does not host any content on any server. It only uses links to embedded content that was uploaded to popular online video hosting sites. All trademarks, videos, trade names, service marks, copyrighted work, logos referenced herein belong to their respective owners / companies. The program is not responsible for what other people upload to 3rd party sites. We urge all copyright owners, to recognize that the links contained within this program are located somewhere else on the web or video embedded are from other various sites. If you have any legal issues please contact appropriate media file owners / hosters. This program is simply a web browser.'
	xbmcgui.Dialog().textviewer('Digital Millennium Copyright Act (DMCA)',text)
	return

def VERSIONS():
	#url = 'http://raw.githack.com/emadmahdi/KODI/master/addons.xml'
	#url = 'https://github.com/emadmahdi/KODI/raw/master/addons.xml'
	xbmcgui.Dialog().notification('جاري جمع المعلومات','الرجاء الانتظار')
	url = 'https://raw.githubusercontent.com/emadmahdi/KODI/master/ADDONS/addons.xml'
	html = openURL_cached(NO_CACHE,url,'','','','SERVICES-VERSIONS-1st')
	latest_ADDON_VER = re.findall('plugin.video.arabicvideos" name="Arabic Videos" version="(.*?)"',html,re.DOTALL)[0]
	current_ADDON_VER = addon_version
	latest_REPO_VER = re.findall('name="EMAD Repository" version="(.*?)"',html,re.DOTALL)[0]
	current_REPO_VER = xbmc.getInfoLabel('System.AddonVersion(repository.emad)')
	if latest_ADDON_VER > current_ADDON_VER or latest_REPO_VER > current_REPO_VER:
		need_update = True
		message1 = 'الرجاء تحديث إضافات كودي لحل المشاكل'
		message3 = '\n\n' + 'انت بحاجة لتحديث هذا البرنامج أو تحديث مخزن عماد'
	else:
		need_update = False
		message1 = 'لا توجد تحديثات للبرنامج أو المخزن حاليا'
		message3 = '\n\n' + 'الرجاء إبلاغ المبرمج عن المشكلة التي تواجهك'
	if current_REPO_VER=='': current_REPO_VER='لا يوجد'
	else: current_REPO_VER = ' ' + current_REPO_VER
	message2  = 'الإصدار الأخير للبرنامج المتوفر الآن هو :   ' + latest_ADDON_VER
	message2 += '\n' + 'الإصدار الذي انت تستخدمه للبرنامج هو :   ' + current_ADDON_VER
	message2 += '\n' + 'ألإصدار الأخير لمخزن عماد المتوفر الآن هو :   ' + latest_REPO_VER
	message2 += '\n' + 'ألإصدار الذي انت تستخدمه لمخزن عماد هو :  ' + current_REPO_VER
	message3 += '\n\n' + 'لكي يعمل عندك التحديث الأوتوماتيكي ... يجب أن يكون لديك في كودي مخزن عماد EMAD Repository'
	message3 += '\n\n' + 'ملفات التنصيب مع التعليمات متوفرة على هذا الرابط'
	message3 += '\n' + 'https://github.com/emadmahdi/KODI'
	xbmcgui.Dialog().textviewer(message1,message2+message3)
	#threads22 = CustomThread()
	#threads22.start_new_thread('22',LATEST_KODI)
	#xbmcgui.Dialog().notification('thread submitted','')
	LATEST_KODI()
	if need_update:
		INSTALL_REPOSITORY(False)
		CHECK_FOR_ADDONS_UPDATES()
	#LATEST_KODI()
	#threads22.wait_finishing_all_threads()
	return

def SSL_WARNING():
	xbmcgui.Dialog().ok('تحذير مهم','البرنامج لا يفحص شهادة التشفير عند الاتصال بالمواقع المشفرة ولهذا في حال وجود شهادة غير صحيحة أو منتهية الصلاحية أو مزيفة فان هذا لن يوقف الربط المشفر ولن يوقف عمل البرنامج')
	WHY_IGNORE_SSL_CERTIFICATE()
	return

def LATEST_KODI():
	#	https://kodi.tv/download/849
	#   https://play.google.com/store/apps/details?id=org.xbmc.kodi
	#	http://mirror.math.princeton.edu/pub/xbmc/releases/windows/win64
	#	http://mirrors.mit.edu/kodi/releases/windows/win64'
	url = 'http://mirrors.kodi.tv/releases/windows/win64/'
	#xbmc.log('ZZZZ: 1111:', level=xbmc.LOGNOTICE)
	html = openURL_cached(REGULAR_CACHE,url,'','','','SERVICES-LATEST_KODI-1st')
	#html = openURL_requests(url,'','','','SERVICES-LATEST_KODI-1st')
	#xbmc.log('ZZZZ: 2222:', level=xbmc.LOGNOTICE)
	latest_KODI_VER = re.findall('title="kodi-(.*?)-',html,re.DOTALL)[0]
	#xbmc.log('ZZZZ: 3333:', level=xbmc.LOGNOTICE)
	current_KODI_VER = str(kodi_version)
	#xbmc.log('ZZZZ: 4444:', level=xbmc.LOGNOTICE)
	message4a = 'إصدار كودي الأخير المتوفر الآن هو :   ' + latest_KODI_VER
	message4b = 'إصدار كودي الذي انت تستخدمه هو :   ' + current_KODI_VER
	xbmcgui.Dialog().ok('كودي',message4a,message4b)
	return

def TEST_ALL_WEBSITES():
	#xbmcgui.Dialog().notification('جاري فحص','جميع المواقع')
	websites_keys = WEBSITES.keys()
	headers = { 'User-Agent' : '' }
	def test_all(type,proxy_url=''):
		def dummyFunc(site,type,proxy_url):
			if type=='proxy': url = WEBSITES[site][0]+'||MyProxyUrl='+proxy_url
			else: url = WEBSITES[site][0]
			if type=='direct': html = openURL_cached(NO_CACHE,url,'',headers,'','SERVICES-TEST_ALL_WEBSITES-1st')
			elif type=='proxy': html = openURL_HTTPSPROXIES(url,'',headers,'','SERVICES-TEST_ALL_WEBSITES-2nd')
			#if 'https' in url: html = '___Error___'
			#else: html = ''
			return html
		threads = CustomThread(True)
		for site in websites_keys:
			threads.start_new_thread(type+'_'+site,dummyFunc,site,type,proxy_url)
		threads.wait_finishing_all_threads()
		return threads.resultsDICT
	DIRECTdict_result = test_all('direct')
	type,messageDIRECT,proxyname,PROXYdict_result = 'direct','','',''
	for site in sorted(websites_keys):
		result = DIRECTdict_result[type+'_'+site]
		if '___Error___' not in result: messageDIRECT += site.lower()+'  '
		else: messageDIRECT += '[COLOR FFC89008]'+site.lower()+'[/COLOR]  '
	if '___Error___' in str(DIRECTdict_result):
		testedLIST,timingLIST = TEST_HTTPS_PROXIES()
		proxies_name,proxies_url = [],[]
		i = 0
		for id in testedLIST:
			proxies_name.append(PROXIES[id][0]+'   '+str(int(1000*timingLIST[i]))+'ms')
			proxies_url.append(PROXIES[id][1])
			i += 1
		selection = xbmcgui.Dialog().select(str(len(proxies_name))+' اختر بروكسي (الأسرع فوق)', proxies_name)
		if selection == -1: return
		else: 
			proxyname = proxies_name[selection].split('   ')[0]
			proxyurl = proxies_url[selection]
		type,messagePROXY = 'proxy',''
		PROXYdict_result = test_all('proxy',proxyurl)
		for site in sorted(websites_keys):
			result = PROXYdict_result[type+'_'+site]
			if '___Error___' not in result: messagePROXY += site.lower()+'  '
			else: messagePROXY += '[COLOR FFC89008]'+site.lower()+'[/COLOR]  '
	else: messagePROXY = 'جميع المواقع تعمل عندك والبرنامج لا يحتاج بروكسي'
	message  = '== المواقع البيضاء تعمل والحمراء لا تعمل =='
	message += '\n\n'+'== [COLOR FFC89008]فحص باستخدام شبكة الإنترنيت الخاصة بك[/COLOR] =='
	message += '\n'+messageDIRECT.strip(' ')
	if proxyname!='': message += '\n\n'+'== [COLOR FFC89008]فحص باستخدام بروكسي موجود في '+proxyname+'[/COLOR] =='
	else: message += '\n\n'+'== [COLOR FFC89008]فحص باستخدام بروكسي ببلد وإنترنيت مختلفة[/COLOR] =='
	message += '\n'+messagePROXY.strip(' ')
	xbmcgui.Dialog().textviewer('فحص جميع مواقع البرنامج',message)
	direct,proxy = '',''
	if '___Error___' in str(DIRECTdict_result): direct = 'problem'
	if '___Error___' in str(PROXYdict_result): proxy = 'problem'
	if direct=='problem' and proxy!='problem':
		xbmcgui.Dialog().ok('نتيجة فحص مواقع البرنامج','المشكلة التي عندك في بعض المواقع قد اختفت باستخدام بروكسي وهذا معناه ان المشكلة من طرفك وليست من البرنامج. حاول حل مشكلتك إما باستخدام DNS أو Proxy أو VPN')
	elif direct=='problem' and proxy=='problem':
		xbmcgui.Dialog().ok('نتيجة فحص مواقع البرنامج','مشكلتك ظهرت مع بروكسي وبدون بروكسي وسببها إما من الموقع الأصلي أو البرنامج أو البروكسي الذي انت اخترته. جرب إعادة الفحص باختيار بروكسي مختلف وارسل سجل الأخطاء والاستخدام للمبرمج (من قائمة خدمات البرنامج)')		
	elif direct!='problem':
		xbmcgui.Dialog().ok('نتيجة فحص مواقع البرنامج','جميع المواقع تعمل عندك بدون مشكلة وهذا معناه إن جهازك لا يحتاج أي تعديلات. فإذا كانت لديك مشكلة في البرنامج فقم بإرسال سجل الأخطاء والاستخدام إلى المبرمج (من قائمة خدمات البرنامج)')
	return

def ANALYTICS_REPORT():
	payload,usageDICT,message1,message2,message3,message4 = {'a':'a'},{},'','','',''
	data = urllib.urlencode(payload)
	html = openURL_cached(SHORT_CACHE,WEBSITES['LIVETV'][1],data,'','','SERVICES-ANALYTICS_REPORT-1st')
	#xbmcgui.Dialog().ok('',html)
	resultsLIST = eval(html)
	siteLIST,countLIST,countryLIST = zip(*resultsLIST)
	siteLIST,countLIST,countryLIST = list(siteLIST),list(countLIST),list(countryLIST)
	for i in range(len(siteLIST)):
		site = siteLIST[i].encode('utf8')
		usage = countLIST[i]
		if   usage=='highusage': message1 += '  '+site
		elif usage=='lowusage': message2 += '  '+site
		countries = countryLIST[i].encode('utf8')
		#countries = countries.replace('___',' . ')
		countries = countries.strip(' ').strip(' .')
		countries = countries.replace('___','  ')
		countries = countries.replace('United States','USA')
		countries = countries.replace('United Kingdom','UK')
		countries = countries.replace('United Arab Emirates','UAE')
		countries = countries.replace('Saudi Arabia','KSA')
		countries = countries.replace('Western Sahara','W.Sahara')
		countries = countries[:43].strip(' ').strip(' .')
		message4 += '\n[COLOR FFC89008]'+site+' : [/COLOR]'+countries
	for site in sorted(WEBSITES.keys()):
		if site not in siteLIST:
			message3 += '  '+site
			message4 += '\n[COLOR FFC89008]'+site+' : [/COLOR]'+'لا يوجد'
	message1 = message1.strip(' ')
	message2 = message2.strip(' ')
	message3 = message3.strip(' ')
	message4 = message4.strip('\n')
	LOG_THIS('NOTICE',LOGGING(script_name)+'   HighUsage: [ '+message1+' ]')
	LOG_THIS('NOTICE',LOGGING(script_name)+'   LowUsage: [ '+message2+' ]')
	LOG_THIS('NOTICE',LOGGING(script_name)+'   NoUsage: [ '+message3+' ]')
	message6 = message1+'  '+message2
	message5  = 'مواقع شغل منها البرنامج مؤخراً فيديوهات بدون مشاكل'+'\n'
	message5 += 'وهذا معناه إذا لديك مشكلة فهي ليست من البرنامج'+'\n'
	message5 += '[COLOR FFC89008]'+message6+'[/COLOR]'+'\n\n'
	message5 += 'مواقع لم يشغل البرنامج منها مؤخراً أي فيديوهات'+'\n'
	message5 += 'وهذا معناه احتمال كبير وجود مشكلة في البرنامج'+'\n'
	message5 += '[COLOR FFC89008]'+message3+'[/COLOR]'+'\n\n'
	"""
	message5  = 'مواقع شغل منها البرنامج مؤخراً فيديوهات كثيرة'+'\n'
	message5 += 'وهذا معناه إذا لديك مشكلة فهي ليست من البرنامج'+'\n'
	message5 += '[COLOR FFC89008]'+message1+'[/COLOR]'+'\n\n'
	message5 += 'مواقع شغل منها البرنامج مؤخراً فيديوهات قليلة\n'
	message5 += 'وهذا معناه إذا لديك مشكلة فهي ليست من البرنامج'+'\n'
	message5 += '[COLOR FFC89008]'+message2+'[/COLOR]'+'\n\n'
	"""
	xbmcgui.Dialog().textviewer('مواقع اشتغلت مؤخراً في جميع دول العالم',message5)
	xbmcgui.Dialog().textviewer('أعلى الدول التي استخدمت مؤخراً البرنامج',message4)
	return

def KODI_SKIN():
	xbmcgui.Dialog().textviewer('واجهة كودي Kodi Skin','هذا البرنامج يعمل افضل باستخدام واجهة كودي التي اسمها\nkodi skin "[COLOR FFC89008]metropolisEMAD[/COLOR]"\n\nوهي موجودة في نفس موقع البرنامج\n[COLOR FFC89008]https://github.com/emadmahdi/KODI [/COLOR]\n\nهذه الرسالة وغيرها كثير موجودة في قائمة خدمات البرنامج')
	return

def RESOLVEURL_SETTINGS():
	xbmc.executebuiltin('Addon.OpenSettings(script.module.resolveurl)', True)
	return

def YOUTUBE_DL_SETTINGS():
	xbmc.executebuiltin('Addon.OpenSettings(script.module.youtube.dl)', True)
	return

def CHECK_FOR_ADDONS_UPDATES():
	yes = xbmcgui.Dialog().yesno('تحديث جميع إضافات كودي','كودي يقوم بعملية تحديث جميع الإضافات أوتوماتيكيا كل 24 ساعة ولكن ممكن إجراءها الآن . هل تريد تحديث جميع إضافات كودي الآن ؟','','','كلا','نعم')
	if yes==1:
		xbmc.executebuiltin('UpdateAddonRepos')
		xbmcgui.Dialog().ok('تحديث جميع إضافات كودي','تم إرسال طلب إلى كودي لكي يقوم بتحديث جميع إضافات كودي . بما فيها تحديث هذا البرنامج وتحديث مخزن عماد . يرجى إعطاء كودي 5 دقائق لكي ينهي عملية التحديثات')
	return

def INSTALL_REPOSITORY(show_ok_msg=True):
	repo_addon = 'repository.emad'
	url = 'https://raw.githubusercontent.com/emadmahdi/KODI/master/ADDONS/addons.xml'
	html = openURL_cached(NO_CACHE,url,'','','','SERVICES-INSTALL_REPOSITORY-1st')
	repo_version = re.findall('name="EMAD Repository" version="(.*?)"',html,re.DOTALL)[0]
	installed_repo_version = xbmc.getInfoLabel('System.AddonVersion('+repo_addon+')')
	#installed_repo_version = '4.2.99999'
	is_installed = (installed_repo_version!='')
	is_old_version = (repo_version>installed_repo_version)
	is_enabled = (xbmc.getCondVisibility('System.HasAddon('+repo_addon+')')==1)
	#xbmcgui.Dialog().ok(str(is_enabled),str(is_old_version))
	if is_installed and is_enabled and not is_old_version:
		if show_ok_msg: xbmcgui.Dialog().ok('EMAD Repository مخزن عماد','المخزن موجود عندك ومفعل وجاهز للاستخدام v'+installed_repo_version)
	elif is_installed and not is_enabled and not is_old_version:
		yes = xbmcgui.Dialog().yesno('EMAD Repository مخزن عماد','مخزن عماد موجود عندك ولكن غير مفعل . هل تريد تصليح المشكلة الآن ؟','','','كلا','نعم')
		if yes: 
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"'+repo_addon+'","enabled":true}}')
			xbmcgui.Dialog().ok('EMAD Repository مخزن عماد','تم تفعيل المخزن')
	else:
		yes = xbmcgui.Dialog().yesno('EMAD Repository مخزن عماد','مخزن عماد عندك فيه مشكلة ... أما قديم أو غير مفعل أو غير موجود عندك ... هل تريد تصحيح المشكلة الآن ؟','','','كلا','نعم')
		if yes: 
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"'+repo_addon+'","enabled":true}}')
			repo_zipfile = repo_addon+'-'+repo_version+'.zip'
			zipfile_url = 'https://raw.githubusercontent.com/emadmahdi/KODI/master/ADDONS/'+repo_addon+'/'+repo_zipfile
			zipfile_html = openURL_cached(LONG_CACHE,zipfile_url,'','','','SERVICES-INSTALL_REPOSITORY-2nd')
			addons_folder = os.path.join(xbmc.translatePath('special://home'),'addons')
			import zipfile,StringIO
			stream = StringIO.StringIO(zipfile_html)
			zf = zipfile.ZipFile(stream)
			zf.extractall(addons_folder)
			xbmc.sleep(1000)
			xbmc.executebuiltin('UpdateLocalAddons')
			xbmc.sleep(1000)
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"'+repo_addon+'","enabled":true}}')
			xbmcgui.Dialog().ok('EMAD Repository مخزن عماد','تم تنصيب وتفعيل المخزن في كودي','الإصدار رقم v'+repo_version)
	return


















def TESTINGS():

	urls = [ 'http://www.youtube.com/watch?v=BaW_jenozKc' ]

	# from __future__ import unicode_literals

	success = 0
	xbmc.log('======= STARTING ==================================',level=xbmc.LOGNOTICE)
	import youtube_dl
	#import resolveurl
	#import urlresolver
	ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
	for url in urls:
		t1 = time.time()
		try:
			with ydl:
				result = ydl.extract_info(url,download=False) # We just want to extract the info
			#result = urlresolver.HostedMediaFile(url).resolve()
			#result = resolveurl.HostedMediaFile(url).resolve()
			if not result: raise
			success += 1
			message = '      Succeeded_input:  '+url+'   '+str(result)
			xbmc.log('      Succeeded_output:  '+str(result['formats'][0]['url']),level=xbmc.LOGNOTICE)
			xbmc.log('      Succeeded_output:  '+str(result['formats'][0]['format']),level=xbmc.LOGNOTICE)
		except:
			message = '      Failed:  '+url
		t2 = time.time()
		t0 = str(t2-t1)[0:4]
		xbmc.log(t0+message,level=xbmc.LOGNOTICE)
	xbmcgui.Dialog().ok('Done','Succeeded:  '+str(success))
	xbmc.log('======= FINISHED =================================',level=xbmc.LOGNOTICE)
	return


	if 'entries' in result:
		# Can be a playlist or a list of videos
		video = result['entries'][0]
	else:
		# Just a video
		video = result
	video_url = video['url']
	xbmcgui.Dialog().ok(video_url,video)
	return


	#PLAY_VIDEO(url)
	#return

	#url = ''
	import resolveurl
	try:
		#resolvable = urlresolver.HostedMediaFile(url).valid_url()
		link = resolveurl.HostedMediaFile(url).resolve()
		xbmcgui.Dialog().ok(str(link),url)
	except: xbmcgui.Dialog().ok('Resolver: failed',url)
	return

	import RESOLVERS
	titles,urls = RESOLVERS.RESOLVE(url)
	selection = xbmcgui.Dialog().select('TITLES :', titles)
	selection = xbmcgui.Dialog().select('URLS :', urls)
	#url = ''
	#PLAY_VIDEO(url)
	#settings = xbmcaddon.Addon(id=addon_id)
	#settings.setSetting('test1','hello test1')
	#var = settings.getSetting('test2')
	#xbmc.log('EMAD11 ' + str(var) + ' 11EMAD',level=xbmc.LOGNOTICE)
	#import subprocess
	#var = subprocess.check_output('wmic csproduct get UUID')
	#xbmc.log('EMAD11 ' + str(var) + ' 11EMAD',level=xbmc.LOGNOTICE)
	#import os
	#var = os.popen("wmic diskdrive get serialnumber").read()
	#xbmc.log('EMAD11 ' + str(var) + ' 11EMAD',level=xbmc.LOGNOTICE)

	#var = dummyClientID(32)
	#xbmcgui.Dialog().ok(var,'')
	#xbmc.log('EMAD11' + html + '11EMAD',level=xbmc.LOGNOTICE)
	url = ''
	urllist = [
		''
		]
	#play_item = xbmcgui.ListItem(path=url, thumbnailImage='')
	#play_item.setInfo(type="Video", infoLabels={"Title":''})
	# Pass the item to the Kodi player.
	#xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
	# directly play the item.
	#xbmc.Player().play(url, play_item) 

	#import RESOLVERS
	#url = RESOLVERS.PLAY(urllist,script_name,'no')
	#PLAY_VIDEO(url,script_name,'yes')
	return
