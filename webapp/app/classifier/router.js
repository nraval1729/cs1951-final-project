// External dependencies
var express = require('express');

// Local dependencies
var controller = require('./controller');

// Router object
var router = express.Router();

router.route('/classifyNewSong')
  .post(controller.classifyNewSongPost);

router.route('/exploreSpotter')
  .post(controller.exploreSpotterPost);

router.route('/featureAverages')
  .get(controller.featureAveragesGet)

module.exports = router;
