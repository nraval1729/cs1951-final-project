var join = require('path').join;

module.exports = {
  homeGet: homeGet
}

function homeGet(req, res) {
  res.sendFile(join(__dirname, '../..', 'views', './home.html'));
}
