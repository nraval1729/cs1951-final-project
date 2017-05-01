// https://github.com/youngrrrr/ardios/blob/master/routes/index.js

var buffer = require('buffer');
var request = require('request');
var join = require('path').join;
var keys = require('../../private/keys.js');

var Promise = require('bluebird');

var SPOTIFY_ID = '003d9ea869764a3fa7e4c1a3e10b1c86';
var SPOTIFY_SECRET = keys.SPOTIFY_SECRET; //Private

module.exports = {
  accessTokenGet: Promise.coroutine(accessTokenGenerator)
}

function* accessTokenGenerator(req, res) {
  var authorizationVal = 'Basic ' + new Buffer(SPOTIFY_ID + ':' + SPOTIFY_SECRET).toString('base64');
  var postRequestOptions = {};

  postRequestOptions = {
    url: 'https://accounts.spotify.com/api/token',
    headers: {
      'Authorization': authorizationVal
    },
    form: {
      'grant_type': 'client_credentials'
    }
  };

  var token = yield getSpotifyAccessToken(postRequestOptions);

  res.status(200).send(token);
}

function getSpotifyAccessToken(postRequestOptions) {
  return new Promise(function(resolve, reject) {
    request.post(postRequestOptions, function(err, res, body) {
      if (err) {
        reject(err);
        return;
      }

      var parsedBody = JSON.parse(body);
      resolve(parsedBody.access_token);
    });
  });
}