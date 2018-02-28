# -*- coding: utf-8 -*-
"""
Created on Tue May 16 14:22:55 2017

@author: musfiqur
"""

### PHP to Python

import os
import psycopg2, fnmatch
import pandas as pd
import re
import sys, traceback

root_dir = "/home/rupak/crash_analysis/"
dest_dir = "/home/rupak/firefox_crash_rpt/"

connect_db = psycopg2.connect("dbname='firefox_build_crash' user='rupak' host='localhost' password='karmadhar'")
connect_db.autocommit = True
cursor = connect_db.cursor()

def unzip_file():
    crash_reports = []
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, '*.gz'):
            crash_reports.append(os.path.join(root, filename))
    
    for report in crash_reports:
        os.system("mkdir " + dest_dir + str(report).split("crash_analysis/")[1].split("/")[0])
	d = str(report).split("crash_analysis/")[1].split(".gz")[0]
        os.system("gunzip -c " + str(report) + " > " + dest_dir + d)
        print "Processing: " + dest_dir + d
	prepare_query(dest_dir + d)
	#connect_db.commit()
	print "Deleting..."
	#os.system("rm -rf " + dest_dir + str(report).split("crash_analysis/")[1].split("/")[0])
	#os.system("rm -rf " + str(report))
        
def prepare_query(data_file):
    df = pd.read_csv(data_file, sep='\t', error_bad_lines=False, low_memory = False)
    data_list = df.values.tolist()
    if (df.shape)[1] == 21:
        sql = "INSERT INTO fx_crash (signature, url, uuid_url, client_crash_date, date_processed, last_crash, product, version, build, branch, os_name, os_version, cpu_info, address, bug_list, user_comments, uptime_seconds, adu_count, topmost_filenames, addons_checked) VALUES ("
        #$signature = $a[0]; $url = $a[1]; $client_crash_date = $a[3]; $date_processed = $a[4]; $last_crash = $a[5]; $product = $a[6];
        #$version = $a[7]; $build = $a[8]; $branch = $a[9]; $os_name = $a[10]; $os_version = $a[11]; $cpu_info = $a[12]; $address = $a[13]; $bug_list = $a[14];
        #$user_comments = $a[15]; $uptime_seconds = $a[16]; $adu_count = $a[18]; $topmost_filenames = $a[19]; $addons_checked = $a[20];
        #$flash_version = $a[21]; $hangid = $a[22]; $reason = $a[23]; $process_type = $a[24]; $app_notes = $a[25]; $install_age = $a[26]; $duplicate_of = $a[27];
        #$release_channel = $a[28]; $product_id = $a[29];

	for row in data_list:
            for i in range (0,21):
		if i==2:
                    uuidurl = row[i]
		if i==17:
		    continue
                elif i<20:
                    sql += "'" + re.escape(str(row[i])) + "',"
                else:
                    sql += "'" + re.escape(str(row[i])) + "')"
	    cursor.execute("SELECT COUNT(*) FROM fx_crash WHERE uuid_url = '" + uuidurl + "'")
            result = cursor.fetchone()
            if result[0]>0:
                print "Already exists.\n"
            else:
		print sql
                #insert_into_db(sql)
        
    if (df.shape)[1] == 20:
        sql = "INSERT INTO fx_crash (signature, url, uuid_url, client_crash_date, date_processed, last_crash, product, version, build, branch, os_name, os_version, cpu_info, address, bug_list, user_comments, uptime_seconds, adu_count, topmost_filenames) VALUES ("
        for row in data_list:
            for i in range (0,20):
		if i==2:
                    uuidurl = row[i]
		if i==17:
                    continue
                elif i<19:
                    sql += "'" + re.escape(unicode(str(row[i]), "utf-8")) + "',"
                else:
                    sql += "'" + re.escape(unicode(str(row[i]), "utf-8")) + "')"
	    cursor.execute("SELECT COUNT(*) FROM fx_crash WHERE uuid_url = '" + uuidurl + "'")
            result = cursor.fetchone()
            if result[0]>0:
                print "Already exists.\n"
            else:
		print sql
                #insert_into_db(sql)

    if (df.shape)[1] == 15:
        sql = "INSERT INTO fx_crash (signature, url, uuid_url, client_crash_date, date_processed, last_crash, product, version, build, branch, os_name, os_version, cpu_info, address, bug_list) VALUES ("
        for row in data_list:
            for i in range (0,15):
		if i==2:
                    uuidurl = row[i]
                elif i<14:
                    sql += "'" + re.escape(unicode(str(row[i]), "utf-8")) + "',"
                else:
                    sql += "'" + re.escape(unicode(str(row[i]), "utf-8")) + "')"
	    cursor.execute("SELECT COUNT(*) FROM fx_crash WHERE uuid_url = '" + uuidurl + "'")
            result = cursor.fetchone()
            if result[0]>0:
                print "Already exists.\n"
            else:
		print sql
                #insert_into_db(sql)

    if (df.shape)[1] == 26:
        sql = "INSERT INTO fx_crash (signature, url, uuid_url, client_crash_date, date_processed, last_crash, product,version, build, branch, os_name, os_version, cpu_info, address, bug_list, user_comments, uptime_seconds, adu_count, topmost_filenames, addons_checked, flash_version, hangid, reason, process_type, app_notes) VALUES ("
        for row in data_list:
            for i in range (0,26):
		if i==2:
                    uuidurl = row[i]
		if i==17:
                    continue
                elif i<25:
                    sql += "'" + re.escape(unicode(str(row[i]), "utf-8")) + "',"
                else:
                    sql += "'" + re.escape(unicode(str(row[i]), "utf-8")) + "')"
            cursor.execute("SELECT COUNT(*) FROM fx_crash WHERE uuid_url = '" + uuidurl + "'")
            result = cursor.fetchone()
            if result[0]>0:
                print "Already exists.\n"
            else:
		print sql
                #insert_into_db(sql)

    if (df.shape)[1] == 30:
        sql = "INSERT INTO fx_crash (signature, url, uuid_url, client_crash_date, date_processed, last_crash, product, version, build, branch, os_name, os_version, cpu_info, address, bug_list, user_comments, uptime_seconds, adu_count, topmost_filenames, addons_checked, flash_version,hangid, reason, process_type, app_notes, install_age, duplicate_of, release_channel, productid) VALUES ("
	for row in data_list:
            for i in range (0,30):
		if i==2:
		    uuidurl = row[i]
		if i==17:
                    continue
                elif i<29:
                    sql += "'" + re.escape(unicode(str(row[i]), "utf-8")) + "',"
                else:
                    sql += "'" + re.escape(unicode(str(row[i]), "utf-8")) + "')"
	    print "SELECT COUNT(*) FROM fx_crash WHERE uuid_url = '" + uuidurl + "'"
	    #cursor.execute("SELECT COUNT(*) FROM fx_crash WHERE uuid_url = '" + uuidurl + "'")
	    #result = cursor.fetchone()
	    #print result[0]
	    sys.exit(0)
	    if result[0]>0:
	        print "Already exists.\n"
            else:
		print sql
		#insert_into_db(sql)

def insert_into_db(query):
    try:
        cursor.execute(query)

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        print '\nCould not dump data!\n'

unzip_file()

if connect_db:
    connect_db.close() 
