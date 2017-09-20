const orm = require('orm');

orm.connect('mysql://root:@127.0.0.1:51130/zabbix', function(err,db){
    if (err) throw err;
    orm.settings.set("properties.primary_key", 'itemid');
    orm.settings.set("properties.required", false);
    
    console.log('mysql connection ok');
    const history = db.define('history', {
        itemid : {type:'number'},
        clock : {type:'number'},
        value : {type:'number'},
        ns : {type:'number'}
    });
    rtmdb_test(history);
    //process.exit(0);
});

function rtmdb_test(history) {
    history.one(
        {itemid:70355,clock:1489645655},
        function(err,res){
            console.log('err:',err);
            console.log('res',res);
        }
    )
}

