var join = require('path').join;

module.exports = {
  genrePageGet: genrePageGet
}

function genrePageGet(req, res) {
  console.log("in genrepageget");
  res.sendFile(join(__dirname, '../..', 'views', './genres.html'));
}
