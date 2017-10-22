#coding=utf-8

from GetConfig import *

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

# make sql scripts for parts of 'select', 'from', 'where'
def getSAEGWSQL_main(api_sql_info, param):
    
    sql_item_type = 'sql_items_' + param.selectperiod + '_' + param.selectsaegwelement
    #print('sql_item_type : ',sql_item_type)
    sql_item = api_sql_info['sql_items'][sql_item_type]
    sqlstring = 'select \n'
    sqlstring = sqlstring + ',\n'.join(sql_item) + '\n'
    sqlstring = sqlstring + 'from ' + ','.join(api_sql_info['sql_tables']) + '\n'
    sqlstring = sqlstring + 'where ' + ' and '.join(api_sql_info['sql_where']) + '\n'
    return sqlstring

# SAEGW PGW
def saegw_4g_pgw(kpi_title, cursor, param):
	
    sqlstring = ""
    
    api_sql_info = saegw_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getSAEGWSQL_main(api_sql_info, param)
    #print sqlstring

    sqlstring = getSAEGWSQL_other_oracle(sqlstring,param)
    #print(sqlstring)
    cursor.execute(sqlstring)
    row=cursor.fetchall()
    return (api_sql_info['title'],row)

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
    except:
        print 'something error!'
        return (['error'], None)
	
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
    except:
        print 'something error!'
        return (['error'], None)

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
    except:
        print 'something error!'
        return (['error'], None)	

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
    except:
            print 'something error!'
            return (['error'], None)	

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
    except:
        print 'something error!'
        return (['error'], None)	
		
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
    except:
        print 'something error!'
        return (['error'], None)	
		
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
    except:
        print 'something error!'
        return (['error'], None)	

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
    except:
        print 'something error!'
        return (['error'], None)

saegw_api_sql_function = {
    'LTE-PGW'     : {
        'func'         : saegw_4g_pgw,
        'title'        : [
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'Session',
                        u'PGW承载容量峰值',
                        u'PGW承载容量峰值利用率',
                        u'PGW承载容量平均值',
                        u'PGW承载容量平均利用率',
                        u'PGW专用承载建立成功次数',
                        u'PGW专用承载建立次数',
                        u'PGW专用承载建立成功率',
                        u'PGW session建立次数',
                        u'PGW session建立成功数',
                        u'PGW session建立成功率',
                        u'PGW session去激活数',
                        u'PGW 全部session',
                        u'PGW 2g session',
                        u'PGW 3g session',
                        u'PGW 4g session',
                        u'PGW Session数',
                        u'SAEGW Session'
        ],
        'sql_items'      : {
          'sql_items_15_SAEGW' : [
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')                  BH",
            "'ALL' ",
            "SUM(SM_MAX_NBR_ACT_BEAR_P_GW) SM_MAX_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_MAX_NBR_ACT_BEAR_P_GW)/1280000*100,2) SM_MAX_NBR_ACT_BEAR_P_GW_R",
            "SUM(SM_AVE_NBR_ACT_BEAR_P_GW) SM_AVE_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_AVE_NBR_ACT_BEAR_P_GW)/1280000*100,2) SM_AVE_NBR_ACT_BEAR_P_GW_R",
            "sum(SM_SUCC_BEARER_ACT) SM_SUCC_BEARER_ACT",
            "sum(SM_ATT_BEARER_ACT) SM_ATT_BEARER_ACT",
            "decode(nvl((sum(SM_ATT_BEARER_ACT)),0),0,0,(round((sum(SM_SUCC_BEARER_ACT)/(sum(SM_ATT_BEARER_ACT))),4)*100)) PdpSR",
            " SUM(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW) PGW_ACT_ATT",
            "SUM(SM_SUCC_SESS_ACT_P_GW) PGW_ACT_SUCC",
            "decode(nvl((sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW)),0),0,0,(round((sum(SM_SUCC_SESS_ACT_P_GW)/(sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW))),4)*100)) PGWSR",
            "sum(SM_SUCC_SESS_DEACT_GGSN_INIT) deactsession ",
            "sum(SM_NBR_ACT_SESS_P_GW+SM_NBR_ACT_SESS_SAE_GW) allsession",
            "sum(SM_NBR_ACT_SESS_RAT_2G) twogsession",
            "SUM(SM_NBR_ACT_SESS_RAT_3G) threegsession",
            "SUM(SM_NBR_ACT_SESS_RAT_4G) fourgSESSION",
            "sum(SM_NBR_ACT_SESS_P_GW) allpgwsession",
            "sum(SM_NBR_ACT_SESS_SAE_GW) allsaegwsession"
	      ],
          'sql_items_60_SAEGW' : [
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')                  BH",
            "'ALL' ",
            "round(SUM(SM_MAX_NBR_ACT_BEAR_P_GW)/4,0) SM_MAX_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_MAX_NBR_ACT_BEAR_P_GW)/4/1280000*100,2) SM_MAX_NBR_ACT_BEAR_P_GW_R",
            "round(SUM(SM_AVE_NBR_ACT_BEAR_P_GW)/4,0) SM_AVE_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_AVE_NBR_ACT_BEAR_P_GW)/4/1280000*100,2) SM_AVE_NBR_ACT_BEAR_P_GW_R",
            "sum(SM_SUCC_BEARER_ACT) SM_SUCC_BEARER_ACT", 
            "sum(SM_ATT_BEARER_ACT) SM_ATT_BEARER_ACT", 
            "decode(nvl((sum(SM_ATT_BEARER_ACT)),0),0,0,(round((sum(SM_SUCC_BEARER_ACT)/(sum(SM_ATT_BEARER_ACT))),4)*100)) PdpSR",
            "SUM(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW) PGW_ACT_ATT",
            "SUM(SM_SUCC_SESS_ACT_P_GW) PGW_ACT_SUCC",
            "decode(nvl((sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW)),0),0,0,(round((sum(SM_SUCC_SESS_ACT_P_GW)/(sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW))),4)*100)) PGWSR",
            "sum(SM_SUCC_SESS_DEACT_GGSN_INIT) deactsession ",
            "round(sum(SM_NBR_ACT_SESS_P_GW+SM_NBR_ACT_SESS_SAE_GW)/4,0) allsession",
            "round(sum(SM_NBR_ACT_SESS_RAT_2G)/4,0) twogsession",
            "round(SUM(SM_NBR_ACT_SESS_RAT_3G)/4,0) threegsession",
            "round(SUM(SM_NBR_ACT_SESS_RAT_4G)/4,0) fourgSESSION",
            "round(sum(SM_NBR_ACT_SESS_P_GW)/4,0) allpgwsession",
            "round(sum(SM_NBR_ACT_SESS_SAE_GW)/4,0) allsaegwsession"
           ],
           'sql_items_15_SESSION' : [
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')                  BH",
            "SSPROF_ID SSPROF",
            "SUM(SM_MAX_NBR_ACT_BEAR_P_GW) SM_MAX_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_MAX_NBR_ACT_BEAR_P_GW)/1280000*100,2) SM_MAX_NBR_ACT_BEAR_P_GW_R",
            "SUM(SM_AVE_NBR_ACT_BEAR_P_GW) SM_AVE_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_AVE_NBR_ACT_BEAR_P_GW)/1280000*100,2) SM_AVE_NBR_ACT_BEAR_P_GW_R",
            "sum(SM_SUCC_BEARER_ACT) SM_SUCC_BEARER_ACT", 
            "sum(SM_ATT_BEARER_ACT) SM_ATT_BEARER_ACT", 
            "decode(nvl((sum(SM_ATT_BEARER_ACT)),0),0,0,(round((sum(SM_SUCC_BEARER_ACT)/(sum(SM_ATT_BEARER_ACT))),4)*100)) PdpSR",
            " SUM(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW) PGW_ACT_ATT",
            "SUM(SM_SUCC_SESS_ACT_P_GW) PGW_ACT_SUCC",
            "decode(nvl((sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW)),0),0,0,(round((sum(SM_SUCC_SESS_ACT_P_GW)/(sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW))),4)*100)) PGWSR",
            "sum(SM_SUCC_SESS_DEACT_GGSN_INIT) deactsession ",
            "sum(SM_NBR_ACT_SESS_P_GW+SM_NBR_ACT_SESS_SAE_GW) allsession",
            "sum(SM_NBR_ACT_SESS_RAT_2G) twogsession",
            "SUM(SM_NBR_ACT_SESS_RAT_3G) threegsession",
            "SUM(SM_NBR_ACT_SESS_RAT_4G) fourgSESSION",
            "sum(SM_NBR_ACT_SESS_P_GW) allpgwsession",
            "sum(SM_NBR_ACT_SESS_SAE_GW) allsaegwsession"
	      ],
          'sql_items_60_SESSION' : [
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')                  BH",
            "SSPROF_ID SSPROF",
            "round(SUM(SM_MAX_NBR_ACT_BEAR_P_GW)/4,0) SM_MAX_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_MAX_NBR_ACT_BEAR_P_GW)/4/1280000*100,2) SM_MAX_NBR_ACT_BEAR_P_GW_R",
            "round(SUM(SM_AVE_NBR_ACT_BEAR_P_GW)/4,0) SM_AVE_NBR_ACT_BEAR_P_GW",
            "round(SUM(SM_AVE_NBR_ACT_BEAR_P_GW)/4/1280000*100,2) SM_AVE_NBR_ACT_BEAR_P_GW_R",
            "sum(SM_SUCC_BEARER_ACT) SM_SUCC_BEARER_ACT", 
            "sum(SM_ATT_BEARER_ACT) SM_ATT_BEARER_ACT", 
            "decode(nvl((sum(SM_ATT_BEARER_ACT)),0),0,0,(round((sum(SM_SUCC_BEARER_ACT)/(sum(SM_ATT_BEARER_ACT))),4)*100)) PdpSR",
            "SUM(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW) PGW_ACT_ATT",
            "SUM(SM_SUCC_SESS_ACT_P_GW) PGW_ACT_SUCC",
            "decode(nvl((sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW)),0),0,0,(round((sum(SM_SUCC_SESS_ACT_P_GW)/(sum(SM_FAIL_SESS_ACT_P_GW+SM_SUCC_SESS_ACT_P_GW))),4)*100)) PGWSR",
            "sum(SM_SUCC_SESS_DEACT_GGSN_INIT) deactsession ",
            "round(sum(SM_NBR_ACT_SESS_P_GW+SM_NBR_ACT_SESS_SAE_GW)/4,0) allsession",
            "round(sum(SM_NBR_ACT_SESS_RAT_2G)/4,0) twogsession",
            "round(SUM(SM_NBR_ACT_SESS_RAT_3G)/4,0) threegsession",
            "round(SUM(SM_NBR_ACT_SESS_RAT_4G)/4,0) fourgSESSION",
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
                        u'SGW 4g 接入数',
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
            "sum(SM_NBR_ACT_SGW_RAT_4G) SGW4G",
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
            "round(SUM(SM_NBR_ACT_SGW_RAT_4G)/4,0) SGW4G",
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
                        u'GTPU下行吞吐率(Mbit/s)'
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
            "sum(GTPU_DOWNLINK_THROUGHPUT) GTPU_DOWNLINK_THROUGHPUT"
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
            "round(sum(GTPU_DOWNLINK_THROUGHPUT)/4,4) GTPU_DOWNLINK_THROUGHPUT"
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
                            u'Delete Session超时个数',
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
            "sum(GTPCV2_DEL_SESS_REQ_EXCEED_N3) GTPCV2_DEL_SESS_REQ_EXCEED_N3"
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
    }
    
}
