// External dependencies
var express = require('express');

// Local dependencies
var controller = require('./controller');

// Router object
var router = express.Router();

router.route('/')
  .post(controller.genreData);

module.exports = router;
