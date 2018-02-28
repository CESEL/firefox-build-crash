__author__ = 'md tajmilur rahman'

"""
load firefox build steps into database
"""

#BUILD_DIR_ALL = "/media/rupak/3164-9A73/rupak/firefox_build_fail/"
#BUILD_DIR_ALL = "/media/rupak/3164-9A73/rupak/SOEN691FF/scripts/test/"
BUILD_DIR_ALL = "/home/rupak/Documents/git/SOEN691FF/scripts/test/"
import os
import csv
import psycopg2
import re

#conn_string = "dbname= 'firefox_build_crash' user='rupak' password='rupak'"
#conn = psycopg2.connect(conn_string)
#cursor = conn.cursor()

for path, sub_dir, files in os.walk(BUILD_DIR_ALL):
        for name in files:
		buildId = ""
		buildUid = ""
		builder = ""
		buildSlave = ""
		startTime = ""
		overallResult = ""
		revisionNumber = ""
		bugNumber = ""
		test_fail = ""
		expected = ""
		actual = ""
                txt_file = os.path.join(path, name)
                if os.path.isdir(txt_file) == False:
                        if txt_file.endswith('.txt'):
				#print txt_file
				fin = open(txt_file, 'rb')
				reader = fin.readlines()
				elapsedTime = 0
				#step_block_pattern = '^=========\sStarted\s.*\(.*\)\s=========$'
				for line in reader:
					#print line
					if "builder: " in line:
						builder = line.split('builder: ')[1].strip('\n')
						builder = builder.replace("'","")
						print "Builder: "+builder
					if "slave: " in line:
						buildSlave = line.split('slave: ')[1].strip('\n')
						print buildSlave		
					if "starttime: " in line:
						startTime = line.split('starttime: ')[1].strip('\n')
						print startTime
					if "results: " in line:
                                		overallResult = re.search('results:\s[a-z]+([0-9])', line)
						if overallResult:
							overallResult = overallResult.group(1).strip('\n')
						print overallResult
					if "buildid: " in line:
                                		buildId = line.split('buildid: ')[1].strip('\n')
						buildId = buildId.replace("'","")
						print buildId
					if "buildUid: " in line:
                                		buildUid = line.split('buildUid: ')[1].strip('\n')
						buildUid = buildUid.replace("'","")
						print buildUid
					if "revision: " in line:
                                		revisionNumber = line.split('revision: ')[1].strip('\n')
						revisionNumber = revisionNumber.replace("'","")
						print revisionNumber
						break
				#	step_block = re.search(step_block_pattern,line)
				#	if step_block is not None:
				#		# in a step block
				#		s = re.search('^=========\sStarted\s(.*)\s\(results:\s(\d*),\selapsed:\s(\d*\ssecs)\)\s\(at\s(.*)?\)\s=========$',line)
				#		if s is not None:
				#			step_name = s.group(1)
				#			talos = 0
				#			if "talos" in step_name:
				#				talos = 1
				#			results = s.group(2)
				#			elapsed = s.group(3)
				#			start_time = s.group(4)
				#
				#		statement = "INSERT INTO build_steps (buildid,build_step,talos,elapsed_time,starttime,results) VALUES ('"+str(buildid).replace("'","")+"','"+str(step_name).replace("'","")+"','"+str(talos)+"','"+str(elapsed)+"','"+str(start_time)+"','"+str(results)+"')"
				#		print statement+'\n'
				#		cursor.execute(statement)
				#		conn.commit()
			else:
				print "Not a text file. "+name
#cursor.close()
#conn.close()
#del cursor

#create table build_all(builder text, slave text, starttime text, results text, buildid text, builduid text, revision text, elapsed_time text);
