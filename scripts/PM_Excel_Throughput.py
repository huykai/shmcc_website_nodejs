# -*- coding: utf-8 -*-

import sys
import os
import io
import json
import logging
import time
import datetime
import re

from GetConfig import *
from PM_excelfill import PM_ExcelFill

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
    if (configs.has_key('selectmmesgsn')):
        params.selectmmesgsn = configs['selectmmesgsn']
    else:
        params.selectmmesgsn = ''
    if (configs.has_key('selectsaegwggsn')):
        params.selectsaegwggsn = configs['selectsaegwggsn']
    else:
        params.selectsaegwggsn = ''
    if (configs.has_key('selectrtm')):
        params['selectrtm'] = configs['selectrtm']
    else:
        params['selectrtm'] = true
    
    
def paramsdate_fix(param):
    # adjust per environment in test or prod
    timeArray = time.localtime(float(param['stopdatetime']))
    stopdate = time.strftime('%Y/%m/%d', timeArray)
    curtime = time.strftime('%H', timeArray)
    curtime = curtime + ":00"
    
    timeArray = time.localtime(float(param['startdatetime']))
    startdate = time.strftime('%Y/%m/%d',timeArray)
    pretime = time.strftime('%H', timeArray)
    pretime = pretime + ":00"
    
    param.starttime=pretime
    param.stoptime=curtime
    param.startdate=startdate
    param.stopdate=stopdate
        
if __name__ == '__main__':

    logging.info('query time : ' + time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time())))
    
    formparams = None
    runmode = 'test'
    if ( len(sys.argv) ) > 2 :
        logging.info("\t run mode : " + str(sys.argv[1]))
        logging.info("\t excel config : " + str(sys.argv[2]))
        if (len(sys.argv) > 3):
            logging.info("\t params : " + str(sys.argv[3])) 
            formparams = sys.argv[3]
        runmode = sys.argv[1]
        excelconfig = sys.argv[2]
        
        print("\t run mode : " + runmode) 
        print("\t excel config : " + excelconfig) 
        print("\t formparams : " , formparams) 
    else:
        print('Process should provide three argument at least, mode(test/rtm) configfilename')    
        sys.exit(1)
    
    param = PmSqlParam()

    if (not formparams == None):
        try:
            getforminfo(param, formparams)
            logging.info('\tparams info : ' + prn_obj(param))
            print('\tparams info : ' + prn_obj(param))
        except Exception as e:
            logging.error('error in param get: %s' % e )
    else:
        logging.info('form params is None.')
    
    # for excel , we need input hour 
    #currtime = datetime.datetime.strptime(param.time, "%Y-%m-%dT%H:%M:%S.%fZ")
    if not hasattr(param, 'time') or param['time'] == None:
        param['time'] = time.time()
    else:
        timestr = param['time']
        inputdatetime = datetime.datetime.strptime(timestr, '%Y/%m/%d-%H:%M:%S')
        param['time'] = time.mktime(inputdatetime.timetuple())

    timeArray = time.localtime(float(param.time))
    param_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    currtime = datetime.datetime.strptime(param_time, "%Y-%m-%d %H:%M:%S")
    currtime = datetime.datetime(currtime.year, currtime.month, currtime.day, currtime.hour, 0)
    #currtime = currtime + datetime.timedelta（hours=-1)
    pretime = currtime + datetime.timedelta(hours=-1)

    
    param['startdatetime'] = time.mktime(pretime.timetuple())
    param['stopdatetime'] = time.mktime(currtime.timetuple())

    paramsdate_fix(param)

    param['extraparams']['year'] = currtime.strftime('%Y')
    param['extraparams']['month'] = currtime.strftime('%m')
    param['extraparams']['day'] = currtime.strftime('%d')
    param['extraparams']['hour'] = currtime.strftime('%H')
    
    param['selectrtm'] = 'true'
    
    if param['selectsaegwggsn'] == '':
        param['selectsaegwggsn'] == 'SHSAEGW03BNK'

    print('param: \n%s' % param)

    result = {
        'resultcode': '0',
        'resultdetail': ''
    }

    filepath = os.path.split(os.path.realpath(__file__))[0]
    print('main filepath: ', filepath)
    pm_excelfill = PM_ExcelFill(param, runmode, excelconfig)

    init_result = pm_excelfill.init()
    if init_result['resultcode'] == 0:
        print('PM_ExcelFill initialize failed : %s', init_result['result'])
        sys.exit(1)
    
    fill_result = pm_excelfill.excel_fill()
    if fill_result['resultcode'] == 0:
        print('PM_ExcelFill fill failed : %s', fill_result['result'])
        sys.exit(1)
    
    pm_excelfill.closeAll()
    print(json.dumps(fill_result['result']))

# run script
# python scripts\PM_Excel_Throughput.py test Throughput_Excel.json {\"selectsaegwggsn\":\ "SHSAEGW03BNK\",\"selectrtm\":\"true\",\"time\":\"2018/08/08-19:00:00\"}

	
	
