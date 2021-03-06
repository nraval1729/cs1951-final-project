// External dependencies
var express = require('express');

// Local dependencies
var controller = require('./controller');

// Router object
var router = express.Router();

router.route('/')
  .get(controller.artistPageGet);

module.exports = router;
