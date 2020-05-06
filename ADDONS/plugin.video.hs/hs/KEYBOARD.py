# -*- coding: utf-8 -*-
from LIBRARY import *

#import unicodedata,simplejson

def MAIN(mode,keyboard):
	#LOG_MENU_LABEL(script_name,menu_label,mode,menu_path)
	if keyboard=='': return
	if mode==1:
		window_id = xbmcgui.getCurrentWindowDialogId()
		window = xbmcgui.Window(window_id)
		keyboard = mixARABIC(keyboard)
		window.getControl(311).setLabel(keyboard)

	if mode==0:
		#keyboard = keyboard.decode('unicode_escape')
		#keyboard = keyboard.decode('raw_unicode_escape')
		#keyboard = keyboard.decode('utf-8')
		ttype='X'
		check=isinstance(keyboard, unicode)
		if check==True: ttype='U'
		new1=str(type(keyboard))+' '+keyboard+' '+ttype+' '
		for i in range(0,len(keyboard),1):
			new1 += hex(ord(keyboard[i])).replace('0x','')+' '
		keyboard = mixARABIC(keyboard)
		#keyboard = keyboard.decode('utf-8')
		ttype='X'
		check=isinstance(keyboard, unicode)
		if check==True: ttype='U'
		new2=str(type(keyboard))+' '+keyboard+' '+ttype+' '
		for i in range(0,len(keyboard),1):
			new2 += hex(ord(keyboard[i])).replace('0x','')+' '
		#xbmcgui.Dialog().ok(new1,new2)

	return

	#for i in range(0,len(keyboard)-2,3):
	#	string=hex(ord(keyboard[i+0]))+'  '+hex(ord(keyboard[i+1]))+'  '+hex(ord(keyboard[i+2]))
	#	xbmcgui.Dialog().ok('',string)
	#return
	#keyboard = keyboard.decode('utf8')
	#xbmcgui.Dialog().ok('',keyboard)

	#keyboard = mixARABIC(keyboard)
	#keyboard = keyboard.decode('utf8')
	#keyboard = unicodedata.normalize('NFKD',keyboard)
	#xbmcgui.Dialog().ok('',   hex(  unicodedata.combining(keyboard[0])  )   )
	#xbmcgui.Dialog().ok(keyboard,   hex(ord(  keyboard[0]  ))   )

	#new = ''
	#for letter in keyboard:
	#	xbmcgui.Dialog().ok('Mode 0',unicodedata.decomposition(letter) )
	#	new += '\u0' + hex(ord(letter)).replace('0x','')
	#keyboard = new
	#xbmcgui.Dialog().ok('',keyboard)

	#new = ''
	#for i in range(len(keyboard)-6,-5,-6):
	#	#xbmcgui.Dialog().ok('',str(i))
	#	new += keyboard[i] + keyboard[i+1] + keyboard[i+2] + keyboard[i+3] + keyboard[i+4] + keyboard[i+5]
	#keyboard = new
	#xbmcgui.Dialog().ok('',keyboard)

	#keyboard = keyboard.decode('unicode_escape')
	#xbmcgui.Dialog().ok('',keyboard)

	#keyboard = keyboard.encode('utf8')
	#xbmcgui.Dialog().ok('',keyboard)


	#keyboard = 'emad'
	#json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Input.SendText","params":{"text":"'+keyboard+'","done":false},"id":1}')
	#simplejson.loads(json_query)

	#keyboard = keyboard.encode('utf8')
	#new = keyboard.decode('unicode_escape')
	#keyboard = new
	#xbmcgui.Dialog().ok('',keyboard)
	#keyboard = mixARABIC(keyboard)
	#xbmcgui.Dialog().ok('',keyboard)

	#new = ''
	#for i in range(len(keyboard)-2,-1,-2):
	#	new += keyboard[i] + keyboard[i+1]
	#keyboard = new
	#xbmcgui.Dialog().ok('',keyboard)

	#keyboard = keyboard.encode('utf8')
	#xbmcgui.Dialog().ok('',keyboard)

	#new = ''
	#for i in range(len(keyboard)-2,-1,-2):
	#	new += keyboard[i] + keyboard[i+1]
	#keyboard = new
	#xbmcgui.Dialog().ok('',keyboard)




		#keyboard = keyboard.replace(' ','')
		#new = ''
		#for i in range(len(keyboard)-3,-2,-3):
		#	new += keyboard[i] + keyboard[i+1] + keyboard[i+2]
		#keyboard = new
		#new = ''
		#for i in range(len(keyboard)-2,-1,-2):
		#	new += keyboard[i] + keyboard[i+1]
		#keyboard = new
		#xbmcgui.Dialog().ok('',keyboard)


		#keyboard = keyboard.dedcode('utf8')
		#xbmcgui.Dialog().ok(str(ord(keyboard[0]))+' '+str(ord(keyboard[1]))+' '+str(ord(keyboard[2])),str(len(keyboard)))
		#xbmcgui.Dialog().ok('Mode 0 Letters',keyboard)
		#new = ''
		#for i in range(len(keyboard)-2,-1,-2):
		#	new += keyboard[i] + keyboard[i+1]
		#keyboard = new
		#new = keyboard.decode('utf8')
		#new = new.decode('utf8')
		#xbmcgui.Dialog().ok('Mode 0',new )
		#new1 = ''
		#for letter in new:
		#	xbmcgui.Dialog().ok('Mode 0',unicodedata.decomposition(letter) )
		#	new1 += '\u' + hex(ord(letter)).replace('x','')
		#new1 = new1.decode('unicode_escape')
		#xbmcgui.Dialog().ok('Mode 0',new1 )
		#new = unicodedata.decomposition(    unichr(   ord(new[1])    )   )
		#new = unicodedata.decomposition(    unichr(   hex(ord(new[1]))    )   )
		#new = mixARABIC(new)
		#keyboard = new.encode('utf8')
		#new = new.decode('utf8') #.decode('unicode_escape')
		#xbmcgui.Dialog().ok('Mode 0',str(ord(new[2])) ) #unicodedata.decomposition(new.decode('utf8'))   )
		#keyboard = mixARABIC(new)
		#keyboard = mixARABIC(keyboard)
		#method="Input.SendText"
		#params='{"text":"%s", "done":false}' % keyboard
		#json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "%s", "params": %s, "id": 1}' % (method, params))



