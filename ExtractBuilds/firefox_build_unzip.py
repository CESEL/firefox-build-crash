__author__ = 'md tajmilur rahman'

"""
unzip firefox crash logs
"""

#BUILD_DIR_ALL = "/media/rupak/Seagate Expansion Drive/firefox/TBPL/"
BUILD_DIR_ALL = "/media/rupak/3164-9A73/rupak/firefox_build_fail/mozilla_central/"
import gzip
import glob
import os.path

for path, subdir, filelist in os.walk(BUILD_DIR_ALL):
	for name in filelist:
		gzip_file = os.path.join(path, name)
		if os.path.isdir(gzip_file) == False:
			if gzip_file.endswith('.gz'):
				# uncompress the file
				print gzip_file
				inF = gzip.open(gzip_file, 'rb')
				s = inF.read()
				inF.close()
				# get gzip filename (without directories)
				gzip_fname = os.path.basename(gzip_file)
				# get original filename (remove 3 characters from the end: ".gz")
				fname = gzip_fname[:-3]
				uncompressed_path = os.path.join(path, fname)
				print "File: " + uncompressed_path
				# store uncompressed file data from 's' variable
				open(uncompressed_path, 'w').write(s)
				os.remove(gzip_file)
