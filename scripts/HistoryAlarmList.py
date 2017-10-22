#coding=utf-8

import cgi
import cx_Oracle
import time
import os
import json
import logging

from GetConfig import *

logging.basicConfig(filename='alarm_logger.log', level=logging.INFO)
reload(sys)
sys.setdefaultencoding("utf-8")

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
    
    if (params.isMME == "true"):
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

def run_query(query_title, cursor, param):
    
    writexmltablebegin(query_title)

    query_function = alarm_sql_function[query_title]['func']
    title,row=query_function(query_title, cursor, param)
    if title[0]!='error' and len(row)>0:
        #title[0]='tt'+form.getvalue('starttime')
        writetabname(query_title)
        writetitle(title)
        writedata(row)
        #pass
    writexmltableend(query_title)

def getSQL_other_oracle(sqlstring, api_sql_info, param):
		
    if (param.isMME == "true"):
        if (param.selectmmesgsn == "Error"):
            param.selectmmesgsn = 'all'
        if (not param.selectmmesgsn == 'all'):
            elementlist = []
            for item in param.selectmmesgsn.split(','):
                elementlist.append('\''+item+'\'')
            sqlstring=sqlstring+" and UTP_COMMON_OBJECTS.co_name in ( "+','.join(elementlist)+" ) " 
    else:
        if (param.selectsaegwggsn == "Error"):
            param.selectsaegwggsn = 'all'
        if (not param.selectsaegwggsn == 'all'):
            elementlist = []
            for item in param.selectsaegwggsn.split(','):
                elementlist.append('\''+item+'\'')
            sqlstring=sqlstring+" and UTP_COMMON_OBJECTS.co_name in ( "+','.join(elementlist)+" ) " 
	

    if (param.alarm_number != 'All'):
        sqlstring = sqlstring + " and alarm_number=\'" + param.alarm_number + "\' "
    if (param.alarm_level != '0'):
        sqlstring = sqlstring + " and severity =\'" + param.alarm_level + "\' "
	

    sqlstringtime=" and to_char(fx_alarm.alarm_time,\'yyyy/mm/dd/hh24:mi\')<\'" + param.stopdate+"/"+param.stoptime + "\' and to_char(fx_alarm.alarm_time,\'yyyy/mm/dd/hh24:mi\')>\'" + param.startdate+"/"+param.starttime + "\' "

    sqlstring1 = ""
    if(len(api_sql_info['sql_group']) != 0):
		sqlstring1 = "\ngroup by " + " , ".join(api_sql_info['sql_group'])
    if(len(api_sql_info['sql_order']) != 0):
    	sqlstring1 = sqlstring1 + "\norder by " + " , ".join(api_sql_info['sql_order'])

    sqlstring=sqlstring+sqlstringtime+sqlstring1
    return sqlstring

# make sql scripts for parts of 'select', 'from', 'where'
def getSQL_main(api_sql_info, param):
    
    #sql_item_type = 'sql_items_' + param.selectperiod + '_' + param.selectmmeelement
    #print('sql_item_type : ',sql_item_type)
    sql_item = api_sql_info['sql_items']['sql_items']
    sqlstring = 'select \n'
    sqlstring = sqlstring + ',\n'.join(sql_item) + '\n'
    sqlstring = sqlstring + 'from ' + ','.join(api_sql_info['sql_tables']) + '\n'
    if (param.isMME == "true"):
        sqlstring = sqlstring + 'where ' + ' and '.join(api_sql_info['sql_where_mme']) + '\n'
    else:
        sqlstring = sqlstring + 'where ' + ' and '.join(api_sql_info['sql_where_saegw']) + '\n'
    return sqlstring

# Alarm Query
def alarm_query(query_title, cursor, param):
	
    sqlstring = ""
    #print('alarm_query:' + query_title)
    api_sql_info = alarm_sql_function[query_title]
    #print(api_sql_info)
    sqlstring = getSQL_main(api_sql_info, param)
    sqlstring = getSQL_other_oracle(sqlstring, api_sql_info, param)
    #print(sqlstring)
    cursor.execute(sqlstring)
    row = cursor.fetchall()
    return (api_sql_info['title'],row)

alarm_sql_function = {
    'ALARM_QUERY_DETAIL'     : {
        'func'         : alarm_query,
        'title'        : [
                        u"设备名称",
                        u"设备域名",
						u"告警号",
                        u"发生时间",
						u"清除时间",
                        u"告警状态",
                        u"告警类型",
						u"告警级别",
                        u"告警文本",
                        u"补充内容"
        ],
        'sql_items'      : {
            'sql_items' : [
				"UTP_COMMON_OBJECTS.co_name",
				"DN",
				"alarm_number",
				"alarm_time",
                "cancel_time",
				"alarm_status",
				"alarm_type",
				"severity",
				"text",
				"fx_alarm.SUPPLEMENTARY_INFO"
		   ]
        },
        'sql_tables' : [
			'fx_alarm',
			'objects',  
            'UTP_COMMON_OBJECTS'
        ],     
        'sql_where_mme' : [ 
            'UTP_COMMON_OBJECTS.CO_GID=fx_alarm.ne_gid',
			'objects.int_id = UTP_COMMON_OBJECTS.co_int_id',
			'objects.object_class in (463,3766)'
        ],
		'sql_where_saegw' : [ 
            'UTP_COMMON_OBJECTS.CO_GID=fx_alarm.ne_gid',
			'objects.int_id = UTP_COMMON_OBJECTS.co_int_id',
			'objects.object_class = 3529'
        ],
        'sql_group' : [],
        'sql_order' : []
    },
	'ALARM_QUERY_SUMMARY'     : {
        'func'         : alarm_query,
        'title'        : [
                        u"设备名称",
                        u"告警号",
                        u'告警数量',
                        u"告警类型",
						u"告警级别",
                        u"告警文本"
        ],
        'sql_items'      : {
            'sql_items' : [
				"UTP_COMMON_OBJECTS.co_name",
				"alarm_number",
				'count(*)',
				"min(alarm_type)",
				"min(severity)",
				"min(text)"
		   ]
        },
        'sql_tables' : [
			'fx_alarm',
			'objects',  
            'UTP_COMMON_OBJECTS'
        ],     
        'sql_where_mme' : [ 
            'UTP_COMMON_OBJECTS.CO_GID=fx_alarm.ne_gid',
			'objects.int_id = UTP_COMMON_OBJECTS.co_int_id',
			'objects.object_class in (463,3766)'
        ],
		'sql_where_saegw' : [ 
            'UTP_COMMON_OBJECTS.CO_GID=fx_alarm.ne_gid',
			'objects.int_id = UTP_COMMON_OBJECTS.co_int_id',
			'objects.object_class = 3529'
        ],
		'sql_group' : [ 
            'UTP_COMMON_OBJECTS.CO_NAME',
			'alarm_number'
        ],
		'sql_order' : [ 
            'UTP_COMMON_OBJECTS.CO_NAME',
            'count(*) desc',
			'min(alarm_type) desc',
			'min(severity) asc'
        ]
    }
}


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
       
    param = AlarmSqlParam()

    if (not formparams is None):
        try:
            getforminfo(param, formparams)
            logging.info('\tparams info : ' + prn_obj(param))
        except Exception, e:
            logging.error('error in param get.' )
    else:
        logging.info('form params is None.')
    
	#print('dbparams:'+dbuser+dbpasswd+dburl+dburlport+db_dbname)
    if (param.isMME == "true"):
        (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(runmode, "mmedb")
    else:
        (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(runmode, "saegwdb")
    
    con = None

    try:
        
        db = cx_Oracle.connect(dbuser, dbpasswd, dburl)
        dbcursor=db.cursor()
    
        writexmlhead()
        #print "kpilist: ", param.kpilist
        
        #print('param.isAlarmDetail:' +param.isAlarmDetail)
        if(param.isAlarmDetail == "true"):
            run_query("ALARM_QUERY_DETAIL", dbcursor, param)
        else:
            run_query("ALARM_QUERY_SUMMARY", dbcursor, param)

        
			
        writexmltail()
        
    except Exception as e:
        logging.error("Error %s" % e.args[0])
        sys.exit(1)
    finally:
        if con:
            con.close()


