# -*- coding: utf-8 -*-

import sys
import cx_Oracle
import time
import datetime
#import smtplib 
import cgi
#import xlsxwriter,xlrd
import MySQLdb as mysql

import os
import io
import json
import logging
import re

import openpyxl

logging.basicConfig(filename='pm_excel_logger.log', level=logging.INFO)

reload(sys)
sys.setdefaultencoding("utf-8")


#from MME_statis_mysql import *
from MME_statis_new import *
from SAEGW_statis_new import *




def getforminfo(params,formparams):
    # Get data from formparams
    configs = json.loads(formparams)
    logging.info("formparams : " + formparams)
    #print configs
    for key, item in configs.items():
        #print key," : ",item
        params.__dict__[key] = item
    
    if (configs['netype'] == 'mme'):
        params.isMME = True
    else:
        params.isMME = False
    if (not configs.has_key('selectperiod')):
        params.selectperiod = '60'
    if (params.selectperiodtype == None):
        params.selectperiodtype = 'continue'
    if (params.isMME):
        params.selectmmesgsn = configs['ne'] 
        if (params.selectmmeelement == None):
            params.selectmmeelement = 'MME'
    else :
        params.selectsaegwggsn = configs['ne'] 
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

def avg_cacul(algo, rows, algoindex):
    sum = 0
    for row in rows:
        sum += float(row[int(algoindex)-1])
    if(len(rows)>0):
        return str(sum/len(rows))
    return 0

def max_cacul(algo, rows, algoindex):
    max = 0
    for row in rows:
        if(float(row[int(algoindex)-1]) > max):
            max = float(row[int(algoindex)-1])
    return str(max)

def min_cacul(algo, rows, algoindex):
    min = 0
    for row in rows:
        if(float(row[int(algoindex)-1]) < min):
            min = float(row[int(algoindex)-1])
    return str(min)

def sum_cacul(algo, rows, algoindex):
    sum = 0
    for row in rows:
        sum += float(row[int(algoindex)-1])
    return str(sum)


def algo_cacul(algo, rows, algoindex):
    ret = '0'
    if (algo == 'avg'):
        ret = avg_cacul(algo, rows, algoindex)
    elif (algo == 'max'):
        ret = max_cacul(alog, rows, algoindex)
    elif (algo == 'min'):
        ret = min_cacul(alog, rows, algoindex)
    elif (algo == 'sum'):
        ret = sum_cacul(alog, rows, algoindex)
    
    return ret

def caculate(rows, sqlextrastruct):
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
        ret = algo_cacul(algo, tmprow, algoindex)
        #print('caculate after algo: ' + str(ret))
        return ret
    else:
        return ''

    

def getsqlinfo(valuestruct):
    #try:
    sqlfunc = valuestruct['sql_function']
    #print('getsqlinfo : ', sqlfunc)
    sqlitemindex = valuestruct['sql_selectitem_index']
    #print('getsqlinfo : ', sqlitemindex)
    kpi_function = api_sql_function[sqlfunc]['func']
    #print('getsqlinfo : ', kpi_function)
    if (kpi_report_result.has_key(sqlfunc)):
        if (valuestruct.has_key("sql_extra")):
            #print('getsqlinfo valuestruct has key sql_extra')
            return caculate(kpi_report_result[sqlfunc], valuestruct["sql_extra"])
        else:    
            return kpi_report_result[sqlfunc][0][int(sqlitemindex) - 1]
    else:
        title,row=kpi_function(sqlfunc, dbcursor, param)
        if title[0]!='error' and len(row)>0:
            #print('getsqlinfo ' + sqlfunc + ' ' + str(row[0]))
            kpi_report_result[sqlfunc] = row
            #print('getsqlinfo valuestruct has key sql_extra ? ', valuestruct.has_key("sql_extra"))
            if (valuestruct.has_key("sql_extra")):
                #print('getsqlinfo valuestruct has key sql_extra')
                return caculate(row, valuestruct["sql_extra"])
            
            return str(row[0][int(sqlitemindex) - 1])
        else:
            logging.error("getsqlinfo %s with Error : %s" % (sqlfunc, title[1]))
            return ''

    #except Exception, e:
    #    print('Exception : ', str(e))
    #    return str(e)

def getData(outputformat, values):
    if (outputformat['type'] == "string"):
        return outputformat['value']
    elif(outputformat['type'] == "data"):
        if (values[int(outputformat['value']) - 1] != None):
            datasource = values[int(outputformat['value']) - 1]['datasource']
            if (datasource == 'params'):
                datavalue = values[int(outputformat['value']) - 1]['datavalue']
                return param[datavalue]
            elif(datasource == "sql"):
                datainfo = getsqlinfo(values[int(outputformat['value'])-1])
                #print('sql datainfo: %s' % datainfo)
                return str(datainfo)

def saveInExcel(datastr, KPI, ws):
    ws[KPI['outputlocation']] = datastr

if __name__ == '__main__':

    logging.info('query time : ' + time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time())))

    KPI_Excel_Cutover_filename = os.path.realpath(__file__) + '/scripts/config/KPI_Excel_Cutover.json'
    KPI_Excel_Cutover_Result = {}
    #print('{"result":"Ok", "data":"Whatever"}')
    #exit(0)
    formparams = None
    runmode = 'test'
    if ( len(sys.argv) ) > 2 :
        logging.info("\t run mode : " + str(sys.argv[1])) 
        logging.info("\t params : " + str(sys.argv[2])) 
        #print("\t run mode : " + str(sys.argv[1])) 
        #print("\t params : " + str(sys.argv[2])) 
        runmode = sys.argv[1]
        formparams = sys.argv[2]
       
    param = PmSqlParam()

    if (not formparams is None):
        try:
            getforminfo(param, formparams)
            logging.info('\tparams info : ' + prn_obj(param))
            #print('\tparams info : ' + prn_obj(param))
        except Exception, e:
            logging.error('error in param get.' )
    else:
        logging.info('form params is None.')
    #sys.exit()
    # for excel , in these param
    # we need netype(mme or saegw), ne(SHMME03BNK), time(2018-06-30T13:03:51.155Z)

    currtime = datetime.datetime.strptime(param.time, "%Y-%m-%dT%H:%M:%S.%fZ")
    currtime = datetime.datetime(currtime.year, currtime.month, currtime.day, currtime.hour, 0)
    currtime = currtime + datetime.timedelta(minutes=-1)
    pretime = currtime + datetime.timedelta(minutes=-1*59)
    
    param.startdate = pretime.strftime("%Y/%m/%d")
    param.stopdate = currtime.strftime("%Y/%m/%d")
    param.starttime = pretime.strftime("%H:%M")
    param.stoptime = currtime.strftime("%H:%M")

    #print('\tparams info : ' + prn_obj(param))
    # for test
    #paramsdate_fix()

    # connect to mysql
    #(mmedbuser,mmedbpasswd,mmedburl,mmedburlport,mmedb_dbname)=getdbconfig("mmedb_mysql")
    # connect to oracle
    if (param.netype == "mme"):
        (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(runmode, "mmedb")
    else:
        (dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(runmode, "saegwdb")
    
    #print 'mmeuser:', mmedbuser, mmedbpasswd, mmedburl
	#mmedb = cx_Oracle.connect('omc', 'omc', '127.0.0.1:51063/oss')
    con = None
    result = {
        'resultcode': '0',
        'resultdetail': ''
    }
    try:
        # mysql
        #con = mysql.connect(host=mmedburl, port=int(mmedburlport), user=mmedbuser, passwd=mmedbpasswd, db=mmedb_dbname)
        #mmecursor=con.cursor()
        # oracle
        logging.info('dbuser, dbpasswd, dburl : %s, %s, %s' % (dbuser, dbpasswd, dburl))
	    #mmedb = cx_Oracle.connect('omc', 'omc','10.221.255.4:1521/oss') 

        with io.open(KPI_Excel_Cutover_filename, 'r', encoding='utf-8') as load_f:
            KPI_Excel_Cutover = json.load(load_f)
            #print(load_dict)
        wb = openpyxl.load_workbook(KPI_Excel_Cutover['EXCEL_MODEL'])
        
        filename = KPI_Excel_Cutover['EXCEL_FILENAME']
        db = cx_Oracle.connect(dbuser, dbpasswd, dburl)
        dbcursor=db.cursor()
    
        #print "kpilist: ", param.kpilist
        if (param.netype == "mme"):
            #print("param.isMME : " + param.isMME)
            ws = wb[KPI_Excel_Cutover['MME_SHEET']]
            api_sql_function = mme_api_sql_function
            kpi_list = KPI_Excel_Cutover['MME_KPI']
        else:
            ws = wb[KPI_Excel_Cutover['SAEGW_SHEET']]
            api_sql_function = saegw_api_sql_function
            kpi_list = KPI_Excel_Cutover['SAEGW_KPI']

        kpi_report_result = {}
        
        for kpi in kpi_list:
            #logging.info('kpi : ' + kpi)
            #print 'kpi : ' + kpi
            values = kpi['values']
            outputformats = kpi['outputformats']
            outputstring = ''
            for outputformat in outputformats:
                if (outputformat['type'] == 'string'):
                    outputstring += outputformat['value']
                else:
                    outputstring += getData(outputformat, values)
            
            saveInExcel(outputstring, kpi, ws)

            #kpi_function = api_sql_function[kpi]['func']
            #run_kpi(kpi, kpi_function, dbcursor, param)

        if (runmode == 'test'):
            site_config_filename = './scripts/config/api_options.json'
        else:
            site_config_filename = './scripts/config/' + runmode + '/api_options.json' 
        site_config = json.load(open(site_config_filename, 'r'))

        nowtime = datetime.datetime.now() 
        filename = filename + param.ne + nowtime.strftime("%Y%m%d") + nowtime.strftime("%H%M%S") + '.xlsx'
        realfilename = site_config['download_dir'] + filename 
        wb.save(realfilename)
        
        result['resultcode'] = 1
        result['resultdetail'] = 'downloads/' + filename

    except Exception as e:
        logging.error("Error PM_Excelfill: %s" % str(e))
        result['resultcode'] = 0
        result['resultdetail'] = "Error PM_Excelfill: %s" % str(e)
        
    finally:
        if con:
            con.close()
    print(json.dumps(result))
    #if (logfile):
    #    logfile.close()
	
	
