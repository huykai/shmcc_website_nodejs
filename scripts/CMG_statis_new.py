#coding=utf-8

# M2 EPCCMG_PS_M2_MDA_RAW measInfoId="KPISystemCP-ISA"
# M5 EPCCMG_PS_M5_MDA_RAW measInfoId="KPIBearerManagementSGWCP-ISA"
# M3 EPCCMG_PS_M3_MDA_RAW measInfoId="KPIBearerManagementPGWCP-ISA"
# M4 EPCCMG_PS_M4_MDA_RAW measInfoId="KPIBearerManagementGGSNCP-ISA"
# M10 EPCCMG_PS_M10_MDA_RAW measInfoId="KPIBearerTrafficMSMSGW"
# M11 EPCCMG_PS_M11_MDA_RAW measInfoId="KPIBearerTrafficMSMPGW"
# M12 EPCCMG_PS_M12_MDA3_RAW measInfoId="KPIBearerTrafficApnCP-ISA"
# M17 EPCCMG_PS_M17_SLOT1_RAW measInfoId="KPISystemCPM"
# M18 EPCCMG_PS_M18_SLOT1_RAW measInfoId="KPIPathManagementCPM"
# M19 EPCCMG_PS_M19_PORT3_RAW measInfoId="KPIPathManagementS1U"
# M20 EPCCMG_PS_M20_PORT3_RAW measInfoId="KPIPathManagementS11"
# M23 EPCCMG_PS_M23_PORT3_RAW measInfoId="KPIPathManagementS5"
# M24 EPCCMG_PS_M24_PORT3_RAW measInfoId="KPIPathManagementS8"
# M26 EPCCMG_PS_M26_PORT4_RAW measInfoId="KPIPathManagementGX"
# M27 EPCCMG_PS_M27_PORT3_RAW measInfoId="KPIPathManagementGN"
# M30 EPCCMG_PS_M30_PORT4_RAW measInfoId="KPIPathManagementGY" 
# M29 EPCCMG_PS_M29_PORT4_RAW measInfoId="KPIPathManagementGA"
# M39 EPCCMG_PS_M39_PORT3_RAW measInfoId="KPIReferencePointS1U"
# M40 EPCCMG_PS_M40_PORT3_RAW measInfoId="KPIReferencePointS11"
# M43 EPCCMG_PS_M43_PORT3_RAW measInfoId="KPIReferencePointS5"
# M44 EPCCMG_PS_M44_PORT3_RAW measInfoId="KPIReferencePointS8"
# M45 EPCCMG_PS_M45_PORT4_RAW measInfoId="KPIReferencePointGX"
# M46 EPCCMG_PS_M46_PORT3_RAW measInfoId="KPIReferencePointGN"
# M48 EPCCMG_PS_M48_PORT4_RAW measInfoId="KPIReferencePointGY"
# M49 EPCCMG_PS_M49_PORT4_RAW measInfoId="KPIReferencePointGA"
# M63 EPCCMG_PS_M63_MDA_RAW measInfoId="KPISctpMSCPSummary"
# M74 EPCCMG_PS_M74_MDA5_RAW measInfoId="KPIRefPtFailureCauseCodeCPM"
# M16 EPCCMG_PS_M16_QTAG6_RAW measInfoId="KPIIpReasMda"
# M64 EPCCMG_PS_M64_MDA_RAW measInfoId="KCISystemCP-ISA"
# M65 EPCCMG_PS_M65_SLOT1_RAW measInfoId="KCIBearerManagementCPM"
# M66 EPCCMG_PS_M66_MDA_RAW measInfoId="KCIBearerManagementSGWCP-ISA"
# M67 EPCCMG_PS_M67_MDA_RAW measInfoId="KCIBearerManagementPGWCP-ISA"
# M68 EPCCMG_PS_M68_MDA4_RAW measInfoId="KCIBearerManagementPerQciCP-ISA"
# M70 EPCCMG_PS_M67_MDA_RAW measInfoId="KPIBearerTrafficQciCP-ISA"
# M69 EPCCMG_PS_M69_MDA4_RAW measInfoId="KPIBearerManagementQciCP-ISA
# M69 EPCCMG_PS_M69_MDA4_RAW measInfoId="KPIBearerManagementSgwQciCP-ISA"
# M71 EPCCMG_PS_M71_MDA3_RAW measInfoId="KCIBearerManagementApnCP-ISA"
# M1 EPCCMG_PS_M1_MDA3_RAW measInfoId="KPIBearerManagementApnCP-ISA"
# M78 EPCCMG_PS_M80_VRID5_RAW measInfoId="KCIDataPlaneMSM"
# M81 EPCCMG_PS_M81_PLNAME5_RAW measInfoId="KCIControlPlaneCPM"
# M80 EPCCMG_PS_M80_VRID5_RAW measInfoId="KCIControlPlaneVPRN"
# M81 EPCCMG_PS_M81_PLNAME5_RAW measInfoId="KCIControlPlaneIpPool"
# M72 EPCCMG_PS_M72_PLNAME4_RAW measInfoId="KCIBearerManagementVprnPoolCP-ISA"
# M76 EPCCMG_PS_M76_PRB_RAW measInfoId="KCIPolicyRuleBaseUsers"
# M74 EPCCMG_PS_M74_MDA5_RAW M73 EPCCMG_PS_M73_MSGTYPE_RAW measInfoId="KPIGtpMsgFailureCauseCodeCP-ISA"
# M84 EPCCMG_PS_M84_LCADDR18_RAW measInfoId="KPIGtpuPathTxErrorInd"

import logging
from GetConfig import *
from ReportSuite_SQL import *

logging.basicConfig(filename='pm_logger.log', level=logging.INFO)
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

# RUN Script get from report suite
def cmg_reportsuite(kpi_title, cursor, param):
    sqlstring = []
    
    try:
        sqlstring = create_reportsuite_sql(param)
        api_sql_info = cmg_api_sql_function[kpi_title]
        #print('cmg_reportsuite sqlstring: ' , sqlstring)
        droptemptable_sqlstrings = sqlstring['droptemptable']
        createtemptable_sqlstrings = sqlstring['createtemptable']
        selecttemptable_sqlstring = sqlstring['selecttemptable'][0] 
        #print "droptemptable_sqlstrings: " + droptemptable_sqlstrings
        for drop_command in droptemptable_sqlstrings:
            #print "drop_command: " , drop_command
            try:
                cursor.execute(drop_command)
            except Exception as e:
                print 'cmg_reportsuite droptable catch Error: ' + str(e)    
        #print "after execute droptemptable" 
        #print "createtemptable_sqlstring: " + createtemptable_sqlstrings
        for create_command in createtemptable_sqlstrings:
            #print "create_command: " , create_command
            try:
                cursor.execute(create_command)
            except Exception as e:
                print 'cmg_reportsuite createtable catch Error: ' + str(e)    
        #print "after execute createtemptable"
        #print "selecttemptable_sqlstring: " + selecttemptable_sqlstring
        cursor.execute(selecttemptable_sqlstring)
        #print "after execute selecttemptable"
        row=cursor.fetchall()
        #print 'cmg_reportsuite: ', row
        return ([kpi_title],row)
    except Exception as e:
        print 'cmg_reportsuite catch Error: ' + str(e)
        errorMessage = "Error cmg_reportsuite: " + str(e)
        return (['error', errorMessage], None)


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
def cmg_sgw_throughput(kpi_title,cursor,param):
    
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
    logging.info('api_sql_info : ' , api_sql_info)
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
        sqlstring = getCMGSQL_other_oracle(sqlstring,param, "PLNAME_ID")
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
        #sqlstring = sqlstring + ' \ngroup by ' + ','.join(api_sql_info['sql_group']) \
        #    + ' \norder by ' + ','.join(api_sql_info['sql_order'])
        sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        #print("%s sqlstring is: \n%s\n" % ('cmg_downdata_notice', sqlstring))
        #print(sqlstring)
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

def cmg_mdacpu(kpi_title,cursor,param):
	# GSM ATTACH 4G
    sqlstring = ""
    api_sql_info = cmg_api_sql_function[kpi_title]
    #print('api_sql_info : ' , api_sql_info)
    sqlstring = getCMGSQL_main(api_sql_info, param)
    #print sqlstring
    #param['groupitem'] = "perpool_id"
    try:
        #sqlstring = getCMGSQL_other_oracle(sqlstring,param)
        sqlstring = sqlstring + ' \ngroup by ' + ','.join(api_sql_info['sql_group']) \
            + ' \norder by ' + ','.join(api_sql_info['sql_order'])
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
    'CMG-REPORTSUITE'     : {
        'func'         : cmg_reportsuite,
    },
    'LTE-PGW'     : {
        'func'         : cmg_4g_pgw,
        'title'        : [
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'Session',
                        u'PGW承载容量峰值',
                        u'PGW承载容量峰值利用率',
                        u'PGW承载容量平均值',
                        u'PGW承载容量平均利用率',
                        u'SAEGW承载容量平均值',
                        u'SAEGW承载容量峰值',
                        u'PGW专用承载平均值',
                        u'PGW专用承载峰值',
                        u'PGW 全部session',
                        u'PGW 2/3g session',
                        u'PGW 4g session',
                        u'SAEGW Session'
        ],
        'sql_items'      : {
          'sql_items_15_CMG' : [
            #"CMG_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')	BH",
            "'ALL' ",
            "SUM(MAXNUMBEROFBEARERS+MAXNUMBEROFSGWPGWCMBBEARERS) MAXNUMBEROFBEARERS",
            "round(SUM(MAXNUMBEROFBEARERS+MAXNUMBEROFSGWPGWCMBBEARERS)/1280000*100,2) MAXNUMBEROFBEARERS_RATE",
            "SUM(AVGNUMBEROFBEARERS+AVGNUMBEROFSGWPGWCMBBEARERS) AVGNUMBEROFBEARERS",
            "round(SUM(AVGNUMBEROFBEARERS)/1280000*100,2) AVGNUMBEROFBEARERS_RATE",
            "SUM(AVGNUMBEROFSGWPGWCMBBEARERS) AVGNUMBEROFSAEGWBEARERS",
            "SUM(MAXNUMBEROFSGWPGWCMBBEARERS) MAXNUMBEROFSAEGWBEARERS",
            "sum(AVGNUMBEROFDEDICATEDBEARERS+AVGNUMBOFSGWPGWCMBDEDIBEAR) MAXNUMBEROFDEDICATEDBEARERS",
            "sum(MAXNUMBOFSGWPGWCMBDEDIBEAR+MAXNUMBEROFDEDICATEDBEARERS) AVGNUMBEROFDEDICATEDBEARERS",
            "sum(NUMBEROFPDNSESSIONS+NUMBEROFSGWPGWCMBPDNSESSIONS) allsession",
            "sum(NUMBEROF2G3GSESSIONS) NUMBEROF2G3GSESSIONS",
            "SUM(NUMBEROFPDNSESSIONS) NUMBEROFPDNSESSIONS",
            "sum(NUMBOFSGWPGWCMBDEFABEAR) NUMBOFSGWPGWCMBDEFABEAR"
	      ],
          'sql_items_60_CMG' : [
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')                  BH",
            "'ALL' ",
            "round(SUM(MAXNUMBEROFBEARERS+MAXNUMBEROFSGWPGWCMBBEARERS)/4,0) MAXNUMBEROFBEARERS",
            "round(SUM(MAXNUMBEROFBEARERS)/1280000*100,2) MAXNUMBEROFBEARERS_RATE",
            "round(SUM(AVGNUMBEROFBEARERS+AVGNUMBEROFSGWPGWCMBBEARERS)/4,0) AVGNUMBEROFBEARERS",
            "round(SUM(AVGNUMBEROFBEARERS)/1280000*100,2) AVGNUMBEROFBEARERS_RATE",
            "ROUND(SUM(AVGNUMBEROFSGWPGWCMBBEARERS)/4,0) AVGNUMBEROFSAEGWBEARERS",
            "ROUND(SUM(MAXNUMBEROFSGWPGWCMBBEARERS)/4,0) MAXNUMBEROFSAEGWBEARERS",
            "ROUND(sum(AVGNUMBEROFDEDICATEDBEARERS+AVGNUMBOFSGWPGWCMBDEDIBEAR)/4,0) MAXNUMBEROFDEDICATEDBEARERS",
            "ROUND(sum(MAXNUMBOFSGWPGWCMBDEDIBEAR+MAXNUMBEROFDEDICATEDBEARERS)/4,0) AVGNUMBEROFDEDICATEDBEARERS",
            "ROUND(sum(NUMBEROFPDNSESSIONS+NUMBEROFSGWPGWCMBPDNSESSIONS)/4,0) allsession",
            "ROUND(sum(NUMBEROF2G3GSESSIONS)/4,0) NUMBEROF2G3GSESSIONS",
            "ROUND(SUM(NUMBEROFPDNSESSIONS)/4,0) NUMBEROFPDNSESSIONS",
            "ROUND(sum(NUMBOFSGWPGWCMBDEFABEAR)/4,0) NUMBOFSGWPGWCMBDEFABEAR"
           ],
           'sql_items_15_SESSION' : [
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')                  BH",
            "'ALL' ",
            "SUM(MAXNUMBEROFBEARERS+MAXNUMBEROFSGWPGWCMBBEARERS) MAXNUMBEROFBEARERS",
            "round(SUM(MAXNUMBEROFBEARERS)/1280000*100,2) MAXNUMBEROFBEARERS_RATE",
            "SUM(AVGNUMBEROFBEARERS+AVGNUMBEROFSGWPGWCMBBEARERS) AVGNUMBEROFBEARERS",
            "round(SUM(AVGNUMBEROFBEARERS)/1280000*100,2) AVGNUMBEROFBEARERS_RATE",
            "SUM(AVGNUMBEROFSGWPGWCMBBEARERS) AVGNUMBEROFSAEGWBEARERS",
            "SUM(MAXNUMBEROFSGWPGWCMBBEARERS) MAXNUMBEROFSAEGWBEARERS",
            "sum(AVGNUMBEROFDEDICATEDBEARERS+AVGNUMBOFSGWPGWCMBDEDIBEAR) MAXNUMBEROFDEDICATEDBEARERS",
            "sum(MAXNUMBOFSGWPGWCMBDEDIBEAR+MAXNUMBEROFDEDICATEDBEARERS) AVGNUMBEROFDEDICATEDBEARERS",
            "sum(NUMBEROFPDNSESSIONS+NUMBEROFSGWPGWCMBPDNSESSIONS) allsession",
            "sum(NUMBEROF2G3GSESSIONS) NUMBEROF2G3GSESSIONS",
            "SUM(NUMBEROFPDNSESSIONS) NUMBEROFPDNSESSIONS",
            "sum(NUMBOFSGWPGWCMBDEFABEAR) NUMBOFSGWPGWCMBDEFABEAR"
	      ],
          'sql_items_60_SESSION' : [
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')                  BH",
            "'ALL' ",
            "ROUND(SUM(MAXNUMBEROFBEARERS+MAXNUMBEROFSGWPGWCMBBEARERS)/4,0) MAXNUMBEROFBEARERS",
            "round(SUM(MAXNUMBEROFBEARERS)/1280000*100,2) MAXNUMBEROFBEARERS_RATE",
            "ROUND(SUM(AVGNUMBEROFBEARERS+AVGNUMBEROFSGWPGWCMBBEARERS)/4,0) AVGNUMBEROFBEARERS",
            "round(SUM(AVGNUMBEROFBEARERS)/1280000*100,2) AVGNUMBEROFBEARERS_RATE",
            "round(SUM(AVGNUMBEROFSGWPGWCMBBEARERS)/4,0) AVGNUMBEROFSAEGWBEARERS",
            "round(SUM(MAXNUMBEROFSGWPGWCMBBEARERS)/4,0) MAXNUMBEROFSAEGWBEARERS",
            "round(sum(AVGNUMBEROFDEDICATEDBEARERS+AVGNUMBOFSGWPGWCMBDEDIBEAR)/4,0) MAXNUMBEROFDEDICATEDBEARERS",
            "round(sum(MAXNUMBOFSGWPGWCMBDEDIBEAR+MAXNUMBEROFDEDICATEDBEARERS)/4,0) AVGNUMBEROFDEDICATEDBEARERS",
            "round(sum(NUMBEROFPDNSESSIONS+NUMBEROFSGWPGWCMBPDNSESSIONS)/4,0) allsession",
            "round(sum(NUMBEROF2G3GSESSIONS)/4,0) NUMBEROF2G3GSESSIONS",
            "round(SUM(NUMBEROFPDNSESSIONS)/4,0) NUMBEROFPDNSESSIONS",
            "round(sum(NUMBOFSGWPGWCMBDEFABEAR)/4,0) NUMBOFSGWPGWCMBDEFABEAR"
          ]
        },
        'sql_tables' : [
            'EPCCMG_PS_M67_MDA_RAW cmg',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'cmg.cmg_id=objects.CO_Gid' 
        ]
    },
    'LTE-SGW'     : {
        'func'         : cmg_4g_sgw,
        'title'        : [
                        #u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'SGW承载容量平均值',
                        u'SGW承载容量平均利用率',
                        u'SGW承载容量峰值',
                        u'SGW承载容量峰值利用率',
                        u'SGW专有承载平均值',
                        u'SGW专有承载峰值',
                        u'SGW 会话数',
                        u'SGW 用户数',
                        u'SGW 空闲用户数',
                        u'SGW MME',
                        u'SGW PGW',
                        u'SGW ENB'
        ],
        'sql_items'      : {
          'sql_items_15_CMG' : [
            #"sgw.FING_ID",
            "CO_NAME",
            "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(cmg.PERIOD_START_TIME,'hh24:mi')                  BH",
            "SUM(AVGNUMBEROFBEARERS) AVGNUMBEROFBEARERS",
            "round(SUM(AVGNUMBEROFBEARERS)/1280000*100,2) AVGNUMBEROFBEARERS_R",
            "SUM(MAXNUMBEROFBEARERS) MAXNUMBEROFBEARERS",
            "round(SUM(MAXNUMBEROFBEARERS)/1280000*100,2) MAXNUMBEROFBEARERS_R",
            "sum(AVGNUMBEROFDEDICATEDBEARERS) AVGNUMBEROFDEDICATEDBEARERS",
            "sum(MAXNUMBEROFDEDICATEDBEARERS) MAXNUMBEROFDEDICATEDBEARERS",
            "sum(NUMBEROFPDNSESSIONS) NUMBEROFPDNSESSIONS",
            "sum(NUMBEROFUSERS) NUMBEROFUSERS",
            "sum(NUMBEROFIDLEUSERS) NUMBEROFIDLEUSERS",
            "round(avg(NUMBEROFMMES),0) NUMBEROFMMES",
            "round(avg(NUMBEROFPGWS),0) NUMBEROFPGWS",
            "round(avg(NUMBEROFENBS),0) NUMBEROFENBS"           
	      ],
          'sql_items_60_CMG' : [
            #"sgw.FING_ID",
            "CO_NAME",
            "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
            "to_char(cmg.PERIOD_START_TIME,'hh24')                  BH",
            "ROUND(SUM(AVGNUMBEROFBEARERS)/4,0) AVGNUMBEROFBEARERS",
            "round(SUM(AVGNUMBEROFBEARERS)/1280000*100,2) AVGNUMBEROFBEARERS_R",
            "ROUND(SUM(MAXNUMBEROFBEARERS)/4,0) MAXNUMBEROFBEARERS",
            "round(SUM(MAXNUMBEROFBEARERS)/1280000*100,2) MAXNUMBEROFBEARERS_R",
            "ROUND(sum(AVGNUMBEROFDEDICATEDBEARERS)/4,0) AVGNUMBEROFDEDICATEDBEARERS",
            "ROUND(sum(MAXNUMBEROFDEDICATEDBEARERS)/4,0) MAXNUMBEROFDEDICATEDBEARERS",
            "ROUND(sum(NUMBEROFPDNSESSIONS)/4,0) NUMBEROFPDNSESSIONS",
            "ROUND(sum(NUMBEROFUSERS)/4,0) NUMBEROFUSERS",
            "ROUND(sum(NUMBEROFIDLEUSERS)/4,0) NUMBEROFIDLEUSERS",
            "round(avg(NUMBEROFMMES),0) NUMBEROFMMES",
            "round(avg(NUMBEROFPGWS),0) NUMBEROFPGWS",
            "round(avg(NUMBEROFENBS),0) NUMBEROFENBS"  
           ]
        },
        'sql_tables' : [
            'EPCCMG_PS_M66_MDA_RAW cmg',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'cmg.cmg_id=objects.CO_Gid' 
        ]
    },
    'LTE-SGW-THROUGH'     : {
        'func'         : cmg_sgw_throughput,
        'title'        : [
                        #u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'SGW用户面下行流量(MB)',
                        u'SGW 接收S5流量(MB)',
                        u'SGW 接收S8流量(MB)',
                        u'SGW用户面上行流量(MB)',
                        u'SGW 发送S5流量(MB)',
                        u'SGW 发送S8流量(MB)'
        ],
        'sql_items'      : {
          'sql_items_15_CMG' : [
            #"FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')		    BH",
            "round(sum(S5US1UDLBYTES+S8US1UDLBYTES)/1024/1024,0) S5US8US1UDLBYTES",
            "round(sum(S5US1UDLBYTES)/1024/1024,0) S5US1UDLBYTES",
            "round(sum(S8US1UDLBYTES)/1024/1024,0) S8US1UDLBYTES",
            "round(sum(S1US5UULBYTES+S1US8UULBYTES)/1024/1024,0) S1US5US8UULBYTES",
            "round(sum(S1US5UULBYTES)/1024/1024,0) S1US5UULBYTES",
            "round(sum(S1US8UULBYTES)/1024/1024,0) S1US8UULBYTES" 
	      ],
          'sql_items_60_CMG' : [
            #"FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')		    BH",
            "round(sum(S5US1UDLBYTES+S8US1UDLBYTES)/1024/1024,0) S5US8US1UDLBYTES",
            "round(sum(S5US1UDLBYTES)/1024/1024,0) S5US1UDLBYTES",
            "round(sum(S8US1UDLBYTES)/1024/1024,0) S8US1UDLBYTES",
            "round(sum(S1US5UULBYTES+S1US8UULBYTES)/1024/1024,0) S1US5US8UULBYTES",
            "round(sum(S1US5UULBYTES)/1024/1024,0) S1US5UULBYTES",
            "round(sum(S1US8UULBYTES)/1024/1024,0) S1US8UULBYTES" 
           ]
        },
        'sql_tables' : [
            'EPCCMG_PS_M10_MDA_RAW cmg',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'cmg.cmg_id=objects.CO_Gid' 
        ]
    },
    'LTE-S1U-THROUGH'     : {
        'func'         : cmg_s1u_throughput,
        'title'        : [
        #                u'设备ID',
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
        #    "CMG_ID",
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
        #    "CMG_ID",
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
                u'SGi Gn 下行字节(GB)',
                u'SGi Gp 下行字节(GB)',
                u'SGi S1u 下行字节(GB)',
                u'SGi S5u 下行字节(GB)',
                u'SGi S8u 下行字节(GB)',
                u'Gn SGi 上行行字节(GB)',
                u'Gp SGi 上行字节(GB)',
                u'S1u SGi 上行字节(GB)',
                u'S5u SGi 上行字节(GB)',
                u'S8u SGi 上行字节(GB)',
                u'SGi 总流量(GB)'
        ],
        'sql_items'      : {
          'sql_items_15_CMG' : [
            "CMG_ID",
            "CO_NAME",
            "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
            "to_char(cmg.PERIOD_START_TIME,'hh24:mi') BH",
            "ROUND(SUM(giGnDlBytes)/1024/1024/1024,2) giGnDlBytes",
            "ROUND(SUM(giGpDlBytes)/1024/1024/1024,0) giGpDlBytes",
            "ROUND(SUM(giS1uDlBytes)/1024/1024/1024,2) giS1uDlBytes",
            "ROUND(SUM(giS5uDlBytes)/1024/1024/1024,2) giS5uDlBytes",
            "ROUND(SUM(giS8uDlBytes)/1024/1024/1024,2) giS8uDlBytes",
            "ROUND(SUM(gnGiUlBytes)/1024/1024/1024,2) gnGiUlBytes",
            "ROUND(SUM(gpGiUlBytes)/1024/1024/1024,2) gpGiUlBytes",
            "ROUND(SUM(s1uGiUlBytes)/1024/1024/1024,2) s1uGiUlBytes",
            "ROUND(SUM(s5uGiUlBytes)/1024/1024/1024,2) s5uGiUlBytes",
            "ROUND(SUM(s8uGiUlBytes)/1024/1024/1024,2) s8uGiUlBytes",
            "ROUND(SUM(giGnDlBytes+giGpDlBytes+giS1uDlBytes+giS5uDlBytes+giS8uDlBytes+gnGiUlBytes+gpGiUlBytes+s1uGiUlBytes+s5uGiUlBytes+s8uGiUlBytes)/1024/1024/1024,2) SGiBytes"
    	  ],
          'sql_items_60_CMG' : [
            "CMG_ID",
            "CO_NAME",
            "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
            "to_char(cmg.PERIOD_START_TIME,'hh24') BH",
            "ROUND(SUM(giGnDlBytes)/1024/1024/1024,2) giGnDlBytes",
            "ROUND(SUM(giGpDlBytes)/1024/1024/1024,2) giGpDlBytes",
            "ROUND(SUM(giS1uDlBytes)/1024/1024/1024,2) giS1uDlBytes",
            "ROUND(SUM(giS5uDlBytes)/1024/1024/1024,2) giS5uDlBytes",
            "ROUND(SUM(giS8uDlBytes)/1024/1024/1024,2) giS8uDlBytes",
            "ROUND(SUM(gnGiUlBytes)/1024/1024/1024,2) gnGiUlBytes",
            "ROUND(SUM(gpGiUlBytes)/1024/1024/1024,2) gpGiUlBytes",
            "ROUND(SUM(s1uGiUlBytes)/1024/1024/1024,2) s1uGiUlBytes",
            "ROUND(SUM(s5uGiUlBytes)/1024/1024/1024,2) s5uGiUlBytes",
            "ROUND(SUM(s8uGiUlBytes)/1024/1024/1024,2) s8uGiUlBytes",
            "ROUND(SUM(giGnDlBytes+giGpDlBytes+giS1uDlBytes+giS5uDlBytes+giS8uDlBytes+gnGiUlBytes+gpGiUlBytes+s1uGiUlBytes+s5uGiUlBytes+s8uGiUlBytes)/1024/1024/1024,2) SGiBytes"
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
    'LTE-SESSION': {
        'func': cmg_session,
        'title': [
            #u'设备ID',
            u'设备名称',
            u'日期',
            u'时间',
            u'Create Session请求数',
            u'Create Session回复成功个数',
            u'Create Session回复失败个数',
            u'Create Session成功率',
            u'Create Bearer请求数',
            u'Create Bearer回复成功个数',
            u'Create Bearer回复失败个数',
            u'Create Bearer成功率',
            u'Delete Session请求数',
            u'Delete Session请求成功个数',
            u'Delete Session请求失败个数',
            u'Delete Session成功率'
        ],
        'sql_items'      : {
          'sql_items_15_CMG' : [
            #"FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi')		    BH",
            "sum(CREATESESSNREQ) CREATESESSNREQ",
            "sum(CREATESESSNRESPSUCCESS) CREATESESSNRESPSUCCESS",
            "sum(CREATESESSNRESPFAIL) CREATESESSNRESPFAIL",
            "round(sum(CREATESESSNRESPSUCCESS)/sum(CREATESESSNREQ), 4)*100 CREATESESSNRESRATE",
            "sum(CREATEBEARERREQ) CREATEBEARERREQ",
            "SUM(CREATEBEARERRESPSUCCESS) CREATEBEARERRESPSUCCESS",
            "SUM(CREATEBEARERRESPFAIL) CREATEBEARERRESPFAIL",
            "round(sum(CREATEBEARERRESPSUCCESS)/sum(CREATEBEARERREQ), 4)*100 CREATEBEARERRESRATE",
            "sum(DELETESESSNREQ) DELETESESSNREQ",
            "sum(DELETESESSNRESPSUCCESS) DELETESESSNRESPSUCCESS",
            "sum(DELETESESSNRESPFAIL) DELETESESSNRESPFAIL",
            "round(sum(DELETESESSNRESPSUCCESS)/sum(DELETESESSNREQ), 4)*100 DELETESESSNRESPRATE"
    	  ],
          'sql_items_60_CMG' : [
            #"FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd')	REPDATE",
            "to_char(PERIOD_START_TIME,'hh24')		    BH",
            "sum(CREATESESSNREQ) CREATESESSNREQ",
            "sum(CREATESESSNRESPSUCCESS) CREATESESSNRESPSUCCESS",
            "sum(CREATESESSNRESPFAIL) CREATESESSNRESPFAIL",
            "round(sum(CREATESESSNRESPSUCCESS)/sum(CREATESESSNREQ), 4)*100 CREATESESSNRESRATE",
            "sum(CREATEBEARERREQ) CREATEBEARERREQ",
            "SUM(CREATEBEARERRESPSUCCESS) CREATEBEARERRESPSUCCESS",
            "SUM(CREATEBEARERRESPFAIL) CREATEBEARERRESPFAIL",
            "round(sum(CREATEBEARERRESPSUCCESS)/sum(CREATEBEARERREQ), 4)*100 CREATEBEARERRESRATE",
            "sum(DELETESESSNREQ) DELETESESSNREQ",
            "sum(DELETESESSNRESPSUCCESS) DELETESESSNRESPSUCCESS",
            "sum(DELETESESSNRESPFAIL) DELETESESSNRESPFAIL",
            "round(sum(DELETESESSNRESPSUCCESS)/sum(DELETESESSNREQ), 4)*100 DELETESESSNRESPRATE"
         ]
        },
        'sql_tables' : [
            'EPCCMG_PS_M40_PORT3_RAW cmg',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'cmg.cmg_id=objects.CO_Gid' 
        ]
    },
    'LTE-IPPOOL'     : {
        'func'         : cmg_ip_pool,
        'title'        : [
                        #u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'IP POOL ID',
                        u'IPv4 Pool占用比例',
                        u'IPv6 Pool占用比例',
        ],
        'sql_items'      : {
          'sql_items_15_CMG' : [
            #"FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
            "to_char(PERIOD_START_TIME,'hh24:mi') BH",
            "PLNAME_ID POOL_ID",
            "avg(IPV4POOLUTILIZATION) IPV4POOLUTILIZATION",
            "avg(IPV6POOLUTILIZATION) IPV6POOLUTILIZATION"
          ],
          'sql_items_60_CMG' : [
            #"FING_ID",
            "CO_NAME",
            "to_char(PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
            "to_char(PERIOD_START_TIME,'hh24') BH",
            "PLNAME_ID POOL_ID",
            "avg(IPV4POOLUTILIZATION) IPV4POOLUTILIZATION",
            "avg(IPV6POOLUTILIZATION) IPV6POOLUTILIZATION"
        ]
        },
        'sql_tables' : [
            'EPCCMG_PS_M81_PLNAME5_RAW cmg',  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'cmg.cmg_id=objects.CO_Gid' 
        ]
    },
    'LTE-DOWNDATA-NOTICE'     : {
        'func'         : cmg_downdata_notice,
        'title'        : [
                        #u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'成功数',
                        u'用户终止',
                        u'寻呼失败',
                        u'用户上下文不存在',
                        u'切换中',
                        u'下行数据通知成功率',
        ],
        'sql_items'      : {
          'sql_items_15_CMG' : [
            #"sgw.FING_ID",
            "objects.CO_NAME",
            "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
            "to_char(cmg.PERIOD_START_TIME,'hh24:mi') BH",
            "SUM(RXREQACCEPTED) RXREQACCEPTED",
            "SUM(TXUNABLEPAGEDUESUSP) TXUNABLEPAGEDUESUSP",
            "sum(RXUNABLETOPAGEUE) RXUNABLETOPAGEUE",
            "sum(RXCONTEXTNOTFOUND) RXCONTEXTNOTFOUND",
            "sum(RXHANDOVERINPROGRESS) RXHANDOVERINPROGRESS",
            "round(decode(((sum(RXREQACCEPTED)+sum(TXUNABLEPAGEDUESUSP)+sum(RXCONTEXTNOTFOUND)+sum(RXHANDOVERINPROGRESS))),0,NULL,((sum(RXREQACCEPTED) / ((sum(RXREQACCEPTED)+sum(TXUNABLEPAGEDUESUSP)+sum(RXCONTEXTNOTFOUND)+sum(RXHANDOVERINPROGRESS)))))),4)*100 RXREQACCEPTED_R"
          ],
          'sql_items_60_CMG' : [
            #"sgw.FING_ID",
            "objects.CO_NAME",
            "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
            "to_char(cmg.PERIOD_START_TIME,'hh24:mi') BH",
            "SUM(RXREQACCEPTED) RXREQACCEPTED",
            "SUM(TXUNABLEPAGEDUESUSP) TXUNABLEPAGEDUESUSP",
            "sum(RXUNABLETOPAGEUE) RXUNABLETOPAGEUE",
            "sum(RXCONTEXTNOTFOUND) RXCONTEXTNOTFOUND",
            "sum(RXHANDOVERINPROGRESS) RXHANDOVERINPROGRESS",
            "round(decode(((sum(RXREQACCEPTED)+sum(TXUNABLEPAGEDUESUSP)+sum(RXCONTEXTNOTFOUND)+sum(RXHANDOVERINPROGRESS))),0,NULL,((sum(RXREQACCEPTED) / ((sum(RXREQACCEPTED)+sum(TXUNABLEPAGEDUESUSP)+sum(RXCONTEXTNOTFOUND)+sum(RXHANDOVERINPROGRESS)))))),4)*100 RXREQACCEPTED_R"
          ]
        },
        'sql_tables' : [
            'EPCCMG_PS_M74_MDA5_RAW cmg',
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'cmg.cmg_id=objects.CO_Gid',
            "cmg.msgtype_id='DownLinkDataAck'"
        ]
    },
    'LTE-MDACPU'     : {
        'func'         : cmg_mdacpu,
        'title'        : [
                        #u'设备ID',
                        u'设备名称',
                        u'日期',
                        u'时间',
                        u'SDF 负荷',
                        u'SDF CPU负荷',
                        u'平均CPU负荷',
                        u'平均内存负荷',
                        u'CPU负荷峰值',
                        u'内存负荷峰值'
        ],
        'sql_items'      : {
          'sql_items_15_CMG' : [
            #"FING_ID",
            "objects.CO_NAME",
            "cmg1.REPDATE",
            "cmg1.BH",
            "round(AVG(SDFSFPUTILIZATION),2) AVG_SDFSFPUTILIZATION",
            "round(AVG(SDFSLCPUTILIZATION),2) AVG_SDF_SDFSLCPUTILIZATION",
            "round(AVG(AVGCPUUTILIZATION),2) AVG_CPU_USAGE",
            "round(AVG(AVGMEMORYUTILIZATION),2) AVG_MEM_USAGE",
            "MAX(MAXCPUUTILIZATION) MAX_CPU_USAGE",
            "MAX(MAXMEMORYUTILIZATION) MAX_MEM_USAGE"
    	  ],
          'sql_items_60_CMG' : [
            #"FING_ID",
            "objects.CO_NAME",
            "cmg1.REPDATE",
            "cmg1.BH",
            "round(AVG(SDFSFPUTILIZATION),2) AVG_SDFSFPUTILIZATION",
            "round(AVG(SDFSLCPUTILIZATION),2) AVG_SDF_SDFSLCPUTILIZATION",
            "round(AVG(AVGCPUUTILIZATION),2) AVG_CPU_USAGE",
            "round(AVG(AVGMEMORYUTILIZATION),2) AVG_MEM_USAGE",
            "MAX(MAXCPUUTILIZATION) MAX_CPU_USAGE",
            "MAX(MAXMEMORYUTILIZATION) MAX_MEM_USAGE"
          ]
        },
        'sql_tables' : [
            {
                'sql_items'      : {
                    'sql_items_15_CMG' : [
                        "cmg_id",
                        "CO_NAME",
                        "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
                        "to_char(cmg.PERIOD_START_TIME,'hh24:mi') BH",
                        "AVG(SDFSFPUTILIZATION) SDFSFPUTILIZATION",
                        "AVG(SDFSLCPUTILIZATION) SDFSLCPUTILIZATION",
                        "AVG(AVGCPUUTILIZATION) AVGCPUUTILIZATION",
                        "AVG(AVGMEMORYUTILIZATION) AVGMEMORYUTILIZATION"
                    ],
                    'sql_items_60_CMG' : [
                        "cmg_id",
                        "CO_NAME",
                        "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
                        "to_char(cmg.PERIOD_START_TIME,'hh24') BH",
                        "AVG(SDFSFPUTILIZATION) SDFSFPUTILIZATION",
                        "AVG(SDFSLCPUTILIZATION) SDFSLCPUTILIZATION",
                        "AVG(AVGCPUUTILIZATION) AVGCPUUTILIZATION",
                        "AVG(AVGMEMORYUTILIZATION) AVGMEMORYUTILIZATION"
                    ]
                },
                'sql_tables': [
                    'epccmg_ps_m2_mda_raw cmg',
                    'UTP_COMMON_OBJECTS objects'  
                ],
                'sql_where' : [ 
                    'cmg.cmg_id=objects.CO_Gid', 
                ],
                'table_name' : "cmg1"
            },
            {
                'sql_items'      : {
                    'sql_items_15_CMG' : [
                        "cmg_id",
                        "CO_NAME",
                        "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd') REPDATE",
                        "to_char(cmg.PERIOD_START_TIME,'hh24:mi') BH",
                        "MAX(MAXCPUUTILIZATION) MAXCPUUTILIZATION",
                        "MAX(MAXMEMORYUTILIZATION) MAXMEMORYUTILIZATION"
                    ],
                    'sql_items_60_CMG' : [
                        "cmg_id",
                        "CO_NAME",
                        "to_char(cmg.PERIOD_START_TIME,'yyyy/mm/dd')        REPDATE",
                        "to_char(cmg.PERIOD_START_TIME,'hh24')               BH",
                        "MAX(MAXCPUUTILIZATION) MAXCPUUTILIZATION",
                        "MAX(MAXMEMORYUTILIZATION) MAXMEMORYUTILIZATION"
                    ]
                },
                'sql_tables': [
                    'EPCCMG_PS_M64_MDA_RAW cmg',
                    'UTP_COMMON_OBJECTS objects'  
                ],
                'sql_where' : [ 
                    'cmg.cmg_id=objects.CO_Gid', 
                ],
                'table_name' : "cmg2"
            },  
            'UTP_COMMON_OBJECTS objects'
        ],     
        'sql_where' : [ 
            'cmg1.cmg_id=objects.CO_Gid',
            'cmg2.cmg_id=objects.CO_Gid',
            'cmg1.cmg_id=cmg2.cmg_id',
            'cmg1.REPDATE=cmg2.REPDATE',
            'cmg1.BH=cmg2.BH' 
        ],
        'sql_group' : [
            "cmg1.REPDATE",
            "cmg1.BH",
            "cmg1.cmg_id",
            "objects.co_name"
        ],
        'sql_order' : [
            "cmg1.REPDATE",
            "cmg1.BH",
            "cmg1.cmg_id",
            "objects.co_name"
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
