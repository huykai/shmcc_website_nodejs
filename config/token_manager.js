var redisClient = require('./redis_database').redisClient;
var TOKEN_EXPIRATION = 60;
var TOKEN_EXPIRATION_SEC = TOKEN_EXPIRATION * 60;

// Middleware for token verification
exports.verifyToken = function (req, res, next) {
	var token = getToken(req.headers);

	redisClient.get(token, function (err, reply) {
		if (err) {
			console.log(err);
			return res.send(500);
		}

		if (reply) {
			console.log('reply', JSON.stringify(reply));
			res.send(401);
		}
		else {
			next();
		}

	});
};

exports.checkToken = function (req, res, next) {
	var token = getToken(req.headers);
	console.log('checkToken: ', token);
	redisClient.get(token, function (err, reply) {
		if (err) {
			console.log('redisClient.get err', err);
			return res.send(500);
		};
		if (!reply) {
			console.log('redisClient.get reply null');
			//if (req.user) delete req.user;
			//res.status(401).send('nok');
			//redisClient.expire(req.headers, TOKEN_EXPIRATION_SEC);
			//delete req.user;
			//res.headers.authorization = null;	
			res.set('Content-Type', 'text/xml');
            res.status(401).send('<error>token</error>');
			return;
			
		};
		//redisClient.set(token, { is_expired: false });
    	redisClient.expire(token, TOKEN_EXPIRATION_SEC);
		next(req, res);
	});
};


exports.setTokenExpire = function(token,expire_timer) {
	if (token != null) {
		redisClient.set(token, { is_expired: false });
    	//redisClient.expire(token, TOKEN_EXPIRATION_SEC);
		redisClient.expire(token, expire_timer);
	}
};

exports.expireToken = function(headers) {
	var token = getToken(headers);
	
	if (token != null) {
		//redisClient.set(token, { is_expired: true });
    	//redisClient.expire(token, TOKEN_EXPIRATION_SEC);
		redisClient.expire(token, TOKEN_EXPIRATION_SEC);
	}
};

var getToken = function(headers) {
	if (headers && headers.authorization) {
		var authorization = headers.authorization;
		var part = authorization.split(' ');

		if (part.length == 2) {
			var token = part[1];

			return part[1];
		}
		else {
			return null;
		}
	}
	else {
		return null;
	}
};

exports.TOKEN_EXPIRATION = TOKEN_EXPIRATION;
exports.TOKEN_EXPIRATION_SEC = TOKEN_EXPIRATION_SEC;