var fs = require("fs");
var path = require("path");
var log4js = require('log4js');
var log4js_config = require('./logConf.json')

//var resultdir = "E:/PersonalProject/Code_Projects/Javascripts/AngularJS_Demo/shmcc/app/"
var LogFile = log4js.getLogger('log_file');

var getMode = '';
var getParams = '';
var runScript = '';

var scriptMain = 'processrunner.js';
var scriptYML = 'tasks_cdr_tmp1.yml';
var scriptParams = {};
var scriptFilter = {};
scriptParams['test_task_1_vars'] = {};
scriptParams['get_cdr_loop_options'] = [];
// node processrunner.js tasks_cdr_tmp1.yml  
// '{ "get_cdr_loop_options": [{"loop_name":"cmd16", "host":"shcg16bnk-1"},{"loop_name":"cmd17", "host":"shcg17bnk-1"}], 
// "test_task_1_vars":{"startdatetime":"201801141300","stopdatetime":"201801141310",
// "cdrtype":"scdr","filter":"{}","resultfilename":"result-yyy"}, 
// "showresult_task_item_vars":{"resultfilename":"result-yyy"}}'
// [2018-01-15T15:23:37.154] [INFO] log_file - taskoption= { "get_cdr_loop_options": [{"loop_name":"cmd16", "host":"shcg16bnk-1"},{"loop_name":"cmd17", "host":"shcg17bnk-1"}], "test_task_1_vars":{"startdatetime":"201801141300","stopdatetime":"201801141310","cdrtype":"scdr","filter":"{}","resultfilename":"result-yyy"}, "showresult_task_item_vars":{"resultfilename":"result-yyy"}}

if (process.argv.length < 4) {
    console.log(JSON.stringify({"errorinfo":"getCgCdr need parameter! Usage: node getCgCdrInfo rtm/test {params}"}));
    process.exit(1);
} else {
    getMode = process.argv[2];
    getParams = process.argv[3];
    
    if (getParams.imsi && getParams.imsi != '') {
        scriptFilter['servedIMSI'] = getParams.imsi;
    }

    if (getParams.msisdn && getParams.msisdn != '') {
        scriptFilter['servedMSISDN'] = getParams.msisdn;
    }
    
    if (getParams.startdatetime && getParams.startdatetime != '' && getParams.stopdatetime && getParams.stopdatetime != '') {
        scriptParams['test_task_1_vars'] = Object.assign(scriptParams['test_task_1_vars'], {
            'startdatetime': getParams.startdatetime,
            'stopdatetime': getParams.stopdatetime
        });
    } else {
        LogFile.warn('Params have no startdatetime or stopdatetime!');
        process.exit(1);
    }

    if (getParams.cdrtype && getParams.cdrtype != '') {
        scriptParams['test_task_1_vars'] = Object.assign(scriptParams['test_task_1_vars'], {
            'cdrtype': getParams.cdrtype
        });
    } else {
        LogFile.warn('Params have no cdrtype!');
        process.exit(1);
    }

    if (getParams.cglist && getParams.cglist.length <= 0) {
        LogFile.info(`Params cglist = ${getParams.cglist}`);
        let cglist = [];
        for (let cg of getParams.cglist) {
            cglist.push({
                "loop_name": cg,
                "host": cg
            })
        }
        scriptParams['get_cdr_loop_options'] = cglist;
    } else {
        LogFile.warn('Params have no cglist!');
        process.exit(1);
    }

    if (getParams.mmelist && getParams.mmelist != '') {
        LogFile.info(`Params mmelist = ${getParams.mmelist}`);
        scriptParams['test_task_1_vars'] = Object.assign(scriptParams['test_task_1_vars'], {
            'mmelist': getParams.mmelist
        });
    } 

    if (getParams.saegwlist && getParams.saegwlist != '') {
        LogFile.info(`Params saegwlist = ${getParams.saegwlist}`);
        scriptParams['test_task_1_vars'] = Object.assign(scriptParams['test_task_1_vars'], {
            'saegwlist': getParams.saegwlist
        });
    }

    var now = new Date();
    var datetimenowstr = now.getFullYear() + now.getMonth() + now.getDate() + now.getHours() + now.getMinutes() + now.getSeconds();
    scriptParams['test_task_1_vars'] = Object.assign(scriptParams['test_task_1_vars'], {
        'resultfilename': `result_${datetimenowstr}`
    });
    scriptParams['test_task_1_vars'] = Object.assign(scriptParams['test_task_1_vars'], {
        'filter': scriptFilter
    });
    scriptParams['showresult_task_item_vars'] = Object.assign({}, {
        'resultfilename': `result_${datetimenowstr}`
    });


    runScript = `node ${scriptMain} ${scriptYML} ${scripParams} `
    console.log('runScript: ', runScript);
}