#coding=utf-8

from GetConfig import *

def getCMGSQL_other_oracle(sqlstring, param, groupitem = ""):
    if (not param.selectcmg == 'all'):
        elementlist = []
        for item in param.selectcmg.split(','):
            elementlist.append('\''+item+'\'')
        sqlstring=sqlstring+" and objects.co_name in ( "+','.join(elementlist)+" ) " 
	
    if (param.selectperiodtype=='continue'):
        sqlstringtime=" and to_char(cmg.period_start_time,\'yyyy/mm/dd/hh24:mi\')>=\'"+param.startdate+"/"+param.starttime+\
        "\' and to_char(cmg.period_start_time,\'yyyy/mm/dd/hh24:mi\')<=\'"+param.stopdate+"/"+param.stoptime + "\' "
    else:
        sqlstringtime=" and to_char(cmg.period_start_time,\'yyyy/mm/dd')>=\'"+param.startdate+\
        "\' and to_char(cmg.period_start_time,\'hh24\')>=\'"+param.starttime+\
        " and to_char(cmg.period_start_time,\'yyyy/mm/dd')<=\'"+param.stopdate+\
        "\' and to_char(cmg.period_start_time,\'hh24\')<=\'"+param.stoptime + "\' "
	
    if (groupitem != ""):
        groupitem = " " + groupitem +","
    if (param.selectperiod=='60'):
        if (param.selectcmgelement=='CMG'):
            sqlstring1="group by to_char(cmg.period_start_time,'yyyy/mm/dd'), to_char(cmg.period_start_time,'hh24'), cmg.cmg_id, " + groupitem + " objects.co_name " + "order by objects.co_name,to_char(cmg.period_start_time,'yyyy/mm/dd'),to_char(cmg.period_start_time,'hh24')"
        else:
            sqlstring1="group by to_char(cmg.period_start_time,'yyyy/mm/dd'), to_char(cmg.period_start_time,'hh24'), cmg.cmg_id, " + groupitem + " objects.co_name, SSPROF_ID " + "order by objects.co_name,to_char(cmg.period_start_time,'yyyy/mm/dd'),to_char(cmg.period_start_time,'hh24')"
    else:
        if (param.selectcmgelement=='CMG'):
            sqlstring1="group by to_char(cmg.period_start_time,'yyyy/mm/dd'),to_char(cmg.period_start_time,'hh24:mi'), cmg.cmg_ID, " + groupitem + " objects.co_name " +  "order by objects.CO_name,to_char(cmg.period_start_time,'yyyy/mm/dd'),to_char(cmg.period_start_time,'hh24:mi') "
        else:
            sqlstring1="group by to_char(cmg.period_start_time,'yyyy/mm/dd'),to_char(cmg.period_start_time,'hh24:mi'), cmg.cmg_ID, " + groupitem + " objects.co_name,SSPROF_ID  " + "order by objects.CO_name,to_char(cmg.period_start_time,'yyyy/mm/dd'),to_char(cmg.period_start_time,'hh24:mi') "

    sqlstring=sqlstring+sqlstringtime+sqlstring1
    return sqlstring

# generate table part of sql, table can be a single table name or a (select ...) statement
def generateTableStr(tabledescs, param):
    return_desc = []
    for tabledesc in tabledescs:
        if (isinstance(tabledesc, str)):
            return_desc.append(tabledesc)
        else:
            sqlstring = getCMGSQL_main(tabledesc, param)
            sqlstring = getCMGSQL_other_oracle(sqlstring, param)
            return_desc.append("( \n%s\n ) %s" % (sqlstring, tabledesc['table_name']))
    return return_desc

# make sql scripts for parts of 'select', 'from', 'where'
def getCMGSQL_main(api_sql_info, param):
    sql_item_type = 'sql_items_' + param.selectperiod + '_' + param.selectcmgelement
    #print('sql_item_type : ',sql_item_type)
    sql_item = api_sql_info['sql_items'][sql_item_type]
    sqlstring = 'select \n'
    sqlstring = sqlstring + ',\n'.join(sql_item) + '\n'
    sqlstring = sqlstring + 'from ' + ','.join(generateTableStr(api_sql_info['sql_tables'], param)) + '\n'
    sqlstring = sqlstring + 'where ' + ' and '.join(api_sql_info['sql_where']) + '\n'
    return sqlstring

# CMG PGW
def cmg_4g_pgw(kpi_title, cursor, param):
	
    sqlstring = ""
    
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_4g_pgw: " + str(e)
        return (['error', errorMessage], None)
# CMG SGW
def cmg_4g_sgw(kpi_title, cursor, param):

    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_4g_cmg: " + str(e)
        return (['error', errorMessage], None)
	
def cmg_4g_cdr_radius(kpi_title,cursor,param):

    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_4g_cdr_radius: " + str(e)
        return (['error', errorMessage], None)

# SGW THROUGHPUT
def pgw_cmg_throughput(kpi_title,cursor,param):
    
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error pgw_cmg_throughput: " + str(e)
        return (['error', errorMessage], None)	

def cmg_gtpu_throughput(kpi_title,cursor,param):
    # GSM PDP 3G
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_gtpu_throughput: " + str(e)
        return (['error', errorMessage], None)	

def cmg_s1u_throughput(kpi_title,cursor,param):
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_s1u_throughput: " + str(e)
        return (['error', errorMessage], None)	
		
def cmg_session(kpi_title,cursor,param):
	# GSM PAGING 3G
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_session: " + str(e)
        return (['error', errorMessage], None)	
		
def cmg_sgi_throughput(kpi_title,cursor,param):
    # GSM users 4G
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    try:
        sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_sgi_throughput: " + str(e)
        return (['error', errorMessage], None)	

def cmg_ip_pool(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    #param['groupitem'] = "perpool_id"
    try:
        sqlstring = getCMGSQL_other_oracle(sqlstring,param, "perpool_id")
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_ip_pool: " + str(e)
        return (['error', errorMessage], None)

def cmg_downdata_notice(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print ("%s sqlstring is: \n%s\n" % ('cmg_downdata_notice', sqlstring)) 
    #param['groupitem'] = "perpool_id"
    try:
        #sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        sqlstring = sqlstring + ' \ngroup by ' + ','.join(api_sql_info['sql_group']) \
            + ' \norder by ' + ','.join(api_sql_info['sql_order'])
        #print("%s sqlstring is: \n%s\n" % ('cmg_downdata_notice', sqlstring))
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_downdata_notice: " + str(e)
        return (['error', errorMessage], None)

def cmg_dataforward_succ(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print ("%s sqlstring is: \n%s\n" % ('cmg_downdata_notice', sqlstring)) 
    #param['groupitem'] = "perpool_id"
    try:
        #sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        sqlstring = sqlstring + ' \ngroup by ' + ','.join(api_sql_info['sql_group']) \
            + ' \norder by ' + ','.join(api_sql_info['sql_order'])
        #print("%s sqlstring is: \n%s\n" % ('cmg_downdata_notice', sqlstring))
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_dataforward_succ: " + str(e)
        return (['error', errorMessage], None)

def cmg_sbcpu(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    #param['groupitem'] = "perpool_id"
    try:
        sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_sbcpu: " + str(e)
        return (['error', errorMessage], None)

def cmg_sabcpu(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    #param['groupitem'] = "perpool_id"
    try:
        sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_sabcpu: " + str(e)
        return (['error', errorMessage], None)

def cmg_pdn(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    #param['groupitem'] = "perpool_id"
    try:
        sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        #print(sqlstring)
        cursor.execute(sqlstring)
        row=cursor.fetchall()
        return (api_sql_info['title'],row)
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error cmg_pdn: " + str(e)
        return (['error', errorMessage], None)

def cmg_createbearer(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
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
        errorMessage = "Error cmg_createbearer: " + str(e)
        return (['error', errorMessage], None)

def cmg_s11createsession(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
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
        errorMessage = "Error cmg_s11createsession: " + str(e)
        return (['error', errorMessage], None)

def cmgdb_conn(runmode):
    try:
        (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(runmode, "cmgdb")
        db = cx_Oracle.connect(dbuser, dbpasswd, dburl)
        dbcursor=db.cursor()
        return dbcursor
    except Exception as e:
        return None

cmg_api_sql_function = {
    'LTE-S1U-THROUGH'     : {
        'func'         : cmg_s1u_throughput,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'S1US5U上行字节数',
                        u'S1US8U上行字节数',
                        u'S5US1U下行字节数',
                        u'S8US1U下行字节数',
                        u'S1u流量'
        ],
        'sql_items'      : {
          'sql_items_15_CMG' : [
            "CMG_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')	BH",
            "SUM(s1uS5uUlBytes) s1uS5uUlBytes",
            "SUM(s1uS8uUlBytes) s1uS8uUlBytes",
            "SUM(s5uS1uDlBytes) s5uS1uDlBytes",
            "SUM(s8uS1uDlBytes) s8uS1uDlBytes",
            "SUM(s1uS5uUlBytes)+SUM(s1uS8uUlBytes)+SUM(s5uS1uDlBytes)+SUM(s8uS1uDlBytes) s1uAllBytes"
    	  ],
          'sql_items_60_CMG' : [
            "CMG_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')		    BH",
            "SUM(s1uS5uUlBytes) s1uS5uUlBytes",
            "SUM(s1uS8uUlBytes) s1uS8uUlBytes",
            "SUM(s5uS1uDlBytes) s5uS1uDlBytes",
            "SUM(s8uS1uDlBytes) s8uS1uDlBytes",
            "SUM(s1uS5uUlBytes)+SUM(s1uS8uUlBytes)+SUM(s5uS1uDlBytes)+SUM(s8uS1uDlBytes) s1uAllBytes"
          ]
        },
        'sql_tables' : [
            'epccmg_ps_m10_mda_raw cmg',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'cmg.cmg_id=objects.CO_Gid' 
        ]
    },
    'LTE-SGI-THROUGH'     : {
        'func'         : cmg_sgi_throughput,
        'title'        : [
                u'设备ID',
                u'设备名称',
                u'日期',
                u'时间',
                u'SGi Gn 下行字节',
                u'SGi Gp 下行字节',
                u'SGi S1u 下行字节',
                u'SGi S5u 下行字节',
                u'SGi S8u 下行字节',
                u'Gn SGi 下行字节',
                u'Gp SGi 下行字节',
                u'S1u SGi 下行字节',
                u'S5u SGi 下行字节',
                u'S8u SGi 下行字节',
                u'SGi 总流量'
        ],
        'sql_items'      : {
          'sql_items_15_CMG' : [
            "CMG_ID",
            "CO_NAME",
            "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
            "to_char(cmg.PERIOD_START_TIME,'hh24:mi') BH",
            "SUM(giGnDlBytes) giGnDlBytes",
            "SUM(giGpDlBytes) giGpDlBytes",
            "SUM(giS1uDlBytes) giS1uDlBytes",
            "SUM(giS5uDlBytes) giS5uDlBytes",
            "SUM(giS8uDlBytes) giS8uDlBytes",
            "SUM(gnGiUlBytes) gnGiUlBytes",
            "SUM(gpGiUlBytes) gpGiUlBytes",
            "SUM(s1uGiUlBytes) s1uGiUlBytes",
            "SUM(s5uGiUlBytes) s5uGiUlBytes",
            "SUM(s8uGiUlBytes) s8uGiUlBytes",
            "SUM(giGnDlBytes)+SUM(giGpDlBytes)+SUM(giS1uDlBytes)+SUM(giS5uDlBytes)+SUM(giS8uDlBytes)+SUM(gnGiUlBytes)+SUM(gpGiUlBytes)+SUM(s1uGiUlBytes)+SUM(s5uGiUlBytes)+SUM(s8uGiUlBytes) SGiBytes"
    	  ],
          'sql_items_60_CMG' : [
            "CMG_ID",
            "CO_NAME",
            "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
            "to_char(cmg.PERIOD_START_TIME,'hh24') BH",
            "SUM(giGnDlBytes) giGnDlBytes",
            "SUM(giGpDlBytes) giGpDlBytes",
            "SUM(giS1uDlBytes) giS1uDlBytes",
            "SUM(giS5uDlBytes) giS5uDlBytes",
            "SUM(giS8uDlBytes) giS8uDlBytes",
            "SUM(gnGiUlBytes) gnGiUlBytes",
            "SUM(gpGiUlBytes) gpGiUlBytes",
            "SUM(s1uGiUlBytes) s1uGiUlBytes",
            "SUM(s5uGiUlBytes) s5uGiUlBytes",
            "SUM(s8uGiUlBytes) s8uGiUlBytes",
            "SUM(giGnDlBytes)+SUM(giGpDlBytes)+SUM(giS1uDlBytes)+SUM(giS5uDlBytes)+SUM(giS8uDlBytes)+SUM(gnGiUlBytes)+SUM(gpGiUlBytes)+SUM(s1uGiUlBytes)+SUM(s5uGiUlBytes)+SUM(s8uGiUlBytes) SGiBytes"
          ]
        },
        'sql_tables' : [
            'epccmg_ps_m11_mda_raw cmg',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'cmg.cmg_id=objects.CO_Gid' 
        ]
    },
    'LTE-PDN'     : {
        'func'         : cmg_pdn,
        'title'        : [
                        u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'IPv4v6 Session',
                        u'IPv4 Session',
                        u'IPv6 Session'
        ],
        'sql_items'      : {
          'sql_items_15_CMG' : [
            "cmg.CMG_ID",
            "objects.CO_NAME",
            "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
            "to_char(cmg.PERIOD_START_TIME,'hh24:mi') BH",
            "SUM(numberOfIpv4Ipv6PdnSessions) numberOfIpv4Ipv6PdnSessions",
            "SUM(numberOfIpv4PdnSessions) numberOfIpv4PdnSessions",
            "SUM(numberOfIpv6PdnSessions) numberOfIpv6PdnSessions"
          ],
          'sql_items_60_CMG' : [
            "cmg.CMG_ID",
            "objects.CO_NAME",
            "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
            "to_char(cmg.PERIOD_START_TIME,'hh24') BH",
            "round(SUM(numberOfIpv4Ipv6PdnSessions)/4,0) numberOfIpv4Ipv6PdnSessions",
            "round(SUM(numberOfIpv4PdnSessions)/4,0) numberOfIpv4PdnSessions",
            "round(SUM(numberOfIpv6PdnSessions)/4,0) numberOfIpv6PdnSessions"
          ]
        },
        'sql_tables' : [
            'epccmg_ps_m71_mda_raw cmg',
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'cmg.cmg_id=objects.CO_Gid' 
        ]
    }
}
