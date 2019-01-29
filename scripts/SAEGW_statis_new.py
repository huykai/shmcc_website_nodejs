#coding=utf-8

from GetConfig import *
from ReportSuite_SQL import *

def getSAEGWSQL_other_oracle(sqlstring, param, groupitem = ""):
    if (not param.selectsaegwggsn == 'all'):
        elementlist = []
        for item in param.selectsaegwggsn.split(','):
            elementlist.append('\''+item+'\'')
        sqlstring=sqlstring+" and objects.co_name in ( "+','.join(elementlist)+" ) " 
	
    if (param.selectperiodtype=='continue'):
        sqlstringtime=" and to_char(sgw.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
        "\' and to_char(sgw.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
    else:
        sqlstringtime=" and to_char(sgw.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
        "\' and to_char(sgw.period_start_time,\'hh24\')>=\'"+param.starttime+\
        " and to_char(sgw.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
        "\' and to_char(sgw.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
	
    if (groupitem != ""):
        groupitem = " " + groupitem +","
    if (param.selectperiod=='60'):
        if (param.selectsaegwelement=='SAEGW'):
            sqlstring1="group by to_char(sgw.period_start_time,'yyyy/mm/dd'), to_char(sgw.period_start_time,'hh24'), sgw.fing_id, " + groupitem + " objects.co_name " + "order by objects.co_name,to_char(sgw.period_start_time,'yyyy/mm/dd'),to_char(sgw.period_start_time,'hh24')"
        else:
            sqlstring1="group by to_char(sgw.period_start_time,'yyyy/mm/dd'), to_char(sgw.period_start_time,'hh24'), sgw.fing_id, " + groupitem + " objects.co_name, SSPROF_ID " + "order by objects.co_name,to_char(sgw.period_start_time,'yyyy/mm/dd'),to_char(sgw.period_start_time,'hh24')"
    else:
        if (param.selectsaegwelement=='SAEGW'):
            sqlstring1="group by to_char(sgw.period_start_time,'yyyy/mm/dd'),to_char(sgw.period_start_time,'hh24:mi'), sgw.fing_ID, " + groupitem + " objects.co_name " +  "order by objects.CO_name,to_char(sgw.period_start_time,'yyyy/mm/dd'),to_char(sgw.period_start_time,'hh24:mi') "
        else:
            sqlstring1="group by to_char(sgw.period_start_time,'yyyy/mm/dd'),to_char(sgw.period_start_time,'hh24:mi'), sgw.fing_ID, " + groupitem + " objects.co_name,SSPROF_ID  " + "order by objects.CO_name,to_char(sgw.period_start_time,'yyyy/mm/dd'),to_char(sgw.period_start_time,'hh24:mi') "

    sqlstring=sqlstring+sqlstringtime+sqlstring1
    return sqlstring

def getSAEGWSQL_other_mysql(sqlstring, param, groupitem = ""):
	if (not param.selectsaegwggsn == 'all'):
		elementlist = []
		for item in param.selectsaegwggsn.split(','):
			elementlist.append('\"'+item+'\"')
		sqlstring=sqlstring+" and objects.co_name in ( "+','.join(elementlist)+" ) " 
	
	if (param.selectperiodtype=='continue'):
		sqlstringtime=" and date_format(sgw.period_start_time,\'%Y/%m/%d/%H/%i\')>=\'"+param.startdate+"/"+param.starttime+\
		"\' and date_format(sgw.period_start_time,\'%Y/%m/%d/%H/%i\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
	else:
		sqlstringtime=" and date_format(sgw.period_start_time,\'%Y/%m/%d\')>=\'"+param.startdate+\
		"\' and date_format(sgw.period_start_time,\'%H\')>=\'"+param.starttime+\
		" and date_format(sgw.period_start_time,\'%Y/%m/%d\')<=\'"+param.stopdate+\
		"\' and date_format(sgw.period_start_time,\'%H\')<=\'"+param.stoptime + "\' "
		
	if (param.selectperiod=='60'):
		sqlstring1=" group by date_format(sgw.period_start_time,\'%Y/%m/%d\'), date_format(sgw.period_start_time,\'%H\'), sgw.fins_id, objects.co_name " + groupitem + " " + "order by objects.co_name,date_format(sgw.period_start_time,\'%Y/%m/%d\'),date_format(sgw.period_start_time,\'%H\')"
	else:
		sqlstring1=" group by date_format(sgw.period_start_time,\'%Y/%m/%d\'),date_format(sgw.period_start_time,\'%H/%i'), sgw.fins_ID, objects.co_name " + groupitem + " " + "order by date_format(sgw.period_start_time,\'%Y/%m/%d\'),date_format(sgw.period_start_time,\'%H/%i\')"
	sqlstring=sqlstring+sqlstringtime+sqlstring1
	return sqlstring

# generate table part of sql, table can be a single table name or a (select ...) statement
def generateTableStr(tabledescs, param):
    return_desc = []
    for tabledesc in tabledescs:
        if (isinstance(tabledesc, str)):
            return_desc.append(tabledesc)
        else:
            sqlstring = getSAEGWSQL_main(tabledesc, param)
            sqlstring = getSAEGWSQL_other_oracle(sqlstring, param)
            return_desc.append("( \n%s\n ) %s" % (sqlstring, tabledesc['table_name']))
    return return_desc

# make sql scripts for parts of 'select', 'from', 'where'
def getSAEGWSQL_main(api_sql_info, param):
    sql_item_type = 'sql_items_' + param.selectperiod + '_' + param.selectsaegwelement
    #print('sql_item_type : ',sql_item_type)
    sql_item = api_sql_info['sql_items'][sql_item_type]
    sqlstring = 'select \n'
    sqlstring = sqlstring + ',\n'.join(sql_item) + '\n'
    sqlstring = sqlstring + 'from ' + ','.join(generateTableStr(api_sql_info['sql_tables'], param)) + '\n'
    sqlstring = sqlstring + 'where ' + ' and '.join(api_sql_info['sql_where']) + '\n'
    return sqlstring

# RUN Script get from report suite
def saegw_reportsuite(kpi_title, cursor, param):
    sqlstring = []
    
    try:
        sqlstring = create_reportsuite_sql(param)
        api_sql_info = saegw_api_sql_function[kpi_title]
        #print('saegw_reportsuite sqlstring: ' , sqlstring)
        droptemptable_sqlstrings = sqlstring['droptemptable']
        createtemptable_sqlstrings = sqlstring['createtemptable']
        selecttemptable_sqlstring = sqlstring['selecttemptable'][0] 
        #print "droptemptable_sqlstrings: " + droptemptable_sqlstrings
        for drop_command in droptemptable_sqlstrings:
            print "drop_command: " , drop_command
            try:
                cursor.execute(drop_command)
            except Exception as e:
                print 'saegw_reportsuite droptable catch Error: ' + str(e)    
        print "after execute droptemptable" 
        #print "createtemptable_sqlstring: " + createtemptable_sqlstrings
        for create_command in createtemptable_sqlstrings:
            print "create_command: " , create_command
            try:
                cursor.execute(create_command)
            except Exception as e:
                print 'saegw_reportsuite createtable catch Error: ' + str(e)    
        print "after execute createtemptable"
        print "selecttemptable_sqlstring: " + selecttemptable_sqlstring
        cursor.execute(selecttemptable_sqlstring)
        print "after execute selecttemptable"
        row=cursor.fetchall()
        print 'saegw_reportsuite: ', row
        return ([kpi_title],row)
    except Exception as e:
        print 'saegw_reportsuite catch Error: ' + str(e)
        errorMessage = "Error saegw_reportsuite: " + str(e)
        return (['error', errorMessage], None)


# SAEGW PGW
def saegw_4g_pgw(kpi_title, cursor, param):
	
    sqlstring = ""
    
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_4g_pgw: " + str(e)
        return (['error', errorMessage], None)
# SAEGW SGW
def saegw_4g_sgw(kpi_title, cursor, param):

    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_4g_sgw: " + str(e)
        return (['error', errorMessage], None)
	
def saegw_4g_cdr_radius(kpi_title,cursor,param):

    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_4g_cdr_radius: " + str(e)
        return (['error', errorMessage], None)

# SGW THROUGHPUT
def pgw_sgw_throughput(kpi_title,cursor,param):
    
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error pgw_sgw_throughput: " + str(e)
        return (['error', errorMessage], None)	

def saegw_gtpu_throughput(kpi_title,cursor,param):
    # GSM PDP 3G
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_gtpu_throughput: " + str(e)
        return (['error', errorMessage], None)	

def saegw_s1u_throughput(kpi_title,cursor,param):
	# GSM PDP 3G
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_s1u_throughput: " + str(e)
        return (['error', errorMessage], None)	
		
def saegw_session(kpi_title,cursor,param):
	# GSM PAGING 3G
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_session: " + str(e)
        return (['error', errorMessage], None)	
		
def saegw_sgi_throughput(kpi_title,cursor,param):
    # GSM users 4G
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_sgi_throughput: " + str(e)
        return (['error', errorMessage], None)	

def saegw_ip_pool(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    #param['groupitem'] = "perpool_id"
    try:
        sqlstring = getSAEGWSQL_other_oracle(sqlstring,param, "perpool_id")
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_ip_pool: " + str(e)
        return (['error', errorMessage], None)

def saegw_downdata_notice(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print ("%s sqlstring is: \n%s\n" % ('saegw_downdata_notice', sqlstring)) 
    #param['groupitem'] = "perpool_id"
    try:
        #sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
        sqlstring = sqlstring + ' \ngroup by ' + ','.join(api_sql_info['sql_group']) \
            + ' \norder by ' + ','.join(api_sql_info['sql_order'])
        #print("%s sqlstring is: \n%s\n" % ('saegw_downdata_notice', sqlstring))
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_downdata_notice: " + str(e)
        return (['error', errorMessage], None)

def saegw_dataforward_succ(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print ("%s sqlstring is: \n%s\n" % ('saegw_downdata_notice', sqlstring)) 
    #param['groupitem'] = "perpool_id"
    try:
        #sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
        sqlstring = sqlstring + ' \ngroup by ' + ','.join(api_sql_info['sql_group']) \
            + ' \norder by ' + ','.join(api_sql_info['sql_order'])
        #print("%s sqlstring is: \n%s\n" % ('saegw_downdata_notice', sqlstring))
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_dataforward_succ: " + str(e)
        return (['error', errorMessage], None)

def saegw_sbcpu(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    #param['groupitem'] = "perpool_id"
    try:
        sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_sbcpu: " + str(e)
        return (['error', errorMessage], None)

def saegw_sabcpu(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    #param['groupitem'] = "perpool_id"
    try:
        sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_sabcpu: " + str(e)
        return (['error', errorMessage], None)

def saegw_pdn(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    #param['groupitem'] = "perpool_id"
    try:
        sqlstring = sqlstring + ' \ngroup by ' + ','.join(api_sql_info['sql_group']) \
            + ' \norder by ' + ','.join(api_sql_info['sql_order'])
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_pdn: " + str(e)
        return (['error', errorMessage], None)

def saegw_createbearer(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    #param['groupitem'] = "perpool_id"
    try:
        sqlstring = sqlstring + ' \ngroup by ' + ','.join(api_sql_info['sql_group']) \
            + ' \norder by ' + ','.join(api_sql_info['sql_order'])
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_createbearer: " + str(e)
        return (['error', errorMessage], None)

def saegw_s11createsession(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring
    #param['groupitem'] = "perpool_id"
    try:
        sqlstring = sqlstring + ' \ngroup by ' + ','.join(api_sql_info['sql_group']) \
            + ' \norder by ' + ','.join(api_sql_info['sql_order'])
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error saegw_s11createsession: " + str(e)
        return (['error', errorMessage], None)

def saegwdb_conn(runmode):
    try:
        (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(runmode, "saegwdb")
        db = cx_Oracle.connect(dbuser, dbpasswd, dburl)
        dbcursor=db.cursor()
        return dbcursor
    except Exception as e:
        return None

saegw_api_sql_function = {
    'SAEGW-REPORTSUITE'     : {
        'func'         : saegw_reportsuite,
    },
    'LTE-PGW'     : {
        'func'         : saegw_4g_pgw,
        'title'        : [
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'Session',
                        u'SAEGW承载容量值',
                        u'PGW承载容量峰值',
                        u'PGW承载容量峰值利用率',
                        u'PGW承载容量平均值',
                        u'PGW承载容量平均利用率',
                        u'PGW专用承载峰值',
                        u'PGW专用承载建立成功次数',
                        u'PGW专用承载建立次数',
                        u'PGW专用承载建立成功率',
                        u'PGW session建立次数',
                        u'PGW session建立成功数',
                        u'PGW session建立成功率',
                        u'PGW 2G PDP成功次数',
                        u'PGW 2G PDP失败次数',
                        u'PGW 2G PDP建立成功率',
                        u'PGW 3G PDP成功次数',
                        u'PGW 3G PDP失败次数',
                        u'PGW 3G PDP建立成功率',
                        u'PGW session去激活数',
                        u'PGW 全部session',
                        u'PGW 2g session',
                        u'PGW 3g session',
                        u'PGW 4g session',
                        u'PGW 234g session',
                        u'PGW Session数',
                        u'SAEGW Session'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')                  BH",
            "'ALL' ",
            "SUM(SM_NBR_ACT_BEAR_SAE_GW) SM_NBR_ACT_BEAR_SAE_GW",
            "SUM(SM_MAX_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW) SM_MAX_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_MAX_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW)/1280000*100,2) SM_MAX_NBR_ACT_BEAR_P_GW_R",
            "SUM(SM_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW) SM_AVE_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW)/1280000*100,2) SM_AVE_NBR_ACT_BEAR_P_GW_R",
            "SUM(SM_MAX_NBR_ACT_DEDIC_BEAR_P_GW) SM_MAX_NBR_ACT_DEDIC_BEAR_P_GW",
            "sum(SM_SUCC_BEARER_ACT) SM_SUCC_BEARER_ACT",
            "sum(SM_ATT_BEARER_ACT) SM_ATT_BEARER_ACT",
            "decode(nvl((sum(SM_ATT_BEARER_ACT)),0),0,0,(round((sum(SM_SUCC_BEARER_ACT)/(sum(SM_ATT_BEARER_ACT))),4)*100)) PdpSR",
            " SUM(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW) PGW_ACT_ATT",
            "SUM(SM_SUCC_SESS_ACT_P_GW) PGW_ACT_SUCC",
            "decode(nvl((sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW)),0),0,0,(round((sum(SM_SUCC_SESS_ACT_P_GW)/(sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW))),4)*100)) PGWSR",
            "SUM(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) SM_SUC_GE_SES_ACT_W_DYNIP_ADR",
            "SUM(SM_FAIL_GE_SES_ACT_W_DYNIP_ADR) SM_FAIL_GE_SES_ACT_W_DYNIP_ADR",
            "to_number(decode((sum(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) + sum(SM_FAIL_GE_SES_ACT_W_DYNIP_ADR)),0,NULL, 100*(sum(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) / (sum(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) + sum(SM_FAIL_GE_SES_ACT_W_DYNIP_ADR)) ))) flng_1025a",
            "SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) SM_SUC_UT_SES_ACT_W_DYNIP_ADR",
            "SUM(SM_FAIL_UT_SES_ACT_W_DYNIP_ADR) SM_FAIL_UT_SES_ACT_W_DYNIP_ADR",
            "to_number(decode((SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) + SUM(SM_FAIL_UT_SES_ACT_W_DYNIP_ADR)),0,NULL, 100*(SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) / (SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) + SUM(SM_FAIL_UT_SES_ACT_W_DYNIP_ADR))) )) flng_1027a",
            "sum(SM_SUCC_SESS_DEACT_GGSN_INIT) deactsession ",
            "sum(SM_NBR_ACT_SESS_P_GW+SM_NBR_ACT_SESS_SAE_GW) allsession",
            "sum(SM_NBR_ACT_SESS_RAT_2G) twogsession",
            "SUM(SM_NBR_ACT_SESS_RAT_3G) threegsession",
            "SUM(SM_NBR_ACT_SESS_RAT_4G) fourgSESSION",
            "SUM(SM_NBR_ACT_SESS_RAT_2G)+SUM(SM_NBR_ACT_SESS_RAT_3G)+SUM(SM_NBR_ACT_SESS_RAT_4G) ttfSESSION",
            "sum(SM_NBR_ACT_SESS_P_GW) allpgwsession",
            "sum(SM_NBR_ACT_SESS_SAE_GW) allsaegwsession"
	      ],
          'sql_items_60_SAEGW' : [
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')                  BH",
            "'ALL' ",
            "round(SUM(SM_NBR_ACT_BEAR_SAE_GW)/4,0) SM_NBR_ACT_BEAR_SAE_GW",
            "round(SUM(SM_MAX_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW)/4,0) SM_MAX_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_MAX_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW)/4/1280000*100,2) SM_MAX_NBR_ACT_BEAR_P_GW_R",
            "round(SUM(SM_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW)/4,0) SM_AVE_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW)/4/1280000*100,2) SM_AVE_NBR_ACT_BEAR_P_GW_R",
            "round(SUM(SM_MAX_NBR_ACT_DEDIC_BEAR_P_GW)/4,0) SM_MAX_NBR_ACT_DEDIC_BEAR_P_GW",
            "sum(SM_SUCC_BEARER_ACT) SM_SUCC_BEARER_ACT", 
            "sum(SM_ATT_BEARER_ACT) SM_ATT_BEARER_ACT", 
            "decode(nvl((sum(SM_ATT_BEARER_ACT)),0),0,0,(round((sum(SM_SUCC_BEARER_ACT)/(sum(SM_ATT_BEARER_ACT))),4)*100)) PdpSR",
            "SUM(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW) PGW_ACT_ATT",
            "SUM(SM_SUCC_SESS_ACT_P_GW) PGW_ACT_SUCC",
            "decode(nvl((sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW)),0),0,0,(round((sum(SM_SUCC_SESS_ACT_P_GW)/(sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW))),4)*100)) PGWSR",
            "SUM(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) SM_SUC_GE_SES_ACT_W_DYNIP_ADR",
            "SUM(SM_FAIL_GE_SES_ACT_W_DYNIP_ADR) SM_FAIL_GE_SES_ACT_W_DYNIP_ADR",
            "to_number(decode((sum(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) + sum(SM_FAIL_GE_SES_ACT_W_DYNIP_ADR)),0,NULL, 100*(sum(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) / (sum(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) + sum(SM_FAIL_GE_SES_ACT_W_DYNIP_ADR)) ))) flng_1025a",
            "SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) SM_SUC_UT_SES_ACT_W_DYNIP_ADR",
            "SUM(SM_FAIL_UT_SES_ACT_W_DYNIP_ADR) SM_FAIL_UT_SES_ACT_W_DYNIP_ADR",
            "to_number(decode((SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) + SUM(SM_FAIL_UT_SES_ACT_W_DYNIP_ADR)),0,NULL, 100*(SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) / (SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) + SUM(SM_FAIL_UT_SES_ACT_W_DYNIP_ADR))) )) flng_1027a",
            "sum(SM_SUCC_SESS_DEACT_GGSN_INIT) deactsession ",
            "round(sum(SM_NBR_ACT_SESS_P_GW+SM_NBR_ACT_SESS_SAE_GW)/4,0) allsession",
            "round(sum(SM_NBR_ACT_SESS_RAT_2G)/4,0) twogsession",
            "round(SUM(SM_NBR_ACT_SESS_RAT_3G)/4,0) threegsession",
            "round(SUM(SM_NBR_ACT_SESS_RAT_4G)/4,0) fourgSESSION",
            "round((SUM(SM_NBR_ACT_SESS_RAT_2G)+SUM(SM_NBR_ACT_SESS_RAT_3G)+SUM(SM_NBR_ACT_SESS_RAT_4G))/4,0) ttfSESSION",
            "round(sum(SM_NBR_ACT_SESS_P_GW)/4,0) allpgwsession",
            "round(sum(SM_NBR_ACT_SESS_SAE_GW)/4,0) allsaegwsession"
           ],
           'sql_items_15_SESSION' : [
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')                  BH",
            "SSPROF_ID SSPROF",
            "SUM(SM_NBR_ACT_BEAR_SAE_GW) SM_NBR_ACT_BEAR_SAE_GW",
            "SUM(SM_MAX_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW) SM_MAX_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_MAX_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW)/1280000*100,2) SM_MAX_NBR_ACT_BEAR_P_GW_R",
            "SUM(SM_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW) SM_AVE_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW)/1280000*100,2) SM_AVE_NBR_ACT_BEAR_P_GW_R",
            "SUM(SM_MAX_NBR_ACT_DEDIC_BEAR_P_GW) SM_MAX_NBR_ACT_DEDIC_BEAR_P_GW",
            "sum(SM_SUCC_BEARER_ACT) SM_SUCC_BEARER_ACT", 
            "sum(SM_ATT_BEARER_ACT) SM_ATT_BEARER_ACT", 
            "decode(nvl((sum(SM_ATT_BEARER_ACT)),0),0,0,(round((sum(SM_SUCC_BEARER_ACT)/(sum(SM_ATT_BEARER_ACT))),4)*100)) PdpSR",
            " SUM(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW) PGW_ACT_ATT",
            "SUM(SM_SUCC_SESS_ACT_P_GW) PGW_ACT_SUCC",
            "decode(nvl((sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW)),0),0,0,(round((sum(SM_SUCC_SESS_ACT_P_GW)/(sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW))),4)*100)) PGWSR",
            "SUM(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) SM_SUC_GE_SES_ACT_W_DYNIP_ADR",
            "SUM(SM_FAIL_GE_SES_ACT_W_DYNIP_ADR) SM_FAIL_GE_SES_ACT_W_DYNIP_ADR",
            "to_number(decode((sum(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) + sum(SM_FAIL_GE_SES_ACT_W_DYNIP_ADR)),0,NULL, 100*(sum(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) / (sum(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) + sum(SM_FAIL_GE_SES_ACT_W_DYNIP_ADR)) ))) flng_1025a",
            "SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) SM_SUC_UT_SES_ACT_W_DYNIP_ADR",
            "SUM(SM_FAIL_UT_SES_ACT_W_DYNIP_ADR) SM_FAIL_UT_SES_ACT_W_DYNIP_ADR",
            "to_number(decode((SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) + SUM(SM_FAIL_UT_SES_ACT_W_DYNIP_ADR)),0,NULL, 100*(SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) / (SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) + SUM(SM_FAIL_UT_SES_ACT_W_DYNIP_ADR))) )) flng_1027a",
            "sum(SM_SUCC_SESS_DEACT_GGSN_INIT) deactsession ",
            "sum(SM_NBR_ACT_SESS_P_GW+SM_NBR_ACT_SESS_SAE_GW) allsession",
            "sum(SM_NBR_ACT_SESS_RAT_2G) twogsession",
            "SUM(SM_NBR_ACT_SESS_RAT_3G) threegsession",
            "SUM(SM_NBR_ACT_SESS_RAT_4G) fourgSESSION",
            "SUM(SM_NBR_ACT_SESS_RAT_2G)+SUM(SM_NBR_ACT_SESS_RAT_3G)+SUM(SM_NBR_ACT_SESS_RAT_4G) ttfSESSION",
            "sum(SM_NBR_ACT_SESS_P_GW) allpgwsession",
            "sum(SM_NBR_ACT_SESS_SAE_GW) allsaegwsession"
	      ],
          'sql_items_60_SESSION' : [
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')                  BH",
            "SSPROF_ID SSPROF",
            "round(SUM(SM_NBR_ACT_BEAR_SAE_GW)/4,0) SM_NBR_ACT_BEAR_SAE_GW",
            "round(SUM(SM_MAX_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW)/4,0) SM_MAX_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_MAX_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW)/4/1280000*100,2) SM_MAX_NBR_ACT_BEAR_P_GW_R",
            "round(SUM(SM_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW)/4,0) SM_AVE_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_NBR_ACT_BEAR_P_GW+SM_NBR_ACT_BEAR_SAE_GW)/4/1280000*100,2) SM_AVE_NBR_ACT_BEAR_P_GW_R",
            "round(SUM(SM_MAX_NBR_ACT_DEDIC_BEAR_P_GW)/4,0) SM_MAX_NBR_ACT_DEDIC_BEAR_P_GW",
            "sum(SM_SUCC_BEARER_ACT) SM_SUCC_BEARER_ACT", 
            "sum(SM_ATT_BEARER_ACT) SM_ATT_BEARER_ACT", 
            "decode(nvl((sum(SM_ATT_BEARER_ACT)),0),0,0,(round((sum(SM_SUCC_BEARER_ACT)/(sum(SM_ATT_BEARER_ACT))),4)*100)) PdpSR",
            "SUM(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW) PGW_ACT_ATT",
            "SUM(SM_SUCC_SESS_ACT_P_GW) PGW_ACT_SUCC",
            "decode(nvl((sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW)),0),0,0,(round((sum(SM_SUCC_SESS_ACT_P_GW)/(sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW))),4)*100)) PGWSR",
            "SUM(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) SM_SUC_GE_SES_ACT_W_DYNIP_ADR",
            "SUM(SM_FAIL_GE_SES_ACT_W_DYNIP_ADR) SM_FAIL_GE_SES_ACT_W_DYNIP_ADR",
            "to_number(decode((sum(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) + sum(SM_FAIL_GE_SES_ACT_W_DYNIP_ADR)),0,NULL, 100*(sum(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) / (sum(SM_SUC_GE_SES_ACT_W_DYNIP_ADR) + sum(SM_FAIL_GE_SES_ACT_W_DYNIP_ADR)) ))) flng_1025a",
            "SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) SM_SUC_UT_SES_ACT_W_DYNIP_ADR",
            "SUM(SM_FAIL_UT_SES_ACT_W_DYNIP_ADR) SM_FAIL_UT_SES_ACT_W_DYNIP_ADR",
            "to_number(decode((SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) + SUM(SM_FAIL_UT_SES_ACT_W_DYNIP_ADR)),0,NULL, 100*(SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) / (SUM(SM_SUC_UT_SES_ACT_W_DYNIP_ADR) + SUM(SM_FAIL_UT_SES_ACT_W_DYNIP_ADR))) )) flng_1027a",
            "sum(SM_SUCC_SESS_DEACT_GGSN_INIT) deactsession ",
            "round(sum(SM_NBR_ACT_SESS_P_GW+SM_NBR_ACT_SESS_SAE_GW)/4,0) allsession",
            "round(sum(SM_NBR_ACT_SESS_RAT_2G)/4,0) twogsession",
            "round(SUM(SM_NBR_ACT_SESS_RAT_3G)/4,0) threegsession",
            "round(SUM(SM_NBR_ACT_SESS_RAT_4G)/4,0) fourgSESSION",
            "round((SUM(SM_NBR_ACT_SESS_RAT_2G)+SUM(SM_NBR_ACT_SESS_RAT_3G)+SUM(SM_NBR_ACT_SESS_RAT_4G))/4,0) ttfSESSION",
            "round(sum(SM_NBR_ACT_SESS_P_GW)/4,0) allpgwsession",
            "round(sum(SM_NBR_ACT_SESS_SAE_GW)/4,0) allsaegwsession"
          ]
        },
        'sql_tables' : [
            'PCOFNG_PS_SSPROF_SSPROF_RAW sgw',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid' 
        ]
    },
    'LTE-SGW'     : {
        'func'         : saegw_4g_sgw,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'SGW承载容量平均值',
                        u'SGW承载容量平均利用率',
                        u'SGW承载容量峰值',
                        u'SGW承载容量峰值利用率',
                        u'SGW缺省承载建立成功次数',
                        u'SGW缺省承载建立次数',
                        u'SGW缺省承载建立成功率',
                        u'SGW专用承载建立成功次数',
                        u'SGW专用承载建立次数',
                        u'SGW专用承载建立成功率',
                        u'SGW 2g 接入数',
                        u'SGW 3g 接入数',
                        u'SGW 4g 接入数',
                        u'SGW 2/3/4g 接入数',
                        u'SGW 4g UE',
                        u'SGW 4g BEARER',
                        u'SGW 4g 激活session'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "sgw.FING_ID",
            "CO_NAME",
            "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(sgw.PERIOD_START_TIME,'hh24:mi')                  BH",
            "SUM(SM_AVE_NBR_ACT_SGW_BEAR) SM_AVE_NBR_ACT_SGW_BEAR",
            "round(SUM(SM_AVE_NBR_ACT_SGW_BEAR)/1280000*100,2) SM_AVE_NBR_ACT_SGW_BEAR_R",
            "SUM(SM_MAX_NBR_ACT_SGW_BEAR) SM_MAX_NBR_ACT_SGW_BEAR",
            "round(SUM(SM_MAX_NBR_ACT_SGW_BEAR)/1280000*100,2) SM_MAX_NBR_ACT_SGW_BEAR_R",
            "SUM(SM_SUCC_BEARER_ACT_MME) SM_SUCC_BEARER_ACT_MME",
            "SUM(SM_ATT_BEARER_ACT_MME) SM_ATT_BEARER_ACT_MME",
            "decode(nvl((SUM(SM_ATT_BEARER_ACT_MME)),0),0,0,(round((SUM(SM_SUCC_BEARER_ACT_MME)/(SUM(SM_ATT_BEARER_ACT_MME))),4)*100)) SM_ATT_BEARER_ratio",
            "SUM(SM_SUCC_DEDIC_BEARER_ACT_S11) SM_SUCC_DEDIC_BEARER_ACT_S11",
            "SUM(SM_ATT_DEDIC_BEARER_ACT_S11) SM_ATT_DEDIC_BEARER_ACT_S11",
            "decode(nvl((SUM(SM_ATT_DEDIC_BEARER_ACT_S11)),0),0,0,(round((SUM(SM_SUCC_DEDIC_BEARER_ACT_S11)/(SUM(SM_ATT_DEDIC_BEARER_ACT_S11))),4)*100)) SM_ATT_DEDIC_ratio",
            "sum(SM_NBR_ACT_SGW_RAT_2G) SGW2G",
            "sum(SM_NBR_ACT_SGW_RAT_3G) SGW3G",
            "sum(SM_NBR_ACT_SGW_RAT_4G) SGW4G",
            "sum(SM_NBR_ACT_SGW_RAT_2G)+sum(SM_NBR_ACT_SGW_RAT_3G)+sum(SM_NBR_ACT_SGW_RAT_4G) SGW234G",
            "sum(SM_AVE_NBR_ACT_S_GW_UE) SGWUE",
            "sum(SM_NBR_ACT_SGW_BEAR) SGWBEAR",
            "sum(SM_NBR_ACT_SGW_SESS) SGWSESSION"           
	      ],
          'sql_items_60_SAEGW' : [
            "sgw.FING_ID",
            "CO_NAME",
            "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(sgw.PERIOD_START_TIME,'hh24')                  BH",
            "round(SUM(SM_AVE_NBR_ACT_SGW_BEAR)/4,0) SM_AVE_NBR_ACT_SGW_BEAR",
            "round(SUM(SM_AVE_NBR_ACT_SGW_BEAR)/4/1280000*100,2) SM_AVE_NBR_ACT_SGW_BEAR_R",
            "round(SUM(SM_MAX_NBR_ACT_SGW_BEAR)/4,0) SM_MAX_NBR_ACT_SGW_BEAR",
            "round(SUM(SM_MAX_NBR_ACT_SGW_BEAR)/4/1280000*100,2) SM_MAX_NBR_ACT_SGW_BEAR_R",
            "round(SUM(SM_SUCC_BEARER_ACT_MME)/4,0) SM_SUCC_BEARER_ACT_MME",
            "round(SUM(SM_ATT_BEARER_ACT_MME)/4,0) SM_ATT_BEARER_ACT_MME",
            "decode(nvl((SUM(SM_ATT_BEARER_ACT_MME)),0),0,0,(round((SUM(SM_SUCC_BEARER_ACT_MME)/(SUM(SM_ATT_BEARER_ACT_MME))),4)*100)) SM_ATT_BEARER_ratio",
            "round(SUM(SM_SUCC_DEDIC_BEARER_ACT_S11)/4,0) SM_SUCC_DEDIC_BEARER_ACT_S11",
            "round(SUM(SM_ATT_DEDIC_BEARER_ACT_S11)/4,0) SM_ATT_DEDIC_BEARER_ACT_S11",
            "decode(nvl((SUM(SM_ATT_DEDIC_BEARER_ACT_S11)),0),0,0,(round((SUM(SM_SUCC_DEDIC_BEARER_ACT_S11)/(SUM(SM_ATT_DEDIC_BEARER_ACT_S11))),4)*100)) SM_ATT_DEDIC__ratio",
            "round(sum(SM_NBR_ACT_SGW_RAT_2G)/4,0) SGW2G",
            "round(sum(SM_NBR_ACT_SGW_RAT_3G)/4,0) SGW3G",
            "round(SUM(SM_NBR_ACT_SGW_RAT_4G)/4,0) SGW4G",
            "round((sum(SM_NBR_ACT_SGW_RAT_2G)+sum(SM_NBR_ACT_SGW_RAT_3G)+sum(SM_NBR_ACT_SGW_RAT_4G))/4,0) SGW234G",
            "round(SUM(SM_AVE_NBR_ACT_S_GW_UE)/4,0) SGWUE",
            "round(sum(SM_NBR_ACT_SGW_BEAR)/4,0) SGWBEAR",
            "round(SUM(SM_NBR_ACT_SGW_SESS)/4,0) SGWSESSION"
           ]
        },
        'sql_tables' : [
            'PCOFNG_PS_SGWP_SGWP_RAW sgw',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid' 
        ]
    },
    'LTE-CDR-RADIUS'     : {
        'func'         : saegw_4g_cdr_radius,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'话单发送量',
                        u'话单重发量',
                        u'PGW Raduis计费请求次数',
                        u'PGW Raduis计费请求成功次数',
                        u'PGW Raduis计费请求成功率'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "sgw.FING_ID",
            "CO_NAME",
            "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(sgw.PERIOD_START_TIME,'hh24:mi')                  BH",
            "SUM(GTPP_DRT_REQUEST_SENT) GTPP_DRT_REQUEST_SENT",
            "SUM(GTPP_PD_DRT_REQUEST_SENT) GTPP_PD_DRT_REQUEST_SENT",
            "SUM(RADIUS_ACCT_RESP_START_REC) radius_recv",
            "SUM(RADIUS_ACCT_REQ_START_SENT) radius_send",
            "decode(nvl((SUM(RADIUS_ACCT_REQ_START_SENT)),0),0,0,(round((SUM(RADIUS_ACCT_RESP_START_REC)/(SUM(RADIUS_ACCT_REQ_START_SENT))),4)*100)) radius_ratio"
	      ],
          'sql_items_60_SAEGW' : [
            "sgw.FING_ID",
            "CO_NAME",
            "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(sgw.PERIOD_START_TIME,'hh24')                  BH",
            "SUM(GTPP_DRT_REQUEST_SENT) GTPP_DRT_REQUEST_SENT",
            "SUM(GTPP_PD_DRT_REQUEST_SENT) GTPP_PD_DRT_REQUEST_SENT",
            "SUM(RADIUS_ACCT_RESP_START_REC) radius_recv",
            "SUM(RADIUS_ACCT_REQ_START_SENT) radius_send",
            "decode(nvl((SUM(RADIUS_ACCT_REQ_START_SENT)),0),0,0,(round((SUM(RADIUS_ACCT_RESP_START_REC)/(SUM(RADIUS_ACCT_REQ_START_SENT))),4)*100)) radius_ratio"
           ]
        },
        'sql_tables' : [
            'PCOFNG_PS_GTPP1_CG_RAW sgw',
            'PCOFNG_PS_RADIUS_RADIUS_RAW radius',
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid',
            'radius.fing_id=objects.co_gid',
            'sgw.PERIOD_START_TIME=radius.PERIOD_START_TIME'
        ]
    },
    'LTE-SGW-THROUGH'     : {
        'func'         : pgw_sgw_throughput,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'SGW用户面下行流量',
                        u'SGW 异PGW接收S5流量',
                        u'PGW 异SGW接收S5流量',
                        u'PGW SGi接口接收流量 ',
                        u'SGW用户面上行流量',
                        u'SGW 异PGW发送S5流量',
                        u'PGW 异SGW发送S5流量',
                        u'PGW SGi接口发送流量',
                        u'PGW数据吞吐容量利用率',
                        u'SGW数据吞吐容量利用率'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')		    BH",
            "round(sum(GTPU_TPDU_BYTES_SENT_S1_U)/1024/1024,0) GTPU_TPDU_BYTES_SENT_S1_U",
            "round(sum(GTPU_TPDU_BYTES_RECV_S5_S_GW)/1024/1024,0) GTPU_TPDU_BYTES_RECV_S5_S_GW",
            "round(sum(GTPU_TPDU_BYTES_SENT_S5_P_GW)/1024/1024,0) GTPU_TPDU_BYTES_SENT_S5_P_GW",
            "round(sum(GTPU_TPDU_BYTES_SENT_S1_U-GTPU_TPDU_BYTES_RECV_S5_S_GW+GTPU_TPDU_BYTES_SENT_S5_P_GW)/1024/1024,0) PGWSGI_RECV",
            "round(sum(GTPU_TPDU_BYTES_RECV_S1_U)/1024/1024,0) GTPU_TPDU_BYTES_RECV_S1_U",
            "round(sum(GTPU_TPDU_BYTES_SENT_S5_S_GW)/1024/1024,0) GTPU_TPDU_BYTES_SENT_S5_S_GW",
            "round(sum(GTPU_TPDU_BYTES_RECV_S5_P_GW)/1024/1024,0) GTPU_TPDU_BYTES_RECV_S5_P_GW",
            "round(sum(GTPU_TPDU_BYTES_RECV_S1_U-GTPU_TPDU_BYTES_SENT_S5_S_GW+GTPU_TPDU_BYTES_RECV_S5_P_GW)/1024/1024,0) PGWSGI_SEND",
            "round(sum(GTPU_TPDU_BYTES_SENT_S1_U-GTPU_TPDU_BYTES_RECV_S5_S_GW+GTPU_TPDU_BYTES_SENT_S5_P_GW+GTPU_TPDU_BYTES_RECV_S1_U-GTPU_TPDU_BYTES_SENT_S5_S_GW+GTPU_TPDU_BYTES_RECV_S5_P_GW)*8/900/40000000000*100,2) PGWSGIALL",
            "round(sum(GTPU_TPDU_BYTES_SENT_S1_U+GTPU_TPDU_BYTES_RECV_S1_U)*8/900/40000000000*100,2) SGWS1UALL" 
	      ],
          'sql_items_60_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')		    BH",
            "round(sum(GTPU_TPDU_BYTES_SENT_S1_U)/1024/1024,0) GTPU_TPDU_BYTES_SENT_S1_U",
            "round(sum(GTPU_TPDU_BYTES_RECV_S5_S_GW)/1024/1024,0) GTPU_TPDU_BYTES_RECV_S5_S_GW",
            "round(sum(GTPU_TPDU_BYTES_SENT_S5_P_GW)/1024/1024,0) GTPU_TPDU_BYTES_SENT_S5_P_GW",
            "round(sum(GTPU_TPDU_BYTES_SENT_S1_U-GTPU_TPDU_BYTES_RECV_S5_S_GW+GTPU_TPDU_BYTES_SENT_S5_P_GW)/1024/1024,0) PGWSGI_RECV",
            "round(sum(GTPU_TPDU_BYTES_RECV_S1_U)/1024/1024,0) GTPU_TPDU_BYTES_RECV_S1_U",
            "round(sum(GTPU_TPDU_BYTES_SENT_S5_S_GW)/1024/1024,0) GTPU_TPDU_BYTES_SENT_S5_S_GW",
            "round(sum(GTPU_TPDU_BYTES_RECV_S5_P_GW)/1024/1024,0) GTPU_TPDU_BYTES_RECV_S5_P_GW",
            "round(sum(GTPU_TPDU_BYTES_RECV_S1_U-GTPU_TPDU_BYTES_SENT_S5_S_GW+GTPU_TPDU_BYTES_RECV_S5_P_GW)/1024/1024,0) PGWSGI_SEND",
            "round(sum(GTPU_TPDU_BYTES_SENT_S1_U-GTPU_TPDU_BYTES_RECV_S5_S_GW+GTPU_TPDU_BYTES_SENT_S5_P_GW+GTPU_TPDU_BYTES_RECV_S1_U-GTPU_TPDU_BYTES_SENT_S5_S_GW+GTPU_TPDU_BYTES_RECV_S5_P_GW)*8/3600/40000000000*100,2) PGWSGIALL",
            "round(sum(GTPU_TPDU_BYTES_SENT_S1_U+GTPU_TPDU_BYTES_RECV_S1_U)*8/900/40000000000*100,2) SGWS1UALL"
           ]
        },
        'sql_tables' : [
            'PCOFNG_PS_GUV1_GTPU_RAW sgw',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid' 
        ]
    },
    'LTE-GTPU-THROUGH'     : {
        'func'         : saegw_gtpu_throughput,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'GTPU接收包个数2G',
                        u'GTPU接收包个数3G',
                        u'GTPU接收包个数4G',
                        u'GTPU接收包个数其他',
                        u'GTPU接收字节个数2G',
                        u'GTPU接收字节个数3G',
                        u'GTPU接收字节个数4G',
                        u'GTPU接收字节个数其他',
                        u'GTPU发送包个数2G',
                        u'GTPU发送包个数3G',
                        u'GTPU发送包个数4G',
                        u'GTPU发送包个数其他',
                        u'GTPU发送字节个数2G',
                        u'GTPU发送字节个数3G',
                        u'GTPU发送字节个数4G',
                        u'GTPU发送字节个数其他',
                        u'GTPU发送EndMarker个数',
                        u'GTPU上行吞吐率(Mbit/s)',
                        u'GTPU下行吞吐率(Mbit/s)',
                        u'GTPU 4G 总吞吐率(Mbit/s)',
                        u'GTPU 总吞吐率(Mbit/s)',
                        u'GTPU_ECHO_RESPONSE_SENT',
                        u'GTPU_ECHO_REQUEST_RECEIVED',
                        u'GTP-U ECHO响应率'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')		    BH",
            "sum(GTPU_GPDU_PKTS_RECV_RAT_2G) GTPU_GPDU_PKTS_RECV_RAT_2G",
            "sum(GTPU_GPDU_PKTS_RECV_RAT_3G) GTPU_GPDU_PKTS_RECV_RAT_3G",
            "sum(GTPU_GPDU_PKTS_RECV_LTE) GTPU_GPDU_PKTS_RECV_LTE",
            "sum(GTPU_GPDU_PKTS_RECV_RAT_UNKN) GTPU_GPDU_PKTS_RECV_RAT_UNKN",
            "sum(GTPU_GPDU_BYTES_RECV_RAT_2G) GTPU_GPDU_BYTES_RECV_RAT_2G",
            "sum(GTPU_GPDU_BYTES_RECV_RAT_3G) GTPU_GPDU_BYTES_RECV_RAT_3G",
            "sum(GTPU_GPDU_BYTES_RECV_LTE) GTPU_GPDU_BYTES_RECV_LTE",
            "sum(GTPU_GPDU_BYTES_RECV_RAT_UNKN) GTPU_GPDU_BYTES_RECV_RAT_UNKN",
            "sum(GTPU_GPDU_PKTS_SENT_RAT_2G) GTPU_GPDU_PKTS_SENT_RAT_2G",
            "sum(GTPU_GPDU_PKTS_SENT_RAT_3G) GTPU_GPDU_PKTS_SENT_RAT_3G",
            "sum(GTPU_GPDU_PKTS_SENT_LTE) GTPU_GPDU_PKTS_SENT_LTE",
            "sum(GTPU_GPDU_PKTS_SENT_RAT_UNKN) GTPU_GPDU_PKTS_SENT_RAT_UNKN",
            "sum(GTPU_GPDU_BYTES_SENT_RAT_2G) GTPU_GPDU_BYTES_SENT_RAT_2G",
            "sum(GTPU_GPDU_BYTES_SENT_RAT_3G) GTPU_GPDU_BYTES_SENT_RAT_3G",
            "sum(GTPU_GPDU_BYTES_SENT_LTE) GTPU_GPDU_BYTES_SENT_LTE",
            "sum(GTPU_GPDU_BYTES_SENT_RAT_UNKN) GTPU_GPDU_BYTES_SENT_RAT_UNKN",
            "sum(GTPU_END_MARKER_MESSAGES_SENT) GTPU_END_MARKER_MESSAGES_SENT",
            "sum(GTPU_UPLINK_THROUGHPUT) GTPU_UPLINK_THROUGHPUT",
            "sum(GTPU_DOWNLINK_THROUGHPUT) GTPU_DOWNLINK_THROUGHPUT",
            "round((sum(GTPU_GPDU_BYTES_RECV_LTE)+sum(GTPU_GPDU_BYTES_SENT_LTE))*8/943718400,2)  GTPU_THROUGHPUT_LTE",
            "round(((8*(sum(gtpu_gpdu_bytes_recv_rat_2g) + sum(gtpu_gpdu_bytes_recv_rat_3g) + sum(gtpu_gpdu_bytes_recv_lte) + sum(gtpu_gpdu_bytes_recv_rat_unkn) + nvl(sum(gtpu_gpdu_bytes_recv_rat_wlan),0) + nvl(sum(gtpu_gpdu_bytes_recv_rat_virt),0) + sum(gtpu_gpdu_bytes_sent_rat_2g) + sum(gtpu_gpdu_bytes_sent_rat_3g) + sum(gtpu_gpdu_bytes_sent_lte) + sum(gtpu_gpdu_bytes_sent_rat_unkn) + nvl(sum(gtpu_gpdu_bytes_sent_rat_wlan),0) + nvl(sum(gtpu_gpdu_bytes_sent_rat_virt),0)))) / ((15*60*1048576)) , 2) GTPU_THROUGHPUT_ALL",
            "SUM(GTPU_ECHO_RESPONSE_SENT) GTPU_ECHO_RESPONSE_SENT",
            "SUM(GTPU_ECHO_REQUEST_RECEIVED) GTPU_ECHO_REQUEST_RECEIVED",
            "round(decode( ((sum(gtpu_echo_request_received))),0,NULL, ((sum(gtpu_echo_response_sent))) / ((sum(gtpu_echo_request_received)))),4)*100"
    	  ],
          'sql_items_60_SAEGW' : [
	        "FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')		    BH",
            "sum(GTPU_GPDU_PKTS_RECV_RAT_2G) GTPU_GPDU_PKTS_RECV_RAT_2G",
            "sum(GTPU_GPDU_PKTS_RECV_RAT_3G) GTPU_GPDU_PKTS_RECV_RAT_3G",
            "sum(GTPU_GPDU_PKTS_RECV_LTE) GTPU_GPDU_PKTS_RECV_LTE",
            "sum(GTPU_GPDU_PKTS_RECV_RAT_UNKN) GTPU_GPDU_PKTS_RECV_RAT_UNKN",
            "sum(GTPU_GPDU_BYTES_RECV_RAT_2G) GTPU_GPDU_BYTES_RECV_RAT_2G",
            "sum(GTPU_GPDU_BYTES_RECV_RAT_3G) GTPU_GPDU_BYTES_RECV_RAT_3G",
            "sum(GTPU_GPDU_BYTES_RECV_LTE) GTPU_GPDU_BYTES_RECV_LTE",
            "sum(GTPU_GPDU_BYTES_RECV_RAT_UNKN) GTPU_GPDU_BYTES_RECV_RAT_UNKN",
            "sum(GTPU_GPDU_PKTS_SENT_RAT_2G) GTPU_GPDU_PKTS_SENT_RAT_2G",
            "sum(GTPU_GPDU_PKTS_SENT_RAT_3G) GTPU_GPDU_PKTS_SENT_RAT_3G",
            "sum(GTPU_GPDU_PKTS_SENT_LTE) GTPU_GPDU_PKTS_SENT_LTE",
            "sum(GTPU_GPDU_PKTS_SENT_RAT_UNKN) GTPU_GPDU_PKTS_SENT_RAT_UNKN",
            "sum(GTPU_GPDU_BYTES_SENT_RAT_2G) GTPU_GPDU_BYTES_SENT_RAT_2G",
            "sum(GTPU_GPDU_BYTES_SENT_RAT_3G) GTPU_GPDU_BYTES_SENT_RAT_3G",
            "sum(GTPU_GPDU_BYTES_SENT_LTE) GTPU_GPDU_BYTES_SENT_LTE",
            "sum(GTPU_GPDU_BYTES_SENT_RAT_UNKN) GTPU_GPDU_BYTES_SENT_RAT_UNKN",
            "sum(GTPU_END_MARKER_MESSAGES_SENT) GTPU_END_MARKER_MESSAGES_SENT",
            "round(sum(GTPU_UPLINK_THROUGHPUT)/4,4) GTPU_UPLINK_THROUGHPUT",
            "round(sum(GTPU_DOWNLINK_THROUGHPUT)/4,4) GTPU_DOWNLINK_THROUGHPUT",
            "round((sum(GTPU_GPDU_BYTES_RECV_LTE)+sum(GTPU_GPDU_BYTES_SENT_LTE))*8/3774873600,2)  GTPU_THROUGHPUT_LTE",
            "round(((8*(sum(gtpu_gpdu_bytes_recv_rat_2g) + sum(gtpu_gpdu_bytes_recv_rat_3g) + sum(gtpu_gpdu_bytes_recv_lte) + sum(gtpu_gpdu_bytes_recv_rat_unkn) + nvl(sum(gtpu_gpdu_bytes_recv_rat_wlan),0) + nvl(sum(gtpu_gpdu_bytes_recv_rat_virt),0) + sum(gtpu_gpdu_bytes_sent_rat_2g) + sum(gtpu_gpdu_bytes_sent_rat_3g) + sum(gtpu_gpdu_bytes_sent_lte) + sum(gtpu_gpdu_bytes_sent_rat_unkn) + nvl(sum(gtpu_gpdu_bytes_sent_rat_wlan),0) + nvl(sum(gtpu_gpdu_bytes_sent_rat_virt),0)))) / ((60*60*1048576)) ,2) GTPU_THROUGHPUT_ALL",
            "SUM(GTPU_ECHO_RESPONSE_SENT) GTPU_ECHO_RESPONSE_SENT",
            "SUM(GTPU_ECHO_REQUEST_RECEIVED) GTPU_ECHO_REQUEST_RECEIVED",
            "round(decode( ((sum(gtpu_echo_request_received))),0,NULL, ((sum(gtpu_echo_response_sent))) / ((sum(gtpu_echo_request_received)))),4)*100"
        ]
        },
        'sql_tables' : [
            'PCOFNG_PS_GTPU_GTPU_RAW sgw',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid' 
        ]
    },
    'LTE-S1U-THROUGH'     : {
        'func'         : saegw_s1u_throughput,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'S1U接收字节数',
                        u'S1U接收包数',
                        u'S1U发送字节数',
                        u'S1U发送包数'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')	BH",
            "sum(GTPU_TPDU_BYTES_RECV_S1_U) GTPU_TPDU_BYTES_RECV_S1_U",
            "sum(GTPU_GPDU_PKTS_RECV_S1_U) GTPU_GPDU_PKTS_RECV_S1_U",
            "sum(GTPU_TPDU_BYTES_SENT_S1_U) GTPU_TPDU_BYTES_SENT_S1_U",
            "sum(GTPU_GPDU_PKTS_SENT_S1_U) GTPU_GPDU_PKTS_SENT_S1_U"
    	  ],
          'sql_items_60_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')		    BH",
            "sum(GTPU_TPDU_BYTES_RECV_S1_U) GTPU_TPDU_BYTES_RECV_S1_U",
            "sum(GTPU_GPDU_PKTS_RECV_S1_U) GTPU_GPDU_PKTS_RECV_S1_U",
            "sum(GTPU_TPDU_BYTES_SENT_S1_U) GTPU_TPDU_BYTES_SENT_S1_U",
            "sum(GTPU_GPDU_PKTS_SENT_S1_U) GTPU_GPDU_PKTS_SENT_S1_U"
          ]
        },
        'sql_tables' : [
            'PCOFNG_PS_GUV1_GTPU_RAW sgw',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid' 
        ]
    },
    'LTE-SESSION'     : {
        'func'         : saegw_session,
        'title'        : [
                        	u'设备ID',
                            u'设备名称',
                            u'日期',
                            u'时间',
                            u'Create Session接收个数',
                            u'Create Session发送个数',
                            u'S11接收Create Session个数',
                            u'S5发送Create Session个数',
                            u'Release AccessBearer个数',
                            u'Delete Session个数',
                            u'Delete Session超时个数'
                            
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')		    BH",
            "sum(GTPCV2_CRE_SESS_REQ_RECV) GTPCV2_CRE_SESS_REQ_RECV",
            "sum(GTPCV2_CREATE_SESSION_REQ_SENT) GTPCV2_CREATE_SESSION_REQ_SENT",
            "sum(GTPCV2_CRE_SESS_REQ_RECV_S11) GTPCV2_CRE_SESS_REQ_RECV_S11",
            "sum(GTPCV2_CRE_SESS_REQ_SENT_S5) GTPCV2_CRE_SESS_REQ_SENT_S5",
            "sum(GTPCV2_REL_ACC_BEAR_REQ_RECV) GTPCV2_REL_ACC_BEAR_REQ_RECV",
            "sum(GTPCV2_DEL_SESS_REQ_SENT) GTPCV2_DEL_SESS_REQ_SENT",
            "sum(GTPCV2_DEL_SESS_REQ_EXCEED_N3) GTPCV2_DEL_SESS_REQ_EXCEED_N3",
            "SUM(GTPCV2_DL_DATA_NOTIF_SENT) GTPCV2_DL_DATA_NOTIF_SENT",
            "SUM(GTPCV2_DL_DATA_NOTIF_EXCEED_N3) GTPCV2_DL_DATA_NOTIF_EXCEED_N3"
    	  ],
          'sql_items_60_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')		    BH",
            "sum(GTPCV2_CRE_SESS_REQ_RECV) GTPCV2_CRE_SESS_REQ_RECV",
            "sum(GTPCV2_CREATE_SESSION_REQ_SENT) GTPCV2_CREATE_SESSION_REQ_SENT",
            "sum(GTPCV2_CRE_SESS_REQ_RECV_S11) GTPCV2_CRE_SESS_REQ_RECV_S11",
            "sum(GTPCV2_CRE_SESS_REQ_SENT_S5) GTPCV2_CRE_SESS_REQ_SENT_S5",
            "sum(GTPCV2_REL_ACC_BEAR_REQ_RECV) GTPCV2_REL_ACC_BEAR_REQ_RECV",
            "sum(GTPCV2_DEL_SESS_REQ_SENT) GTPCV2_DEL_SESS_REQ_SENT",
            "sum(GTPCV2_DEL_SESS_REQ_EXCEED_N3) GTPCV2_DEL_SESS_REQ_EXCEED_N3"
         ]
        },
        'sql_tables' : [
            'PCOFNG_PS_GTPCV2_GTPCV2_RAW sgw',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid' 
        ]
    },
    'LTE-SGI-THROUGH'     : {
        'func'         : saegw_sgi_throughput,
        'title'        : [
                u'设备ID',
                u'设备名称',
                u'日期',
                u'时间',
                u'SGi/Gi 发送IPv4字节',
                u'SGi/Gi 接收IPv4字节',
                u'SGi/Gi 发送IPv6字节',
                u'SGi/Gi 接收IPv6字节'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(sgw.PERIOD_START_TIME,'hh24:mi')                  BH",
            "SUM(IPV4_TPDU_BYTES_SENT) PV4_TPDU_BYTES_SENT",
            "SUM(IPV4_TPDU_BYTES_RECEIVED) IPV4_TPDU_BYTES_RECEIVED",
            "SUM(IPV6_TPDU_BYTES_SENT) IPV6_TPDU_BYTES_SENT",
            "SUM(IPV6_TPDU_BYTES_RECEIVED) IPV6_TPDU_BYTES_RECEIVED"
    	  ],
          'sql_items_60_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(sgw.PERIOD_START_TIME,'hh24')                  BH",
            "SUM(IPV4_TPDU_BYTES_SENT) PV4_TPDU_BYTES_SENT",
            "SUM(IPV4_TPDU_BYTES_RECEIVED) IPV4_TPDU_BYTES_RECEIVED",
            "SUM(IPV6_TPDU_BYTES_SENT) IPV6_TPDU_BYTES_SENT",
            "SUM(IPV6_TPDU_BYTES_RECEIVED) IPV6_TPDU_BYTES_RECEIVED"
        ]
        },
        'sql_tables' : [
            'PCOFNG_PS_IPTRA_IP_RAW sgw',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid' 
        ]
    },
    'LTE-IPPOOL'     : {
        'func'         : saegw_ip_pool,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'IP POOL',
                        u'IP POOL 地址数',
                        u'IP POOL 已占用地址数',
                        u'IP POOL 已占用比例',
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(sgw.PERIOD_START_TIME,'hh24:mi')                  BH",
            "PERPOOL_ID POOL_ID",
            "SUM(IPPOOL_SIZE) IPPOOL_SIZE",
            "SUM(IPPOOL_ALLOCATED) IPPOOL_ALLOCATED",
            "decode(nvl((SUM(IPPOOL_SIZE)),0),0,0,(round((SUM(IPPOOL_ALLOCATED)/(SUM(IPPOOL_SIZE))),4)*100)) ippool_alloc_ratio"
    	  ],
          'sql_items_60_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(sgw.PERIOD_START_TIME,'hh24')                  BH",
            "PERPOOL_ID POOL_ID",
            "SUM(IPPOOL_SIZE)/4 IPPOOL_SIZE",
            "SUM(IPPOOL_ALLOCATED)/4 IPPOOL_ALLOCATED",
            "decode(nvl((SUM(IPPOOL_SIZE)),0),0,0,(round((SUM(IPPOOL_ALLOCATED)/(SUM(IPPOOL_SIZE))),4)*100)) ippool_alloc_ratio"
        ]
        },
        'sql_tables' : [
            'PCOFNG_PS_IPDYN_PERPOOL_RAW sgw',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid' 
        ]
    },
    'LTE-DOWNDATA-NOTICE'     : {
        'func'         : saegw_downdata_notice,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'GTPCV2_DL_DATA_NOTIF_SENT',
                        u'GTPCV2_DL_DATA_NOTIF_EXCEED_N3',
                        u'GTPCV2_DL_DATA_NOTIF_FAIL_RECV',
                        u'GTPCV2_DL_DATA_NOTIF_ACK_RECV',
                        u'下行数据通知成功率',
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "sgw.FING_ID",
            "objects.CO_NAME",
            "sgw.REPDATE        REPDATE",
            "sgw.BH                  BH",
            "SUM(GTPCV2_DL_DATA_NOTIF_SENT) GTPCV2_DL_DATA_NOTIF_SENT",
            "SUM(GTPCV2_DL_DATA_NOTIF_EXCEED_N3) GTPCV2_DL_DATA_NOTIF_EXCEED_N3",
            "SUM(GTPCV2_DL_DATA_NOTIF_FAIL_RECV) GTPCV2_DL_DATA_NOTIF_FAIL_RECV",
            "sum(gtpcv2_dl_data_notif_ack_recv) gtpcv2_dl_data_notif_ack_recv",
            "round(decode( ((sum(GTPCV2_DL_DATA_NOTIF_SENT) + sum(GTPCV2_DL_DATA_NOTIF_EXCEED_N3))),0,NULL, ((sum(gtpcv2_dl_data_notif_ack_recv) - sum(GTPCV2_DL_DATA_NOTIF_FAIL_RECV))) / ((sum(GTPCV2_DL_DATA_NOTIF_SENT) + sum(GTPCV2_DL_DATA_NOTIF_EXCEED_N3)))),4)*100 flng_148b"
          ],
          'sql_items_60_SAEGW' : [
            "sgw.FING_ID",
            "objects.CO_NAME",
            "sgw.REPDATE        REPDATE",
            "sgw.BH                  BH",
            "SUM(GTPCV2_DL_DATA_NOTIF_SENT) GTPCV2_DL_DATA_NOTIF_SENT",
            "SUM(GTPCV2_DL_DATA_NOTIF_EXCEED_N3) GTPCV2_DL_DATA_NOTIF_EXCEED_N3",
            "SUM(GTPCV2_DL_DATA_NOTIF_FAIL_RECV) GTPCV2_DL_DATA_NOTIF_FAIL_RECV",
            "sum(gtpcv2_dl_data_notif_ack_recv) gtpcv2_dl_data_notif_ack_recv",
            "round(decode( ((sum(GTPCV2_DL_DATA_NOTIF_SENT) + sum(GTPCV2_DL_DATA_NOTIF_EXCEED_N3))),0,NULL, ((sum(gtpcv2_dl_data_notif_ack_recv) - sum(GTPCV2_DL_DATA_NOTIF_FAIL_RECV))) / ((sum(GTPCV2_DL_DATA_NOTIF_SENT) + sum(GTPCV2_DL_DATA_NOTIF_EXCEED_N3)))),4)*100 flng_148b"
          ]
        },
        'sql_tables' : [
            {
                'sql_items'      : {
                    'sql_items_15_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24:mi')                  BH",
                        "SUM(GTPCV2_DL_DATA_NOTIF_SENT) GTPCV2_DL_DATA_NOTIF_SENT",
                        "SUM(GTPCV2_DL_DATA_NOTIF_EXCEED_N3) GTPCV2_DL_DATA_NOTIF_EXCEED_N3",
                    ],
                    'sql_items_60_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24')                  BH",
                        "SUM(GTPCV2_DL_DATA_NOTIF_SENT) GTPCV2_DL_DATA_NOTIF_SENT",
                        "SUM(GTPCV2_DL_DATA_NOTIF_EXCEED_N3) GTPCV2_DL_DATA_NOTIF_EXCEED_N3",
                    ]
                },
                'sql_tables': [
                    'PCOFNG_PS_GTPCV2_GTPCV2_RAW sgw',
                    'UTP_COMMON_OBJECTS objects'  
                ],
                'sql_where' : [ 
                    'sgw.FING_id=objects.CO_Gid', 
                ],
                'table_name' : "sgw"
            },
            {
                'sql_items'      : {
                    'sql_items_15_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24:mi')                  BH",
                        "SUM(GTPCV2_DL_DATA_NOTIF_FAIL_RECV) GTPCV2_DL_DATA_NOTIF_FAIL_RECV",
                    ],
                    'sql_items_60_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24')                  BH",
                        "SUM(GTPCV2_DL_DATA_NOTIF_FAIL_RECV) GTPCV2_DL_DATA_NOTIF_FAIL_RECV",
                    ],
                },
                'sql_tables': [
                    'pcofng_ps_ddnfr_ddnfr_raw sgw',
                    'UTP_COMMON_OBJECTS objects' 
                ],
                'sql_where' : [ 
                    'sgw.FING_id=objects.CO_Gid'
                ],
                'table_name' : "table1"
            },
            {
                'sql_items'      : {
                    'sql_items_15_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')  REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24:mi')     BH",
                        "SUM(decode(ddnar_id,'16',gtpcv2_dl_data_notif_ack_recv,0)) gtpcv2_dl_data_notif_ack_recv",
                    ],
                    'sql_items_60_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')  REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24')        BH",
                        "SUM(decode(ddnar_id,'16',gtpcv2_dl_data_notif_ack_recv,0)) gtpcv2_dl_data_notif_ack_recv",
                    ],
                },
                'sql_tables': [
                    'pcofng_ps_ddnar_ddnar_raw sgw',
                    'UTP_COMMON_OBJECTS objects'  
                ],
                'sql_where' : [ 
                    'sgw.FING_id=objects.CO_Gid' 
                ],
                'table_name' : "table2"
            },
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid',
            'table1.FING_id=objects.CO_Gid',
            'table2.FING_id=objects.CO_Gid',
            'sgw.REPDATE=table1.REPDATE',
            'sgw.BH=table1.BH', 
            'sgw.REPDATE=table2.REPDATE',
            'sgw.BH=table2.BH', 
        ],
        'sql_group' : [
            "sgw.REPDATE",
            "sgw.BH",
            "sgw.fing_id",
            "objects.co_name"
        ],
        'sql_order' : [
            "sgw.REPDATE",
            "sgw.BH",
            "sgw.fing_id",
            "objects.co_name"
        ]

    },
    'LTE-PDN'     : {
        'func'         : saegw_pdn,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'sm_nbr_act_sess_rat_4g',
                        u'SM_NBR_ACT_SGW_RAT_4G',
                        u'PDN会话数量'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "sgw.FING_ID",
            "objects.CO_NAME",
            "sgw.REPDATE        REPDATE",
            "sgw.BH                  BH",
            "SUM(sm_nbr_act_sess_rat_4g) sm_nbr_act_sess_rat_4g",
            "SUM(SM_NBR_ACT_SGW_RAT_4G) SM_NBR_ACT_SGW_RAT_4G",
            "SUM(sm_nbr_act_sess_rat_4g)+sum(SM_NBR_ACT_SGW_RAT_4G) pdncount",
          ],
          'sql_items_60_SAEGW' : [
            "sgw.FING_ID",
            "objects.CO_NAME",
            "sgw.REPDATE        REPDATE",
            "sgw.BH                  BH",
            "round(SUM(sm_nbr_act_sess_rat_4g)/4,0) sm_nbr_act_sess_rat_4g",
            "round(SUM(SM_NBR_ACT_SGW_RAT_4G)/4,0) SM_NBR_ACT_SGW_RAT_4G",
            "round((SUM(sm_nbr_act_sess_rat_4g)+sum(SM_NBR_ACT_SGW_RAT_4G))/4,0) pdncount",
          ]
        },
        'sql_tables' : [
            {
                'sql_items'      : {
                    'sql_items_15_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24:mi')               BH",
                        "SUM(SM_NBR_ACT_SGW_RAT_4G) SM_NBR_ACT_SGW_RAT_4G"
                    ],
                    'sql_items_60_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24')                 BH",
                        "SUM(SM_NBR_ACT_SGW_RAT_4G) SM_NBR_ACT_SGW_RAT_4G"
                    ]
                },
                'sql_tables': [
                    'pcofng_ps_sgwp_sgwp_raw sgw',
                    'UTP_COMMON_OBJECTS objects'  
                ],
                'sql_where' : [ 
                    'sgw.FING_id=objects.CO_Gid', 
                ],
                'table_name' : "sgw"
            },
            {
                'sql_items'      : {
                    'sql_items_15_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24:mi')                BH",
                        "SUM(sm_nbr_act_sess_rat_4g) sm_nbr_act_sess_rat_4g"
                    ],
                    'sql_items_60_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24')               BH",
                        "SUM(sm_nbr_act_sess_rat_4g) sm_nbr_act_sess_rat_4g"
                    ]
                },
                'sql_tables': [
                    'pcofng_ps_ssprof_ssprof_raw sgw',
                    'UTP_COMMON_OBJECTS objects'  
                ],
                'sql_where' : [ 
                    'sgw.FING_id=objects.CO_Gid', 
                ],
                'table_name' : "table1"
            },
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid',
            'table1.FING_id=objects.CO_Gid',
            'sgw.REPDATE=table1.REPDATE',
            'sgw.BH=table1.BH' 
        ],
        'sql_group' : [
            "sgw.REPDATE",
            "sgw.BH",
            "sgw.fing_id",
            "objects.co_name"
        ],
        'sql_order' : [
            "sgw.REPDATE",
            "sgw.BH",
            "sgw.fing_id",
            "objects.co_name"
        ]
    },
    'LTE-CREATEBEARER'     : {
        'func'         : saegw_createbearer,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'GTPCV2_CREATE_BEARER_RESP_RECV',
                        u'GTPCV2_CR_BEARER_RESP_RECV_16',
                        u'GTPCV2_CR_BEARER_RESP_RECV_17',
                        u'GTPCV2_CR_BEARER_RESP_RECV_18',
                        u'GTPCV2_CR_BEARER_RESP_RECV_19',
                        u'GTPCV2_CR_BEARER_RESP_RECV_92',
                        u'GTPCV2_CR_BEARER_RESP_RECV_93',
                        u'专用承载建立成功率'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "sgw.FING_ID",
            "objects.CO_NAME",
            "sgw.REPDATE        REPDATE",
            "sgw.BH                  BH",
            "SUM(GTPCV2_CREATE_BEARER_RESP_RECV) GTPCV2_CREATE_BEARER_RESP_RECV",
            "SUM(GTPCV2_CR_BEARER_RESP_RECV_16) GTPCV2_CR_BEARER_RESP_RECV_16",
            "SUM(GTPCV2_CR_BEARER_RESP_RECV_17) GTPCV2_CR_BEARER_RESP_RECV_17",
            "SUM(GTPCV2_CR_BEARER_RESP_RECV_18) GTPCV2_CR_BEARER_RESP_RECV_18",
            "SUM(GTPCV2_CR_BEARER_RESP_RECV_19) GTPCV2_CR_BEARER_RESP_RECV_19",
            "SUM(GTPCV2_CR_BEARER_RESP_RECV_92) GTPCV2_CR_BEARER_RESP_RECV_92",
            "SUM(GTPCV2_CR_BEARER_RESP_RECV_93) GTPCV2_CR_BEARER_RESP_RECV_93",
            "round(decode(sum(GTPCV2_CREATE_BEARER_RESP_RECV),0,NULL,1-((sum(GTPCV2_CREATE_BEARER_RESP_RECV) - (sum(GTPCV2_CR_BEARER_RESP_RECV_16) + sum(GTPCV2_CR_BEARER_RESP_RECV_17) + sum(GTPCV2_CR_BEARER_RESP_RECV_18) + sum(GTPCV2_CR_BEARER_RESP_RECV_19) + sum(GTPCV2_CR_BEARER_RESP_RECV_92) + sum(GTPCV2_CR_BEARER_RESP_RECV_93))) / (sum(GTPCV2_CREATE_BEARER_RESP_RECV)))),4)*100 FLNG_1002A"
          ],
          'sql_items_60_SAEGW' : [
            "sgw.FING_ID",
            "objects.CO_NAME",
            "sgw.REPDATE        REPDATE",
            "sgw.BH                  BH",
            "SUM(GTPCV2_CREATE_BEARER_RESP_RECV) GTPCV2_CREATE_BEARER_RESP_RECV",
            "SUM(GTPCV2_CR_BEARER_RESP_RECV_16) GTPCV2_CR_BEARER_RESP_RECV_16",
            "SUM(GTPCV2_CR_BEARER_RESP_RECV_17) GTPCV2_CR_BEARER_RESP_RECV_17",
            "SUM(GTPCV2_CR_BEARER_RESP_RECV_18) GTPCV2_CR_BEARER_RESP_RECV_18",
            "SUM(GTPCV2_CR_BEARER_RESP_RECV_19) GTPCV2_CR_BEARER_RESP_RECV_19",
            "SUM(GTPCV2_CR_BEARER_RESP_RECV_92) GTPCV2_CR_BEARER_RESP_RECV_92",
            "SUM(GTPCV2_CR_BEARER_RESP_RECV_93) GTPCV2_CR_BEARER_RESP_RECV_93",
            "round(decode(sum(GTPCV2_CREATE_BEARER_RESP_RECV),0,NULL,1-((sum(GTPCV2_CREATE_BEARER_RESP_RECV) - (sum(GTPCV2_CR_BEARER_RESP_RECV_16) + sum(GTPCV2_CR_BEARER_RESP_RECV_17) + sum(GTPCV2_CR_BEARER_RESP_RECV_18) + sum(GTPCV2_CR_BEARER_RESP_RECV_19) + sum(GTPCV2_CR_BEARER_RESP_RECV_92) + sum(GTPCV2_CR_BEARER_RESP_RECV_93))) / (sum(GTPCV2_CREATE_BEARER_RESP_RECV)))),4)*100 FLNG_1002A"
          ]
        },
        'sql_tables' : [
            {
                'sql_items'      : {
                    'sql_items_15_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24:mi')                BH",
                        "SUM(GTPCV2_CREATE_BEARER_RESP_RECV) GTPCV2_CREATE_BEARER_RESP_RECV",
                        "SUM(decode(cbrr_id,'16',gtpcv2_create_bearer_resp_recv,'cs_1_16',gtpcv2_create_bearer_resp_recv, 0)) GTPCV2_CR_BEARER_RESP_RECV_16",
                        "SUM(decode(cbrr_id,'17',gtpcv2_create_bearer_resp_recv,'cs_1_17',gtpcv2_create_bearer_resp_recv, 0)) GTPCV2_CR_BEARER_RESP_RECV_17",
                        "SUM(decode(cbrr_id,'18',gtpcv2_create_bearer_resp_recv,'cs_1_18',gtpcv2_create_bearer_resp_recv, 0)) GTPCV2_CR_BEARER_RESP_RECV_18",
                        "SUM(decode(cbrr_id,'19',gtpcv2_create_bearer_resp_recv,'cs_1_19',gtpcv2_create_bearer_resp_recv, 0)) GTPCV2_CR_BEARER_RESP_RECV_19",
                        "SUM(decode(cbrr_id,'92',gtpcv2_create_bearer_resp_recv,'cs_1_92',gtpcv2_create_bearer_resp_recv, 0)) GTPCV2_CR_BEARER_RESP_RECV_92",
                        "SUM(decode(cbrr_id,'93',gtpcv2_create_bearer_resp_recv,'cs_1_93',gtpcv2_create_bearer_resp_recv, 0)) GTPCV2_CR_BEARER_RESP_RECV_93",
                    ],
                    'sql_items_60_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24')               BH",
                        "SUM(GTPCV2_CREATE_BEARER_RESP_RECV) GTPCV2_CREATE_BEARER_RESP_RECV",
                        "SUM(decode(cbrr_id,'16',gtpcv2_create_bearer_resp_recv,'cs_1_16',gtpcv2_create_bearer_resp_recv, 0)) GTPCV2_CR_BEARER_RESP_RECV_16",
                        "SUM(decode(cbrr_id,'17',gtpcv2_create_bearer_resp_recv,'cs_1_17',gtpcv2_create_bearer_resp_recv, 0)) GTPCV2_CR_BEARER_RESP_RECV_17",
                        "SUM(decode(cbrr_id,'18',gtpcv2_create_bearer_resp_recv,'cs_1_18',gtpcv2_create_bearer_resp_recv, 0)) GTPCV2_CR_BEARER_RESP_RECV_18",
                        "SUM(decode(cbrr_id,'19',gtpcv2_create_bearer_resp_recv,'cs_1_19',gtpcv2_create_bearer_resp_recv, 0)) GTPCV2_CR_BEARER_RESP_RECV_19",
                        "SUM(decode(cbrr_id,'92',gtpcv2_create_bearer_resp_recv,'cs_1_92',gtpcv2_create_bearer_resp_recv, 0)) GTPCV2_CR_BEARER_RESP_RECV_92",
                        "SUM(decode(cbrr_id,'93',gtpcv2_create_bearer_resp_recv,'cs_1_93',gtpcv2_create_bearer_resp_recv, 0)) GTPCV2_CR_BEARER_RESP_RECV_93",
                    ]
                },
                'sql_tables': [
                    'pcofng_ps_cbrr_cbrr_raw sgw',
                    'UTP_COMMON_OBJECTS objects'  
                ],
                'sql_where' : [ 
                    'sgw.FING_id=objects.CO_Gid', 
                ],
                'table_name' : "sgw"
            },
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid'             
        ],
        'sql_group' : [
            "sgw.REPDATE",
            "sgw.BH",
            "sgw.fing_id",
            "objects.co_name"
        ],
        'sql_order' : [
            "sgw.REPDATE",
            "sgw.BH",
            "sgw.fing_id",
            "objects.co_name"
        ]
    },
    'LTE-S11CREATESESSION'     : {
        'func'         : saegw_s11createsession,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'GTPCV2_CRE_SESS_RESP_SENT_S11',
                        u'CRE_SESS_RESP_SENT_S11_16',
                        u'CRE_SESS_RESP_SENT_S11_17',
                        u'CRE_SESS_RESP_SENT_S11_18',
                        u'CRE_SESS_RESP_SENT_S11_19',
                        u'CRE_SESS_RESP_SENT_S11_92',
                        u'CRE_SESS_RESP_SENT_S11_93',
                        u'PDN会话建立成功率'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "sgw.FING_ID",
            "objects.CO_NAME",
            "sgw.REPDATE        REPDATE",
            "sgw.BH                  BH",
            "sum(CRE_SESS_RESP_SENT_S11_ALL) CRE_SESS_RESP_SENT_S11_ALL",
            "sum(CRE_SESS_RESP_SENT_S11_16) CRE_SESS_RESP_SENT_S11_16",
            "sum(CRE_SESS_RESP_SENT_S11_17) CRE_SESS_RESP_SENT_S11_17",
            "sum(CRE_SESS_RESP_SENT_S11_18) CRE_SESS_RESP_SENT_S11_18",
            "sum(CRE_SESS_RESP_SENT_S11_19) CRE_SESS_RESP_SENT_S11_19",
            "sum(CRE_SESS_RESP_SENT_S11_92) CRE_SESS_RESP_SENT_S11_92",
            "sum(CRE_SESS_RESP_SENT_S11_93) CRE_SESS_RESP_SENT_S11_93",
            "round(decode(sum(CRE_SESS_RESP_SENT_S11_ALL),0,NULL,1-((sum(CRE_SESS_RESP_SENT_S11_ALL) - (sum(CRE_SESS_RESP_SENT_S11_16) + sum(CRE_SESS_RESP_SENT_S11_17) + sum(CRE_SESS_RESP_SENT_S11_18) + sum(CRE_SESS_RESP_SENT_S11_19) + sum(CRE_SESS_RESP_SENT_S11_92) + sum(CRE_SESS_RESP_SENT_S11_93))) / (sum(CRE_SESS_RESP_SENT_S11_ALL)))),4)*100 FLNG_1002A"
           ],
          'sql_items_60_SAEGW' : [
            "sgw.FING_ID",
            "objects.CO_NAME",
            "sgw.REPDATE        REPDATE",
            "sgw.BH                  BH",
            "sum(CRE_SESS_RESP_SENT_S11_ALL) CRE_SESS_RESP_SENT_S11_ALL",
            "sum(CRE_SESS_RESP_SENT_S11_16) CRE_SESS_RESP_SENT_S11_16",
            "sum(CRE_SESS_RESP_SENT_S11_17) CRE_SESS_RESP_SENT_S11_17",
            "sum(CRE_SESS_RESP_SENT_S11_18) CRE_SESS_RESP_SENT_S11_18",
            "sum(CRE_SESS_RESP_SENT_S11_19) CRE_SESS_RESP_SENT_S11_19",
            "sum(CRE_SESS_RESP_SENT_S11_92) CRE_SESS_RESP_SENT_S11_92",
            "sum(CRE_SESS_RESP_SENT_S11_93) CRE_SESS_RESP_SENT_S11_93",
            "round(decode(sum(CRE_SESS_RESP_SENT_S11_ALL),0,NULL,1-((sum(CRE_SESS_RESP_SENT_S11_ALL) - (sum(CRE_SESS_RESP_SENT_S11_16) + sum(CRE_SESS_RESP_SENT_S11_17) + sum(CRE_SESS_RESP_SENT_S11_18) + sum(CRE_SESS_RESP_SENT_S11_19) + sum(CRE_SESS_RESP_SENT_S11_92) + sum(CRE_SESS_RESP_SENT_S11_93))) / (sum(CRE_SESS_RESP_SENT_S11_ALL)))),4)*100 FLNG_1002A"
           ]
        },
        'sql_tables' : [
            {
                'sql_items': {
                    'sql_items_15_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24:mi')                BH",
                        "SUM(GTPCV2_CRE_SESS_RESP_SENT_S11) CRE_SESS_RESP_SENT_S11_ALL",
                        "SUM(DECODE(GV211_ID,'16',GTPCV2_CRE_SESS_RESP_SENT_S11,'cs_1_16',GTPCV2_CRE_SESS_RESP_SENT_S11,0)) CRE_SESS_RESP_SENT_S11_16",
                        "SUM(DECODE(GV211_ID,'17',GTPCV2_CRE_SESS_RESP_SENT_S11,'cs_1_17',GTPCV2_CRE_SESS_RESP_SENT_S11,0)) CRE_SESS_RESP_SENT_S11_17",
                        "SUM(DECODE(GV211_ID,'18',GTPCV2_CRE_SESS_RESP_SENT_S11,'cs_1_18',GTPCV2_CRE_SESS_RESP_SENT_S11,0)) CRE_SESS_RESP_SENT_S11_18",
                        "SUM(DECODE(GV211_ID,'19',GTPCV2_CRE_SESS_RESP_SENT_S11,'cs_1_19',GTPCV2_CRE_SESS_RESP_SENT_S11,0)) CRE_SESS_RESP_SENT_S11_19",
                        "SUM(DECODE(GV211_ID,'92',GTPCV2_CRE_SESS_RESP_SENT_S11,'cs_1_92',GTPCV2_CRE_SESS_RESP_SENT_S11,0)) CRE_SESS_RESP_SENT_S11_92",
                        "SUM(DECODE(GV211_ID,'93',GTPCV2_CRE_SESS_RESP_SENT_S11,'cs_1_93',GTPCV2_CRE_SESS_RESP_SENT_S11,0)) CRE_SESS_RESP_SENT_S11_93",
                        "SUM(GTPCV2_SUSP_ACK_SENT_S11) GTPCV2_SUSP_ACK_SENT_S11_ALL",
                        "SUM(DECODE(GV211_ID,'16',GTPCV2_SUSP_ACK_SENT_S11,'cs_1_16',GTPCV2_SUSP_ACK_SENT_S11,0)) GTPCV2_SUSP_ACK_SENT_S11_16",
                        "SUM(GTPCV2_RESUM_ACK_SENT_S11) GTPCV2_RESUM_ACK_SENT_S11_ALL",
                        "SUM(DECODE(GV211_ID,'16',GTPCV2_RESUM_ACK_SENT_S11,'cs_1_16',GTPCV2_RESUM_ACK_SENT_S11,0)) GTPCV2_RESUM_ACK_SENT_S11_16"  
                    ],
                    'sql_items_60_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24')               BH",
                        "SUM(GTPCV2_CRE_SESS_RESP_SENT_S11) CRE_SESS_RESP_SENT_S11_ALL",
                        "SUM(DECODE(GV211_ID,'16',GTPCV2_CRE_SESS_RESP_SENT_S11,'cs_1_16',GTPCV2_CRE_SESS_RESP_SENT_S11,0)) CRE_SESS_RESP_SENT_S11_16",
                        "SUM(DECODE(GV211_ID,'17',GTPCV2_CRE_SESS_RESP_SENT_S11,'cs_1_17',GTPCV2_CRE_SESS_RESP_SENT_S11,0)) CRE_SESS_RESP_SENT_S11_17",
                        "SUM(DECODE(GV211_ID,'18',GTPCV2_CRE_SESS_RESP_SENT_S11,'cs_1_18',GTPCV2_CRE_SESS_RESP_SENT_S11,0)) CRE_SESS_RESP_SENT_S11_18",
                        "SUM(DECODE(GV211_ID,'19',GTPCV2_CRE_SESS_RESP_SENT_S11,'cs_1_19',GTPCV2_CRE_SESS_RESP_SENT_S11,0)) CRE_SESS_RESP_SENT_S11_19",
                        "SUM(DECODE(GV211_ID,'92',GTPCV2_CRE_SESS_RESP_SENT_S11,'cs_1_92',GTPCV2_CRE_SESS_RESP_SENT_S11,0)) CRE_SESS_RESP_SENT_S11_92",
                        "SUM(DECODE(GV211_ID,'93',GTPCV2_CRE_SESS_RESP_SENT_S11,'cs_1_93',GTPCV2_CRE_SESS_RESP_SENT_S11,0)) CRE_SESS_RESP_SENT_S11_93",
                        "SUM(GTPCV2_SUSP_ACK_SENT_S11) GTPCV2_SUSP_ACK_SENT_S11_ALL",
                        "SUM(DECODE(GV211_ID,'16',GTPCV2_SUSP_ACK_SENT_S11,'cs_1_16',GTPCV2_SUSP_ACK_SENT_S11,0)) GTPCV2_SUSP_ACK_SENT_S11_16",
                        "SUM(GTPCV2_RESUM_ACK_SENT_S11) GTPCV2_RESUM_ACK_SENT_S11_ALL",
                        "SUM(DECODE(GV211_ID,'16',GTPCV2_RESUM_ACK_SENT_S11,'cs_1_16',GTPCV2_RESUM_ACK_SENT_S11,0)) GTPCV2_RESUM_ACK_SENT_S11_16"  
                    ]
                },
                'sql_tables': [
                    'pcofng_ps_gv211_gv211_raw sgw',
                    'UTP_COMMON_OBJECTS objects'  
                ],
                'sql_where' : [ 
                    'sgw.FING_id=objects.CO_Gid', 
                ],
                'table_name' : "sgw"
            },    
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid'             
        ],
        'sql_group' : [
            "sgw.REPDATE",
            "sgw.BH",
            "sgw.fing_id",
            "objects.co_name"
        ],
        'sql_order' : [
            "sgw.REPDATE",
            "sgw.BH",
            "sgw.fing_id",
            "objects.co_name"
        ]
    },
    'LTE-DATAFORWARD-SUCC'     : {
        'func'         : saegw_dataforward_succ,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'GTPU_GPDU_PKTS_RECV_RAT_2G',
                        u'GTPU_GPDU_PKTS_RECV_RAT_3G',
                        u'GTPU_GPDU_PKTS_RECV_LTE',
                        u'GTPU_GPDU_PKTS_RECV_RAT_UNKN',
                        u'GTPU_GPDU_PKTS_RECV_RAT_WLAN',
                        u'GTPU_GPDU_PKTS_RECV_RAT_VIRT',
                        u'GRE_TUN_PMIP_IPV4_PACKETS_RX',
                        u'GRE_TUN_PMIP_IPV6_PACKETS_RX',
                        u'IPV4_TPDU_PACKETS_RECEIVED',
                        u'IPV6_TPDU_PACKETS_RECEIVED',
                        u'UP_PKTS_DROPPED',
                        u'UPLINK_DROP_FORGED_UE_SRC_ADDR',
                        u'UP_DROP_PKTS_BLOCKING_FLAG_SET',
                        u'PKTS_DROPPED_MAX_FLOW_REACHED',
                        u'包转发成功率'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "sgw.FING_ID",
            "objects.CO_NAME",
            "sgw.REPDATE        REPDATE",
            "sgw.BH                  BH",
            "SUM(GTPU_GPDU_PKTS_RECV_RAT_2G) GTPU_GPDU_PKTS_RECV_RAT_2G",
            "SUM(GTPU_GPDU_PKTS_RECV_RAT_3G) GTPU_GPDU_PKTS_RECV_RAT_3G",
            "SUM(GTPU_GPDU_PKTS_RECV_LTE) GTPU_GPDU_PKTS_RECV_LTE",
            "SUM(GTPU_GPDU_PKTS_RECV_RAT_UNKN) GTPU_GPDU_PKTS_RECV_RAT_UNKN",
            "SUM(GTPU_GPDU_PKTS_RECV_RAT_WLAN) GTPU_GPDU_PKTS_RECV_RAT_WLAN",
            "SUM(GTPU_GPDU_PKTS_RECV_RAT_VIRT) GTPU_GPDU_PKTS_RECV_RAT_VIRT",
            "SUM(GRE_TUN_PMIP_IPV4_PACKETS_RX) GRE_TUN_PMIP_IPV4_PACKETS_RX",
            "SUM(GRE_TUN_PMIP_IPV6_PACKETS_RX) GRE_TUN_PMIP_IPV6_PACKETS_RX",
            "SUM(IPV4_TPDU_PACKETS_RECEIVED) IPV4_TPDU_PACKETS_RECEIVED",
            "SUM(IPV6_TPDU_PACKETS_RECEIVED) IPV6_TPDU_PACKETS_RECEIVED",
            "SUM(UP_PKTS_DROPPED) UP_PKTS_DROPPED",
            "SUM(UPLINK_DROP_FORGED_UE_SRC_ADDR) UPLINK_DROP_FORGED_UE_SRC_ADDR",
            "SUM(UP_DROP_PKTS_BLOCKING_FLAG_SET) UP_DROP_PKTS_BLOCKING_FLAG_SET",
            "SUM(PKTS_DROPPED_MAX_FLOW_REACHED) PKTS_DROPPED_MAX_FLOW_REACHED",
            """round(decode(((
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_2G),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_3G),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_LTE),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_UNKN),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_WLAN),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_VIRT),0) + 
nvl(SUM(IPV4_TPDU_PACKETS_RECEIVED),0) + 
nvl(SUM(IPV6_TPDU_PACKETS_RECEIVED),0) + 
nvl(SUM(GRE_TUN_PMIP_IPV4_PACKETS_RX),0) + 
nvl(SUM(GRE_TUN_PMIP_IPV6_PACKETS_RX),0)
)),0,NULL, (((
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_2G),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_3G),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_LTE),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_UNKN),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_WLAN),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_VIRT),0) + 
nvl(SUM(IPV4_TPDU_PACKETS_RECEIVED),0) + 
nvl(SUM(IPV6_TPDU_PACKETS_RECEIVED),0) + 
nvl(SUM(GRE_TUN_PMIP_IPV4_PACKETS_RX),0) + 
nvl(SUM(GRE_TUN_PMIP_IPV6_PACKETS_RX),0)
) - (
SUM(UP_PKTS_DROPPED) + 
nvl(SUM(UPLINK_DROP_FORGED_UE_SRC_ADDR),0) + 
nvl(SUM(UP_DROP_PKTS_BLOCKING_FLAG_SET),0) + 
nvl(SUM(PKTS_DROPPED_MAX_FLOW_REACHED),0) )
)) / ((
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_2G),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_3G),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_LTE),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_UNKN),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_WLAN),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_VIRT),0) + 
nvl(SUM(IPV4_TPDU_PACKETS_RECEIVED),0) + 
nvl(SUM(IPV6_TPDU_PACKETS_RECEIVED),0) + 
nvl(SUM(GRE_TUN_PMIP_IPV4_PACKETS_RX),0) + 
nvl(SUM(GRE_TUN_PMIP_IPV6_PACKETS_RX),0)))),4)*100 a"""
          ],
          'sql_items_60_SAEGW' : [
            "sgw.FING_ID",
            "objects.CO_NAME",
            "sgw.REPDATE        REPDATE",
            "sgw.BH                  BH",
            "SUM(GTPU_GPDU_PKTS_RECV_RAT_2G) GTPU_GPDU_PKTS_RECV_RAT_2G",
            "SUM(GTPU_GPDU_PKTS_RECV_RAT_3G) GTPU_GPDU_PKTS_RECV_RAT_3G",
            "SUM(GTPU_GPDU_PKTS_RECV_LTE) GTPU_GPDU_PKTS_RECV_LTE",
            "SUM(GTPU_GPDU_PKTS_RECV_RAT_UNKN) GTPU_GPDU_PKTS_RECV_RAT_UNKN",
            "SUM(GTPU_GPDU_PKTS_RECV_RAT_WLAN) GTPU_GPDU_PKTS_RECV_RAT_WLAN",
            "SUM(GTPU_GPDU_PKTS_RECV_RAT_VIRT) GTPU_GPDU_PKTS_RECV_RAT_VIRT",
            "SUM(GRE_TUN_PMIP_IPV4_PACKETS_RX) GRE_TUN_PMIP_IPV4_PACKETS_RX",
            "SUM(GRE_TUN_PMIP_IPV6_PACKETS_RX) GRE_TUN_PMIP_IPV6_PACKETS_RX",
            "SUM(IPV4_TPDU_PACKETS_RECEIVED) IPV4_TPDU_PACKETS_RECEIVED",
            "SUM(IPV6_TPDU_PACKETS_RECEIVED) IPV6_TPDU_PACKETS_RECEIVED",
            "SUM(UP_PKTS_DROPPED) UP_PKTS_DROPPED",
            "SUM(UPLINK_DROP_FORGED_UE_SRC_ADDR) UPLINK_DROP_FORGED_UE_SRC_ADDR",
            "SUM(UP_DROP_PKTS_BLOCKING_FLAG_SET) UP_DROP_PKTS_BLOCKING_FLAG_SET",
            "SUM(PKTS_DROPPED_MAX_FLOW_REACHED) PKTS_DROPPED_MAX_FLOW_REACHED",
            """round(decode(((
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_2G),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_3G),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_LTE),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_UNKN),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_WLAN),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_VIRT),0) + 
nvl(SUM(IPV4_TPDU_PACKETS_RECEIVED),0) + 
nvl(SUM(IPV6_TPDU_PACKETS_RECEIVED),0) + 
nvl(SUM(GRE_TUN_PMIP_IPV4_PACKETS_RX),0) + 
nvl(SUM(GRE_TUN_PMIP_IPV6_PACKETS_RX),0)
)),0,NULL, (((
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_2G),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_3G),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_LTE),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_UNKN),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_WLAN),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_VIRT),0) + 
nvl(SUM(IPV4_TPDU_PACKETS_RECEIVED),0) + 
nvl(SUM(IPV6_TPDU_PACKETS_RECEIVED),0) + 
nvl(SUM(GRE_TUN_PMIP_IPV4_PACKETS_RX),0) + 
nvl(SUM(GRE_TUN_PMIP_IPV6_PACKETS_RX),0)
) - (
SUM(UP_PKTS_DROPPED) + 
nvl(SUM(UPLINK_DROP_FORGED_UE_SRC_ADDR),0) + 
nvl(SUM(UP_DROP_PKTS_BLOCKING_FLAG_SET),0) + 
nvl(SUM(PKTS_DROPPED_MAX_FLOW_REACHED),0) )
)) / ((
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_2G),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_3G),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_LTE),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_UNKN),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_WLAN),0) + 
nvl(SUM(GTPU_GPDU_PKTS_RECV_RAT_VIRT),0) + 
nvl(SUM(IPV4_TPDU_PACKETS_RECEIVED),0) + 
nvl(SUM(IPV6_TPDU_PACKETS_RECEIVED),0) + 
nvl(SUM(GRE_TUN_PMIP_IPV4_PACKETS_RX),0) + 
nvl(SUM(GRE_TUN_PMIP_IPV6_PACKETS_RX),0)))),4)*100 a"""
          ]
        },
        'sql_tables' : [
            {
                'sql_items'      : {
                    'sql_items_15_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24:mi')                  BH",
                        "SUM(GTPU_GPDU_PKTS_RECV_RAT_2G) GTPU_GPDU_PKTS_RECV_RAT_2G",
                        "SUM(GTPU_GPDU_PKTS_RECV_RAT_3G) GTPU_GPDU_PKTS_RECV_RAT_3G",
                        "SUM(GTPU_GPDU_PKTS_RECV_LTE) GTPU_GPDU_PKTS_RECV_LTE",
                        "SUM(GTPU_GPDU_PKTS_RECV_RAT_UNKN) GTPU_GPDU_PKTS_RECV_RAT_UNKN",
                        "SUM(GTPU_GPDU_PKTS_RECV_RAT_WLAN) GTPU_GPDU_PKTS_RECV_RAT_WLAN",
                        "SUM(GTPU_GPDU_PKTS_RECV_RAT_VIRT) GTPU_GPDU_PKTS_RECV_RAT_VIRT"
                    ],
                    'sql_items_60_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24')                  BH",
                        "SUM(GTPU_GPDU_PKTS_RECV_RAT_2G) GTPU_GPDU_PKTS_RECV_RAT_2G",
                        "SUM(GTPU_GPDU_PKTS_RECV_RAT_3G) GTPU_GPDU_PKTS_RECV_RAT_3G",
                        "SUM(GTPU_GPDU_PKTS_RECV_LTE) GTPU_GPDU_PKTS_RECV_LTE",
                        "SUM(GTPU_GPDU_PKTS_RECV_RAT_UNKN) GTPU_GPDU_PKTS_RECV_RAT_UNKN",
                        "SUM(GTPU_GPDU_PKTS_RECV_RAT_WLAN) GTPU_GPDU_PKTS_RECV_RAT_WLAN",
                        "SUM(GTPU_GPDU_PKTS_RECV_RAT_VIRT) GTPU_GPDU_PKTS_RECV_RAT_VIRT"
                    ]
                },
                'sql_tables': [
                    'pcofng_ps_gtpu_gtpu_raw sgw',
                    'UTP_COMMON_OBJECTS objects'  
                ],
                'sql_where' : [ 
                    'sgw.FING_id=objects.CO_Gid', 
                ],
                'table_name' : "sgw"
            },
            {
                'sql_items'      : {
                    'sql_items_15_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24:mi')                  BH",
                        "SUM(GRE_TUN_PMIP_IPV4_PACKETS_RX) GRE_TUN_PMIP_IPV4_PACKETS_RX",
                        "SUM(GRE_TUN_PMIP_IPV6_PACKETS_RX) GRE_TUN_PMIP_IPV6_PACKETS_RX"
                ],
                    'sql_items_60_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24')                  BH",
                        "SUM(GRE_TUN_PMIP_IPV4_PACKETS_RX) GRE_TUN_PMIP_IPV4_PACKETS_RX",
                        "SUM(GRE_TUN_PMIP_IPV6_PACKETS_RX) GRE_TUN_PMIP_IPV6_PACKETS_RX"
                    ],
                },
                'sql_tables': [
                    'pcofng_ps_gretun_gre_raw sgw',
                    'UTP_COMMON_OBJECTS objects' 
                ],
                'sql_where' : [ 
                    'sgw.FING_id=objects.CO_Gid'
                ],
                'table_name' : "table1"
            },
            {
                'sql_items'      : {
                    'sql_items_15_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')  REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24:mi')     BH",
                        "SUM(IPV4_TPDU_PACKETS_RECEIVED) IPV4_TPDU_PACKETS_RECEIVED",
                        "SUM(IPV6_TPDU_PACKETS_RECEIVED) IPV6_TPDU_PACKETS_RECEIVED"
                    ],
                    'sql_items_60_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')  REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24')        BH",
                        "SUM(IPV4_TPDU_PACKETS_RECEIVED) IPV4_TPDU_PACKETS_RECEIVED",
                        "SUM(IPV6_TPDU_PACKETS_RECEIVED) IPV6_TPDU_PACKETS_RECEIVED"
                    ],
                },
                'sql_tables': [
                    'pcofng_ps_iptra_ip_raw sgw',
                    'UTP_COMMON_OBJECTS objects'  
                ],
                'sql_where' : [ 
                    'sgw.FING_id=objects.CO_Gid' 
                ],
                'table_name' : "table2"
            },
            {
                'sql_items'      : {
                    'sql_items_15_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')  REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24:mi')     BH",
                        "SUM(UP_PKTS_DROPPED) UP_PKTS_DROPPED",
                        "SUM(UPLINK_DROP_FORGED_UE_SRC_ADDR) UPLINK_DROP_FORGED_UE_SRC_ADDR",
                        "SUM(UP_DROP_PKTS_BLOCKING_FLAG_SET) UP_DROP_PKTS_BLOCKING_FLAG_SET",
                        "SUM(PKTS_DROPPED_MAX_FLOW_REACHED) PKTS_DROPPED_MAX_FLOW_REACHED"
                    ],
                    'sql_items_60_SAEGW' : [
                        "FING_ID",
                        "CO_NAME",
                        "to_char(sgw.PERIOD_START_TIME,'yyyy/mm/dd')  REPDATE",
                        "to_char(sgw.PERIOD_START_TIME,'hh24')        BH",
                        "SUM(UP_PKTS_DROPPED) UP_PKTS_DROPPED",
                        "SUM(UPLINK_DROP_FORGED_UE_SRC_ADDR) UPLINK_DROP_FORGED_UE_SRC_ADDR",
                        "SUM(UP_DROP_PKTS_BLOCKING_FLAG_SET) UP_DROP_PKTS_BLOCKING_FLAG_SET",
                        "SUM(PKTS_DROPPED_MAX_FLOW_REACHED) PKTS_DROPPED_MAX_FLOW_REACHED"
                    ],
                },
                'sql_tables': [
                    'pcofng_ps_urpl_usrplane_raw sgw',
                    'UTP_COMMON_OBJECTS objects'  
                ],
                'sql_where' : [ 
                    'sgw.FING_id=objects.CO_Gid' 
                ],
                'table_name' : "table3"
            },
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid',
            'table1.FING_id=objects.CO_Gid',
            'table2.FING_id=objects.CO_Gid',
            'table3.FING_id=objects.CO_Gid',
            'sgw.REPDATE=table1.REPDATE',
            'sgw.BH=table1.BH', 
            'sgw.REPDATE=table2.REPDATE',
            'sgw.BH=table2.BH',
            'sgw.REPDATE=table3.REPDATE',
            'sgw.BH=table3.BH',
        ],
        'sql_group' : [
            "sgw.REPDATE",
            "sgw.BH",
            "sgw.fing_id",
            "objects.co_name"
        ],
        'sql_order' : [
            "sgw.REPDATE",
            "sgw.BH",
            "sgw.fing_id",
            "objects.co_name"
        ]

    },
    'LTE-SBCPU'     : {
        'func'         : saegw_sbcpu,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'SB板卡CPU负荷',
                        u'IB板卡CPU负荷'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')	BH",
            "round(AVG(CASE WHEN FNODE_ID LIKE 'AS%_%' THEN (OLC_LOAD_LEVEL_AVE) ELSE NULL END), 1) AVG_SB_CPU_USAGE",
            "round(AVG(CASE WHEN FNODE_ID LIKE 'IB%_%' THEN (OLC_LOAD_LEVEL_AVE) ELSE NULL END), 1) AVG_IB_CPU_USAGE"
    	  ],
          'sql_items_60_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')		    BH",
            "round(AVG(CASE WHEN FNODE_ID LIKE 'AS%_%' THEN (OLC_LOAD_LEVEL_AVE) ELSE NULL END), 1) AVG_SB_CPU_USAGE",
            "round(AVG(CASE WHEN FNODE_ID LIKE 'IB%_%' THEN (OLC_LOAD_LEVEL_AVE) ELSE NULL END), 1) AVG_IB_CPU_USAGE"
          ]
        },
        'sql_tables' : [
            'pcofng_ps_ovld_ovld_raw sgw',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid' 
        ]
    },
    'LTE-SABCPU'     : {
        'func'         : saegw_sabcpu,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'SAB板卡CPU负荷'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')	BH",
            "round(AVG(CASE WHEN FNODE_ID LIKE 'SAB%_%' THEN UP_AVG_FASTPATH_CPU_LOAD ELSE NULL END),1) UP_AVG_FASTPATH_CPU_LOAD_SAB"
    	  ],
          'sql_items_60_SAEGW' : [
            "FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')		    BH",
            "round(AVG(CASE WHEN FNODE_ID LIKE 'SAB%_%' THEN UP_AVG_FASTPATH_CPU_LOAD ELSE NULL END),1) UP_AVG_FASTPATH_CPU_LOAD_SAB"
          ]
        },
        'sql_tables' : [
            'pcofng_ps_urpl_usrplane_raw sgw',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'sgw.FING_id=objects.CO_Gid' 
        ]
    }
    
}
