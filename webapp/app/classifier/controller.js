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

var featureAveragesObj;
var songIdToPredictedPopularityObj = null;

/////////////////////
// Route Functions //
/////////////////////

// Spawn the two python processes
launchSendPopularUnpopularAverages();

// Given the raw feature values for a random Spotify song, classify its
// popularity by our classification algorithm
function classifyNewSongPost(req, res) {
  var songIdToFeaturesObj = {};
  songIdToFeaturesObj.artist_hotness = req.body.artist_popularity;
  songIdToFeaturesObj.duration = req.body.duration;
  songIdToFeaturesObj.key = req.body.key;
  songIdToFeaturesObj.loudness = req.body.loudness;
  songIdToFeaturesObj.mode = req.body.mode;
  songIdToFeaturesObj.tempo = req.body.tempo;
  songIdToFeaturesObj.tempoXkey = req.body.tempoXkey
  songIdToFeaturesObj.time_signature = req.body.time_signature;
  console.log("FUCKING OBJECT: " +JSON.stringify(songIdToFeaturesObj, null, 4));


  // Input must be in array
  classifyFeatures(songIdToFeaturesObj, res);
  // predictedSongPopularity = predictedSongPopularity[0];

  // Return this single value to the client
  // res.status(200).send(predictedSongPopularity);
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

  var songIdToFeaturesObj = {};
  for (var i = 0; i < results.length; i++) {
    var songId = results[i]['song_id'];
    delete(results[i]['song_id']);

    songIdToFeatures[songId] = results[i];
  }

  var songIdToPredictedPopularityObj = classifyFeatures(songIdToFeaturesObj);

  for (var songId in songIdToPredictedPopularityObj) {
    songIdToFeaturesObj[songId]['predicted_song_hotness'] = songIdToPredictedPopularityObj[songId];
  }

  res.status(200).send(songIdToFeaturesObj);
}

// Get the popular and unpopular averages for all classifier features
function featureAveragesGet(req, res) {
  res.status(200).send(featureAveragesObj);
}

//////////////////////
// Helper Functions //
//////////////////////

// songIdToFeaturesObj:
//   The actual object input to the Python ML Process
//   A map/object/dictionary where the keys are the song id
//     and the values are the corresponding features for said song, also an
//     object which maps the feature name to its corresponding raw value
function classifyFeatures(songIdToFeaturesObj, response) {

  var featuresArray = Object.keys(songIdToFeaturesObj).map(function (key) {
    return songIdToFeaturesObj[key];
  });

  console.log("features array: ");
  console.log(JSON.stringify(featuresArray));


  // Send the features to the process
  var filePath = __dirname + "/../../../scripts/send_classifier_output.py";
  // console.log("FILEPATH FOR classifier: " +filePath);
  var proc = spawn('python3',[filePath]);

  proc.stdin.write(JSON.stringify(featuresArray));
  proc.stdin.end();

  // Explain what to do when data is received from the process
  proc.stdout.on('data', function(data) {
    console.log("Received from send_classifier_output: \n" +data);
    response.status(200).send(data);
    });

  // Assign the output to variable 'classifierPopularity', as below:
  // var songIdToPredictedPopularityObj = {'song_id_1': 92.229, 'song_id_2': 28.393};

  // return songIdToPredictedPopularityObj;
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

function launchSendPopularUnpopularAverages() {
  var filePath = __dirname + "/../../../scripts/send_popular_unpopular.py";
  var proc = spawn('python3',[filePath]);
  proc.stdout.on('data', function(data) {
      // console.log("Received: \n" +data);
      featureAveragesObj = data;
    });
  }
