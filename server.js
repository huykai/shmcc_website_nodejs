const http = require('http');
var app = require('./app');
var domain = require('domain');

const hostname = '127.0.0.1';
const port = 3000;

var d = domain.create();

//const server = http.createServer((req, res) => {
//  res.statusCode = 200;
//  res.setHeader('Content-Type', 'text/plain');
//  res.end('Hello World\n');
//});
d.run( function(){
  const server = http.createServer(app).listen(app.get('port'),function() {
    console.log('Express server listening on port ' + app.get('port'));
    
  });


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