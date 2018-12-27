// argument should include 
// runmode: 'rtm' for run in rtm environment
// runmode: 'test' for run in test(development) environment
// use process.env will be a better way
//const mode = process.argv[2] || 'test'; //'rtm' or 'test'
console.log('Run Mode: ', process.env.shmccpsmode);
let modedir = (!process.env.shmccpsmode || process.env.shmccpsmode === 'test') ? '':process.env.shmccpsmode + '/'
console.log(`modedir: ${modedir}`)
var processOption = require(`./config/${modedir}processoption`)
console.log(`processOption.env: ${JSON.stringify(processOption.env)}`)
process.shmccpsenv = processOption;
var express = require('express');
var bodyParser = require('body-parser');
var cookieParser = require('cookie-parser');
var csurf = require('csurf');
var site_config = require(`./config/${modedir}site_config`);
var routers = require(`./config/${modedir}route_api`);
var jwt = require('express-jwt');
var secret = require(`./config/${modedir}secret`);
var fs = require('fs');

var external_webs = require(`./config/${modedir}external_webs`);
//var socketIOServer = require('./socketioserver');
var socketIOServer = require('./ioserver');

const http = require('http');
const hostname = processOption.env.hostname;
const ServerTimeout = processOption.env.ServerTimeout;

var routes = {};
routes.posts = require('./route/posts_v2.js');
routes.users = require('./route/users_v2.js');

var csrfProtection = csurf({ cookie: true });

// create application/json parser
var jsonParser = bodyParser.json();
// create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({ extended: false });
console.log(`app_v2 process.env.NODE_APP_INSTANCE: ${process.env.NODE_APP_INSTANCE}`)
process.env.NODE_APP_INSTANCE = process.env.NODE_APP_INSTANCE  || "1"
let socketPort = processOption.env.socketPort + parseInt(process.env.NODE_APP_INSTANCE);
//let httpssocketPort = processOption.env.httpssocketPort + parseInt(process.env.NODE_APP_INSTANCE);

var app = express();
//app.set('http_port', processOption.env.env.HTTP_PORT || 3000);
//app.set('https_port', processOption.env.env.HTTPS_PORT || 3010);
app.set('views', __dirname + '/views');
//app.engine('.ejs', ejs.__express);
app.set('view engine', 'ejs');

app.use(express.static(site_config.static_dir));
console.log(`Static Directory: ${processOption.env.site_config.static_dir}`);
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
  console.log('all * Cookies: ', req.cookies);
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
  console.log(`Server with port: ${socketPort}`)
  //console.log('Signed Cookies: ', req.signedCookies);
  var fileName = processOption.env.site_config.static_dir + site_config.home_page;
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


// app.all('/api/*', urlencodedParser, csrfProtection, routers);
// /api/* mean routers for api
app.all('/api/*', urlencodedParser, routers);
// /informationbrowser/index.jsp
// app.all('/webs/*', urlencodedParser, external_webs);
// /webs/* 原来是为了支持代理功能，可以转发到其他网页，现在觉得nginx更理想，所以暂时不考虑继续使用
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
  res.send('EBADCSRFTOKEN');
});

var http_server = http.createServer(app).listen(socketPort,function() {
  console.log('Express http server listening on port ' + socketPort);
});
http_server['ServerPort'] = socketPort;
http_server.timeout = ServerTimeout;

process.on('uncaughtException', function (err) {
  console.log('uncaughtException: ');
  console.error(err);
  http_server.close(); 
  setTimeout(process.exit, 5000, 1);
});

console.log(`socketio server port: ${socketPort}`)
let ttypath = '/hyktty/socket.io';
const tty_socket_httpServer = socketIOServer(http_server, ttypath);
let inspectorpath = '/inspector/socket.io';
const inspector_socket_httpServer = socketIOServer(http_server, inspectorpath, processOption);

module.exports = {
  app: app,
  host: hostname,
  http_port: processOption.env.env.HTTP_PORT
}
