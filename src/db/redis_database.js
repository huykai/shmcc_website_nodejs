var redis = require('redis');
console.log(`process.shmccpsenv.env.redisport: ${process.shmccpsenv.env.redisPort}`)
var redisClient = redis.createClient(process.shmccpsenv.env.redisPort || 6379);

redisClient.on('error', function (err) {
    console.log('Error ' + err);
});

redisClient.on('connect', function () {
    console.log('Redis is ready');
});

exports.redis = redis;
exports.redisClient = redisClient;