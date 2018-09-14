'use strict';

var external_webs_config = [
    {
        url_string: '/webs/ned/index.jsp', 
        options: {
            target: 'http://172.20.24.250:9090',
            // target: 'http://172.20.24.250:9090',
            changeOrigin: true,               // needed for virtual hosted sites
            ws: true,                         // proxy websockets
            pathRewrite: {
                '^/webs/ned/index.jsp' : '/informationbrowser/index.jsp',     // rewrite path
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
        url_string: '/webs/ned/*', 
        options: {
            target: 'http://172.20.24.250:9090',
            // target: 'http://172.20.24.250:9090',
            // changeOrigin: true,               // needed for virtual hosted sites
            // ws: true,                         // proxy websockets
            pathRewrite: {
                '^/webs/ned/' : '/informationbrowser/',
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
        url_string: '/webs/fma/login.xhtml', 
        options: {
            // target: 'http://localhost:51018',
            target: 'http://10.10.31.19:8080',
            changeOrigin: true,               // needed for virtual hosted sites
            ws: true,                         // proxy websockets
            pathRewrite: {
                '^/webs/fma/login.xhtml' : '/FMANS17/login.xhtml',     // rewrite path
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
        url_string: '/FMANS17/*', 
        options: {
            // target: 'http://localhost:51018',
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
    },
    {
        url_string: '/webs/ICES', 
        options: {
            target: 'http://10.222.5.35:8888',
            // target: 'http://localhost:3000',
            // changeOrigin: true,               // needed for virtual hosted sites
            // ws: true,                         // proxy websockets
            pathRewrite: {
                '^/webs/ICES' : '/epc-ices/',     // rewrite path
            //    // '^/api/remove/path' : '/path'           // remove base path
            },
            //router: {
                // when request.headers.host == 'dev.localhost:3000',
                // override target 'http://www.example.org' to 'http://localhost:8000'
            //    '/webs/ICES' : 'http://localhost:51150/epc-ices'
            //}
        }
    },
    {
        url_string: '/epc-ices/*', 
        options: {
            // target: 'http://localhost:51018',
            target: 'http://10.222.5.35:8888',
            changeOrigin: true,               // needed for virtual hosted sites
            // ws: true,                         // proxy websockets
            //pathRewrite: {
            //    '^/epc-ices' : '/epc-ices',     // rewrite path
                // '^/api/remove/path' : '/path'           // remove base path
            //},
            //router: {
                // when request.headers.host == 'dev.localhost:3000',
                // override target 'http://www.example.org' to 'http://localhost:8000'
                // 'http://localhost:3000' : 'http://localhost:51150'
            //}
        }
    }
]

module.exports = external_webs_config;
