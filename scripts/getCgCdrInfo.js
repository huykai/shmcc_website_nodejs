var fs = require("fs");
var path = require("path");
const { exec, spawn } = require('child_process');
var log4js = require('log4js');
var log4js_config = require('./logConf.json')

//var resultdir = "E:/PersonalProject/Code_Projects/Javascripts/AngularJS_Demo/shmcc/app/"
var LogFile = log4js.getLogger('log_file');
var nodePath = '/root/huykai/node-v6.10.2-linux-x64/bin';
var scriptPath = '/root/huykai/node_webserver/nodejs_shmcc_website/scripts';
var taskPath = '/root/huykai/javascript_projects/taskrunner';
var getMode = '';
var getParams = {};
var runScript = '';


// Set child_process buffer
var CP_Parameters = {
    encoding: 'utf8',
    timeout: 0,
    //maxBuffer: 50000 * 1024,
    maxBuffer: Infinity,
    cwd: taskPath,
    killSignal: 'SIGTERM'
}


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
    getParams = JSON.parse(process.argv[3]);
    
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

    if (getParams.cglist && getParams.cglist != '') {
        let cgs = getParams.cglist.split(',');
        let cglist = [];
        //LogFile.info(`Params cglist = ${getParams.cglist}`);
        for (let cg of cgs) {
            cglist.push({
                "loop_name": cg,
                "host": cg
            })
        }
        scriptParams['get_cdr_loop_options'] = cglist;
    } else {
        //LogFile.warn('Params have no cglist!');
        process.exit(1);
    }

    if (getParams.mmelist && getParams.mmelist != '') {
        // LogFile.info(`Params mmelist = ${getParams.mmelist}`);
        let mmelist = getParams.mmelist.split(',');
        scriptFilter['mmelist'] = mmelist
    } 

    if (getParams.saegwlist && getParams.saegwlist != '') {
        //LogFile.info(`Params saegwlist = ${getParams.saegwlist}`);
        let saegwlist = getParams.saegwlist.split(',');
        scriptFilter['saegwlist'] = saegwlist
    }

    var date = new Date();
    let dateYear = date.getFullYear();
    let dateMonth = date.getMonth() < 10 ? '0' + (date.getMonth() + 1) : (date.getMonth() + 1)
    let dateDate = date.getDate() < 10 ? '0' + date.getDate() : date.getDate()
    let timeHour = date.getHours() < 10 ? '0' + date.getHours() : date.getHours()
    let timeMinute = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()
    let timeSecond = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds()
    let datetimenowstr = dateYear + dateMonth + dateDate + timeHour + timeMinute + timeSecond
    scriptParams['test_task_1_vars'] = Object.assign(scriptParams['test_task_1_vars'], {
        'resultfilename': `result-${datetimenowstr}`
    });
    scriptParams['test_task_1_vars'] = Object.assign(scriptParams['test_task_1_vars'], {
        'filter': `${JSON.stringify(scriptFilter)}`
    });
    scriptParams['showresult_task_item_vars'] = Object.assign({}, {
        'resultfilename': `result-${datetimenowstr}`
    });


    //runScript = `cd ${taskPath}; ${nodePath}/node ${taskPath}/${scriptMain} ${scriptYML} '${JSON.stringify(scriptParams)}' `
    runScript = `${nodePath}/node ${taskPath}/${scriptMain} ${taskPath}/${scriptYML} '${JSON.stringify(scriptParams)}'`
    //console.log(`runScript = ${runScript}`);
    const runProcess = exec(runScript, CP_Parameters,  (error, stdout,stderr) => {
        if (error) {
            console.log(`exec error: ${error}`);
            return;
        }
        console.log(stdout);
        //console.log(stderr);
    });
    //runScript = `${nodePath}/node ${taskPath}/${scriptMain} ${scriptYML} '${JSON.stringify(scriptParams)}' `
    //const runProcess = spawn('node', [`${taskPath}/${scriptMain}`, `${scriptYML}`, '${JSON.stringify(scriptParams)}\\\'`], CP_Parameters);
    //runProcess.stdout.on('data', (data) => {
    //    console.log(data.toString());
    //});
    //runProcess.on('error', (err) => {
    //    console.log(err);
    //    process.exit(1);
    //});
    //runProcess.on('close', (code) => {
    //     process.exit(code);
    //});
    //console.log('runScript: ', runScript);
}
