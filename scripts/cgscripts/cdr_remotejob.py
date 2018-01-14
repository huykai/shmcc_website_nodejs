#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import json
import re
import multiprocessing
import threading, time
import subprocess
import logging
from time import sleep

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename='log/cgscripts_logger.log', format=FORMAT)
logger = logging.getLogger("cdr_remotejob")

logger.setLevel(logging.DEBUG)


cg_filter_script_name = 'cdr_filter_cg.py'
cg_host_user = 'cmd'
cg_script_dir = '/tmp/'
resultfile_dir = './'
cg_hosts = {
    'CG16' : {
        'CG16-1' : "172.20.25.88" ,
        'CG16-2' : "172.20.25.89" 
    },
    'CG17' : {
        'CG17-1' : "172.20.14.167" ,
        'CG17-2' : "172.20.14.168" 
    },
    'CG18' : {
        'CG18-1' : "172.20.14.176" ,
        'CG18-2' : "172.20.14.177" 
    },
    'CG19' : {
        'CG19-1' : "172.20.25.70" ,
        'CG19-2' : "172.20.25.71" 
    },
    'CG20' : {
        'CG20-1' : "172.20.25.79" ,
        'CG20-2' : "172.20.25.80" 
    },
    'CG21' : {
        'CG21-1' : "172.20.25.199" ,
        'CG21-2' : "172.20.25.200" 
    },
    'CG22' : {
        'CG22-1' : "172.20.25.208" ,
        'CG22-2' : "172.20.25.209" 
    },
    'CG23' : {
        'CG23-1' : "172.20.25.217" ,
        'CG23-2' : "172.20.25.218" 
    },
    'CG24' : {
        'CG24-1' : "172.20.25.226" ,
        'CG24-2' : "172.20.25.227" 
    }, 
    'CG25' : {
        'CG25-1' : "172.20.24.231" ,
        'CG25-2' : "172.20.24.232" 
    },
    'CG26' : {
        'CG26-1' : "172.20.24.240" ,
        'CG26-2' : "172.20.24.241" 
    },
    'CG27' : {
        'CG27-1' : "172.20.30.9" ,
        'CG27-2' : "172.20.30.10" 
    },
    'CG28' : {
        'CG28-1' : "172.20.30.18" ,
        'CG28-2' : "172.20.30.19" 
    },
    'CG29' : {
        'CG29-1' : "172.20.30.27" ,
        'CG29-2' : "172.20.30.28" 
    },
    'CG30' : {
        'CG30-1' : "172.20.30.36" ,
        'CG30-2' : "172.20.30.37" 
    }
}

def DoJobInProcesses(startdatetime, stopdatetime, cglist, cdrtype, filterCriteria):
    
    if (cglist == "all"):
        process_thread_number = len(cg_hosts)
        cghosts = cg_hosts.keys()
    else:
        cghosts = cglist.split(":")
        process_thread_number = len(cghosts)

    logger.info('cghosts : %s' % cghosts)
    pool = multiprocessing.Pool(processes = process_thread_number)
    results = []
    process_results = [[] for cghost in cghosts]
    
    index = 0
    for cghost in cghosts:
        process_results[index] = pool.apply_async(DoJob, args=(cghost, startdatetime, stopdatetime, cdrtype, filterCriteria))
        index += 1

    pool.close()
    pool.join()
    
    index = 0
    for cghost in cghosts:
        #results.append(process_results[j].get())
        results.append(cghost + ":" + process_results[index].get())
        index += 1
    return results

def trycg(cghost, no):
    cghostname = cghost + "-" + str(no + 1)
    command = ' scp %s %s:%s' % \
        (os.path.dirname(os.path.realpath(__file__)) + '/' + cg_filter_script_name, cg_host_user + "@" + cg_hosts[cghost][cghostname], \
        cg_script_dir + cg_filter_script_name )
    logger.info('command = %s' % command)
    p_thread = subprocess.Popen(command , shell=True, \
        stdout = subprocess.PIPE, stderr = subprocess.STDOUT)	
    ret = p_thread.poll() 
    while (ret == None):
        sleep(0.1)
        ret = p_thread.poll()
    output, error = p_thread.communicate()
    logger.info(output)
    del p_thread
    if ret <> 0:
        logger.debug(cghost + '-' + str(no) + ' scp failed.' )
        return None
    logger.debug(cghost + '-' + str(no) + ' scp success.' )
    return True

def trycghost(cghost):
    if trycg(cghost, 0):
        return cghost + "-1"
    if trycg(cghost, 1):
        return cghost + "-2"
    return None

def DoJob(cghost, startdatetime, stopdatetime, cdrtype, filterCriteria):
    """
    1, scp py script to cgxx /tmp
    2, run the py script with parameter
    3, collect the result files
    """
    cghostname = trycghost(cghost)
    logger.info('cghostname : %s' % cghostname)
    if cghostname == None:
        return None

    command = ' ssh %s %s' % \
        (cg_host_user + "@" + cg_hosts[cghost][cghostname], \
         ' python %s %s %s %s %s ' % (cg_script_dir + cg_filter_script_name, \
         cdrtype, startdatetime, stopdatetime, \
         '\\\"' + filterCriteria +'\\\"'))
    logger.info('command = %s' % command)
    p_thread = subprocess.Popen(command , shell=True, \
        stdout = subprocess.PIPE, stderr = subprocess.STDOUT)	
    ret = p_thread.poll() 
    while (ret == None):
        sleep(0.1)
        ret = p_thread.poll()
    output, error = p_thread.communicate()
    logger.info(output)
    del p_thread
    if ret <> 0:
        logger.debug(cghostname + ' ssh remote command failed.' )
        return None
    
    logger.info('command return : %s' % output )
    returndirfilename = output.split(':')[1].strip()
    returnfilename = returndirfilename.split('/')[-1]
    if (returnfilename != None):
        
        command = ' scp %s:%s %s' % \
            (cg_host_user + "@" + cg_hosts[cghost][cghostname], \
            returnfilename, resultfile_dir + returnfilename)
        logger.info('command = %s' % command)
        p_thread = subprocess.Popen(command , shell=True, \
            stdout = subprocess.PIPE, stderr = subprocess.STDOUT)	
        ret = p_thread.poll() 
        while (ret == None):
            sleep(0.1)
            ret = p_thread.poll()
        #output, error = p_thread.communicate()
        del p_thread
        if ret <> 0:
            logger.debug(cghostname + ' scp result file failed.' )
            return None
    	return resultfile_dir + returnfilename
    return None


if __name__ == '__main__':

    process_thread_number = 20

    if len(sys.argv) < 6:
        print("usage: python cdr_remotejob.py cglist(all/cg17:cg18:...:cg-30) cdrtype(scdr/sgw/pgw) startdatetime(mmddHHMM) stopdatetime(mmddHHMM) search_condition")
        exit(1)

    cglist = sys.argv[1]
    cdrtype = sys.argv[2]
    
    startdatetime = sys.argv[3]
    stopdatetime = sys.argv[4]
    filterCriteriaObject = {}
    #print("startdatetime : ", startdatetime)
    #print("stopdatetime : ", stopdatetime)
    #print("filterCriteria : " + filterCriteria)
    
    try:
        filterCriteriaObject = json.loads(sys.argv[5])
        filterCriteria = json.dumps(filterCriteriaObject)
        filterCriteria = filterCriteria.replace('"','\\\\\\\"')
    except Exception as e:
        logger.warning('Json Exception : ')
        logger.warning(e)
        logger.warning("parameter error: filter not valid ")
        exit(1)
    try:
        longstartdatetime = long(startdatetime)
        longstopdatetime = long(stopdatetime)
    except Exception as e: 
        logger.warning(e)
        logger.warning("parameter error: startdatetime(mmddHHMM)/stopdatetime(mmddHHMM) should be number ")
        exit(1)

    if ( startdatetime > stopdatetime ):
        logger.warning("parameter error: startdatetime(mmddHHMM) should less than stopdatetime(mmddHHMM)")
        exit(1)
    
    
    results = DoJobInProcesses(startdatetime, stopdatetime, cglist, cdrtype, filterCriteria)

    #results_filename = cdrtype + "_" + time.strftime("%Y%m%d%H%M%S") + "_cdr.log"
    #results_file = open(results_filename, "w")
    #results_file.write(json.dumps(results))
    #result_dir = os.path.dirname(os.path.realpath(__file__))
    for result in results: 
        print(result) 
    #print("result file name: ", results_filename)
    

# test scripts:
# python cdr_remotejob.py cg17:cg18 scdr 201711041036 201711041038 "{\"accessPointNameNI\": \"CMNET\"}"