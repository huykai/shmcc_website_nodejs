'use strict';

var apiconfig = [
    {
        api_string: '/api/mme_query', 
        mode: 'exec',
        program: 'e:\\Develop_Language\\Python27\\python.exe ',
        script: 'scripts/PM_statis_report_new.py test ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query',
        mode: 'exec',
        program: 'e:\\Develop_Language\\Python27\\python.exe ',
        //script: 'scripts/SAEGW_statis_mysql.py',
        script: ' scripts/PM_statis_report_new.py test ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/mme_query_alarm', 
        mode: 'exec',
        program: 'e:\\Develop_Language\\Python27\\python.exe ',
        script: 'scripts/HistoryAlarmList.py test ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query_alarm',
        mode: 'exec',
        program: 'e:\\Develop_Language\\Python27\\python.exe ',
        //script: 'scripts/SAEGW_statis_mysql.py',
        script: ' scripts/HistoryAlarmList.py test ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/mme_query', 
        mode: 'execFile',
        program: 'python.exe ',
        script: 'scripts/PM_statis_report_mysql.py',
        method_type: 'GET',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query',
        mode: 'execFile',
        program: 'python.exe ',
        script: 'scripts/SAEGW_statis_mysql.py',
        method_type: 'GET',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/getTrafficaRecord',
        mode: 'exec',
        program: 'java.exe -jar e:\\eclipse_projects\\eclipse_projects\\TrafficaDBAPI\\target\\TrafficaDBAPI-0.0.1-SNAPSHOT-jar-with-dependencies.jar test ',
        //mode: 'file',
        //program: './reactjs/data/data_tmp.json',
        script: "",
        method_type: 'POST',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getResultSubInfo',
        mode: 'exec',
        program: 'node.exe ', 
        script: 'scripts/getResultSubInfo.js test ',
        method_type: 'GET',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getCgCdr',
        mode: 'exec',
        program: 'node.exe ', 
        script: 'scripts/getCgCdr.js test ',
        method_type: 'POST',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getDocumentList',
        mode: 'exec',
        program: 'e:\\Develop_Language\\Python27\\python.exe ',
        script: 'scripts/getDocumentList.py test ',
        method_type: 'GET',
        return_type: 'text/json'
    },
    {
        api_string: '/api/invokeInspectTask',
        mode: 'exec',
        program: 'node.exe ',
        script: 'scripts/invokeInspectTask.js test ',
        method_type: 'POST',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getExcel',
        mode: 'exec',
        program: 'python ',
        script: 'scripts/PM_excelfill.py test KPI_Excel_Cutover.json ',
        method_type: 'POST',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getThroughputExcel',
        mode: 'exec',
        program: 'python ',
        script: 'scripts/PM_Excel_Throughput_v2.py test Throughput_Excel.json ',
        method_type: 'POST',
        return_type: 'text/json'
    }
]

module.exports = apiconfig;