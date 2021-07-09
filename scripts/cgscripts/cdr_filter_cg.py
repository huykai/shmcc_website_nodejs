#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import json
import re
import multiprocessing
import threading, time

class cdr_handle(object):

    def __init__(self):
        self.records = []
        self.records_count = 0

    """
    export records
    """    
    def export_records(self):
        for record in self.records:
            print(json.dumps(record))
    
    """
    add record
    """
    def add_record(self, rec):
        self.records.append(rec)

class ProcessFilter(threading.Thread):
    def __init__(self, lock, config, cdrtype, filenames, filterCriteria):
        """
        @summary init class
        @param lock: lock object
        @param threadName: thread Name
        @param processString: thread's process to run
        """
        super(ProcessFilter, self).__init__(name = "Thread_" + filename)
        self.lock = lock
        self.config = config
        self.cdrtype = cdrtype
        self.cdrfilenames = filenames
        self.processString = "java -jar " + config.config['cdrhandle_proc'][cdrtype]
        self.filterCriteria = filterCriteria
        #print('filterCriteria : ' + filterCriteria)
        self.result = []
        
    def matchitem(self, itemkey, itemstr):
        #print('itemkey : ' + itemkey)
        if (itemkey in self.filterCriteria.keys()):
            return self.filterCriteria[itemkey] == itemstr
        return True

        
    def MatchRecord(self, RecordString):
        recordregs = self.config.config['cdr_records_item_regex'][self.cdrtype]
        record = {}
        isMatch = True
        for RecordItem in recordregs.keys():
            RecordReg = recordregs[RecordItem]
            #print('regex:',RecordReg['regex'])
            #print('regmode:',RecordReg['regmode'])
            result = re.search(RecordReg['regex'], RecordString, RecordReg['regmode'])
            if (result != None):
                resultstr = result.group(1)
                if(self.matchitem(RecordItem, resultstr)):
                    record[RecordItem] = resultstr
                else:
                    isMatch = False
                    break
        if (isMatch):
            self.result.append(record) 
                    

    def filterRecord(self, resultFileContent):
        """
        @summary: filter the cdr file
        """
        #self.result = ['process: ' + self.processString]
        start_position = 0
        regexstr = self.config.config['cdr_records_regex'][self.cdrtype]['regex']
        regexmode = self.config.config['cdr_records_regex'][self.cdrtype]['regmode']
            
        #while( 1 ):
            #record = re.match(r'^(>sgsnPDPRecord.*?\n\n)', resultFileContent[start_position:], re.S|re.I)
            #record = re.search(regexstr, resultFileContent[start_position:], regexmode)
        records = re.findall(regexstr, resultFileContent[start_position:], regexmode)
        #print('find records : ' + str(len(records)))
        if(records != None):
            for record in records:
                self.MatchRecord(record)
            #(_, record_stop_position) = record.span()
            #start_position += record_stop_position
            #break
        #else:
        #    break

    def run(self):
        """
        @summary: overload suport run method, run after thread start
        """ 
        #self.lock.acquire()
        #self.lock.release()
        for cdrfilename in self.cdrfilenames:
            
            match_filepathname = self.config.config['cdrfile_path'][cdrtype] + "/" + cdrfilename
            resultfilename = self.config.config['cdrfile_txt_dir'][cdrtype] + cdrfilename + ".txt.log"
            processString = self.processString + " " + match_filepathname + " > " + resultfilename
            #print()
            try:
                os.system(processString)

                resultfile = open(resultfilename,'r')
                resultfilelines = resultfile.readlines()
                resultcontents = ''.join(resultfilelines)
                self.filterRecord(resultcontents)
                #print('thread result : ' + cdrfilename + " " + resultcontents)    
            except Exception as e:
                print(e)
                self.result = ['exception']
            finally:
                resultfile.close()
                os.unlink(resultfilename)
                
        #print('thread result : ' + resultcontents)
                
                


class cdr_config:
    """
    class for cdr handle config
    """
    def __init__(self):
        """
        This for real cmd config
        """
        self.config_file = './config/cdr_config.json'
        
        
        """
        This for test cmd config
        """
        self.config_file = './config/cdr_config.json'
        
        self.scdr_recordreg = {
            'recordOpeningTime' : {
                'regex' : r'-->recordOpeningTime.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'duration' : {
                'regex' : r'-->duration.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'accessPointNameNI' : {
                'regex' : r'-->accessPointNameNI.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'cForRecClosing' : {
                'regex' : r'-->causeForRecClosing.*value: (\w*).*$',
                'regmode' : re.M|re.I
            },
            'servedIMSI' : {
                'regex' : r'-->servedIMSI.*value: 0x(.*)f$',
                'regmode' : re.M|re.I
            },
            'sgsnAddress' : {
                'regex' : r'-->sgsnAddress.*?value: ([\d\W]*)\n',
                'regmode' : re.S|re.I
            },
            'accessPointNameOI' : {
                'regex' : r'-->accessPointNameOI.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'servedMSISDN' : {
                'regex' : r'-->servedMSISDN.*value: 0x(.*)f$',
                'regmode' : re.M|re.I
            },
            'chargingCharacteristics' : {
                'regex' : r'-->chargingCharacteristics.*value: 0x(.*)$',
                'regmode' : re.M|re.I
            },
            'systemType' : {
                'regex' : r'-->systemType.*value: (\w*).*$',
                'regmode' : re.M|re.I
            },
            'dataVolumeGPRSUplink' : {
                'regex' : r'-->dataVolumeGPRSUplink.*value: (\d*)$',
                'regmode' : re.M|re.I
            },
            'dataVolumeGPRSDownlink' : {
                'regex' : r'-->dataVolumeGPRSDownlink.*value: (\d*)$',
                'regmode' : re.M|re.I
            }
        }
        self.sgwcdr_recordreg = {
            'recordOpeningTime' : {
                'regex' : r'-->recordOpeningTime.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'duration' : {
                'regex' : r'-->duration.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'accessPointNameNI' : {
                'regex' : r'-->accessPointNameNI.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'servedIMSI' : {
                'regex' : r'-->servedIMSI.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'sGWAddress' : {
                'regex' : r'-->sGWAddress.*?value: ([\d\W]*)\n',
                'regmode' : re.S|re.I
            },
            'pGWAddressUsed' : {
                'regex' : r'-->pGWAddressUsed.*?value: ([\d\W]*)\n',
                'regmode' : re.S|re.I
            },
            'nodeID' : {
                'regex' : r'-->nodeID.*?value: (.*)\n',
                'regmode' : re.M|re.I
            },
            'rATType' : {
                'regex' : r'-->rATType.*?value: (\w*).*\n',
                'regmode' : re.M|re.I
            },
            'servedMSISDN' : {
                'regex' : r'-->servedMSISDN.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'chargingCharacteristics' : {
                'regex' : r'-->chargingCharacteristics.*value: 0x(.*)$',
                'regmode' : re.M|re.I
            },
            'dataVolumeGPRSUplink' : {
                'regex' : r'-->dataVolumeGPRSUplink.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'dataVolumeGPRSDownlink' : {
                'regex' : r'-->dataVolumeGPRSDownlink.*value: (.*)$',
                'regmode' : re.M|re.I
            }
        }
        self.pgwcdr_recordreg = {
            'recordOpeningTime' : {
                'regex' : r'-->recordOpeningTime.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'duration' : {
                'regex' : r'-->duration.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'accessPointNameNI' : {
                'regex' : r'-->accessPointNameNI.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'causeForRecClosing' : {
                'regex' : r'-->causeForRecClosing.*value: (\w*).*$',
                'regmode' : re.M|re.I
            },
            'servedIMSI' : {
                'regex' : r'-->servedIMSI.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'pGWAddress' : {
                'regex' : r'-->pGWAddress.*?value: ([\d\W]*)\n',
                'regmode' : re.S|re.I
            },
            'nodeID' : {
                'regex' : r'-->nodeID.*?value: (.*)\n',
                'regmode' : re.M|re.I
            },
            'ratingGroup' : {
                'regex' : r'-->ratingGroup.*?value: (.*)\n',
                'regmode' : re.M|re.I
            },
            'serviceIdentifier' : {
                'regex' : r'-->serviceIdentifier.*?value: (.*)\n',
                'regmode' : re.M|re.I
            },
            'rATType' : {
                'regex' : r'-->rATType.*?value: (\w*).*\n',
                'regmode' : re.M|re.I
            },
            'servedMSISDN' : {
                'regex' : r'-->servedMSISDN.*value: (.*)$',
                'regmode' : re.M|re.I
            },
            'chargingCharacteristics' : {
                'regex' : r'-->chargingCharacteristics.*value: 0x(.*)$',
                'regmode' : re.M|re.I
            },
            'datavolumeFBCUplink' : {
                'regex' : r'-->datavolumeFBCUplink.*value: (\d*)$',
                'regmode' : re.M|re.I
            },
            'datavolumeFBCDownlink' : {
                'regex' : r'-->datavolumeFBCDownlink.*value: (\d*)$',
                'regmode' : re.M|re.I
            }
        }
        self.config = {
            'cdrfile_path' : {
                'scdr' : '/cdr/work/backup/wlkf/scdr',
                'sgwcdr' : '/cdr/work/backup/wlkf/sgw',
                'pgwcdr' : '/cdr/work/backup/wlkf/pgw'
            },
            'cdrfile_txt_dir' : {
                'scdr' : 'cdr/cdr_log/scdr/',
                'sgwcdr' : 'cdr/cdr_log/sgw/',
                'pgwcdr' : 'cdr/cdr_log/pgw/'
            },
            'cdrfile_txt_file' : {
                'scdr' : [],
                'sgwcdr' : [],
                'pgwcdr' : []
            },
            'cdrhandle_proc' : {
                'scdr' : '/home/cmd/cutover/asn1decm.jar',
                'sgwcdr' : '/home/cmd/cutover/epcdeccm.jar',
                'pgwcdr' : '/home/cmd/cutover/epcdeccm.jar'
            },
            'cdr_records_regex' : {
                'scdr' : {
                    'regex' : r'(>sgsnPDPRecord.*?\n\n)',
                    'regmode' : re.S|re.I
                },
                'sgwcdr' : {
                    'regex' : r'(>sGWRecord.*?\n\n)',
                    'regmode' : re.S|re.I
                },
                'pgwcdr' : {
                    'regex' : r'(>pGWRecord.*?\n\n)',
                    'regmode' : re.S|re.I
                }
            },
            'cdr_records_item_regex' : {
                'scdr' : self.scdr_recordreg,
                'sgwcdr' : self.sgwcdr_recordreg,
                'pgwcdr' : self.pgwcdr_recordreg
            },
            'cdr_result_files' : {
                'scdr' : '',
                'sgwcdr' : '',
                'pgwcdr' : ''
            }
        }
        """
        self.config = {
            'cdrfile_path' : {
                'scdr' : 'cdr/cdr_raw/scdr',
                'sgwcdr' : 'cdr/cdr_raw/sgw',
                'pgwcdr' : 'cdr/cdr_raw/pgw'
            },
            'cdrfile_txt_dir' : {
                'scdr' : 'cdr/cdr_log/scdr/',
                'sgwcdr' : 'cdr/cdr_log/sgw/',
                'pgwcdr' : 'cdr/cdr_log/pgw/'
            },
            'cdrfile_txt_file' : {
                'scdr' : ['scdr.log'],
                'sgwcdr' : ['PGW_cdr.log'],
                'pgwcdr' : ['SGW_cdr.log']
            },
            'cdrhandle_proc' : {
                'scdr' : 'tools/asn1decm.jar',
                'sgwcdr' : 'tools/epcdeccm.jar',
                'pgwcdr' : 'tools/epcdeccm.jar'
            },
            'cdr_records_regex' : {
                'scdr' : {
                    'regex' : r'^(>sgsnPDPRecord.*?\n\n)',
                    'regmode' : re.S|re.I
                },
                'sgwcdr' : {
                    'regex' : r'^(>sGWRecord.*?\n\n)',
                    'regmode' : re.S|re.I
                },
                'pgwcdr' : {
                    'regex' : r'^(>pGWRecord.*?\n\n)',
                    'regmode' : re.S|re.I
                }
            },
            'cdr_records_item_regex' : {
                'scdr' : self.scdr_recordreg,
                'sgwcdr' : self.sgwcdr_recordreg,
                'pgwcdr' : self.pgwcdr_recordreg
            },
            'cdr_result_files' : {
                'scdr' : '',
                'sgwcdr' : '',
                'pgwcdr' : ''
            }
        }
        """

    def makeresult(self, err, info):
        """
        generate result
        """
        return {"err" : err, "info" : info}

    def read_config(self):
        """
        read config file for loading the config parameters
        """
        try:
            if ( len(self.config_file) > 0 ):
                config_file = open(self.config_file, 'r')
                config_string = config_file.read()
                self.config = json.loads(config_string)
                config_file.close()
                config_file = None
            else:
                return self.makeresult("1", "Read Config File Error (Config file name is NULL)!")
        except Exception as e: 
            return self.makeresult("1", "Read Config File Error (Exception Message : " + e.__cause__ + ")")
        finally:
            if (config_file):
                config_file.close()
        return self.makeresult("0", self.config)

def match_condition(filename, start, stop):
    match_result = False
    curr = start
    while filename.find(str(curr)) < 0:
        curr = curr + 1
        if (curr > stop):
            return match_result
    match_result = True
    return match_result

def DoJobInProcesses(match_files, c_conf, cdrtype, filterCriteria):
    process_thread_number = 10
    pool = multiprocessing.Pool(processes = process_thread_number)
    results = []
    process_results = [[]]
    filesInThreads = [[]]
    i = 0
    for match_file in match_files:
        if (len(filesInThreads) <= i) and (len(filesInThreads) < process_thread_number):
            filesInThreads.append([])
            process_results.append([])
        filesInThreads[i % process_thread_number].append(match_file)
        i += 1
    i = 0
    for filesInThread in filesInThreads:    
        process_results[i] = pool.apply_async(DoJobInThreads, args=(filesInThread, c_conf, cdrtype, filterCriteria))
        i += 1
        
    pool.close()
    pool.join()
    j = 0
    while ( j < i ):
        #results.append(process_results[j].get())
        results += process_results[j].get()
        j += 1

    return results

def DoJobInThreads(match_files, c_conf, cdrtype, filterCriteria):
    process_thread_number = 10
    lock  = threading.Lock()
    jobs = []
    results = []
    filesInThreads = [[]]
    i = 0
    for match_file in match_files:
        if (len(filesInThreads) <= i) and (len(filesInThreads) < process_thread_number):
            filesInThreads.append([])    
        filesInThreads[i % process_thread_number].append(match_file)
        i += 1
        
    for filesInThread in filesInThreads:    
        #print('thread : handle('+ str(filesInThread) +')')
        p = ProcessFilter(lock, c_conf, cdrtype, filesInThread, filterCriteria)
        p.start()
        jobs.append(p)

    #print('thread count:' + str(len(filesInThreads)))
    for p in jobs:
        p.join()
    
    for p in jobs:
        if(len(p.result) > 0):
            results += p.result
    return results

if __name__ == '__main__':

    process_thread_number = 20

    if len(sys.argv) < 5:
        print("usage: python cdr_filter cdrtype(scdr/sgw/pgw) startdatetime(mmddHHMM) stopdatetime(mmddHHMM) search_condition")
        exit(1)

    cdrtype = sys.argv[1]
    startdatetime = sys.argv[2]
    stopdatetime = sys.argv[3]
    filterCriteria = {}
    #print("startdatetime : ", startdatetime)
    #print("stopdatetime : ", stopdatetime)
    #print("filterCriteria : " + filterCriteria)
    
    try:
        #print(sys.argv[4])
        filterCriteria = json.loads(sys.argv[4])
        
    except Exception as e:
        print('Json Exception : ')
        print(e)
        print("parameter error: filter not valid ")
        exit(1)
    try:
        longstartdatetime = long(startdatetime)
        longstopdatetime = long(stopdatetime)
    except Exception as e: 
        print(e)
        print("parameter error: startdatetime(mmddHHMM)/stopdatetime(mmddHHMM) should be number ")
        exit(1)

    if ( startdatetime > stopdatetime ):
        print("parameter error: startdatetime(mmddHHMM) should less than stopdatetime(mmddHHMM)")
        exit(1)
    c_conf = cdr_config()
    
    #print('cdr file dir : ', c_conf.config['cdrfile_path'][cdrtype])
    cdr_filenames = os.listdir(c_conf.config['cdrfile_path'][cdrtype])
    match_files = []
    for filename in cdr_filenames:
        if match_condition(filename, longstartdatetime, longstopdatetime):
            match_files.append(filename)
    #print("match_files : ", match_files)
    try:
        os.makedirs(c_conf.config['cdrfile_txt_dir'][cdrtype])
    except OSError as e:
        pass
    #print('file count:' + str(len(match_files)))
    #results = DoJobInThreads(match_files, c_conf, cdrtype, filterCriteria)
    results = DoJobInProcesses(match_files, c_conf, cdrtype, filterCriteria)

    results_filename = cdrtype + "_" + time.strftime("%Y%m%d%H%M%S") + "_cdr.log"
    results_file = open(results_filename, "w")
    results_file.write(json.dumps(results))
    result_dir = os.path.dirname(os.path.realpath(__file__))
    print("result file name: %s/%s" % (result_dir, results_filename)) 
    #print("result file name: ", results_filename)
    
