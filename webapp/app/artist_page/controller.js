var join = require('path').join;

module.exports = {
  artistPageGet: artistPageGet
}

function artistPageGet(req, res) {
  res.sendFile(join(__dirname, '../..', 'views', './artists.html'));
}
