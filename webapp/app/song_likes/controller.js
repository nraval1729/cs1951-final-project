//  External dependencies
var sqlite3 = require('sqlite3').verbose();

// path for database
var path = require('path');
var dbPath = path.resolve(__dirname, '..', 'database.db')

var db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY);

// // Constants
// var SEARCH_SIZE = 5;

module.exports = {
  searchSongLikes: searchSongLikes
}

function searchSongLikes(req, res) {
  var songId = req.body.songId; // frontend should pass the user's search as a 'songId' parameter
  console.log("songId = " + songId);
  db.serialize(function() {
    var sqlParams = [songId];
    var sqlQuery = 'SELECT COUNT(*) AS likes, creation_date, jams_of_this_song.jam_id \
                    FROM \
                      ( \
                      SELECT jam_id, creation_date \
                      FROM jams \
                      WHERE song_id = ? \
                      ) jams_of_this_song \
                    JOIN \
                    LIKES \
                    ON likes.jam_id = jams_of_this_song.jam_id \
                    GROUP BY creation_date';
    var sqlStatement = db.prepare(sqlQuery);
    var results = sqlStatement.all(sqlParams, function(err, rows){
      if (err) {
        console.log(err);
      } else {
        console.log(rows);

        res.status(200).send(rows);
      }
    });
  });
}
