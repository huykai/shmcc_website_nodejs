//var errors = require('./errors');
var express = require('express');
var router = express.Router();
var site_config = require('./site_config');
var api_config = require('./api_config');
var cp = require('child_process');
var tokenManager = require('./token_manager');
var path = require('path');
var fs = require('fs');

// Set parameter in array to get from router.post() or router.get()
var post_api_exec_mode = []
var post_api_exec_program = []
var post_api_exec_script = []
var post_api_exec_returntype = []
var get_api_exec_program = []
var get_api_exec_script = []
var get_api_exec_returntype = []

// Set child_process buffer
var CP_Parameters = {
    encoding: 'utf8', 
    timeout: 0,
    maxBuffer: Infinity,
    killSignal: 'SIGTERM'
}

for (let api in api_config) {
    //console.log(api_config[api]);
    let api_string = api_config[api].api_string;
    let exec_mode = api_config[api].mode;
    let method_type = api_config[api].method_type;
    let exec_program = api_config[api].program;
    let exec_script = api_config[api].script;
    let return_type = api_config[api].return_type;
    if (method_type == 'POST') {
        post_api_exec_mode[api_string]=exec_mode;
        post_api_exec_program[api_string]=exec_program
        post_api_exec_script[api_string]=exec_script
        post_api_exec_returntype[api_string]=return_type
        router.post(api_string , function(req, res, next) {

            console.log('exec in router : post');
            //console.log(req)
            //console.log(req.path)
            //if (!tokenManager.verifyToken(req, res)){
            //    res.send(401);
            //    return;
            //};
            tokenManager.checkToken(req, res, function(req, res, next){
                //var queryparamstr = JSON.stringify(req.body);
                //queryparamstr = queryparamstr.replace(/"/g,'\\"');
                //console.log('queryparamstr:',queryparamstr);
                let queryparam = JSON.stringify(req.body) ;
                //var queryparam = "'" + queryparamstr + "'" ;
                //var queryparam = "'" + '{\"IMSI\":\"\",\"MSISDN\":\"\",\"LTECAUSEPROC\":\"all\"}' + "'"; 
                //var queryparam = '\'{\'IMSI\':\'\',\'MSISDN\':\'\',\'LTECAUSEPROC\':\'all\'}\'';
                
                console.log('POST parameters: ', queryparam);
                
                let api_string = req.path;
                let exec_mode = post_api_exec_mode[api_string];
                let exec_program = post_api_exec_program[api_string];
                let exec_script = post_api_exec_script[api_string];
                let return_type = post_api_exec_returntype[api_string];
                
                if (exec_mode === "execFile" ) {
                    cp.execFile(exec_program, [exec_script, queryparam], CP_Parameters, function (err, stdout, stderr){
                        if (err) {
                            console.error(err);
                            res.set('Content-Type', return_type);
                            res.status(200).send(stdout);
                        }else {
                            //console.log(stdout);
                            res.set('Content-Type', return_type);
                            //res.cookie('XSRF-TOKEN', req.csrfToken());
                            res.status(200).send(stdout);
                        }
                    });
                } else if (exec_mode === "exec") {
                    queryparam = queryparam.replace(/"/g,'\\"');
                    console.log('exec:',exec_program, exec_script, queryparam);
                    cp.exec(exec_program + exec_script + queryparam, CP_Parameters, function (err, stdout, stderr){
                        if (err) {
                            console.error(`${err}`);

                            res.set('Content-Type', return_type);
                            res.status(200).send(stdout);
                        }else {
                            console.log(stdout);
                            res.set('Content-Type', return_type);
                            //res.cookie('XSRF-TOKEN', req.csrfToken());
                            res.status(200).send(stdout);
                        }
                    });
                } else if (exec_mode === "file") {
                    //var fileName = site_config.static_dir + exec_program;
                    let fileName = exec_program;
                    console.log('file:',exec_program,queryparam);
                    console.log(fileName);
                    //res.cookie.csrfToken = req.cookies.csrfToken;
                    //res.locals._csrf = req.csrfToken();
                    //res.cookie('XSRF-TOKEN', req.csrfToken());
                    res.set('Content-Type', return_type);
                    let returninfo = {
                        filename : fileName,
                        columninfo : [
                            {field:'itemid',title:'Item ID',width:100},
                            {field:'productid',title:'List Price',width:100},
                            {field:'unitcost',title:'Unit Cost',width:100,align:'right'}
                        ]
                    }
                    res.status(200).send(returninfo);
                    //res.status(200).sendFile(fileName, function (err) {
                    //res.status(200).send(returninfo, function(err){
                    //    if (err) {
                    //    console.log(err);
                    //    } else {
                    //    console.log('Sent:', returninfo);
                    //    }
                    //});
                }
                
            });

            
        })
    } else if (method_type == 'GET') {
        
        get_api_exec_program[api_string]=exec_program
        get_api_exec_script[api_string]=exec_script
        get_api_exec_returntype[api_string]=return_type
        router.get(api_string , function(req, res, next) {
            //console.log(req);
            let queryparam = JSON.stringify(req.query);
            console.log('exec in router : get');
            console.log('Get params : ', queryparam);
            
            let api_string = req.path
            let exec_program = get_api_exec_program[api_string]
            let exec_script = get_api_exec_script[api_string]
            let return_type = get_api_exec_returntype[api_string]
                
            //console.log(exec_script)
            //console.log(exec_program)
            //console.log(return_type)
            if (exec_mode === "exec") {
                queryparam = queryparam.replace(/"/g,'\\"');
                console.log('exec:',exec_program, exec_script, queryparam);
                cp.exec(exec_program + exec_script + queryparam, CP_Parameters, function (err, stdout, stderr){
                    if (err) console.error(err);
                    else {
                        //console.log(stdout);
                        res.set('Content-Type', return_type);
                        //res.cookie('XSRF-TOKEN', req.csrfToken());
                        res.status(200).send(stdout);
                    }
                });
            } else if (exec_mode === "execFile") {
                cp.execFile(exec_program, [exec_script, queryparam], CP_Parameters, function (err, stdout, stderr){
                    if (err) console.error(err);
                    else {
                        //console.log(stdout);
                        res.set('Content-Type', return_type);
                        res.status(200).send(stdout); 
                    }
                })
            } else if (exec_mode === "execDownload") { // this kind of mode for download generated file, stdout is filename
                queryparam = queryparam.replace(/"/g,'\\"');
                console.log('execDownload: ',exec_program, exec_script, queryparam);
                cp.exec(exec_program + exec_script + queryparam, CP_Parameters, function (err, stdout, stderr){
                    if (err) console.error(err);
                    else {
                        console.log(stdout);
                        try {
                            let FullFileName = (stdout + "").trim()
                            let FileName = path.basename(FullFileName)
                            console.log(`execDownload FileName: ${FileName} FullFileName:${FullFileName}`)
                            let FileData = fs.readFileSync(FullFileName);
                            res.set("Content-Type", return_type);
                            res.set("Content-Disposition", "attachment; filename=\"" + FileName + "\"")
                            res.set("Expires", "0")
                            res.set("Cache-Control", "must-revalidate, post-check=0, pre-check=0")
                            res.set("Content-Transfer-Encoding", "binary")
                            res.set("Pragma", "public")
                            res.set("Content-Length", FileData.length + "")
                            
                            res.status(200).send(FileData);
                        } catch (Error){
                            console.log(`execDownload with error: ${Error}`)
                            res.set("Content-Type", return_type);
                            res.status(200).send(`Err: ${Error}`);
                        }
                        
                    }
                })
            }
        })
    }
    
    
}





//API_Items_Collection.prototype.remove = function(id, cb) {
//id = parseInt(id, 10);
//if (this.store[id]) {
//    delete this.store[id];
//    cb();
//} else {
//    cb(new errors.NotFound('Item not found'));
//}
//};

module.exports = router;
