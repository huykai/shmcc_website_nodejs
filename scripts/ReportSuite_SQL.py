# -*- coding: utf-8 -*-

import sys
import os
import io
import json
import logging
import time
import datetime
import re

#import cx_Oracle as oracle
#from CMG_statis_new import *

#runmode = "test"
#(dbuser,dbpasswd,dburl,dburlport,db_dbname)=getdbconfig(runmode, "cmgdb")
#print "cmgdb parameter: ", dbuser,dbpasswd,dburl,dburlport,db_dbname
#cmgdb = oracle.connect(dbuser, dbpasswd, dburl)
#cmgdbcursor=cmgdb.cursor()

def create_reportsuite_sql(param):
    sqlstring = ""
    droptemptable_sqlstrings = []
    createtemptable_sqlstrings = []
    selecttemptable_sqlstrings = []
    startdatetime = param.startdate + ' ' + param.starttime + ":00"
    stopdatetime = param.stopdate + ' ' + param.stoptime + ":00"
    
    try:
        startdatetime_regex = re.compile(r"period_start_time >= to_date\('\d+/\d+/\d+ \d+:\d+:\d+'",re.M)
        stopdatetime_regex = re.compile(r"period_start_time < to_date\('\d+/\d+/\d+ \d+:\d+:\d+'",re.M)
        reportsuite_sqltemp = param['SQLCUSTOM'][param['sql_template']]
        temp_tables = reportsuite_sqltemp['temp_table']
        for temp_table in temp_tables:
          droptemptable_sqlstrings.append("truncate table " + temp_table + " DROP STORAGE")
          droptemptable_sqlstrings.append("drop table " + temp_table)
        for cratetemp_table in reportsuite_sqltemp['create_temptable']:
          createtemptable_sqlstring = ""
          createtemptable_sqlstring += startdatetime_regex.sub("period_start_time >= to_date('" + startdatetime + "'", cratetemp_table) 
          createtemptable_sqlstring = stopdatetime_regex.sub("period_start_time < to_date('" + stopdatetime + "'", createtemptable_sqlstring)
          createtemptable_sqlstrings.append(createtemptable_sqlstring) 
        selecttemptable_sqlstrings.append(reportsuite_sqltemp['select_temptable'])
        #print(droptemptable_sqlstring)
        #print(createtemptable_sqlstring)
        #print(selecttemptable_sqlstring)
        sqlstring = {
          "droptemptable": droptemptable_sqlstrings,
          "createtemptable": createtemptable_sqlstrings,
          "selecttemptable": selecttemptable_sqlstrings
        }
    except Exception as e:
    #    print 'something error!'
        errorMessage = "Error create_reportsuite_sql: " + str(e)
        return (['error', errorMessage], None) 
    return sqlstring

if __name__ == "__main__":
    print 'begin getconfig'
    if len(sys.argv) > 2:
        print sys.argv[1]
        print sys.argv[2]
    else:
        print 'please input your command parameter for runmode and database model name.'
        sys.exit()
    (username, passwd, url, urlport, db_name) = getdbconfig(sys.argv[1], sys.argv[2])
    print username
    print passwd
    print url
    print urlport
    print db_name

    #print sqlstring
    cmgdbcursor.execute(createtable_sqlstring)
    cmgdbcursor.execute(select_sqlstring)
    row=cmgdbcursor.fetchall()
    print row
    cmgdbcursor.execute(trunctable_sqlstring)
    cmgdbcursor.execute(droptable_sqlstring)
