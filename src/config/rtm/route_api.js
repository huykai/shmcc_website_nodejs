//var errors = require('./errors');
var express = require('express');
var router = express.Router();
var site_config = require('./site_config');
var api_config = require('./api_config');
var cp = require('child_process');
var tokenManager = require('./token_manager');

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
    //maxBuffer: 50000 * 1024,
    maxBuffer: Infinity,
    killSignal: 'SIGTERM'
}

for (var api in api_config) {
    //console.log(api_config[api]);
    var api_string = api_config[api].api_string;
    var exec_mode = api_config[api].mode;
    var method_type = api_config[api].method_type;
    var exec_program = api_config[api].program;
    var exec_script = api_config[api].script;
    var return_type = api_config[api].return_type;
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
                var queryparam = JSON.stringify(req.body) ;
                //var queryparam = "'" + queryparamstr + "'" ;
                //var queryparam = "'" + '{\"IMSI\":\"\",\"MSISDN\":\"\",\"LTECAUSEPROC\":\"all\"}' + "'"; 
                //var queryparam = '\'{\'IMSI\':\'\',\'MSISDN\':\'\',\'LTECAUSEPROC\':\'all\'}\'';
                
                //console.log(queryparam);
                
                var api_string = req.path;
                var exec_mode = post_api_exec_mode[api_string];
                var exec_program = post_api_exec_program[api_string];
                var exec_script = post_api_exec_script[api_string];
                var return_type = post_api_exec_returntype[api_string];
                
                if (exec_mode === "execFile" ) {
                    //cp.execFile(exec_program, [exec_script, queryparam], CP_Parameters, function (err, stdout, stderr){
                    cp.exec(exec_program + exec_script + " '" + queryparam + "'", CP_Parameters, function (err, stdout, stderr){
                        if (err) console.error(err);
                        else {
                            //console.log(stdout);
                            res.set('Content-Type', return_type);
                            //res.cookie('XSRF-TOKEN', req.csrfToken());
                            res.status(200).send(stdout);
                        }
                    });
                } else if (exec_mode === "exec") {
                    //queryparam = queryparam.replace(/"/g,'\\"');
                    queryparam = "'" + queryparam + "'";
                    console.log('exec:',exec_program, queryparam, ' \nOptions : ', CP_Parameters);
                    cp.exec(exec_program + queryparam, CP_Parameters, function (err, stdout, stderr){
                        if (err) console.error(err);
                        else {
                            //console.log(stdout);
                            res.set('Content-Type', return_type);
                            //res.cookie('XSRF-TOKEN', req.csrfToken());
                            res.status(200).send(stdout);
                        }
                    });
                } else if (exec_mode === "file") {
                    //var fileName = site_config.static_dir + exec_program;
                    var fileName = exec_program;
                    console.log('file:',exec_program,queryparam);
                    console.log(fileName);
                    //res.cookie.csrfToken = req.cookies.csrfToken;
                    //res.locals._csrf = req.csrfToken();
                    //res.cookie('XSRF-TOKEN', req.csrfToken());
                    res.set('Content-Type', return_type);
                    var returninfo = {
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
            console.log('exec in router : get');
            console.log('params :');
            var queryparam = JSON.stringify(req.query);
            console.log(queryparam);
            //console.log(req.path)
           var api_string = req.path
           var exec_program = get_api_exec_program[api_string]
           var exec_script = get_api_exec_script[api_string]
           var return_type = get_api_exec_returntype[api_string]
            
            //console.log(exec_script)
            //console.log(exec_program)
            //console.log(return_type)

            if (exec_mode === "exec") {
                cp.exec(exec_program + exec_script + " '" + queryparam + "'", CP_Parameters, function (err, stdout, stderr){
                    if (err) console.error(err);
                    else {
                        //console.log(stdout);
                        res.set('Content-Type', return_type);
                        //res.cookie('XSRF-TOKEN', req.csrfToken());
                        res.status(200).send(stdout);
                    }
                });
            } else if (exec_mode === "execFile") {
                queryparam = "'" + queryparam + "'";
                cp.execFile(exec_program, [exec_script, queryparam], CP_Parameters, function (err, stdout, stderr){
                    if (err) console.error(err);
                    else {
                        //console.log(stdout);
                        res.set('Content-Type', return_type);
                        res.status(200).send(stdout);
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
