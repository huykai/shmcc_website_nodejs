var express = require('express');
var path = require('path');
var bodyParser = require('body-parser');
var cookieParser = require('cookie-parser');
var csurf = require('csurf');
var session = require('express-session');
var methodOverride = require('method-override');
//var routes = require('./routes');
var site_config = require('./config/rtm/site_config');
var routers = require('./config/rtm/route_api');

var jwt = require('express-jwt');
var morgan  = require('morgan'); // logger
var tokenManager = require('./config/rtm/token_manager');
var secret = require('./config/rtm/secret');
var netelements = require('./config/rtm/netelementconfig.js');

const http = require('http');
const hostname = '10.222.5.38';
const port = 3000;

const ServerTimeout = 3600000;

var processOption = {
  env: {
    PORT : 3000
  }
}
var fs = require('fs');
var ejs = require('ejs');
var ioserver = require('socket.io');
var pty = require('node-pty');

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
module.exports = app; 

app.set('port', processOption.env.PORT || 3000);
app.set('views', __dirname + '/views');
app.engine('.html', ejs.__express);
app.set('view engine', 'html');

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

//app.post('/index_traffica.html', csrfProtection, function (req, res, next) {
//  console.log('/ Cookies: ', req.cookies);
//  var fileName = site_config.static_dir + req.url;
//  console.log(fileName);
//  //res.cookie.csrfToken = req.cookies.csrfToken;
// //res.locals._csrf = req.csrfToken();
//  //res.cookie('XSRF-TOKEN', req.csrfToken());
//  res.sendFile(fileName, function (err) {
//    if (err) {
//      next(err);
//    } else {
//      console.log('Sent:', fileName);
//    }
//  });
//});

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
//app.post('/user/register', urlencodedParser, routes.users.register); 
app.post('/user/register', urlencodedParser, routes.users.register); 

//Login
app.post('/user/signin', urlencodedParser, routes.users.signin); 

//Logout
app.get('/user/logout', jwt({secret: secret.secretToken}), routes.users.logout); 


//app.all('/api/*', urlencodedParser, csrfProtection, routers);
app.all('/api/*', urlencodedParser, routers);
//app.all('/api/*', routers);
//app.all('/api/*', function (req, res, next) {
//    routers.
//    if (err) {
//      next(err);
//    } else {
//      console.log('app.all is running');
//    }
//  });

//app.listen(3000, () => {
//  console.log(`App listening at port 3000`)
//})

//app.use(express.json()); 
//app.use(express.methodOverride()); 

//app.get('/pages', routes.pages.index); //<co id="callout-web-rest-1-3" />
//app.get('/pages/:id', routes.pages.show);
//app.post('/pages', routes.pages.create);
//app.patch('/pages/:id', routes.pages.patch);
//app.put('/pages/:id', routes.pages.update);
//app.del('/pages/:id', routes.pages.remove);

// error handler
app.use(function (err, req, res, next) {
  console.log("error code:",err.code);
  if (err.code !== 'EBADCSRFTOKEN') return next(err);
  //res.cookie('XSRF-TOKEN', req.csrfToken());
  // handle CSRF token errors here
  res.status(403);
  //console.log('req is: ',req.headers);
  //console.log('res is: ',res.headers);
  res.send('form tampered with');
});

var server = http.createServer(app).listen(app.get('port'),function() {
  console.log('Express server listening on port ' + app.get('port'));
});
server.timeout = ServerTimeout;
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

process.on('uncaughtException', function (err) {
  console.log('uncaughtException: ');
  console.error(err);
  server.close(); 
  setTimeout(process.exit, 5000, 1);
});

var io = ioserver(server,{path: '/hyktty/socket.io'});
io.on('connection', function(socket){
  console.log('io connected');
  socket.on('login', function(loginparam){
    console.log('io login param:', JSON.stringify(loginparam));
    let netelement = find(loginparam['name'], netelements);
    if (netelement == null) {
      console.log('netelement ', loginparam['name'], ' not found!');
      return;
    }

    var logintype = netelement.type || 'ssh';
    var loginuser = netelement.user || 'root' + '@';
    var loginhost = netelement.host || 'localhost';
    var loginport = netelement.port || '22';
    var loginauth = netelement.auth || 'password,keyboard-interactive';
    var loginauto = netelement.login || [];
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
        term = pty.spawn('ssh', [loginuser + '@' + loginhost, '-p', loginport, '-o', 'PreferredAuthentications=' + loginauth], {
          name: 'xterm-256color',
          cols: 80,
          rows: 30
        });
      } else if (logintype === 'telnet'){
        term = pty.spawn('telnet', [loginhost, loginport], {
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
});

var findNetElement = function(name, netelements){
  for (let netelement of netelements) {
    if (netelement['name'] === name) {
      return netelement;
    }
  }
  return null;
}

module.exports = {
  app: app,
  host: hostname,
  port: port
}