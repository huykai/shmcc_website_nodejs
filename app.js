var express = require('express');
var path = require('path')
var bodyParser = require('body-parser');
var cookieParser = require('cookie-parser');
var csurf = require('csurf');
var session = require('express-session');
var methodOverride = require('method-override');
//var routes = require('./routes');
var site_config = require('./config/site_config');
var routers = require('./config/route_api');
var fs = require('fs');
var ejs = require('ejs');

module.exports = app = express();

app.set('port', process.env.PORT || 3000);
app.set('views', __dirname + '/views');
app.engine('.html', ejs.__express);
app.set('view engine', 'html');

//app.use(express.static(path.join(__dirname, 'public')))
app.use(express.static(site_config.static_dir));
app.use(bodyParser());
app.use(cookieParser('secret'));
app.use(session({ secret: 'secret' }));
app.use(methodOverride());
app.use(csurf());

app.get('/', function (req, res, next) {
  var fileName = site_config.static_dir + site_config.home_page;
  //console.log(fileName);
  res.sendFile(fileName, function (err) {
    if (err) {
      next(err);
    } else {
      console.log('Sent:', fileName);
    }
  });
});

app.all('/api/*', routers);
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
