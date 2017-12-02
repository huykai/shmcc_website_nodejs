"""
for database parameter get from config/db.xml
"""
# -*- coding: utf-8 -*-
#coding=utf-8

import xml.dom.minidom
import sys
import os

class PmSqlParam(object):
    """
    class pm_sql_param
    """
    def __init__(self):
        self.startdate = ""
        self.stopdate = ""
        self.starttime = ""
        self.stoptime = ""
        self.selectperiod = 15
        self.selectperiodtype = 'continue'
        self.selectmmesgsn = "all"
        self.selectmmeelement = "MMESGSN"
        self.selectsaegwelement = "SAEGWGGSN"
        self.selectsaegwggsn = "all"
        self.selectsession = "0"
        self.localsave = "0"
        self.kpilist = ""
        self.isMME = 1

class AlarmSqlParam(object):
    """
    class pm_sql_param
    """
    def __init__(self):
        self.startdate = ""
        self.stopdate = ""
        self.starttime = ""
        self.stoptime = ""
        self.selectmmesgsn = "all"
        self.selectmmeelement = "MMESGSN"
        self.selectsaegwelement = "SAEGWGGSN"
        self.selectsaegwggsn = "all"
        self.alarm_level = "all"
        self.alarm_number = "All"
        self.isAlarmDetail = "true"
        self.localsave = "0"
        self.isMME = 1

def prn_obj():
    print ('\n'.join(['%s:%s' % item for item in this.__dict__.items()]))

def getdbconfig(runmode, dbmodelname):
    """
    from db.xml get the db's params
    """
    try:
        path = os.path.split(os.path.realpath(__file__))[0]
        #print 'db.xml path: ' + path + "/config/db.xml"
        if (runmode != "test"):
            dom = xml.dom.minidom.parse(path + '/config/' + runmode + '/db.xml')
            #console.log('config file path',path + "./config/' + runmode + '/db.xml")
        else:
            dom = xml.dom.minidom.parse(path + "/config/db.xml")
        #print 'db.xml : ' + path + "/config/db.xml"
        dbs = dom.getElementsByTagName('dbmodelname')
        
        #print 'dbs',dbs
        for db in dbs:
            #print db.getAttribute('id')
            if db.getAttribute('id') == dbmodelname:
                dbuser = db.getElementsByTagName('userid')[0].firstChild.data
                dbpasswd = db.getElementsByTagName('password')[0].firstChild.data
                dburl = db.getElementsByTagName('dburl')[0].firstChild.data
                dburlport = db.getElementsByTagName('dburlport')[0].firstChild.data
                dbname = db.getElementsByTagName('dbname')[0].firstChild.data
                break
        return (dbuser, dbpasswd, dburl, dburlport, dbname)
    except:
        return ('except', '', '', '', '')


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
	
