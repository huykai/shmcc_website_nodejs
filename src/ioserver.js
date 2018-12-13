'use strict';

var ioserver = require('socket.io');

let modedir = '';
if (process.env.shmccpsmode && process.env.shmccpsmode !== "test"){
    modedir = process.env.shmccpsmode + "/"
}
console.log('ioserver mode : ', process.env.shmccpsmode)
var netelements = require('./config/'+ modedir + 'netelementconfig');
var pty = require('node-pty');

const socketServer = function(server, path) {
    let ioServer = null;
    switch (path) {
        case '/hyktty/socket.io':
            ioServer = createTTYIOServer(server, path);            
            break;
        case '/inspector/socket.io':
            ioServer = createInspectIOServer(server, path);            
            break;
        default:
            ioServer = createIOServer(server, path);            
            break;
    }
    return ioServer
}

const createTTYIOServer = function(server, path){
    var io = ioserver(server, {path: path, ws:true});
    io.on('connection', function(socket){
        io['TTYIOSocket'] == socket;
        console.log('hyktty io connected');
        socket.on('login', function(loginparam){
            console.log('io login param:', JSON.stringify(loginparam));
            let netelement = findNetElement(loginparam['name'], netelements);
            if (netelement == null) {
                console.log('netelement ', loginparam['name'], ' not found!');
                return;
            }

            var logintype = netelement.type || 'ssh';
            var loginuser = netelement.user || 'root' + '@';
            var loginhost = netelement.host || 'localhost';
            var loginport = netelement.port || '22';
            var loginauth = netelement.auth || 'password,keyboard-interactive';
            var loginauto = netelement.login ? Object.assign([],netelement.login) : [];
            // var request = socket.request;
            // console.log((new Date()) + ' Connection accepted.');
            // if (match = request.headers.referer.match('/wetty/ssh/.+$')) {
            //    sshuser = match[0].replace('/wetty/ssh/', '') + '@';
            // } else if (globalsshuser) {
            //    sshuser = globalsshuser + '@';
            // }
            //console.log('login : ', JSON.stringify(loginparam));
            var term;
            if (loginhost === 'localhost') {
            console.log('host : localhost');
            term = pty.spawn('/usr/bin/env', ['login'], {
                name: 'xterm-256color',
                cols: 80,
                rows: 30
            });
            } else {
            console.log('host : ', loginhost);
            if (logintype === 'ssh') {
                term = pty.spawn('E:\\DevelopTools\\Git\\usr\\bin\\ssh.exe ', [loginuser + '@' + loginhost, '-p', loginport, '-o', 'PreferredAuthentications=' + loginauth], {
                name: 'xterm-256color',
                cols: 80,
                rows: 30
                });
            } else if (logintype === 'telnet'){
                term = pty.spawn('telnet.exe ', [loginhost, loginport], {
                name: 'xterm-256color',
                cols: 80,
                rows: 30
                });
            }
            }
            
            console.log((new Date()) + " PID=" + term.pid + " STARTED on behalf of user=" + loginuser)
            term.on('data', function(data) {
            // console.log('term.on data: ', data);
            socket.emit('output', data);
            if (loginauto && loginauto.length > 0){
                let loginautoitem = loginauto[0];
                if (data.indexOf(loginautoitem['prompt']) >= 0) {
                console.log('login prompt: ',loginautoitem['prompt']);
                loginauto.splice(0,1);
                term.write(loginautoitem['answer']);
                
                }
            }
            });
            term.on('exit', function(code) {
                console.log('term.on exit: ', code);
                console.log((new Date()) + " PID=" + term.pid + " ENDED")
            });
            socket.on('resize', function(data) {
                console.log('socket.on resize resize: ', data);
                term.resize(data.col, data.row);
            });
            socket.on('input', function(data) {
                //console.log('socket.on input: ', data);
                term.write(data);
            });
            socket.on('disconnect', function() {
                console.log('socket.on disconnect: ');
                term._close();
                term.kill();
            });
            socket.on('connect_error', function() {
                console.log('socket.on connect_error: ');
                term._close();
                term.end();
            });
            socket.on('error', function() {
                console.log('socket.on error: ');
                term._close();
                term.end();
            });
        });
        socket.on('register', (hostparam) => {
            console.log(`client ${hostparam} register`);
            //setInterval( () => {
            //    console.log('interval 10000');
            //    socket.emit("message", "message from server");
            //}, 10000);
        });
    });
    return io;
}

const createInspectIOServer = function(server, path){
    var io = ioserver(server, {path: path, ws:true});
    io.on('connection', function(socket){
        console.log(`Inspector io connected port: ${JSON.stringify(socket)} ${server['ServerPort']}`);
        socket.on('login', function(loginparam){
            console.log('io login param:', JSON.stringify(loginparam));
        });
        socket.on('register', (message) => {
            console.log(`client ${message['id']} ${message['role']} register`);
            let id = message['id']
            io[id] = socket
            socket['socket_id'] = id
            if (message['role'] === 'backend'){
                console.log(`backend socket id: ${id}`)
                io['backend' ] = id;
            }
        });
        socket.on('front_message', (info) => {
            info['source_id'] = socket['socket_id']
            console.log(`Front to End:  ${JSON.stringify(info)} `);
            console.log(`End:  ${io['backend']} ${JSON.stringify(info)} `);
            if(io[io['backend']]){
                io[io['backend']].emit('message', info)
            }
        });
        socket.on('end_message', (info) => {
            console.log(`End to Front:  ${JSON.stringify(info)} `);
            if (info['source_id']) {
                if (io[info['source_id']])
                    io[info['source_id']].emit('message_'+info['cmd'], info)
            } 
        });
    });
    return io;
}

const createIOServer = function(server, path){
    var io = ioserver(server, {path: path});
    io.on('connection', function(socket){
        io['IOSocket'] == socket;
        console.log('io connected');
        socket.on('login', function(loginparam){
            console.log('io login param:', JSON.stringify(loginparam));
        });
        socket.on('register', (hostparam) => {
            console.log(`client ${hostparam} register`);
        });
    });
    return io;
}


var findNetElement = function(name, netelements){
  for (let netelement of netelements) {
    if (netelement['name'] === name) {
      return netelement;
    }
  }
  return null;
}

module.exports = socketServer;