__author__ = 'TecSUS-3'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Este arquivo tem que estar na pasta modules/, porque o web2py não reconhece
# a pasta tests/ como módulo, porém a modules/ sim.

try:
	from fake_import import *
	print '\nSystem in Test.\n'
except:
	#print '\nWeb2py is running.\n'
	pass