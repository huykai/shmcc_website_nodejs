# -*- coding: utf-8 -*-

import sys
import os
import io
import json
import logging
import time
import datetime
import re

import cx_Oracle as oracle
import MySQLdb as mysql
import pyzabbix
import openpyxl
import subprocess

from MME_statis_new import *
from SAEGW_statis_new import *
from RTM_statis_new import *
from CMG_statis_new import *

class PM_Data_Get:

    mmedb = None
    saegwdb = None
    cmgdb = None
    mmedbcursor = None
    saegwcursor = None
    cmgcursor = None
    rtm_statis = None
    
    logging.basicConfig(filename='pm_data_get_logger.log', level=logging.INFO)

    def __init__(self, param, runmode, config):
        self.param = param
        self.runmode = runmode
        self.config = config
        self.initMethod = {
            'sql': self.init_sql,
            'rtm': self.init_rtm,
            'traffica': self.init_traffica
        }
        self.kpi_report_result = {}
        
    def init(self):
        try:
            datasource = self.param['datasource']
            initproc = self.initMethod[datasource]
            if (callable(initproc)):
                initproc()           
            return self.make_return(1, 'PM_Data_Get initialize ok')
        except Exception as e:
            logging.info('PM_Data_Get initialize failed : %s' % e)
            return self.make_return(0, 'PM_Data_Get initialize failed : %s' % e)
    
    def init_sql(self):
        try:
            netype = self.param['netype']
            if (netype == 'mme'):
                self.init_mmedb()
            elif (netype == 'saegw'):
                self.init_saegwdb()
            elif (netype == 'cmg'):
                self.init_cmgdb()
        except Exception as e:
            raise Exception('init_sql error: ' + str(e))

    def init_traffica(self):
        pass

    def init_rtm(self):
        try:
            if self.param['datasource'] == 'rtm':
                (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(self.runmode, "rtmdb")
                self.rtm_statis = RTM_Statis()
                if (self.runmode == 'test'):
                    result = self.rtm_statis.rtm_conn_win(dburl, dbuser, dbpasswd)
                else:
                    result = self.rtm_statis.rtm_conn_linux(dburl, dbuser, dbpasswd)
                if (result['resultcode'] == 0):
                    print('self.rtm_statis init failed ' + result['result'])
                    raise Exception('initiate zabbix failed: %s' % result['result'])
        except Exception as e:
            raise Exception('init_rtm error : %s' % e)
        
    def init_cmgdb(self):
        try:
            # CMGDB
            (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(self.runmode, "cmgdb")
            #print "cmgdb parameter: ", dbuser,dbpasswd,dburl,dburlport,db_dbname
            self.cmgdb = oracle.connect(dbuser, dbpasswd, dburl)
            self.dbcursor=self.cmgdb.cursor()
            if hasattr(self.param, 'netype') and self.param.netype == 'cmg' :
                self.param.isMME = 0
                self.param.isSAEGW = 0
                self.param.isCMG = 1
                self.param.selectcmg = self.param['netelement'] or 'SHSAEGW37BNK'
            self.api_sql_function = cmg_api_sql_function
        except Exception as e:
            raise Exception('init_cmgdb error : %s' % e)
    
    def init_saegwdb(self):
        try:
            # SAEGWDB
            (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(self.runmode, "saegwdb")
            #print "saegwdb parameter: ", dbuser,dbpasswd,dburl,dburlport,db_dbname
            self.saegwdb = oracle.connect(dbuser, dbpasswd, dburl)
            self.dbcursor=self.saegwdb.cursor()
            if hasattr(self.param, 'netype') and self.param.netype == 'saegw' :
                self.param.isMME = 0
                self.param.isSAEGW = 1
                self.param.isCMG = 0
                self.param.selectsaegwggsn = self.param['netelement'] or 'SHSAEGW03BNK'
            self.api_sql_function = saegw_api_sql_function
        except Exception as e:
            raise Exception('init_saegwdb error : %s' % e)

    def init_mmedb(self):
        try:
            # MMEDB
            (dbuser,dbpasswd,dburl,dburlport,db_dbname) = getdbconfig(self.runmode, "mmedb")
            #print("mmedb parameter: ",dbuser,dbpasswd,dburl,dburlport,db_dbname)
            self.mmedb = oracle.connect(dbuser, dbpasswd, dburl)
            self.dbcursor=self.mmedb.cursor()
            if hasattr(self.param, 'netype') and self.param.netype == 'mme':
                self.param.isMME = 1
                self.param.isSAEGW = 0
                self.param.isCMG = 0
                self.param.selectmmesgsn = self.param['netelement'] or 'SHMME03BNK'
            self.api_sql_function = mme_api_sql_function
        except Exception as e:
            raise Exception('init_mmedb error : %s' % e)

    def getData(self):
        logging.info('getData...')
        datasource = self.param['datasource']
        if (datasource == "sql"):
            datainfo = self.getsqlinfo()
            logging.info('sql datainfo: %s' % datainfo)
            return self.make_return(1, str(datainfo))
        elif (datasource == 'rtm'):
            datainfo = self.getRTMKPI()
            logging.info('rtm datainfo: %s' % datainfo)
            return self.make_return(1, str(datainfo))
        elif (datasource == 'traffica'):
            datainfo = self.getTrafficaData()
            logging.info('traffica datainfo: %s' % datainfo)
            return self.make_return(1, str(datainfo))
        else:
            return self.make_return(0, 'datasource %s not support' % self.param['datasource'])

    def getsqlinfo(self):
        try:
            sqlfunc = self.param['sql_function']
            #print('getsqlinfo : ', sqlfunc)
            kpi_function = self.api_sql_function[sqlfunc]['func']
            #print('getsqlinfo : ', kpi_function)
            
            title,row=kpi_function(sqlfunc, self.dbcursor, self.param)
            #print 'kpi_function param: ', self.param
            if title[0]!='error' and len(row)>0:
                #print('getsqlinfo ' + sqlfunc + ' ' + str(row[0]))
                self.kpi_report_result = row
                return self.make_return(1, self.kpi_report_result)
            else:
                logging.error("getsqlinfo %s with Error : %s" % (sqlfunc, title[1]))
                return self.make_return(0, "getsqlinfo %s with Error : %s" % (sqlfunc, title[1]))
        except Exception, e:
            logging.error('Exception : ' + str(e))
            return self.make_return(0, "getsqlinfo Exception: %s" % str(e))

    
    def getRTMKPI(self):
        hostname = self.param['host']
        itemname = self.param['itemname']
        valueindex = self.param['valueindex']
        
        resultvalues = self.rtm_statis.rtm_get_value(hostname, itemname, self.param.startdatetime, self.param.stopdatetime)
        print('rtm resultvalues: ' , str(resultvalues))
        result = ''
        if (resultvalues['resultcode'] == 1 ):
            if (valueindex == 'min'):
                result += str(round(float(resultvalues['result'][0]['value_min']),2))
            if (valueindex == 'avg'):
                result += str(round(float(resultvalues['result'][0]['value_avg']),2))
            else:
                result += str(round(float(resultvalues['result'][0]['value_max']),2))
        else:
            result += ' '
        return result

    def getTrafficaData(self):
        try:
            trafficaQueryParam = {
                "QUERYTYPE":"QuerySummary",
                "IMSI":"",
                "MSISDN":"",
                "LTECAUSEPROC":"0x1",
                "GSMCAUSEPROC":"0x0",
                "MMELIST":"SHMME03BNK,SHMME04BNK",
                "NETTYPE":"MME_TRAFFICA",
                "MME_TRAFFICA":"REPORT_TIME,IMSI,ATTACH_TIME,TAI_TAC,GLOBAL_ENODEB_ID,CPPU_LOGICAL_ADDRESS,MMDU_LOGICAL_ADDRESS,IPDU_LOGICAL_ADDRESS,CAUSE_PROC,INTERNAL_CAUSE,S1AP_CAUSE,S11_CAUSE_CODE,SGW_CONTROL_PLANE_TEID_IP_ADDRESS,MSISDN,IMEI_IMEISV,EMM_CAUSE,ESM_CAUSE,APN",
                "SGSN_TRAFFICA":"REPORT_TIME,IMSI,APN,GGSN_ADDRESS,CGI_LAC,CGI_RAC,CAUSE_PROC,CAUSE_INI,CAUSE_FAMILY,CAUSE_CAUSE,CAUSE_INT_CAUSE,PAPU_ID,MSISDN_NUMBERS,RA_ACCESS_TYPE,RNC_ID",
                "STARTDATE":"2018-11-22",
                "STARTTIME":"12:00:34",
                "STOPDATE":"2018-11-22",
                "STOPTIME":"13:00:43"
            }
            if (hasattr(self.param, 'trafficaQueryParam')):
                configs = self.param['trafficaQueryParam']
                #print configs
                for key, item in configs.items():
                    #print key," : ",item
                    trafficaQueryParam[key] = item
            trafficaQueryParam['STARTDATE'] = self.param['trafficastartdate']
            trafficaQueryParam['STOPDATE'] = self.param['trafficastopdate']
            trafficaQueryParam['STARTTIME'] = self.param['trafficastarttime']
            trafficaQueryParam['STOPTIME'] = self.param['trafficastoptime']
            
            p = subprocess.Popen(["java","-jar",
                "e:\\eclipse_projects\\eclipse_projects\\TrafficaDBAPI\\target\\TrafficaDBAPI-0.0.1-SNAPSHOT-jar-with-dependencies.jar",
                "test",
                json.dumps(trafficaQueryParam)],
            shell=True,
            stdout=subprocess.PIPE)
            output, errors = p.communicate()
            print('subprocess command: ', ["java","-jar",
                "e:\\eclipse_projects\\eclipse_projects\\TrafficaDBAPI\\target\\TrafficaDBAPI-0.0.1-SNAPSHOT-jar-with-dependencies.jar",
                json.dumps(trafficaQueryParam)])
            print('subprocess stdout: ', output)
            print('subprocess error: ', errors)

            outputdata = json.loads(output)
            if (outputdata.has_key('MME_TRAFFICA')):
                mme_traffica_file = open(__dirname + '/../' + outputdata['MME_TRAFFICA'], 'r')
                print json.load(mme_traffica_file)
            if (outputdata.has_key('SGSN_TRAFFICA')):
                sgsn_traffica_file = open(__dirname + '/../' + outputdata['SGSN_TRAFFICA'], 'r')
                print json.load(sgsn_traffica_file)
        except Exception as e:
            print('getTrafficaData catch Exception: ', str(e))
        

    def make_return(self, resultcode, result):
        return {'resultcode': resultcode, 'resultdetail': result}
  
    def closeAll(self):
        if (self.mmedb != None):
            self.mmedb.close
        if (self.saegwdb != None):
            self.saegwdb.close
        if (self.cmgdb != None):
            self.cmgdb.close

def getforminfo(params, formparams):
    # Get data from formparams
    configs = json.loads(formparams)
    logging.info("formparams : " + formparams)
    #print configs
    for key, item in configs.items():
        #print key," : ",item
        params.__dict__[key] = item
    if (not configs.has_key('selectperiod')):
        params.selectperiod = '60'
    if (params.selectperiodtype == None):
        params.selectperiodtype = 'continue'
    
    
def paramsdate_fix(param):
    pass
    
        
if __name__ == '__main__':

    logging.info('PM_Data_GET time : ' + time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time())))
    promptparams = None
    runmode = 'test'
    if ( len(sys.argv) ) > 2 :
        runmode = sys.argv[1]
        promptparams = sys.argv[2]
        queryconfig = sys.argv[3] or {}
        logging.info("\t Run Mode : " + runmode) 
        logging.info("\t Params : " + promptparams) 
        logging.info("\t QueryConfig : " + queryconfig) 
        
    param = PmSqlParam()
    print 'new param %s' % param
    if (not param == None):
        try:
            getforminfo(param, promptparams)
            getforminfo(param, queryconfig)
            logging.info('\tparams info : ' + prn_obj(param))
        except Exception as e:
            logging.error('error in param get: %s' % e )
    else:
        logging.info('form params is None.')
    
    # we need there parameter
    # datasource(sql, rtm, traffica)
    # netype(mme or saegw), netelement(SHMME03BNK), 
    # time(20180630130351) %Y%m%d%H%M%S
    # duration(3600)s
    if not hasattr(param, 'time') or param['time'] == None:
        param['time'] = time.strftime('%Y%m%d%H%M%S')
    if not hasattr(param, 'duration') or param['duration'] == None:
        param['duration'] = 3600
    currtime = datetime.datetime.strptime(param['time'], "%Y%m%d%H%M%S")
    pretime = currtime + datetime.timedelta(seconds=int(param['duration']))
    
    param.startdate = pretime.strftime("%Y/%m/%d")
    param.stopdate = currtime.strftime("%Y/%m/%d")
    param.starttime = pretime.strftime("%H:%M")
    param.stoptime = currtime.strftime("%H:%M")
    
    param.trafficastartdate = pretime.strftime("%Y-%m-%d")
    param.trafficastopdate = currtime.strftime("%Y-%m-%d")
    param.trafficastarttime = pretime.strftime("%H:%M:%S")
    param.trafficastoptime = currtime.strftime("%H:%M:%S")

    param['startdatetime'] = int(time.mktime(pretime.timetuple()))
    param['stopdatetime'] = int(time.mktime(currtime.timetuple()))
    param.maketime = time.strftime("%Y-%m-%d %H:%M:%S")
    paramsdate_fix(param)
    logging.info('param: \n%s' % param)

    print promptparams
    print param
    pm_data_get = PM_Data_Get(param, runmode, queryconfig)

    init_result = pm_data_get.init()
    print('init_result: ' + json.dumps(init_result))
    data_result = init_result
    if init_result['resultcode'] == 0:
        logging.info('PM_Data_Get initialize failed : %s' % init_result['resultdetail'])
        #sys.exit(1)
    else:
        data_result = pm_data_get.getData()
        if data_result['resultcode'] == 0:
            logging.info('PM_Data_Get GetData failed : %s' % data_result['resultdetail'])
            #sys.exit(1)
    
    pm_data_get.closeAll()
    
    #print(json.dumps(fill_result['result']))
    print(json.dumps(data_result['resultdetail']))

# test script
# python scripts\PM_data_get.py test "{\"datasource\":\"sql\",\"time\":\"201811201000\",\"duration\" :\"-3600\",\"netype\":\"mme\",\"netelement\":\"SHMME03BNK,SHMME04BNK\",\"sql_function\":\"LTE-AUTH\"}" "{}"
# python scripts\PM_data_get.py test "{\"datasource\":\"sql\",\"time\":\"201811201000\",\"duration\" :\"-3600\",\"netype\":\"saegw\",\"netelement\":\"SHSAEGW03BNK,SHSAEGW04BNK\",\"sql_function\":\"LTE-GTPU-THROUGH\"}" "{}"
# python scripts\PM_data_get.py test "{\"datasource\":\"rtm\",\"time\":\"20181120101010\",\"duration \":\"-3600\",\"host\":\"SHMME04BNK\",\"itemname\":\"extMME_Memory_Total_MMDU8\",\"valueindex\":\"max\"}" "{}" 
# traffica 
# test 
"""
java.exe -jar e:\eclipse_projects\eclipse_projects\TrafficaDBAPI\target\TrafficaDBAPI-0.0.1-SNAPSH OT-jar-with-dependencies.jar test  {\"QUERYTYPE\":\"QuerySummary\",\"IMSI\":\"\",\"MSISDN\":\"\",\"LTECAUSEPROC\":\"0x1\",\"GSMCAUSEPROC\":\"0x0\",\"MMELIST\":\"SHMME03BNK,SHMME04BNK\",\"NETTYPE\":\"MME_TRAFFICA\",\"MME_TRAFFICA\":\"REPORT_TIME,IMSI,ATTACH_TIME,TAI_TAC,GLOBAL_ENODEB_ID,CPPU_LOGICAL_ADDRESS,MMDU_LOGICAL_ADDRESS,IPDU_LOGICAL_ADDRESS,CAUSE_PROC,INTERNAL_CAUSE,S1AP_CAUSE,S11_CAUSE_CODE,SGW_CONTROL_PLANE_TEID_IP_ADDRESS,MSISDN,IMEI_IMEISV,EMM_CAUSE,ESM_CAUSE,APN\",\"SGSN_TRAFFICA\":\"REPORT_TIME,IMSI,APN,GGSN_ADDRESS,CGI_LAC,CGI_RAC,CAUSE_PROC,CAUSE_INI,CAUSE_FAMILY,CAUSE_CAUSE,CAUSE_INT_CAUSE,PAPU_ID,MSISDN_NUMBERS,RA_ACCESS_TYPE,RNC_ID\",\"STARTDATE\":\"2018-11-22\",\"STARTTIME\":\"12:00:34\",\"STOPDATE\":\"2018-11-22\",\"STOPTIME\":\"13:00:43\"}
"""
"""
{
    "QUERYTYPE": "QueryDetail",
    "IMSI":"",
    "MSISDN":"",
    "LTECAUSEPROC":"0x1,0x2",
    "GSMCAUSEPROC":"0x0",
    "MMELIST":"SHMME10BNK",
    "NETTYPE":"MME_TRAFFICA,SGSN_TRAFFICA",
    "MME_TRAFFICA":"REPORT_TIME,IMSI,ATTACH_TIME,TAI_TAC,GLOBAL_ENODEB_ID,CPPU_LOGICAL_ADDRESS,MMDU_LOGICAL_ADDRESS,IPDU_LOGICAL_ADDRESS,MME_S1AP_ID,ENODEB_S1AP_ID,CAUSE_PROC,INTERNAL_CAUSE,S1AP_CAUSE,S11_CAUSE_CODE,SGW_CONTROL_PLANE_TEID_IP_ADDRESS,CHARGING_CHARACTERISTICS,MSISDN,IMEI_IMEISV,LAST_VISITED_TAI_TAC,ECGI,EMM_CAUSE,ECM_IN_STATE,ECM_OUT_STATE,EMM_IN_STATE,EMM_OUT_STATE,INTEGRITY_PROTECTION_ALG,CONFIDENTIALITY_PROTECTION_ALG,ESM_CAUSE,BEARER_CREATION_TIME,APN,SGW_USER_PLANE_TEID_IP_ADDRESS,PDN_GATEWAY_CONTROL_PLANE_TEID_IP_ADDRESS,PDN_GATEWAY_USER_PLANE_TEID_IP_ADDRESS,ENODEB_USER_PLANE_TEID_IP_ADDRESS",
    "SGSN_TRAFFICA":"REPORT_TIME,IMSI,APN,GGSN_ADDRESS,CGI_LAC,CGI_RAC,CGI_CI,CAUSE_PROC,CAUSE_INI,CAUSE_FAMILY,CAUSE_CAUSE,CAUSE_INT_CAUSE,PAPU_ID,MSISDN_NUMBERS,PS_EXTERNAL_CAUSE,CS_EXTERNAL_CAUSE,EXT_DATA_AMOUNT_UP,EXT_DATA_AMOUNT_DOWN,PDP_CONTEXT_TYPE,CHARGING_INDEX,RA_ACCESS_TYPE,RNC_ID,SAI_LAC,SAI_SAC,MS_PDP_ADDRESS,OLD_SAI_LAC,OLD_SAI_SAC,OLD_CGI_LAC,OLD_CGI_RAC,OLD_CGI_CI,EVENT_START_TIME,EVENT_STOP_TIME,OLD_RNC_ID",
    "STARTDATE":"2017-11-9",
    "STARTTIME":"01:00:00",
    "STOPDATE":"2017-11-9",
    "STOPTIME":"01:00:02"
}
"""
"""
java.exe -jar e:\\eclipse_projects\\eclipse_projects\\TrafficaDBAPI\\target\\TrafficaDBAPI-0.0.1-SNAPSHOT-jar-with-dependencies.jar test 
{
    "QUERYTYPE":"QuerySummary",
    "IMSI":"",
    "MSISDN":"",
    "LTECAUSEPROC":"0x1",
    "GSMCAUSEPROC":"0x0",
    "MMELIST":"SHMME03BNK,SHMME04BNK",
    "NETTYPE":"MME_TRAFFICA",
    "MME_TRAFFICA":"REPORT_TIME,IMSI,ATTACH_TIME,TAI_TAC,GLOBAL_ENODEB_ID,CPPU_LOGICAL_ADDRESS,MMDU_LOGICAL_ADDRESS,IPDU_LOGICAL_ADDRESS,CAUSE_PROC,INTERNAL_CAUSE,S1AP_CAUSE,S11_CAUSE_CODE,SGW_CONTROL_PLANE_TEID_IP_ADDRESS,MSISDN,IMEI_IMEISV,EMM_CAUSE,ESM_CAUSE,APN",
    "SGSN_TRAFFICA":"REPORT_TIME,IMSI,APN,GGSN_ADDRESS,CGI_LAC,CGI_RAC,CAUSE_PROC,CAUSE_INI,CAUSE_FAMILY,CAUSE_CAUSE,CAUSE_INT_CAUSE,PAPU_ID,MSISDN_NUMBERS,RA_ACCESS_TYPE,RNC_ID",
    "STARTDATE":"2018-11-22",
    "STARTTIME":"12:00:34",
    "STOPDATE":"2018-11-22",
    "STOPTIME":"13:00:43"
}
"""