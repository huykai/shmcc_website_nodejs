# -*- coding: utf-8 -*-

import sys
import time
import cgi
import MySQLdb as mysql

import os
import json
import logging


logging.basicConfig(filename='pm_rtm_logger.log', level=logging.INFO)

reload(sys)
sys.setdefaultencoding("utf-8")

from GetConfig import *
from RTM_statis_new import *

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

if __name__ == '__main__':

    logging.info('query time : ' + time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time())))

    formparams = None  
    if ( len(sys.argv) ) > 1 :
        logging.info("\t run mode : " + str(sys.argv[1]))
        logging.info("\t params : " + str(sys.argv[2])) 
        runmode = sys.argv[1]
        formparams = sys.argv[2]
       
    param = PmSqlParam()

    if (not formparams is None):
        try:
            getforminfo(param, formparams)
            logging.info('\tparams info : ' + prn_obj(param))
        except Exception, e:
            logging.error('error in param get.' + e.message )
    else:
        logging.info('form params is None.')
    
    #paramsdate_fix()

    # connect to rtm api 
    (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(runmode, "rtmdb")
    
    print('dbuser: ', dbuser)
    print('dbpasswd: ', dbpasswd)
    print('dburl: ', dburl)
    try:
        zapi_result = rtm_conn(url=dburl, user=dbuser, password=dbpasswd)
        if (zapi_result['resultcode'] == 0):
            print('zabbix api init failed')
            sys.exit(1)
        zapi = zapi_result['result']
        print('zapi: ', zapi)
        startdatetime = param.startdate + '_' + param.starttime
        stopdatetime = param.stopdate + '_' + param.stoptime
        startdate = datetime.datetime.strptime(startdatetime, '%Y/%m/%d_%H')
        stopdate = datetime.datetime.strptime(stopdatetime, '%Y/%m/%d_%H')
        starttime = int(time.mktime(startdate.timetuple()))
        stoptime = int(time.mktime(stopdate.timetuple()))
        print('startdatetime: %s' % startdatetime)
        print('stopdatetime: %s' % stopdatetime)
        print('startdate: %s' % startdate)
        print('stopdate: %s' % stopdate)
        print('starttime: %s' % starttime)
        print('stoptime: %s' % stoptime)

        if (param.isMME):
            result = rtm_get_value(zapi, param.selectmmesgsn, param.kpilist, starttime, stoptime)
        else:
            result = rtm_get_value(zapi, param.selectsaegwggsn, param.kpilist, starttime, stoptime)
        
        print(result)
        
    except Exception as e:
        logging.error("Error %s" % e)
        sys.exit(1)
    
# python scripts\PM_statictics_RTM.py test {\"selectmmesgsn\":[\"SHMME03BNK\",\"SHMME04BNK\"],\"kpilist\":[\"calEPS_DEF_BEARER_ACT_VOLTE_SUCC_Rate\",\"calEPS_DEF_BEARER_ACT_SUCC_Rate\"],\"startdate\":\"2018/08/01\",\"starttime\":\"10\",\"stopdate\":\"2018/08/01\",\"stoptime\":\"11\"}