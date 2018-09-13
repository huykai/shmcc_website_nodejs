var express = require('express');
var path = require('path');
var bodyParser = require('body-parser');
var cookieParser = require('cookie-parser');
var csurf = require('csurf');
var session = require('express-session');
var methodOverride = require('method-override');
//var routes = require('./routes');
var site_config = require('./config/site_config');
var routers = require('./config/route_api');
var jwt = require('express-jwt');
var morgan  = require('morgan'); // logger
var tokenManager = require('./config/token_manager');
var secret = require('./config/secret');

var external_webs = require('./config/external_webs');
var external_webs_config = require('./config/external_webs_config');
var proxy = require('http-proxy-middleware');
var socketServer = require('./ioserver');

const http = require('http');
const https = require('https');
const hostname = '127.0.0.1';
const http_port = 3000;
const https_port = 3010;

const ServerTimeout = 3600000;

var processOption = {
  env: {
    HTTP_PORT : 3000,
    HTTPS_PORT : 3010
  }
}
var fs = require('fs');
var ejs = require('ejs');
var ioserver = require('socket.io');


//var privateKey  = fs.readFileSync(__dirname + '/sslcert/privatekey.pem', 'utf8');
//var certificate = fs.readFileSync(__dirname + '/sslcert/certificate.pem', 'utf8');
var privateKey  = fs.readFileSync(__dirname + '/sslcert/www.huykai.com.cn/3_huykai.com.cn.key', 'utf8');
var certificate = fs.readFileSync(__dirname + '/sslcert/www.huykai.com.cn/2_huykai.com.cn.crt', 'utf8');

var ssloptions = {
  key: privateKey,
  cert: certificate
}

var routes = {};
routes.posts = require('./route/posts.js');
routes.users = require('./route/users.js');
//routes.rss = require('./route/rss.js');

var csrfProtection = csurf({ cookie: true });

// create application/json parser
var jsonParser = bodyParser.json();
// create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({ extended: false });

var app = express();


app.set('http_port', processOption.env.HTTP_PORT || 3000);
app.set('https_port', processOption.env.HTTPS_PORT || 3010);
app.set('views', __dirname + '/views');
//app.engine('.ejs', ejs.__express);
app.set('view engine', 'ejs');

//app.use(express.static(path.join(__dirname, 'public')))
app.use(express.static(site_config.static_dir));
//console.log(site_config.static_dir);
//app.use(bodyParser());
app.use(urlencodedParser);

app.use(cookieParser('secret'));
//app.use(session({ secret: 'secret' }));
//app.use(methodOverride());
app.use(csurf({ cookie: true }));

app.use(function(req, res, next) {
  //console.log("app.use req.csrfToken(): ",req.csrfToken);
  res.cookie('XSRF-TOKEN', req.csrfToken());
  return next();
});

app.all('*', function(req, res, next) {
  console.log('app.all req is: ',req.url,req.method);
  //console.log('res is: ',res.headers);
  //console.log('all * Cookies: ', req.cookies);
  //console.log('Signed Cookies: ', req.signedCookies);
  res.set('Access-Control-Allow-Origin', '*');
  //res.set('Access-Control-Allow-Origin', 'http://192.168.1.126:3000');
  //res.set('Access-Control-Allow-Origin', '/index_traffica.html');
  res.set('Access-Control-Allow-Credentials', true);
  res.set('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT');
  res.set('Access-Control-Allow-Headers', 'X-CSRFToken, x-xsrf-token, X-Csrf-Token, X-Requested-With, Content-Type, Authorization');
  res.cookie('XSRF-TOKEN', req.csrfToken());
  if ('OPTIONS' == req.method) 
    
    return res.send(200);
  next();
});


app.get('/', csrfProtection, function (req, res, next) {
  console.log('/ Cookies: ', req.cookies);
  //console.log('Signed Cookies: ', req.signedCookies);
  var fileName = site_config.static_dir + site_config.home_page;
  console.log(fileName);
  //res.cookie.csrfToken = req.cookies.csrfToken;
  //res.locals._csrf = req.csrfToken();
  //res.cookie('XSRF-TOKEN', req.csrfToken());
  res.sendFile(fileName, function (err) {
    if (err) {
      next(err);
    } else {
      console.log('Sent:', fileName);
    }
  });
});




app.get('/orig', function (req, res, next) {
  var fileName = site_config.static_dir + site_config.orig_home_page;
  console.log(fileName);
  res.sendFile(fileName, function (err) {
    if (err) {
      next(err);
    } else {
      console.log('Sent:', fileName);
    }
  });
});

//app.use(bodyParser());

//Create a new user
app.post('/user/register', urlencodedParser, routes.users.register); 

//Login
app.post('/user/signin', urlencodedParser, routes.users.signin); 

//Logout
app.get('/user/logout', jwt({secret: secret.secretToken}), routes.users.logout); 

//ejs test
app.get('/ejs', (req, res, next) => {
  res.render('index', {page:'Home', menuId:'home'})
}); 


//app.all('/api/*', urlencodedParser, csrfProtection, routers);
// /api/* mean routers for api
app.all('/api/*', urlencodedParser, routers);
// /informationbrowser/index.jsp
//app.all('/webs/*', urlencodedParser, external_webs);
app.all('/*', urlencodedParser, external_webs);



// error handler
app.use(function (err, req, res, next) {
  console.log("error code:",err.code);
  console.log("app req.cookies:",req.cookies);
  console.log("app req.headers:",req.headers);
  if (err.code !== 'EBADCSRFTOKEN') return next(err);
  //res.cookie('XSRF-TOKEN', req.csrfToken());
  // handle CSRF token errors here
  res.status(403);
  //console.log('req is: ',req.headers);
  //console.log('res is: ',res.headers);
  res.send('form tampered with');
});

var http_server = http.createServer(app).listen(app.get('http_port'),function() {
  console.log('Express http server listening on port ' + app.get('http_port'));
});

http_server.timeout = ServerTimeout;

var https_server = https.createServer(ssloptions, app).listen(app.get('https_port'),function() {
  console.log('Express https server listening on port ' + app.get('https_port'));
});

https_server.timeout = ServerTimeout;

process.on('uncaughtException', function (err) {
  console.log('uncaughtException: ');
  console.error(err);
  http_server.close(); 
  https_server.close(); 
  setTimeout(process.exit, 5000, 1);
});

const socket_httpServer = socketServer(http_server);
const socket_httpsServer = socketServer(https_server);

var io = require('socket.io')(http_server);
io.on('connection', function(socket){
  console.log('a user connected.');
  socket.on('disconnected', function(){
    console.log('user disconnected.');
  });
  //socket.on('add-message', (message) => {
    //setTimeout(function(){
    //  let data = [
    //    ['Evolution', 'Imports', 'Exports'],
    //    ['A ' + message, Math.round(Math.random()*10000), Math.round(Math.random()*10000)],
    //    ['B ' + message, Math.round(Math.random()*10000), Math.round(Math.random()*10000)],
    //    ['C ' + message, Math.round(Math.random()*10000), Math.round(Math.random()*10000)]
    //  ];
    //  io.emit(message, {type:'new-message', text: data});    
  //  },10000);
    
  //});
  //let count = 0;
  //setInterval(()=>{count++; socket.emit('message',count)},1000);
})

module.exports = {
  app: app,
  host: hostname,
  http_port: http_port,
  https_port: https_port
}