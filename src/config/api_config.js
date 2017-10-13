'use strict';

var apiconfig = [
    {
        api_string: '/api/mme_query', 
        mode: 'execFile',
        program: 'e:\\Develop_Language\\Python27\\python.exe ',
        script: 'scripts/PM_statis_report_new.py',
        method_type: 'POST',
        return_type: 'text/xml'
    },
    {
        api_string: '/api/saegw_query',
        mode: 'execFile',
        program: 'python.exe ',
        script: 'scripts/SAEGW_statis_mysql.py',
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
        program: 'java.exe -jar e:\\eclipse_projects\\TrafficaDBAPI\\target\\TrafficaDBAPI-0.0.1-SNAPSHOT-jar-with-dependencies.jar ',
        //mode: 'file',
        //program: './reactjs/data/data_tmp.json',
        script: "",
        method_type: 'POST',
        return_type: 'text/json'
    }
]

module.exports = apiconfig;