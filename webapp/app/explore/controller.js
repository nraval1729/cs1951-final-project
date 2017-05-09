var join = require('path').join;

module.exports = {
  exploreGet: exploreGet
}

function exploreGet(req, res) {
  res.sendFile(join(__dirname, '../..', 'views', './explore.html'));
}
