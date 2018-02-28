__author__ = 'md tajmilur rahman'

"""
"""

import psycopg2
import glob
import os.path

LOG_FILES = "/media/rupak/3164-9A73/rupak/SOEN691FF/scripts/test_logs/"

conn_string = "dbname= 'firefox_build_crash' user='rupak' password='rupak'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

for path, subdir, filelist in os.walk(LOG_FILES):
	i = 0
        for name in filelist:
                log_file = os.path.join(path, name)
		print i+": "+log_file
                if os.path.isdir(log_file) == False:
			read file content
			_file = open(log_file, 'r')
			for line in _file:
				extract overall result
				if 'results: ' in line:
					print line.split('results: ')[1]
					overall_result = line.split('results: ')[1].split('\n')
					overall_result = overall_result.replace("'","")
					print overall_result
				#extract build id
				if 'buildid: ' in line:
					buildid = line.split('buildid: ')[1].strip('\n')
                                        buildid = buildid.replace("'","")
				#extract build uid
				if 'builduid: ' in line:
					builduid = line.split('builduid: ')[1].strip('\n')
					builduid = builduid.replace("'","")
				if 'INFO -  TEST-INFO |' in line or 'REFTEST TEST-START' in line:

	insert = "insert into build_cluster(buildid,build_steps) values ('"+buildid+"','"+build_step.encode('hex')+"')"
	cursor.execute(insert)
	conn.commit()

cursor.close()
conn.close()
del cursor

