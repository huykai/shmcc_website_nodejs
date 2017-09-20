const Sequelize = require('sequelize');

const sequelize = new Sequelize('mysql://root:@127.0.0.1:51130/zabbix');

sequelize.authenticate()
        .then( () => {
            console.log('Connection to rtm db has been established successfully.');
            rtmdb_test();
        })
        .catch( err => {
            console.log('Unable to connect to the rtm database:',err);
        })

const history = sequelize.define('history', {
    itemid : {
        type: Sequelize.BIGINT(20)
    },
    clock : {
        type: Sequelize.BIGINT(11)
    },
    value : {
        type: Sequelize.DECIMAL(16,4)
    },
    ns : {
        type: Sequelize.BIGINT(11)
    }
});

function rtmdb_test() {
    history.findOne({
        where: {itemid:70355,clock:1489645655},
        attributes: ['itemid','clock','value']
    }).then(history =>{

    })
}
