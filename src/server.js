const http = require('http');
const app = require('./app');
const domain = require('domain');

const hostname = '127.0.0.1';
const port = 3000;

const ServerTimeout = 600000;

const d = domain.create();

//const server = http.createServer((req, res) => {
//  res.statusCode = 200;
//  res.setHeader('Content-Type', 'text/plain');
//  res.end('Hello World\n');
//});
d.run( function(){
  var server = http.createServer(app).listen(app.get('port'),function() {
    console.log('Express server listening on port ' + app.get('port'));
  });
  server.timeout = ServerTimout;
  var io = require('socket.io')(server);
  io.on('connection', function(socket){
    console.log('a user connected.');
    socket.on('disconnected', function(){
      console.log('user disconnected.');
    });
    socket.on('add-message', (message) => {
      setTimeout(function(){
        let data = [
          ['Evolution', 'Imports', 'Exports'],
          ['A ' + message, Math.round(Math.random()*10000), Math.round(Math.random()*10000)],
          ['B ' + message, Math.round(Math.random()*10000), Math.round(Math.random()*10000)],
          ['C ' + message, Math.round(Math.random()*10000), Math.round(Math.random()*10000)]
        ];
        io.emit(message, {type:'new-message', text: data});    
      },10000);
      
    });
    //let count = 0;
    //setInterval(()=>{count++; socket.emit('message',count)},1000);
  })
})

//server.listen(port, hostname, () => {
//server.listen(port, hostname, () => {
//  console.log(`Server running at http://${hostname}:${port}/`);
//});


process.on('uncaughtException', function (err) {
  console.log('uncaughtException: ');
  console.error(err);
  server.close(); 
  setTimeout(process.exit, 5000, 1);
});

module.exports = {
  host: hostname,
  port: port
}