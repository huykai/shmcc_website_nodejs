# -*- coding: utf-8 -*-

import sys
import json
import logging

from openpyxl import Workbook

logging.basicConfig(filename='JsonExcel_logger.log', level=logging.INFO)

class JsonToExcel:
    def __init__(self, JsonData, FileName):
        self.JsonData = JsonData
        self.FileName = FileName

    def writeTitles(self, ws):
        jsonData = self.JsonData[0]
        if (jsonData != None):
            #rowName = 1
            #colName = 1
            ws.append(['%s' % attr for attr, value in jsonData.items()])
            
    def writeData(self, ws):
        #rowName = 'B'
        #colName = 1
        for jsonData in self.JsonData:
            ws.append(['%s' % str(value) for attr, value in jsonData.items()])

    def makeFile(self):
        wb = Workbook()
        ws = wb.active
        self.writeTitles(ws)
        self.writeData(ws)
        wb.save(self.FileName)

if __name__ == '__main__':
    try:
        JsonFile = sys.argv[1]
        ExcelFile = sys.argv[2]
        logging.info('JSON FileName: %s' % JsonFile )
        logging.info('Excel FileName: %s' % ExcelFile)
        with open(JsonFile, 'r') as jsonFp:
            JsonData = json.load(jsonFp)['rows']
        jsonToExcel = JsonToExcel(JsonData, ExcelFile)
        jsonToExcel.makeFile()
    except Exception as e:
        print("JsonToExcel run with Exception: %s" % e)
        logging.error("JsonToExcel run with Exception: %s" % e)
    print("JsonToExcel run finished!")

