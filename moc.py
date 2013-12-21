#usage: moc.py .

__author__ = "Kirill Makhonin"
__copyright__ = "Copyright 2013, K.Makhonin"
__credits__ = ["Kirill Makhonin"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Kirill Makhonin"
__email__ = "kroks.rus at gmail.com"
__status__ = "Production"

import os
import sys
import re
from subprocess import call
import fileinput

filemasks = ['.*\.h']


def search(dir):
	founded = 0
	patched = 0
	search = re.compile('.*Q_OBJECT.*')
	
	reg = [re.compile('^' + m + '$') for m in filemasks]
	for root, subFolders, files in os.walk(rootdir):
		files = list(x for x in files if sum( rx.match(x) != None for rx in reg) > 0)
		for f in files:
			if sum(1 for line in open(root + '\\' + f) if re.match(search, line) != None) == 0:
				continue
			founded += 1	
			file = root + '\\' + f
			mocfile = file + '.moc'
			if os.path.isfile(mocfile):
				os.remove(mocfile)
			call(["moc", '-o', mocfile, file])
			if not os.path.isfile(mocfile):
				print("Error compiling " + file)
				continue
			if sum(1 for line in open(file) if file + '.moc' in line) > 0:
				continue
			patched += 1
			currentFilePatched = False			
			
			for line in fileinput.input(file, inplace=1):
				print(re.sub("\n|\r", '', line))
				if not currentFilePatched and (line.startswith('//MOC')):
					print ('#include "' +mocfile+ '"')
					currentFilePatched = True
			if not currentFilePatched:
				with open(file, 'r+') as f:
					content = f.read()
					f.write('#include "' +mocfile+ '"\n')
			
	print('Founded: ' + str(founded))
	print('Patched: ' + str(patched))

if __name__ != '__main__':
	quit()

if len(sys.argv) != 2:
	quit(1)
	
rootdir = sys.argv[1]
if not os.path.isdir(rootdir):
	print("Error: " + rootdir + " not dir!")
	quit(1)
	
print("Search in " + rootdir)
search(rootdir)
