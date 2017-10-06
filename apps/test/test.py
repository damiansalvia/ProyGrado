# -*- coding: utf-8 -*-

chars = ['…','“','”']
for c in chars:
	print 1,c
	print 2,repr(c)
	print 3,c.decode('windows-1252','replace').encode('utf8')
	print 4, c.decode('utf8')
	print 5, repr(c.decode('utf8'))
	print 6, c.decode('cp1252','replace')
	print 7, repr(c.decode('cp1252','replace').encode('utf8'))
	print 8, c in ['\xe2\x80\xa6','\xe2\x80\x9c','\xe2\x80\x9d']
	print
