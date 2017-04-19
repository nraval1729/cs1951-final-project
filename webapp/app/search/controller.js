//  External dependencies
var sqlite3 = require('sqlite3').verbose();

// path for database
var path = require('path');
var dbPath = path.resolve(__dirname, '..', 'database.db')

var db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY);

// Constants
var SEARCH_SIZE = 5;

module.exports = {
  searchPost: searchPost
}

function searchPost(req, res) {
  var search = req.body.search; // frontend should pass the user's search as a 'search' parameter
  db.serialize(function() {
    search += '%'
    var sqlParams = [search, SEARCH_SIZE];
      
    var sqlQuery = "SELECT song_id, song_name, artist_name \
    FROM songs NATURAL JOIN artists \
    WHERE song_name LIKE ? \
    ORDER BY spotify_song_popularity DESC \
    LIMIT (?)";
    var sqlStatement = db.prepare(sqlQuery);
    var results = sqlStatement.all(sqlParams, function(err, rows){
      if (err) {
        console.log(err);
      } else {
        console.log(rows);
        res.status(200).send(rows);
      }
    });
    //console.log(results);

    return results;

    /*db.all(query, [search, SEARCH_SIZE], function(err, rows) {
      console.log('3', rows);
      return rows;
      res.status(200).send('bleh blah bloo');
    });*/
    // var results = db.run(query, [search, SEARCH_SIZE]);
    //res.status(200).send('asdf');
  });
}
