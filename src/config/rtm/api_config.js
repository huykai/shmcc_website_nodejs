'use strict';

var apiconfig = [
    {
        api_string: '/api/mme_query', 
        mode: 'exec',
        program: 'python /root/huykai/node_webserver/nodejs_shmcc_website/scripts/PM_statis_report_new.py rtm ',
        script: ' ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query',
        mode: 'exec',
        program: 'python /root/huykai/node_webserver/nodejs_shmcc_website/scripts/PM_statis_report_new.py rtm ',
        //script: '/root/huykai/python27/bin/python scripts/SAEGW_statis_mysql.py',
        script: ' ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/mme_query_alarm', 
        mode: 'exec',
        program: 'python /root/huykai/node_webserver/nodejs_shmcc_website/scripts/HistoryAlarmList.py rtm ',
        script: ' ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query_alarm',
        mode: 'exec',
        program: 'python /root/huykai/node_webserver/nodejs_shmcc_website/scripts/HistoryAlarmList.py rtm ',
        //script: '/root/huykai/python27/bin/python scripts/SAEGW_statis_mysql.py',
        script: ' ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/mme_query', 
        mode: 'execFile',
        program: 'python ',
        script: '/root/huykai/node_webserver/nodejs_shmcc_website/scripts/PM_statis_report_mysql.py',
        method_type: 'GET',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query',
        mode: 'execFile',
        program: 'python ',
        script: '/root/huykai/node_webserver/nodejs_shmcc_website/scripts/SAEGW_statis_mysql.py',
        method_type: 'GET',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/getTrafficaRecord',
        mode: 'exec',
        program: 'cd /root/huykai/node_webserver/nodejs_shmcc_website/; java -jar /root/huykai/node_webserver/nodejs_shmcc_website/TrafficaDBAPI-0.0.1-SNAPSHOT-jar-with-dependencies.jar rtm ',
        script: "",
        method_type: 'POST',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getResultSubInfo',
        mode: 'exec',
        program: '/root/huykai/node-v6.10.2-linux-x64/bin/node ', 
        script: '/root/huykai/node_webserver/nodejs_shmcc_website/scripts/getResultSubInfo.js rtm ',
        method_type: 'GET',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getCgCdr',
        mode: 'exec',
        program: 'cd /root/huykai/javascript_projects/taskrunner; /root/huykai/node-v6.10.2-linux-x64/bin/node ', 
        script: '/root/huykai/javascript_projects/taskrunner/scripts/getCgCdrInfo.js rtm tasks_cdr_tmp1.yml ',
        method_type: 'POST',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getCgCdrStatistics',
        mode: 'exec',
        program: 'cd /root/huykai/javascript_projects/taskrunner; /root/huykai/node-v6.10.2-linux-x64/bin/node ',
        script: '/root/huykai/javascript_projects/taskrunner/scripts/getCgCdrInfo.js rtm tasks_cdr_statistics.yml ',
        method_type: 'POST',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getCgCdrAnalysis',
        mode: 'exec',
        program: 'cd /root/huykai/javascript_projects/taskrunner; /root/huykai/node-v6.10.2-linux-x64/bin/node ',
        script: '/root/huykai/javascript_projects/taskrunner/scripts/getCgCdrAnalysis.js rtm tasks_cdr_analysis.yml ',
        method_type: 'POST',
        return_type: 'text/json'
    },
    {
        api_string: '/api/getDocumentList',
        mode: 'exec',
        program: 'python /root/huykai/node_webserver/nodejs_shmcc_website/scripts/getDocumentList.py rtm ',
        script: ' ',
        method_type: 'GET',
        return_type: 'text/json'
    }
]

module.exports = apiconfig;
