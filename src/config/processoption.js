exports.env = {   
  env: {
    HTTP_PORT : 3000,
    HTTPS_PORT : 3010
  },
  site_config: {
    static_dir : "E:\\Personal_Projects\\Code_Projects\\javascript\\AngularJS\\shmccps_angularjs\\app\\",
    home_page : "index_v2.html",
    orig_home_page : "shmccps_main_v1_2.html"
  },
  mode: 'test',
  hostname: '127.0.0.1',
  ServerTimeout: 3600000,
  mongodbURL: 'mongodb://shmccps:shmccps@localhost:27017/shmccps',
  redisPort: 6379,
  secretToken: 'aMdoeb5ed87zorRdkD6greDML81DcnrzeSD648ferFejmplx',
  socketPort: 3100,
  inspectClient: {
    script: 'E:\\Personal_Projects\\Code_Projects\\javascript\\NodeJS\\intelligentinspection\\InspectWorker.js',
    args: [
      'yml/WorkerConfig.yml'
    ]
  }
}
