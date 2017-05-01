//  External dependencies
var sqlite3 = require('sqlite3').verbose();

// path for database
var path = require('path');
var dbPath = path.resolve(__dirname, '..', 'database.db')

var db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY);

// // Constants
// var SEARCH_SIZE = 5;

module.exports = {
  genreData: genreData
}

// Pass in a span of years
function genreData(req, res) {
  var beginYear = parseInt(req.body.beginYear);
  var endYear = beginYear + 10;
  // add 5 to beginning year, or make this parameterizable

  db.serialize(function() {
    var sqlParams = [beginYear, endYear];
    console.log(sqlParams)
    var sqlQuery = 'SELECT song_hotness, artist_mbtags, release_year \
                    FROM songs WHERE CAST(release_year AS INT) > ? AND CAST(release_year AS INT) < ?;'
    var sqlStatement = db.prepare(sqlQuery);
    var results = sqlStatement.all(sqlParams, function(err, rows){
      if (err) {
        console.log(err);
      } else {
        res.status(200).send(rows);
      }
    });
    return results;
  });
}
