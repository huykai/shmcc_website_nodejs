//var db = require('../config/mongo_database');
var db = require('../db/mongo_database');
var jwt = require('jsonwebtoken');
var tokenManager = require('./token_manager_v2');

var secret = process.shmccpsenv.env;

var TOKEN_EXPIRATION = 480;
var TOKEN_EXPIRATION_SEC = TOKEN_EXPIRATION * 60;

exports.signin = function(req, res) {
	var username = req.body.username || '';
	var password = req.body.password || '';
	
	//console.log('signin User Cookies: ', req.cookies);
    //console.log('signin Signed Cookies: ', req.signedCookies);
	//console.log('req:',req);
	//console.log('user:',username);
	//console.log('pwd:',password);
	//console.log('url:',req.url);
	if (username == '' || password == '') {
        console.log("User loging user: null.");
		return res.send(401); 
	}

	db.userModel.findOne({username: username}, function (err, user) {
		if (err) {
            console.log("User loging err: ", err);
			return res.send(401);
		}

		if (user == undefined) {
        	console.log("User loging user: undefined.");
			return res.send(401);
		}
		//console.log(`findOne user: ${user}`)
		user.comparePassword(password, function(isMatch) {
			if (!isMatch) {
				console.log("Attempt failed to login with " + user.username);
				return res.sendStatus(401);
            }
			console.log("user password matched.")
			//var token = jwt.sign({id: user._id}, secret.secretToken, { expiresInMinutes: tokenManager.TOKEN_EXPIRATION });
			var token = jwt.sign({id: user._id}, secret.secretToken, { expiresIn: tokenManager.TOKEN_EXPIRATION_SEC });
			
			tokenManager.setTokenExpire(token, tokenManager.TOKEN_EXPIRATION_SEC);
			//console.log("signin: token get:",token)
			//res.set();
			//res.type('application/json');
			//return res.status(200);
			return res.status(200).json({
				token: token, 
				is_admin: user.is_admin
			});
		});

	});
};

exports.logout = function(req, res) {
	if (req.user) {
		//console.log('req.user:',req.user);
		//console.log('req.headers.authorization',req.headers.authorization);
		tokenManager.expireToken(req.headers);
		//console.log(req.user);
		delete req.user;	
		return res.send(200);
	}
	else {
		return res.send(401);
	}
}

exports.register = function(req, res) {
	var username = req.body.username || '';
	var password = req.body.password || '';
	var passwordConfirmation = req.body.passwordConfirmation || '';

	if (username == '' || password == '' || password != passwordConfirmation) {
		return res.send(400);
	}

	var user = new db.userModel();
	user.username = username;
	user.password = password;
	console.log(`register: user ${user.username}`);
	user.save(function(err) {
		if (err) {
			console.log(err);
			return res.send(500);
		}	
		
		db.userModel.count(function(err, counter) {
			if (err) {
				console.log(err);
				return res.send(500);
			}

			if (counter == 1) {
				db.userModel.update({username:user.username}, {is_admin:true}, function(err, nbRow) {
					if (err) {
						console.log(err);
						return res.send(500);
					}

					console.log('First user created as an Admin');
					return res.send(200);
				});
			} 
			else {
				return res.send(200);
			}
		});
	});
}
