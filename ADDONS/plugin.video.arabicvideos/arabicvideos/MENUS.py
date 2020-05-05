# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from LIBRARY import *

script_name='MENUS'

def MAIN(mode,url,text=''):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if   mode==260: results = MAIN_MENU()
	elif mode==261: results = WEBSITES_MENU()
	elif mode==262: results = GLOBAL_SEARCH_MENU(text,True)
	elif mode==263: results = ANSWERS_MENU()
	elif mode==264: results = SERVICES_MENU()
	elif mode==265: results = LAST_VIDEOS_MENU()
	elif mode==266: results = DELETE_LAST_VIDEOS_MENU()
	else: results = False
	return results

def MAIN_MENU():
	#addMenuItem('link','Testing - watched enabled','',179,'','','IsPlayable=yes')
	#addMenuItem('link','Testing - watched disabled','',179,'','','IsPlayable=no')
	addMenuItem('dir','[COLOR FFC89008]  1.  [/COLOR]'+'قائمة المواقع','',261)
	addMenuItem('dir','[COLOR FFC89008]  2.  [/COLOR]'+'قائمة الاقسام','',165,'','','WEBSITES')
	addMenuItem('dir','[COLOR FFC89008]  3.  [/COLOR]'+'قائمة  القنوات','',100)
	addMenuItem('dir','[COLOR FFC89008]  4.  [/COLOR]'+'قائمة العشوائية','',160)
	addMenuItem('dir','[COLOR FFC89008]  5.  [/COLOR]'+'قائمة اشتراك IPTV','',230)
	addMenuItem('dir','[COLOR FFC89008]  6.  [/COLOR]'+'IPTV قائمة أقسام الـ','',165,'','','IPTV')
	addMenuItem('dir','[COLOR FFC89008]  7.  [/COLOR]'+'بحث في جميع المواقع','',262)
	addMenuItem('dir','[COLOR FFC89008]  8.  [/COLOR]'+'اخر 12 فيديو تم تشغيلها','',265)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  9.  [/COLOR]'+'تقرير عن استخدام البرنامج','',176)
	addMenuItem('link','[COLOR FFC89008]10.  [/COLOR]البرنامج إصدار رقم ( '+addon_version+' )','',7,'','','IsPlayable=no')
	#addMenuItem('dir','[COLOR FFC89008]10.  [/COLOR]'+'ـ Services Menu  قائمة الخدمات','',172)
	#addMenuItem('dir','  4.  [COLOR FFC89008]ـ Services Menu  قائمة الخدمات[/COLOR]','',264)
	#addMenuItem('link','  5.  [COLOR FFC89008]البرنامج إصدار رقم ('+addon_version+')[/COLOR]','',7,'','','IsPlayable=no')
	addMenuItem('dir','[COLOR FFC89008]11.  [/COLOR]ـ Answers Menu  قائمة الاجوبة','',263)
	addMenuItem('dir','[COLOR FFC89008]12.  [/COLOR]ـ Services Menu  قائمة الخدمات','',264)
	addMenuItem('link','[COLOR FFC89008]13.  [/COLOR]ـ Contact Me  كيف تتصل بالمبرمج','',196,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	return

def WEBSITES_MENU():
	#addMenuItem('dir','  1.  [COLOR FFC89008]TV    [/COLOR]'+'قنوات تلفزيونية','',100)
	#addMenuItem('dir','  2.  [COLOR FFC89008]IPT   [/COLOR]'+'اشتراك IPTV مدفوع','',230)
	addMenuItem('link','[COLOR FFC89008]مواقع سيرفرات خاصة - قليلة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addMenuItem('dir','  1.  [COLOR FFC89008]PNT  [/COLOR]'+'موقع بانيت','',30)
	addMenuItem('dir','  2.  [COLOR FFC89008]YUT  [/COLOR]'+'موقع يوتيوب','',140)
	addMenuItem('dir','  3.  [COLOR FFC89008]KLA  [/COLOR]'+'موقع كل العرب','',10)
	addMenuItem('dir','  4.  [COLOR FFC89008]KWT  [/COLOR]'+'موقع قناة الكوثر','',130)
	addMenuItem('dir','  5.  [COLOR FFC89008]IFL    [/COLOR]'+'موقع قناة آي فيلم','',20)
	addMenuItem('dir','  6.  [COLOR FFC89008]AKW [/COLOR]'+'موقع أكوام الجديد','',240)
	addMenuItem('dir','  7.  [COLOR FFC89008]SHF  [/COLOR]'+'موقع شوف ماكس','',50)
	addMenuItem('dir','  8.  [COLOR FFC89008]MRF  [/COLOR]'+'موقع قناة المعارف','',40)
	addMenuItem('dir','  9.  [COLOR FFC89008]FTM  [/COLOR]'+'موقع المنبر الفاطمي','',60)
	addMenuItem('link','[COLOR FFC89008]مواقع سيرفرات خاصة وعامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addMenuItem('dir','10.  [COLOR FFC89008]ARS  [/COLOR]'+'موقع عرب سييد','',250)
	addMenuItem('dir','11.  [COLOR FFC89008]AKO  [/COLOR]'+'موقع أكوام القديم','',70)
	addMenuItem('dir','12.  [COLOR FFC89008]EGV  [/COLOR]'+'موقع إيجي بيست vip','',220)    # 220
	addMenuItem('link','[COLOR FFC89008]مواقع سيرفرات عامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addMenuItem('dir','13.  [COLOR FFC89008]ARL   [/COLOR]'+'موقع عرب ليونز','',200)
	addMenuItem('dir','14.  [COLOR FFC89008]SHA  [/COLOR]'+'موقع شاهد فوريو','',110)
	addMenuItem('dir','15.  [COLOR FFC89008]HEL  [/COLOR]'+'موقع هلال يوتيوب','',90)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	#addMenuItem('dir','16.  [COLOR FFC89008]HLA  [/COLOR]'+'موقع هلا سيما','',88) # 80
	#addMenuItem('dir','17.  [COLOR FFC89008]SFW  [/COLOR]'+'موقع سيريس فور وتش','',218)  # 210
	#addMenuItem('dir','18.  [COLOR FFC89008]MVZ  [/COLOR]'+'موقع موفيزلاند اونلاين','',188) # 180
	#addMenuItem('dir','19.  [COLOR FFC89008]EGB  [/COLOR]'+'موقع ايجي بيست','',128) # 120
	return

def SERVICES_MENU():
	#addMenuItem('dir','[COLOR FFC89008]ـ Problems & Questions  قائمة مشاكل وأسئلة  .1 [/COLOR]','',264)
	#addMenuItem('link','[COLOR FFC89008]  2.  [/COLOR]'+'فحص جميع مواقع البرنامج','',175,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  1.  [/COLOR]'+'Can\'t see Arabic Text or Letters','',151,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  2.  [/COLOR]'+'تحديث جميع إضافات كودي','',159,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  3.  [/COLOR]'+'فحص مخزن عماد','',172,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  4.  [/COLOR]'+'تنصيب وتفعيل مخزن عماد','',172,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  5.  [/COLOR]'+'فحص الإصدار الأخير والتحديثات','',7,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  6.  [/COLOR]'+'فحص تفعيل فيديوهات mpd','',173,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  7.  [/COLOR]'+'فحص تفعيل فيديوهات rtmp','',174,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  8.  [/COLOR]'+'فحص اتصال المواقع المشفرة','',4,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  9.  [/COLOR]'+'مسح كاش البرنامج','',9,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]10.  [/COLOR]'+'إرسال سجل الأخطاء والاستخدام للمبرمج','',2,'','','IsPlayable=no,problem=yes')
	addMenuItem('link','[COLOR FFC89008]11.  [/COLOR]'+'إبلاغ المبرمج بوجود مشكلة','',2,'','','IsPlayable=no,problem=yes')
	addMenuItem('link','[COLOR FFC89008]12.  [/COLOR]'+'إرسال رسالة إلى المبرمج','',2,'','','IsPlayable=no,problem=no')
	addMenuItem('link','[COLOR FFC89008]13.  [/COLOR]'+'اعدادت ResolveURL','',177,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]14.  [/COLOR]'+'اعدادت Youtube-DL','',178,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	return

def ANSWERS_MENU():
	addMenuItem('link','[COLOR FFC89008]  1.  [/COLOR]'+'كيف تتصل وتتواصل مع المبرمج','',196,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  2.  [/COLOR]'+'DMCA  قانون الألفية للملكية الرقمية','',3,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  3.  [/COLOR]'+'تحذير يخص شهادة التشفير','',171,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  4.  [/COLOR]'+'ما هي افضل واجهة للبرنامج','',197,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  5.  [/COLOR]'+'لماذا بعض المواقع لا تعمل','',195,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  6.  [/COLOR]'+'كيف تحل مشكلة حجب بعض المواقع','',195,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  7.  [/COLOR]'+'بعض الفيديوهات بطيئة وتقطع','',158,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  8.  [/COLOR]'+'كيف تحل بنفسك مشكلة مؤقته','',192,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]  9.  [/COLOR]'+'بعض الروابط لا تعمل','',153,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]10.  [/COLOR]'+'بعض الروابط بطيئة','',155,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]11.  [/COLOR]'+'لماذا يوجد سيرفرات مجهولة','',156,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]12.  [/COLOR]'+'ما هي السيرفرات العامة والخاصة','',157,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]13.  [/COLOR]'+'ما معنى هذه العلامات بالبرنامج ,'+escapeUNICODE('\u02d1')+';','',191,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]14.  [/COLOR]'+'ما هو آخر إصدار لكودي وللبرنامج','',7,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]15.  [/COLOR]'+'ما هو الكاش وكم مقداره بالبرنامج','',190,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]16.  [/COLOR]'+'الفيديوهات نوع mpd لا تعمل','',194,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]17.  [/COLOR]'+'المواقع المشفرة لا تعمل','',152,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]18.  [/COLOR]'+'لماذا لا نفحص شهادة التشفير','',193,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]19.  [/COLOR]'+'أين مواقع الأفلام والمسلسلات الأجنبية','',154,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	return

def GLOBAL_SEARCH_MENU(search='',show=True):
	if search=='': search = KEYBOARD()
	if search == '': return
	LOG_THIS('NOTICE',LOGGING(script_name)+'   Global Search For: [ '+search+' ]')
	search = search.lower()
	if show: search2 = search
	else: search2 = 'كلمة عشوائية'
	addMenuItem('link','[COLOR FFC89008]مواقع سيرفرات خاصة - قليلة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addMenuItem('dir','  1.  [COLOR FFC89008]IPT   [/COLOR]'+search2+' - خدمة IPTV','',239,'','',search)
	#addMenuItem('dir','  2.  [COLOR FFC89008]PNT   [/COLOR]'+search2+' - 39 بانيت','',9999,'','',search)
	addMenuItem('dir','  2.  [COLOR FFC89008]YUT   [/COLOR]'+search2+' - موقع يوتيوب','',149,'','',search)
	addMenuItem('dir','  3.  [COLOR FFC89008]KLA   [/COLOR]'+search2+' - موقع كل العرب','',19,'','',search)
	addMenuItem('dir','  4.  [COLOR FFC89008]KWT  [/COLOR]'+search2+' - موقع قناة الكوثر','',139,'','',search)
	addMenuItem('dir','  5.  [COLOR FFC89008]IFL    [/COLOR]'+search2+' - موقع قناة آي فيلم','',29,'','',search)
	addMenuItem('dir','  6.  [COLOR FFC89008]AKW [/COLOR]'+search2+' - موقع أكوام الجديد','',249,'','',search)
	addMenuItem('dir','  7.  [COLOR FFC89008]SHF   [/COLOR]'+search2+' - موقع شوف ماكس','',59,'','',search)
	addMenuItem('dir','  8.  [COLOR FFC89008]MRF  [/COLOR]'+search2+' - موقع قناة المعارف','',49,'','',search)
	addMenuItem('dir','  9.  [COLOR FFC89008]FTM   [/COLOR]'+search2+' - موقع المنبر الفاطمي','',69,'','',search)
	#addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]مواقع سيرفرات خاصة وعامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addMenuItem('dir','10. [COLOR FFC89008]ARS  [/COLOR]'+search2+' - موقع عرب سييد','',259,'','',search)
	addMenuItem('dir','11. [COLOR FFC89008]AKO  [/COLOR]'+search2+' - موقع أكوام القديم','',79,'','',search)
	addMenuItem('dir','12. [COLOR FFC89008]EGV  [/COLOR]'+search2+' - موقع إيجي بيست vip','',229,'','',search)
	#addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]مواقع سيرفرات عامة - كثيرة المشاكل[/COLOR]','',157,'','','IsPlayable=no')
	addMenuItem('dir','13. [COLOR FFC89008]ARL  [/COLOR]'+search2+' - موقع عرب ليونز','',209,'','',search)
	addMenuItem('dir','14. [COLOR FFC89008]SHA  [/COLOR]'+search2+' - موقع شاهد فوريو','',119,'','',search)
	addMenuItem('dir','15. [COLOR FFC89008]HEL  [/COLOR]'+search2+' - موقع هلال يوتيوب','',99,'','',search)
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	#addMenuItem('dir','16. [COLOR FFC89008]HLA  [/COLOR]'+search+' - موقع هلا سيما','',88,'','',search) # 89
	#addMenuItem('dir','17. [COLOR FFC89008]SFW  [/COLOR]'+search+' - موقع سيريس فور وتش','',218,'','',search) # 219
	#addMenuItem('dir','18. [COLOR FFC89008]MVZ  [/COLOR]'+search+' - موقع موفيز لاند','',188,'','',search)# 189
	#addMenuItem('dir','19. [COLOR FFC89008]EGB  [/COLOR]'+search+' - موقع ايجي بيست','',128,'','',search)# 129
	return

def LAST_VIDEOS_MENU():
	addMenuItem('dir','مسح هذه القائمة','',266,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	if os.path.exists(lastvideosfile):
		with open(lastvideosfile,'r') as f: videoLIST = f.read()
		videoLIST = eval(videoLIST)
		#LOG_THIS('NOTICE',str(videoLIST))
		for name,url,mode,image,page,text in videoLIST:
			addMenuItem('link',name,url,mode,image,page,text)
	return

def DELETE_LAST_VIDEOS_MENU():
	if os.path.exists(lastvideosfile): os.remove(lastvideosfile)
	addMenuItem('dir','مسح هذه القائمة','',266,'','','IsPlayable=no')
	addMenuItem('link','[COLOR FFC89008]=========================[/COLOR]','',9999,'','','IsPlayable=no')
	return






