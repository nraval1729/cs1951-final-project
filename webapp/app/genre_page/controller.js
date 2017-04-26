var join = require('path').join;

module.exports = {
  genrePageGet: genrePageGet
}

function genrePageGet(req, res) {
  res.sendFile(join(__dirname, '../..', 'views', './genres.html'));
}
