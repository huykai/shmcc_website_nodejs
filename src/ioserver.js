'use strict';

var ioserver = require('socket.io');
var netelements = require('./config/netelementconfig');
var pty = require('node-pty');

const socketServer = function(server) {
    var io = ioserver(server, {path: '/hyktty/socket.io'});
    io.on('connection', function(socket){
        console.log('io connected');
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


var findNetElement = function(name, netelements){
  for (let netelement of netelements) {
    if (netelement['name'] === name) {
      return netelement;
    }
  }
  return null;
}

module.exports = socketServer;