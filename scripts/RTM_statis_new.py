#coding=utf-8
import datetime
import time
#from zabbix.api import ZabbixAPI
from pyzabbix import ZabbixAPI

from GetConfig import *

# zapi = ZabbixAPI(url='http://localhost:51081/api_jsonrpc.php', user='Admin', password='NokiaRtm') 
import logging
logging.basicConfig(filename='pm_excel_logger.log', level=logging.INFO)

class RTM_Statis(object):
    zapi = None
    url = 'http://localhost:51081/api_jsonrpc.php'
    user = 'Admin'
    password = 'NokiaRtm'
    def make_result(self, resultcode, result):
        return { 'resultcode': resultcode, 'result': result }

    def __init__(self):
        self.zapi = None

    def rtm_conn_win(self, url, user, password):
        try:
            self.url = url
            self.user = user
            self.password = password
            self.zapi = ZabbixAPI(url=url, user=user, password=password)
            #print('rtm_conn: ', url, user, password)
            #self.zapi = ZabbixAPI(url)
            #self.zapi.login(user, password)
            return self.make_result(1, "zabbix initialize successfully")
        except Exception as e:
            return self.make_result(0, e)
    
    def rtm_conn_linux(self, url, user, password):
        try:
            self.url = url
            self.user = user
            self.password = password
            #self.zapi = ZabbixAPI(url=url, user=user, password=password)
            #print('rtm_conn: ', url, user, password)
            self.zapi = ZabbixAPI(url)
            self.zapi.login(user, password)
            return self.make_result(1, "zabbix initialize successfully")
        except Exception as e:
            return self.make_result(0, e)

    def rtm_get_host(self, hostname):
        try:
            apiresult = self.zapi.do_request('host.get', {
                'filter': {
                    'host': [hostname]
                }
            })
            if (apiresult and len(apiresult['result'])>0):
                return self.make_result(1, apiresult['result'][0]['hostid'])
            else:
                return self.make_result(0, 'host query return null')
        except Exception as e:
            return self.make_result(0, e)

    def rtm_get_item(self, itemname, hostid):
        try:
            apiresult = self.zapi.do_request('item.get', {
                'output': 'extend',
                'hostids': hostid,
                'search': {
                    'name': itemname
                }
            })
            if (apiresult and len(apiresult['result'])>0):
                return self.make_result(1, apiresult['result'][0]['itemid'])
            else:
                return self.make_result(0, 'item query return null')
        except Exception as e:
            return self.make_result(0, e)

    def rtm_get_trend(self, itemid, starttime, stoptime):
        try:
            apiresult = self.zapi.do_request('trend.get', {
                'output': [
                    "itemid",
                    "clock",
                    "num",
                    "value_min",
                    "value_avg",
                    "value_max",
                ],
                'itemids': [itemid],
                'time_from': starttime,
                'time_till': stoptime
            })
            if (apiresult and len(apiresult['result'])>0):
                return self.make_result(1, apiresult['result'])
            else:
                return self.make_result(0, 'trend query return null')
        except Exception as e:
            return self.make_result(0, e)

    def rtm_get_value(self, hostnames, itemnames, starttime, stoptime):
        if (self.zapi == None):
            connresult = self.rtm_conn(url, user, password)
            if (connresult['resultcode'] == 1):
                self.zapi = connresult['result']
            else:
                return self.make_result(0, 'zabbix api connect fail')

        if type(hostnames) != list:
            hostnames = [hostnames]
        if type(itemnames) != list:
            itemnames = [itemnames]

        logging.info('starttime: ' + str(starttime))
        logging.info('stoptime: ' + str(stoptime))
                
        return_result = []
        for hostname in hostnames: 
            host_result = self.rtm_get_host(hostname)
            if (host_result['resultcode'] == 0):
                return self.make_result(0, 'hostname %s can not be found : %s' % (hostname, host_result['result']))
            hostid = host_result['result']
            logging.info('hostid find: ' + hostid)

            for itemname in itemnames:
                item_result = self.rtm_get_item(itemname, hostid)
                if (item_result['resultcode'] == 0):
                    return self.make_result(0, 'itemname %s can not be found : %s' % (itemname, item_result['result']))
                itemid = item_result['result']
                logging.info('itemid find: ' + itemid)
                
                trend_result = self.rtm_get_trend(itemid, starttime, stoptime)
                logging.info('trend_result: ' + str(trend_result))
                if trend_result['resultcode'] != 0:
                    for trend_result_item in trend_result['result']:
                        trend_result_item['hostname'] = hostname
                        trend_result_item['itemname'] = itemname
                        return_result.append(trend_result_item)
                
        if len(return_result)>0:
            return self.make_result(1, return_result)
        else:
            return self.make_result(0, return_result)

if __name__ == '__main__':
    stopdatetime = datetime.datetime.now()
    startdatetime = stopdatetime + datetime.timedelta(hours = -1)

    #stoptime = int(time.mktime(stopdatetime.timetuple()))
    #starttime = int(time.mktime(startdatetime.timetuple()))

    stoptime = 1533171300 
    starttime = 1533162700

    url = 'http://localhost:51081/api_jsonrpc.php'
    user = 'Admin'
    password = 'NokiaRtm'
    rtm_statis = RTM_Statis()
    api_result = rtm_statis.rtm_conn(url=url, user=user, password=password)
    if (api_result['resultcode'] == 0):
        logging.info('Zabbix API init failed: %s' % api_result['result'])
        exit(1)
    else:
        zapi = api_result['result']

    value_result = rtm_statis.rtm_get_value(['SHMME03BNK','SHMME04BNK'], ['calEPS_DEF_BEARER_ACT_VOLTE_SUCC_Rate', 'calEPS_DEF_BEARER_ACT_SUCC_Rate'], starttime, stoptime)
    if (value_result['resultcode'] == 1):
        logging.info('RTM result: ' + value_result['result'])
    else:
        logging.info('RTM query failed: ' + value_result['result'])


# test script
# python scripts\RTM_statis_new.py