'use strict';

var apiconfig = [
    {
        api_string: '/api/mme_query', 
        mode: 'exec',
        program: 'python scripts/PM_statis_report_new.py rtm ',
        script: ' ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query',
        mode: 'exec',
        program: 'python scripts/PM_statis_report_new.py rtm ',
        //script: '/root/huykai/python27/bin/python scripts/SAEGW_statis_mysql.py',
        script: ' ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/mme_query_alarm', 
        mode: 'exec',
        program: 'python scripts/HistoryAlarmList.py rtm ',
        script: ' ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query_alarm',
        mode: 'exec',
        program: 'python scripts/HistoryAlarmList.py rtm ',
        //script: '/root/huykai/python27/bin/python scripts/SAEGW_statis_mysql.py',
        script: ' ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/mme_query', 
        mode: 'execFile',
        program: 'python ',
        script: 'scripts/PM_statis_report_mysql.py',
        method_type: 'GET',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query',
        mode: 'execFile',
        program: 'python ',
        script: 'scripts/SAEGW_statis_mysql.py',
        method_type: 'GET',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/getTrafficaRecord',
        mode: 'exec',
        program: 'java -jar /root/huykai/node_webserver/nodejs_shmcc_website/TrafficaDBAPI-0.0.1-SNAPSHOT-jar-with-dependencies.jar rtm ',
        script: "",
        method_type: 'POST',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getResultSubInfo',
        mode: 'exec',
        program: 'node ', 
        script: 'scripts/getResultSubInfo.js rtm ',
        method_type: 'GET',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getCgCdr',
        mode: 'exec',
        program: 'node ', 
        script: 'scripts/getCgCdr.js rtm ',
        method_type: 'POST',
        return_type: 'text/json'
    }
]

module.exports = apiconfig;
