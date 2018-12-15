exports.env = {   
  env: {
    HTTP_PORT : 3000,
    HTTPS_PORT : 3010
  },
  site_config: {
    static_dir : "/root/huykai/node_webserver/angularjs_shmccps/app/",
    home_page : "index_v2.html",
    orig_home_page : "shmccps_main_v1_2.html"
  },
  mode: 'rtm',
  hostname: '10.222.5.38',
  ServerTimeout: 3600000,
  mongodbURL: 'mongodb://shmccps:shmccps@localhost:27017/shmccps',
  redisPort: 6379,
  secretToken: 'aMdoeb5ed87zorRdkD6greDML81DcnrzeSD648ferFejmplx',
  socketPort: 3100,
  inspectClient: {
    script: '/root/huykai/javascript_projects/IntelligentInspection/InspectWorker.js',
    args: [
      'yml/WorkerConfigRtm.yml'
    ]
  }
}
