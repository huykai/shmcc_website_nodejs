# -*- coding: utf-8 -*-

import sys
import cx_Oracle
import time
#import smtplib 
import cgi
#import xlsxwriter,xlrd
import MySQLdb as mysql

import os
import json
import logging

logging.basicConfig(filename='pm_logger.log', level=logging.INFO)

reload(sys)
sys.setdefaultencoding("utf-8")


#from MME_statis_mysql import *
from MME_statis_new import *
from SAEGW_statis_new import *



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

def getforminfo(params,formparams):
    # Get data from formparams
    configs = json.loads(formparams)
    logging.info("formparams : " + formparams)
    #print configs
    for key, item in configs.items():
        #print key," : ",item
        params.__dict__[key] = item
    
    if (params.kpilist == None):
        params.kpilist = 'ALL'
    if (params.selectperiod == None):
        params.selectperiod = '15'
    if (params.selectperiodtype == None):
        params.selectperiodtype = 'continue'
    if (params.isMME):
        if (params.selectmmesgsn == None):
            params.selectmmesgsn = 'all'
        if (params.selectmmeelement == None):
            params.selectmmeelement = 'MME'
    else :
        if (params.selectsaegwggsn == None):
            params.selectsaegwggsn = 'all'
        if (params.selectsaegwelement == None):
            params.selectsaegwelement = 'SAEGW'
    
def paramsdate_fix():
    # adjust per environment in test or prod
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
    
def prn_obj(obj):
    return '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])

def run_kpi(kpi_title, kpi_function, cursor, param):
    
    writexmltablebegin(kpi_title)

    title,row=kpi_function(kpi_title, cursor, param)
    if title[0]!='error' and len(row)>0:
        #title[0]='tt'+form.getvalue('starttime')
        writetabname(kpi_title)
        writetitle(title)
        writedata(row)
        #pass
    writexmltableend(kpi_title)

if __name__ == '__main__':

    logging.info('query time : ' + time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time())))

    formparams = None
    runmode = 'test'
    if ( len(sys.argv) ) > 2 :
        logging.info("\t run mode : " + str(sys.argv[1])) 
        logging.info("\t params : " + str(sys.argv[2])) 
        #print("\t params : " + str(sys.argv[1])) 
        runmode = sys.argv[1]
        formparams = sys.argv[2]
       
    param = PmSqlParam()

    if (not formparams is None):
        try:
            getforminfo(param, formparams)
            logging.info('\tparams info : ' + prn_obj(param))
        except Exception, e:
            logging.error('error in param get.' )
    else:
        logging.info('form params is None.')
    #sys.exit()
    
    # for test
    #paramsdate_fix()

    # connect to mysql
    #(mmedbuser,mmedbpasswd,mmedburl,mmedburlport,mmedb_dbname)=getdbconfig("mmedb_mysql")
    # connect to oracle
    if (param.isMME == "true"):
        (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(runmode, "mmedb")
    else:
        (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(runmode, "saegwdb")
    #print 'mmeuser:', mmedbuser, mmedbpasswd, mmedburl
	#mmedb = cx_Oracle.connect('omc', 'omc', '127.0.0.1:51063/oss')
    con = None

    try:
        # mysql
        #con = mysql.connect(host=mmedburl, port=int(mmedburlport), user=mmedbuser, passwd=mmedbpasswd, db=mmedb_dbname)
        #mmecursor=con.cursor()
        # oracle
        #print dbuser, dbpasswd, dburl
	    #mmedb = cx_Oracle.connect('omc', 'omc','10.221.255.4:1521/oss') 

        db = cx_Oracle.connect(dbuser, dbpasswd, dburl)
        dbcursor=db.cursor()
    
        writexmlhead()
        #print "kpilist: ", param.kpilist
        if (param.isMME == "true"):
            #print("param.isMME : " + param.isMME)
            api_sql_function = mme_api_sql_function
        else:
            api_sql_function = saegw_api_sql_function

        for kpi in param.kpilist.split(','):
            logging.info('kpi : ' + kpi)
            #print 'kpi : ' + kpi
            
            kpi_function = api_sql_function[kpi]['func']
            run_kpi(kpi, kpi_function, dbcursor, param)
        
        writexmltail()
        
    except mysql.Error, e:
        logging.error("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)
    finally:
        if con:
            con.close()

    #if (logfile):
    #    logfile.close()
	
	
