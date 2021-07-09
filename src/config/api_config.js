'use strict';

var apiconfig = [
    {
        api_string: '/api/mme_query', 
        mode: 'exec',
        program: 'D:\\Develop_Languages\\python\\Python2.7\\python.exe ',
        script: 'scripts/PM_statis_report_new.py test ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query',
        mode: 'exec',
        program: 'D:\\Develop_Languages\\python\\Python2.7\\python.exe ',
        //script: 'scripts/SAEGW_statis_mysql.py',
        script: ' scripts/PM_statis_report_new.py test ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/mme_query_alarm', 
        mode: 'exec',
        program: 'D:\\Develop_Languages\\python\\Python2.7\\python.exe ',
        script: 'scripts/HistoryAlarmList.py test ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query_alarm',
        mode: 'exec',
        program: 'D:\\Develop_Languages\\python\\Python2.7\\python.exe ',
        //script: 'scripts/SAEGW_statis_mysql.py',
        script: ' scripts/HistoryAlarmList.py test ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/mme_query', 
        mode: 'execFile',
        program: 'D:\\Develop_Languages\\python\\Python2.7\\python.exe ',
        script: 'scripts/PM_statis_report_mysql.py',
        method_type: 'GET',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query',
        mode: 'execFile',
        program: 'D:\\Develop_Languages\\python\\Python2.7\\python.exe ',
        script: 'scripts/SAEGW_statis_mysql.py',
        method_type: 'GET',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/getTrafficaRecord',
        mode: 'exec',
        program: 'D:\\Develop_Languages\\java\\jdk1.8.0_231\\bin\\java.exe -jar e:/Personal_Projects/Code_Projects/javascript/NodeJS/shmcc_website_nodejs/TrafficaDBAPI-0.0.1-SNAPSHOT-jar-with-dependencies.jar test ',
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
        program: 'D:\\Develop_Languages\\python\\Python2.7\\python.exe ',
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
        program: 'D:\\Develop_Languages\\python\\Python2.7\\python.exe ',
        script: 'scripts/PM_excelfill.py test KPI_Excel_Cutover.json ',
        method_type: 'POST',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getThroughputExcel',
        mode: 'exec',
        program: 'D:\\Develop_Languages\\python\\Python2.7\\python.exe ',
        script: 'scripts/PM_Excel_Throughput_v2.py test Throughput_Excel.json ',
        method_type: 'POST',
        return_type: 'text/json'
    },
    {
        api_string: '/api/downloadResultSub',
        mode: 'execDownload',
        program: 'D:\\Develop_Languages\\python\\Python3.8\\python.exe ',
        script: 'scripts/downloadResultSub.py test ',
        method_type: 'GET',
        return_type: 'application/octet-stream'
    }
]

module.exports = apiconfig;