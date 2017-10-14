'use strict';

var apiconfig = [
    {
        api_string: '/api/mme_query', 
        mode: 'exec',
        program: '/root/huykai/python27/bin/python scripts/PM_statis_report_new.py ',
        //#program: 'node  ',
        //#script: ' --version  ',
        script: ' ',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query',
        mode: 'execFile',
        program: 'python ',
        script: 'scripts/SAEGW_statis_mysql.py',
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
        program: 'java -jar /root/huykai/node_webserver/nodejs_shmcc_website/TrafficaDBAPI-0.0.1-SNAPSHOT-jar-with-dependencies.jar ',
        //mode: 'file',
        //program: './reactjs/data/data_tmp.json',
        script: "",
        method_type: 'POST',
        return_type: 'text/json'
    }
]

module.exports = apiconfig;
