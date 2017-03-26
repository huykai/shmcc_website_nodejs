# -*- coding: utf-8 -*-

import sys
#import cx_Oracle
import time
#import smtplib 
import cgi
#import xlsxwriter,xlrd
import MySQLdb as mysql

import os
import json


reload(sys)
sys.setdefaultencoding("utf-8")


from MME_statis_mysql import *
#from SAEGW_statis import *

#to_list=["13802500663@139.com"]
#to_list=[]


def sort(A, num):
     for i in range(len(A)) :
         (A[i][0],A[i][num])=(A[i][num],A[i][0])
     A.sort()
     #for i in range(len(A)):
     #    (A[i][0],A[i][num])=(A[i][num],A[i][0])
         
def writexmlhead():
	#print 'Status: 200 OK'
	#print 'Content-type: text/xml charset=GB2312;\n'
 

    print "<?xml version=\"1.0\" encoding=\"GB2312\"?>"
    print "<response>"

def writexmltablebegin(tablename):
    print "<"+tablename+">"
def writexmltableend(tablename):
    print "</"+tablename+">"

def writexmltail():
	print "</response>"

def writetabname(tabname):
	print u"<TabName>"
	print u"<name>" + tabname + u"</name>"
	print u"</TabName>"

def writetitle(title):
	print u"<Title>"
	for titleitem in title:
		print u"<name>" + titleitem + u"</name>"
	print u"</Title>"

def writedata(rows):
	for row in rows:
		print "<Item>"
		for rowitem in row:
			print "<ItemCol>"
			print "<value>"
			print rowitem
			print "</value>"
			print "</ItemCol>"
		print "</Item>"
		
if __name__ == '__main__':

    # Create instance of FieldStorage 
    form = cgi.FieldStorage()
    
    #logfile = open('logfile.txt','a')

    #logtext = str(form.
    #logfile.write('\n')
    #logfile.write(str(len(sys.argv)))
    #logfile.write(str(sys.argv[1]))
    #logfile.close()
    #config_params = json.loads(str(sys.argv[1]))
    #logfile.write('\n')
    #logfile.write(json.dumps(config_params))

    #define sql param
    param = PmSqlParam()
	
    stopdate = time.strftime('%Y/%m/%d',time.localtime(time.time()))
    startdate = time.strftime('%Y/%m/%d',time.localtime(time.time()-3600))
    curtime = time.strftime('%H',time.localtime(time.time()))
    curtime = curtime+":00"
    pretime = time.strftime('%H',time.localtime(time.time()-3600))
    pretimr = pretime+":00"
    
    # for test , I only have some days data, so I will adjust the stopdate
    startdate = '2017/02/11' 
    if (curtime < '01:00'):
        stopdate = '2017/02/12'
    else:
        stopdate = '2017/02/11'

    param.starttime=pretime
    param.stoptime=curtime
    param.startdate=startdate
    param.stopdate=stopdate

    #print pretime
    #print curtime
    #print startdate
    #print stopdate
	
    # connect to mysql
    (mmedbuser,mmedbpasswd,mmedburl,mmedburlport,mmedb_dbname)=getdbconfig("mmedb_mysql")
    
    con = None

    try:
        con = mysql.connect(host=mmedburl, port=int(mmedburlport), user=mmedbuser, passwd=mmedbpasswd, db=mmedb_dbname)
        mmecursor=con.cursor()
        writexmlhead()
        writexmltablebegin('mme_2g_attach')

	    #2g attach
        title,row=mme_2g_attach(mmecursor,param)
        if title[0]!='error' and len(row)>0:
            #title[0]='tt'+form.getvalue('starttime')
            writetabname('mme_2g_attach')
            writetitle(title)
            writedata(row)
        writexmltableend('mme_2g_attach')
        
        #2g pdp
        writexmltablebegin('mme_2g_pdp')
        mmecursor=con.cursor()
        title,row=mme_2g_pdp(mmecursor,param)
        if title[0]!='error' and len(row)>0:
            #title[0]='tt'+form.getvalue('starttime')
            writetabname('mme_2g_pdp')
            writetitle(title)
            writedata(row)
        writexmltableend('mme_2g_pdp')
        writexmltail()
	
        
    except mysql.Error, e:
  
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if con:
            con.close()

    #if (logfile):
    #    logfile.close()
	
	