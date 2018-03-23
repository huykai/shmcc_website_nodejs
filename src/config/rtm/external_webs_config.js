'use strict';

var external_webs_config = [
    {
        url_string: '/angular/webs/ned/index.jsp', 
        options: {
            target: 'http://172.20.24.252:9090',
            changeOrigin: true,               // needed for virtual hosted sites
            ws: true,                         // proxy websockets
            pathRewrite: {
                '^/angular/webs/ned/index.jsp' : '/informationbrowser/index.jsp',     // rewrite path
                // '^/api/remove/path' : '/path'           // remove base path
            },
            router: {
                // when request.headers.host == 'dev.localhost:3000',
                // override target 'http://www.example.org' to 'http://localhost:8000'
                // 'dev.localhost:3000' : 'http://localhost:8000'
            }
        }
    },
    {
        url_string: '/angular/webs/ned/*', 
        options: {
            target: 'http://172.20.24.252:9090',
            // changeOrigin: true,               // needed for virtual hosted sites
            // ws: true,                         // proxy websockets
            pathRewrite: {
                '^/angular/webs/ned/' : '/informationbrowser/',
                // '^/api/remove/path' : '/path'           // remove base path
            }
            // router: {
                // when request.headers.host == 'dev.localhost:3000',
                // override target 'http://www.example.org' to 'http://localhost:8000'
                // 'dev.localhost:3000' : 'http://localhost:8000'
            // }
        }
    },
    {
        url_string: '/angular/webs/fma', 
        options: {
            target: 'http://10.10.31.19:8080',
            changeOrigin: true,               // needed for virtual hosted sites
            ws: true,                         // proxy websockets
            pathRewrite: {
                '^/angular/webs/fma/login.xhtml' : '/FMANS17/login.xhtml',     // rewrite path
                // '^/api/remove/path' : '/path'           // remove base path
            },
            router: {
                // when request.headers.host == 'dev.localhost:3000',
                // override target 'http://www.example.org' to 'http://localhost:8000'
                // 'dev.localhost:3000' : 'http://localhost:8000'
            }
        }
    },
    {
        url_string: '/angular/FMANS17/*', 
        options: {
            target: 'http://10.10.31.19:8080',
            // changeOrigin: true,               // needed for virtual hosted sites
            // ws: true,                         // proxy websockets
            pathRewrite: {
                // '^/FMANS17/' : '/FMANS17/',     // rewrite path
                // '^/api/remove/path' : '/path'           // remove base path
            },
            router: {
                // when request.headers.host == 'dev.localhost:3000',
                // override target 'http://www.example.org' to 'http://localhost:8000'
                // 'dev.localhost:3000' : 'http://localhost:8000'
            }
        }
    }
]

module.exports = external_webs_config;
