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

from MME_statis_new import *
from SAEGW_statis_new import *
from RTM_statis_new import *

class PM_ExcelFill:

    mmedb = None
    saegwdb = None
    mmedbcursor = None
    saegwcursor = None
    ExcelConfigFileName = None
    Excel_Config = None
    Excel_Result = {}
    SaveFileName = ''
    rtm_statis = None
    workbook = None

    logging.basicConfig(filename='pm_excel_logger.log', level=logging.INFO)

    def __init__(self, param, runmode, excelconfig):
        self.param = param
        self.runmode = runmode
        self.filepath = os.path.split(os.path.realpath(__file__))[0]
        logging.info('filepath: ' + __file__ + self.filepath)
        if (self.runmode == 'test'):
            self.ExcelConfigFileName = self.filepath + '/config/' + excelconfig
        else:
            self.ExcelConfigFileName = self.filepath + '/config/' + runmode + '/' + excelconfig
        logging.info('Excel_Config_filename : ' + self.ExcelConfigFileName)
        logging.info('Excel Config File: ' + self.ExcelConfigFileName)

    def init(self):
        try:
            with open(self.ExcelConfigFileName, 'r') as load_f:
                self.Excel_Config = json.load(load_f)
            self.SaveFileName = self.Excel_Config['EXCEL_FILENAME']
            
            # MMEDB
            (dbuser,dbpasswd,dburl,dburlport,db_dbname) = getdbconfig(self.runmode, "mmedb")
            self.mmedb = oracle.connect(dbuser, dbpasswd, dburl)
            self.mmedbcursor=self.mmedb.cursor()
            # SAEGWDB
            (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(self.runmode, "saegwdb")
            self.saegwdb = oracle.connect(dbuser, dbpasswd, dburl)
            self.saegwdbcursor=self.saegwdb.cursor()

            if hasattr(self.param, 'netype') and self.param.netype == 'mme':
                self.SaveFileName += ('_' + self.param['ne'] or 'SHMME03BNK')
                self.param.isMME = 1
                self.param.isSAEGW = 0
                self.param.selectmmesgsn = self.param['ne'] or 'SHMME03BNK'
                
            if hasattr(self.param, 'netype') and self.param.netype == 'saegw' :
                self.SaveFileName += ('_' + self.param['ne'] or "SHSAEGW03BNK")
                self.param.isMME = 0
                self.param.isSAEGW = 1
                self.param.selectsaegwggsn = self.param['ne'] or 'SHSAEGW03BNK'
                
            if hasattr(self.param, 'selectrtm') and self.param.selectrtm:
                (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(self.runmode, "rtmdb")
                self.rtm_statis = RTM_Statis()
                if (self.runmode == 'test'):
                    result = self.rtm_statis.rtm_conn_win(dburl, dbuser, dbpasswd)
                else:
                    result = self.rtm_statis.rtm_conn_linux(dburl, dbuser, dbpasswd)
                if (result['resultcode'] == 0):
                    logging.info('self.rtm_statis init failed ' + result['result'])
                    raise Exception('initiate zabbix failed: %s' % result['result'])
            
            logging.info('Excel_Config json parse finished')
            logging.info('Excel_Config EXCEL MODEL NAME: ' + self.Excel_Config['EXCEL_MODEL'])
            logging.info('Excel_Config EXCEL_FILENAME : ' + self.SaveFileName)
            self.workbook = openpyxl.load_workbook(self.Excel_Config['EXCEL_MODEL'])
            logging.info('openpyxl load workbook finished')
            return self.make_return(1, 'init ok')
        except Exception as e:
            logging.info('PM_ExcelFill initialize failed : %s' % e)
            return self.make_return(0, 'PM_ExcelFill initialize failed : %s' % e)

    def make_return(self, resultcode, result):
        return {'resultcode': resultcode, 'resultdetail': result}

    def namewithparam(self, name):
        logging.info('namewithparam origin name: ' + name)
        nameparams = re.findall('\$\{[\w\d]+\}', name)
        if (len(nameparams) > 0):
            for nameparam in nameparams:
                nameparamitem = re.search('([\w\d]+)', nameparam).group()
                nameparamstr = ''
                if (hasattr(self.param, nameparamitem)):
                    nameparamstr = self.param[nameparamitem]
                elif (nameparamitem in self.param['extraparams'].keys()):
                    nameparamstr = self.param['extraparams'][nameparamitem]
                name = name.replace(nameparam, nameparamstr)
        logging.info('namewithparam after name: ' + name)
        return name

    def excel_fill(self):
        try:        
            for sheet in self.Excel_Config['SHEETS']:
                if sheet.has_key('runCondition'):
                    logging.info(sheet['runCondition'] + ' : ' + str(self.param[sheet['runCondition']]))
                    logging.info('param has attr: ' + sheet['runCondition'] + ' ' + str(hasattr(self.param, sheet['runCondition'])) + ' ' + str(self.param[sheet['runCondition']]))
                    if hasattr(self.param, sheet['runCondition']) and not(self.param[sheet['runCondition']] == 1):
                        continue
                oldsheetname = sheet.has_key('SHEETNAME') and sheet['SHEETNAME']
                sheetname = oldsheetname
                if (sheet.has_key('SHEET_ORIGIN_NAME')):
                    logging.info('excel_fill sheet begin: ' + sheet['SHEET_ORIGIN_NAME'])
                    oldsheetname = sheet['SHEET_ORIGIN_NAME']
                if (sheet.has_key('SHEET_AFTER_NAME')):
                    logging.info('excel_fill sheet after: ' + sheet['SHEET_AFTER_NAME'])
                    sheetname = sheet['SHEET_AFTER_NAME']
                sheetname = self.namewithparam(sheetname)
                logging.info('sheetname after param modify is: ' + sheetname)
                ws = self.workbook[oldsheetname]
                ws.title = sheetname
                self.saveExcelSheet(ws, sheet)
                logging.info('excel_fill sheet over: ' + sheetname) 
            if (self.runmode == 'test'):
                site_config_filename = self.filepath + '/config/api_options.json'
            else:
                site_config_filename = self.filepath + '/config/' + self.runmode + '/api_options.json' 
            logging.info('site_config_filename  : ' + site_config_filename)
            site_config = json.load(open(site_config_filename, 'r'))
            
            #nowtime = datetime.datetime.now() 
            #self.SaveFileName = self.SaveFileName + '_' + nowtime.strftime("%Y%m%d") + nowtime.strftime("%H%M%S") + '.xlsx'
            self.SaveFileName = self.SaveFileName + '_' + self.maketime
            realfilename = site_config['download_dir'] + self.SaveFileName 
            self.workbook.save(realfilename)
            return self.make_return(1, self.Excel_Config['EXCEL_DOWNLOAD_URL'] + self.SaveFileName)
        except Exception as e:
            logging.error("Error PM_Excelfill: %s" % e)
            return self.make_return(0, "Error PM_Excelfill: %s" % e)
        
    def closeAll(self):
        if (self.mmedb != None):
            self.mmedb.close
        if (self.saegwdb != None):
            self.saegwdb.close

    def prn_obj(self, obj):
        return '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])


    def avg_cacul(self, algo, rows, algoindex):
        sum = 0
        for row in rows:
            sum += float(row[int(algoindex)-1])
        if(len(rows)>0):
            return str(sum/len(rows))
        return 0

    def max_cacul(self, algo, rows, algoindex):
        max = 0
        for row in rows:
            if(float(row[int(algoindex)-1]) > max):
                max = float(row[int(algoindex)-1])
        return str(max)

    def min_cacul(self, algo, rows, algoindex):
        min = 0
        for row in rows:
            if(float(row[int(algoindex)-1]) < min):
                min = float(row[int(algoindex)-1])
        return str(min)

    def sum_cacul(self, algo, rows, algoindex):
        sum = 0
        for row in rows:
            sum += float(row[int(algoindex)-1])
        return str(sum)


    def algo_cacul(self, algo, rows, algoindex):
        ret = '0'
        if (algo == 'avg'):
            ret = self.avg_cacul(algo, rows, algoindex)
        elif (algo == 'max'):
            ret = self.max_cacul(alog, rows, algoindex)
        elif (algo == 'min'):
            ret = self.min_cacul(alog, rows, algoindex)
        elif (algo == 'sum'):
            ret = self.sum_cacul(alog, rows, algoindex)
        
        return ret

    def caculate(self, rows, sqlextrastruct):
        tmprow = []
        if (sqlextrastruct.has_key('valuefilter')):
            itemindex = sqlextrastruct['valuefilter']['filter_index']
            filter = sqlextrastruct['valuefilter']['filter_regex']
            for row in rows:
                #print('caculate filter row: ', str(row))
                if(re.match(filter, row[int(itemindex)-1])):
                    tmprow.append(row)
        else:
            tmprow = rows
        #print('caculate after filter: %d' % len(tmprow))
        if (sqlextrastruct.has_key('valuealgo')):
            algoindex = sqlextrastruct['valuealgo']['algo_index']
            algo = sqlextrastruct['valuealgo']['algo']
            ret = self.algo_cacul(algo, tmprow, algoindex)
            #print('caculate after algo: ' + str(ret))
            return ret
        else:
            return ''

    def getsqlinfo(self, dbcursor, valuestruct, api_sql_function, kpi_report_result):
        try:
            sqlfunc = valuestruct['sql_function']
            #print('getsqlinfo : ', sqlfunc)
            sqlitemindex = valuestruct['sql_selectitem_index']
            #print('getsqlinfo : ', sqlitemindex)
            kpi_function = api_sql_function[sqlfunc]['func']
            #print('getsqlinfo : ', kpi_function)
            if (kpi_report_result.has_key(sqlfunc)):
                if (valuestruct.has_key("sql_extra")):
                    #print('getsqlinfo valuestruct has key sql_extra')
                    return self.caculate(kpi_report_result[sqlfunc], valuestruct["sql_extra"])
                else:    
                    return kpi_report_result[sqlfunc][0][int(sqlitemindex) - 1]
            else:
                title,row=kpi_function(sqlfunc, dbcursor, self.param)
                if title[0]!='error' and len(row)>0:
                    #print('getsqlinfo ' + sqlfunc + ' ' + str(row[0]))
                    kpi_report_result[sqlfunc] = row
                    #print('getsqlinfo valuestruct has key sql_extra ? ', valuestruct.has_key("sql_extra"))
                    if (valuestruct.has_key("sql_extra")):
                        #print('getsqlinfo valuestruct has key sql_extra')
                        return self.caculate(row, valuestruct["sql_extra"])
                    
                    return str(row[0][int(sqlitemindex) - 1])
                else:
                    logging.error("getsqlinfo %s with Error : %s" % (sqlfunc, title[1]))
                    return "getsqlinfo %s with Error : %s" % (sqlfunc, title[1])

        except Exception, e:
            logging.error('Exception : ', str(e))
            return "getsqlinfo Exception: %s" % str(e)

    def getData(self, outputformat, dbcursor, values, api_sql_function, kpi_report_result):
        logging.info('getData...')
        if (outputformat['type'] == "string"):
            return outputformat['value']
        elif(outputformat['type'] == "data"):
            if (values[int(outputformat['value']) - 1] != None):
                datasource = values[int(outputformat['value']) - 1]['datasource']
                if (datasource == 'params'):
                    datavalue = values[int(outputformat['value']) - 1]['datavalue']
                    return param[datavalue]
                elif(datasource == "sql"):
                    datainfo = self.getsqlinfo(dbcursor, values[int(outputformat['value'])-1], api_sql_function, kpi_report_result)
                    logging.info('sql datainfo: %s' % datainfo)
                    return str(datainfo)
                elif(datasource == 'evaldata'):
                    evalstring = values[int(outputformat['value']) - 1]['value']
                    logging.info('evalstring begin: ' + evalstring)
                    evalsubitems = re.findall('\$\{\d+\}', evalstring)
                    logging.info('evalsubitems : ' + str(evalsubitems))
                    if (len(evalsubitems) > 0):
                        for evalsubitem in evalsubitems:
                            evalsubitem_match = re.search('(\d+)', evalsubitem)
                            logging.info('evalsubitem_match : ' + evalsubitem_match.group())
                            if(evalsubitem_match):
                                evalsubitem_index = int(evalsubitem_match.group())
                                newoutputformat = {
                                    "type": "data",
                                    "value": evalsubitem_index
                                }
                                result = self.getData(newoutputformat, dbcursor, values, api_sql_function, kpi_report_result)
                                logging.info('result: ' + result)
                                evalstring = evalstring.replace(evalsubitem, result)
                    try:
                        logging.info('evalstring over: ' + evalstring)
                        return str(round(eval(evalstring), 2))
                    except Exception as e:
                        logging.info('evalstring over Error: ' + str(e))
                        return str(e)


    def saveInExcel(self,datastr, KPI, ws):
        ws[KPI['outputlocation']] = datastr

    def saveExcelSheet(self, ws, sheet):
        if 'RTM_KPI' in sheet.keys():
            self.saveExcelSheetRTMKPI(ws, sheet['RTM_KPI'])
        if 'MME_KPI' in sheet.keys():
            if self.param.selectmmesgsn != '':
                self.saveExcelSheetMMEKPI(ws, self.mmedbcursor, sheet['MME_KPI'])
        if 'SAEGW_KPI' in sheet.keys():
            if self.param.selectsaegwggsn != '':
                self.saveExcelSheetSAEGWKPI(ws, self.saegwdbcursor, sheet['SAEGW_KPI'])
    
    def saveExcelSheetRTMKPI(self, ws, kpiconfig):
        kpi_list = kpiconfig
        kpi_report_result = {}
        self.runRTMKPI(ws, kpi_list)
        
    def runRTMKPI(self, ws, kpi_list):    
        for kpi in kpi_list:
            values = kpi['values']
            outputformats = kpi['outputformats']
            outputstring = ''
            for outputformat in outputformats:
                if (outputformat['type'] == 'string'):
                    outputstring += outputformat['value']
                elif values[int(outputformat['value']) - 1]['datasource'] == 'params':
                    datavalue = values[int(outputformat['value']) - 1]['datavalue']
                    if (hasattr(self.param, datavalue)):
                        outputstring += self.param[datavalue]
                    elif (datavalue in self.param['extraparams'].keys()):
                        outputstring += self.param['extraparams'][datavalue]
                elif values[int(outputformat['value']) - 1]['datasource'] == 'rtm':
                    valuesindex = int(outputformat['value']) - 1
                    result = self.getRTMKPI(values, valuesindex)
                    outputstring += result
                elif values[int(outputformat['value']) - 1]['datasource'] == 'evaldata':
                    evalstring = values[int(outputformat['value']) - 1]['value']
                    logging.info('evalstring begin: ' + evalstring)
                    evalsubitems = re.findall('\$\{\d+\}', evalstring)
                    logging.info('evalsubitems : %s' % evalsubitems)
                    if (len(evalsubitems) > 0):
                        for evalsubitem in evalsubitems:
                            evalsubitem_match = re.search('(\d+)', evalsubitem)
                            logging.info('evalsubitem_match : ' + evalsubitem_match.group())
                            if(evalsubitem_match):
                                evalsubitem_index = int(evalsubitem_match.group()) - 1
                                result = self.getRTMKPI(values, evalsubitem_index)
                                logging.info('result: %s' % result)
                                evalstring = evalstring.replace(evalsubitem, result)
                    try:
                        logging.info('evalstring over: ' + evalstring)
                        outputstring += str(round(eval(evalstring), 2))
                    except Exception as e:
                        outputstring = outputstring + evalstring + str(e)
            self.saveInExcel(outputstring, kpi, ws)

    def getRTMKPI(self, values, valuesindex):
        hostname = values[valuesindex]['host']
        itemname = values[valuesindex]['itemname']
        valueindex = values[valuesindex]['valueindex']
        resultvalues = self.rtm_statis.rtm_get_value(hostname, itemname, self.param.startdatetime, self.param.stopdatetime)
        logging.info('rtm resultvalues: ' + str(resultvalues))
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

    def saveExcelSheetSAEGWKPI(self, ws, dbcursor, kpiconfig):
        logging.info('saveExcelSheetSAEGWKPI...')
        api_sql_function = saegw_api_sql_function
        kpi_list = kpiconfig
        kpi_report_result = {}
        self.runOSSKPI(ws, kpi_list, dbcursor, api_sql_function, kpi_report_result)

    def saveExcelSheetMMEKPI(self, ws, dbcursor, kpiconfig):
        api_sql_function = mme_api_sql_function
        kpi_list = kpiconfig
        kpi_report_result = {}
        self.runOSSKPI(ws, kpi_list, dbcursor, api_sql_function, kpi_report_result)
        
    def runOSSKPI(self, ws, kpi_list, dbcursor, api_sql_function, kpi_report_result):    
        for kpi in kpi_list:
            #logging.info('kpi : ' + kpi)
            logging.info('runOSSKPI: ' + json.dumps(kpi))
            values = kpi['values']
            outputformats = kpi['outputformats']
            outputstring = ''
            for outputformat in outputformats:
                if (outputformat['type'] == 'string'):
                    outputstring += outputformat['value']
                else:
                    outputstring += self.getData(outputformat, dbcursor, values, api_sql_function, kpi_report_result)
            
            self.saveInExcel(outputstring, kpi, ws)

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
        
if __name__ == '__main__':

    logging.info('query time : ' + time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time())))
    
    formparams = None
    runmode = 'test'
    if ( len(sys.argv) ) > 2 :
        logging.info("\t run mode : " + str(sys.argv[1]))
        logging.info("\t excel config : " + str(sys.argv[2]))
        logging.info("\t params : " + str(sys.argv[3])) 
        runmode = sys.argv[1]
        excelconfig = sys.argv[2]
        formparams = sys.argv[3]
        logging.info("\t run mode : " + runmode) 
        logging.info("\t excel config : " + excelconfig) 
        logging.info("\t formparams : " + formparams) 
        
       
    param = PmSqlParam()

    if (not formparams == None):
        try:
            getforminfo(param, formparams)
            logging.info('\tparams info : ' + prn_obj(param))
        except Exception as e:
            logging.error('error in param get: %s' % e )
    else:
        logging.info('form params is None.')
    
    # for excel , in these param
    # we need netype(mme or saegw), ne(SHMME03BNK), time(2018-06-30T13:03:51.155Z)

    #currtime = datetime.datetime.strptime(param.time, "%Y-%m-%dT%H:%M:%S.%fZ")
    if not hasattr(param, 'time') or param['time'] == None:
        param['time'] = time.time()
    timeArray = time.localtime(float(param.time))
    param_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    currtime = datetime.datetime.strptime(param_time, "%Y-%m-%d %H:%M:%S")
    currtime = datetime.datetime(currtime.year, currtime.month, currtime.day, currtime.hour, 0)
    currtime = currtime + datetime.timedelta(minutes=-1)
    pretime = currtime + datetime.timedelta(minutes=-1*59)
    
    param.startdate = pretime.strftime("%Y/%m/%d")
    param.stopdate = currtime.strftime("%Y/%m/%d")
    param.starttime = pretime.strftime("%H:%M")
    param.stoptime = currtime.strftime("%H:%M")
    param.maketime = time.strftime("%Y%m%d%H%M%S", timeArray)

    logging.info('param: \n%s' % param)

    filepath = os.path.split(os.path.realpath(__file__))[0]
    logging.info('main filepath: ' + filepath)
    pm_excelfill = PM_ExcelFill(param, runmode, excelconfig)

    fill_result = pm_excelfill.init()
    if fill_result['resultcode'] == 0:
        logging.info('PM_ExcelFill initialize failed : %s' % fill_result['resultdetail'])
        #sys.exit(1)
    else:
        fill_result = pm_excelfill.excel_fill()
        if fill_result['resultcode'] == 0:
            logging.info('PM_ExcelFill fill failed : %s' % fill_result['resultdetail'])
            #sys.exit(1)
    
    pm_excelfill.closeAll()
    #print(json.dumps(fill_result['result']))
    print(json.dumps(fill_result))

# test script
# python scripts\RTM_statis_new.py
	
