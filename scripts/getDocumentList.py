"""
for pdf document list from $document dir
"""
# -*- coding: utf-8 -*-
#coding=utf-8

import sys
import os
import json
import logging

configEnvir = 'test'
DocumentConfigFile = './'
Document_Dir = './documents/'
Document_Type = '.pdf'

logging.basicConfig(filename='alarm_logger.log', level=logging.INFO)

def getDocumentInfo(configType):
    global DocumentConfigFile
    global Document_Dir
    global Document_Type

    scriptsPath = os.path.abspath(os.path.dirname(__file__))
    
    DocumentConfigFile = scriptsPath + '/scripts/config/api_options.json'
    if (configType == 'test'):
        DocumentConfigFile = scriptsPath + '/scripts/config/api_options.json'
    elif (configType == 'rtm'):
        DocumentConfigFile = scriptsPath + '/scripts/config/rtm/api_options.json'
    
    if(os.path.exists(DocumentConfigFile)):
        try:
            #print DocumentConfigFile
            configFile = open(DocumentConfigFile)
            configFileContent = configFile.read()
            #print configFileContent
            result = json.loads(configFileContent)
            #print str(result)
            Document_Dir = result['document_dir']
            Document_Type = result['document_type']
            #print Document_Dir
            #print Document_Type
        except Exception as e: 
            logging.error('Config File %s Read Failed (detail: %s) ' % (DocumentConfigFile, e))
    else:
        logging.info('Config File %s Can not be found' % (DocumentConfigFile))
    

if __name__ == "__main__":
    #print 'begin get document list'

    if len(sys.argv) > 1:
        configEnvir = sys.argv[1]
    else:
        logging.error('Usage: %s %s [%s] [%s]' % (sys.argv[0], 'test/rtm', 'Document_Dir', 'Document_Type'))
        exit(1)
    
    # get config dir name and file type
    getDocumentInfo(configEnvir)
    
    if len(sys.argv) > 2:
        Document_Config_str = sys.argv[2]
    try:
        Document_Config = json.loads(Document_Config_str)
        Document_Dir = Document_Config.document_dir or Document_Dir
        Document_Type = Document_Config.document_type or Document_Type
    except Exception as e:
        logging.error('Params filter error detail: %s' % e )

    return_file_list = []

    logging.info(Document_Dir)
    logging.info(Document_Type)
    try:
        if (os.path.isdir(Document_Dir)):
            logging.info('dir %s exists' % Document_Dir)
            filelist = os.listdir(Document_Dir)
            for file in filelist:
                if(len(file.split('.'))>1):
                    #logging.info('file name: %s' % file)
                    filetype = file.split('.')[1]
                    if (Document_Type.find(filetype)>0):
                        logging.info('file name: %s' % file)
                        return_file_list.append(file)
        else:
            logging.error('dir %s not exists' % Document_Dir)
    except Exception as e:
        logging.error('Documents Dir filter Failed. (detail: %s)' % e)

    print(json.dumps(return_file_list))
    logging.info(json.dumps(return_file_list))

    
