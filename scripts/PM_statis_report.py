# -*- coding: utf-8 -*-

import sys
import cx_Oracle
import time
import smtplib 
import cgi
import xlsxwriter,xlrd

import os


reload(sys)
sys.setdefaultencoding( "utf-8" )


from MME_statis import *
from SAEGW_statis import *

#to_list=["13802500663@139.com"]
to_list=[]


def sort(A,num):
     for i in range(len(A)):
         (A[i][0],A[i][num])=(A[i][num],A[i][0])
     A.sort()
     #for i in range(len(A)):
     #    (A[i][0],A[i][num])=(A[i][num],A[i][0])
         
def writexmlhead():
	print 'Status: 200 OK'
	print 'Content-type: text/xml charset=GB2312;\n'


	print "<?xml version=\"1.0\" encoding=\"GB2312\"?>"
	print "<response>"

def writexmltail():
	print "</response>"

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
	#print form

	#define sql param
	param=pm_sql_param()
	
	stopdate=time.strftime('%Y/%m/%d',time.localtime(time.time()))
	startdate=time.strftime('%Y/%m/%d',time.localtime(time.time()-3600))
	curtime=time.strftime('%H',time.localtime(time.time()))
	curtime=curtime+":00"
	pretime=time.strftime('%H',time.localtime(time.time()-3600))
	pretimr=pretime+":00"
	#db = cx_Oracle.connect('omc', 'omc', '10.221.255.4:1521/OSS')
	(mmedbuser,mmedbpasswd,mmedburl)=getdbconfig("mmedb")
	#print mmedbuser,mmedbpasswd,mmedburl
	mmedb = cx_Oracle.connect('omc', 'omc', '127.0.0.1:51063/oss')
	#mmedb = cx_Oracle.connect(mmedbuser, mmedbpasswd, mmedburl)
	mmecursor=mmedb.cursor()
	(saegwdbuser,saegwdbpasswd,saegwdburl)=getdbconfig("saegwdb")
	#saegwdb = cx_Oracle.connect('kiu', 'antkiu123', '127.0.0.1:51064/OSS')
	#saegwdb = cx_Oracle.connect(saegwdbuser, saegwdbpasswd, saegwdburl)
	#saegwcursor=saegwdb.cursor()
	 #begin xlsx generate
	curtimehour=time.strftime('%Y%m%d%H',time.localtime(time.time()))
	curtimestr=curtimehour+":00"
	pretimehour=time.strftime('%Y%m%d%H',time.localtime(time.time()-3600))
	pretimestr=pretimehour+":00"
	
	param.starttime=pretime
	param.stoptime=curtime
	param.startdate=startdate
	param.stopdate=stopdate
	
	writexmlhead()

	#2g attach
	title,row=mme_2g_attach(mmecursor,param)
	if title[0]!='error' and len(row)>0:
		#title[0]='tt'+form.getvalue('starttime')
		writetitle(title)
		writedata(row)

	#print result
	
	writexmltail()
	
	#if __name__ == '__main__':
	#    if send_mail(mailto_list,"subject","content"):
	#        print "Send succ!"
	#    else:
	#        print "Send Fail!"
	
	