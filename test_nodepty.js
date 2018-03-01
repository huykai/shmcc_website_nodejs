var os = require('os');
var pty = require('node-pty');

var shell = os.platform() === 'win32' ? 'powershell.exe' : 'telnet';

var ptyProcess = pty.spawn(shell, ['172.20.13.28', '23'], {
  name: 'xterm-color',
  cols: 80,
  rows: 30,
  cwd: process.env.HOME,
  env: process.env
});

ptyProcess.on('data', function(data) {
  console.log(data);
});

ptyProcess.write('ZUSI;\r');
ptyProcess.resize(100, 40);
ptyProcess.write('ZUSI;\r');
