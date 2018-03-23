var express = require('express');
var external_webs = express.Router();
var proxy = require('http-proxy-middleware');
var external_webs_config = require('./external_webs_config');

for (var external_web_config of external_webs_config) {
    let url_string = external_web_config.url_string;
    let options = external_web_config.options;
    // console.log('url_string: ', url_string);
    // console.log('options: ', options);
    let webProxy = proxy(options);
    external_webs.get(url_string, webProxy);
}



module.exports = external_webs;
