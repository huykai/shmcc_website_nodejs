import sys
import os
import json
import logging
from JsonToExcel import JsonToExcel

logging.basicConfig(filename='downloadTrafficaResultSub_logger.log', level=logging.info)

if __name__ == "__main__":
    RunMode = sys.argv[1]
    logging.info("RunMode: %s" % RunMode)
    ResourceFileNameArgv = sys.argv[2]
    
    try:
        ResourceFileNameJSON = json.loads(ResourceFileNameArgv)
        ResourceFileName = ResourceFileNameJSON['resultFile']
        logging.info("ResourceFileName: %s" % ResourceFileName)
        if RunMode == "test":
            RunMode = "/"
        else:
            RunMode = "/" + RunMode + "/"
        API_Config_FileName = os.path.dirname(__file__) + "/config" + RunMode + "api_options.json"
        logging.info("API_Config_FileName: %s" % API_Config_FileName)
        with open(API_Config_FileName, 'r') as API_Config_File:
            API_Config = json.load(API_Config_File)
        ResourceFileDir = API_Config['resultfile_dir']
        FullResourceFileName = ResourceFileDir + ResourceFileName
        logging.info("FullResourceFileName: %s" % FullResourceFileName)
        with open(FullResourceFileName, 'r') as resourceFile:
            jsonData = json.load(resourceFile)
        ExcelFileName = os.path.basename(ResourceFileName).split('.')[0] + ".xlsx"
        FullExcelFileName = API_Config['download_dir'] + ExcelFileName
        logging.info("ExcelFileName: %s" % FullExcelFileName)
        jsonToExcel = JsonToExcel(jsonData['rows'], FullExcelFileName)
        jsonToExcel.makeFile()
        FullExcelFileName = FullExcelFileName.replace("\\","\\\\")
        print(FullExcelFileName)
        #print("Content-Disposition: attachment; filename=\"" + ExcelFileName + "\"")
        #print('Expires: 0')
        #print('Cache-Control: must-revalidate, post-check=0, pre-check=0')
        #print("Content-Transfer-Encoding: binary")
        #print('Pragma: public')
        #print("Content-Length: " + str(os.path.getsize(FullExcelFileName)))
        #with open(API_Config['download_dir'] + ExcelFileName, 'rb') as excelfile:
        #    print(excelfile.read())
    except Exception as e:
        logging.info("downloadTrafficaResultSub run with Exception: %s" % str(e))