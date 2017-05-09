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
  featureAveragesGet: Promise.coroutine(featureAveragesGet)
}

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

  // The actual stringified input to the Python ML Process
  var featuresInputToPythonProcess = JSON.stringify(newSongFeatures);

  /* SPAWN PROCESS HERE: START */
  // Spawn the process here using the above stringified value as input.
  // Assign the output to variable 'classifierPopularity', as below:
  var classifierPopularity = 0;
  /* SPAWN PROCESS HERE: END */

  // Return this single value to the client
  res.status(200).send(classifierPopularity);
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

  res.status(200).send(results);
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

// Get the popular and unpopular averages for all classifier features
function* featureAveragesGet(req, res) {
  var actualAverages = yield* getActualAverages();
  actualAverages = actualAverages[0]; // what we want is nested in another array

  var predictedAverages = getPredictedAverages();

  res.status(200).send([actualAverages, predictedAverages]);
}

function* getActualAverages() {
  var getActualAveragesQuery =
    'SELECT AVG(song_hotness) AS avg_song_hotness, \
            AVG(artist_hotness) AS avg_artist_hotness, \
            AVG(duration) AS avg_duration, \
            AVG(key) AS avg_key, \
            AVG(loudness) AS avg_loudness, \
            AVG(mode) AS avg_mode, \
            AVG(tempo) AS avg_tempo, \
            AVG(time_signature) AS avg_time_signature \
     FROM songs;';

  return yield* runSqlQuery(getActualAveragesQuery);
}

function getPredictedAverages() {
  /* SPAWN PROCESS HERE: START */



  // The output from the Python process
  // Will be the stringified array of 2 JSON objects. The 0-index object will be the popular feature averages and the 1-index object will be the unpopular feature averages. Or vice-versa. Order doesn't really matter, just make sure it's documented.
  var predictedAveragesStr = '{"avg_song_hotness":0.4541682036148893,"avg_artist_hotness":0.4171302102545193,"avg_duration":247.54609482734062,"avg_key":5.33493175949834,"avg_loudness":-9.42896972448431,"avg_mode":0.6634508980506767,"avg_tempo":125.48716993445494,"avg_time_signature":3.6235848253553895}';

  // An important side note: make sure keys in the JSON string are surrounded by double-quote literals, else JSON.parse() will throw an error



  /* SPAWN PROCESS HERE: END */

  var predictedAveragesJson = JSON.parse(predictedAveragesStr);

  return predictedAveragesJson;
}
