//var errors = require('./errors');
var express = require('express');
var router = express.Router();
var site_config = require('./site_config');
var api_config = require('./api_config');
var cp = require('child_process');

// Set parameter in array to get from router.post() or router.get()
post_api_exec_program = []
post_api_exec_script = []
post_api_exec_returntype = []
get_api_exec_program = []
get_api_exec_script = []
get_api_exec_returntype = []

// Set child_process buffer
CP_Parameters = {
    encoding: 'utf8', 
    timeout: 0,
    maxBuffer: 5000 * 1024,
    killSignal: 'SIGTERM'
}

for (var api in api_config) {
    //console.log(api_config[api]);
    var api_string = api_config[api].api_string;
    var method_type = api_config[api].method_type;
    var exec_program = api_config[api].program;
    var exec_script = api_config[api].script;
    var return_type = api_config[api].return_type;
    if (method_type == 'POST') {
        post_api_exec_program[api_string]=exec_program
        post_api_exec_script[api_string]=exec_script
        post_api_exec_returntype[api_string]=return_type
        router.post(api_string , function(req, res, next) {
            console.log('exec in router : post');
            //console.log(req)
            //console.log(req.path)
            var queryparam = JSON.stringify(req.body);
            console.log(queryparam)
            
            var api_string = req.path
            var exec_program = post_api_exec_program[api_string]
            var exec_script = post_api_exec_script[api_string]
            var return_type = post_api_exec_returntype[api_string]
            
            cp.execFile(exec_program, [exec_script, queryparam], CP_Parameters, function (err, stdout, stderr){
                if (err) console.error(err);
                else {
                    //console.log(stdout);
                    res.set('Content-Type', return_type);
                    res.status(200).send(stdout);
                }
            })
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

            cp.execFile(exec_program, [exec_script, queryparam], CP_Parameters, function (err, stdout, stderr){
                if (err) console.error(err);
                else {
                    //console.log(stdout);
                    res.set('Content-Type', return_type);
                    res.status(200).send(stdout);
                }
            })
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
