#!/usr/bin/python2

import sys
import os
from time import sleep
#import grid

if __name__ == '__main__':
	os.makedirs('fgsfds')
	os.chdir('fgsfds')
	f = open('dfgdfg', 'w')
	f.write('test1\n')
	for arg in sys.argv:
		f.write(arg + '\n')
	sleep(60*10)
	f.write('test2\n')
	f.close()
	print('DONE')
