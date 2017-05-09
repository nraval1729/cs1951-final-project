//  External dependencies
var Promise = require('bluebird');
var sqlite3 = require('sqlite3').verbose();

// path for database
var path = require('path');
var dbPath = path.resolve(__dirname, '..', 'database.db');

var db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY);
var spawn = require('child_process').spawn;

module.exports = {
  classifyNewSongPost: classifyNewSongPost,
  exploreSpotterPost: Promise.coroutine(exploreSpotterGenerator),
  featureAveragesGet: featureAveragesGet
}

/////////////////////
// Route Functions //
/////////////////////

// Given the raw feature values for a random Spotify song, classify its
// popularity by our classification algorithm
function classifyNewSongPost(req, res) {
  // Raw feature values from new Spotify song
  var newSongFeatures = {};
  newSongFeatures.artist_hotness = req.body.artistPopularity;
  newSongFeatures.duration = req.body.duration;
  newSongFeatures.key = req.body.key;
  newSongFeatures.loudness = req.body.loudness;
  newSongFeatures.mode = req.body.mode;
  newSongFeatures.tempo = req.body.tempo;
  newSongFeatures.time_signature = req.body.timeSignature;

  var songIdToFeaturesObj = {};
  songIdToFeaturesObj[songId] = newSongFeatures;

  // Input must be in array
  var predictedSongPopularity = classifyFeatures(songIdToFeaturesObj);
  predictedSongPopularity = predictedSongPopularity[0];

  // Return this single value to the client
  res.status(200).send(predictedSongPopularity);
}

function* exploreSpotterGenerator(req, res) {
  // Return a random dataset of size 'n'/'sampleSize'
  var n = req.body.sampleSize;

  var getNRandomRowsQuery =
    'SELECT song_id, \
            song_hotness, \
            artist_hotness, \
            duration, \
            key, \
            loudness, \
            mode, \
            tempo, \
            time_signature \
     FROM songs \
     ORDER BY RANDOM() \
     LIMIT (?);'
  var getNRandomRowsParams = [n];

  var results = yield* runSqlQuery(getNRandomRowsQuery, getNRandomRowsParams);

  var songIdToFeaturesArray = [];  
  for (var i = 0; i < results.length; i++) {
    var songId = results[i]['song_id'];
    delete(results[i]['song_id']);

    var songIdToFeatures = {};
    songIdToFeatures[songId] = results[i];

    songIdToFeaturesArray.push(songIdToFeatures);
  }

  var predictedPopularityArray = classifyFeatures(songIdToFeaturesArray);

  for (var songId in predictedPopularityArray) {

  }

  res.status(200).send();
}

// Get the popular and unpopular averages for all classifier features
function featureAveragesGet(req, res) {
  /* SPAWN PROCESS HERE: START */

  // The output from the Python process
  // Will be the stringified array of 2 JSON objects. The 0-index object will be the popular feature averages and the 1-index object will be the unpopular feature averages. Or vice-versa. Order doesn't really matter, just make sure it's documented.
  var featureAveragesStr = '{"popular": {"avg_song_hotness":0.4541682036148893,"avg_artist_hotness":0.4171302102545193,"avg_duration":247.54609482734062,"avg_key":5.33493175949834,"avg_loudness":-9.42896972448431,"avg_mode":0.6634508980506767,"avg_tempo":125.48716993445494,"avg_time_signature":3.6235848253553895}, "unpopular": {"avg_song_hotness":0.4541682036148893,"avg_artist_hotness":0.4171302102545193,"avg_duration":247.54609482734062,"avg_key":5.33493175949834,"avg_loudness":-9.42896972448431,"avg_mode":0.6634508980506767,"avg_tempo":125.48716993445494,"avg_time_signature":3.6235848253553895}}';

  // An important side note: make sure keys in the JSON string are surrounded by double-quote literals, else JSON.parse() will throw an error

  /* SPAWN PROCESS HERE: END */

  var featureAverages = JSON.parse(featureAveragesStr);

  res.status(200).send(featureAverages);
}

//////////////////////
// Helper Functions //
//////////////////////

// songIdToFeaturesObj: A map/object/dictionary where the keys are the song id
// and the values are the corresponding features for said song, also an object
// which maps the feature name to its corresponding raw value
function classifyFeatures(songIdToFeaturesObj) {
  // The actual stringified input to the Python ML Process
  var songIdToFeaturesObjStr = JSON.stringify(songIdToFeaturesObj);

  /* SPAWN PROCESS HERE: START */



  // Spawn the process here using the above stringified value as input.
  // Assign the output to variable 'classifierPopularity', as below:
  var songIdToPredictedPopularityObj = {'song_id_1': 92.229, 'song_id_2': 28.393};



  /* SPAWN PROCESS HERE: END */

  return songIdToPredictedPopularityObj;
}

function* runSqlQuery(query, params) {
  var statement = db.prepare(query);
  var results = yield sqlResults(statement, params);
  return results;
}

function sqlResults(statement, params) {
  return new Promise(function(resolve, reject) {
    statement.all(params, function(err, rows) {
      if (err) {
        return reject(err);
      } else {
        return resolve(rows);
      }
    });
  });
}
