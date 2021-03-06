//  External dependencies
var bodyParser = require('body-parser');
var cookieParser = require('cookie-parser');
var express = require('express');
var join = require('path').join;
var logger = require('morgan');
var path = require('path');

//  Local dependencies
//    Routers
var artistDataRouter = require('./artist_data/router');
var artistPageRouter = require('./artist_page/router');
var authenticateRouter = require('./authenticate/router');
var classifierRouter = require('./classifier/router');
var exploreRouter = require('./explore/router');
var genrePageRouter = require('./genre_page/router');
var genreDataRouter = require('./genre_data/router');
var homeRouter = require('./home/router');

// Constants
var PORT = 1337;

var app = express();





/******************************************
 *                                        *
 *              0. Services               *
 *                                        *
 ******************************************/





/******************************************
 *                                        *
 *     1. Application-wide middleware     *
 *                                        *
 ******************************************/

//  set up views
app.use(express.static(join(__dirname, '..', 'views')));
app.use(express.static(join(__dirname, '..', 'public')));
app.use(bodyParser.json());       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));

//  logging middleware
app.use(logger('dev'));



/******************************************
 *                                        *
 *  2. Routes and associated middlewares  *
 *                                        *
 ******************************************/

// use modularized routers
app.use('/', homeRouter);
app.use('/artists', artistPageRouter);
app.use('/artistsData', artistDataRouter);
app.use('/authenticate', authenticateRouter);
app.use('/classifier', classifierRouter);
app.use('/explore', exploreRouter);
app.use('/genres', genrePageRouter);
app.use('/genreData', genreDataRouter);

/******************************************
 *                                        *
 *           3. Error handlers            *
 *                                        *
 ******************************************/

//  development error handler
//  will print stacktrace
/*if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

//  production error handler
//  no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});*/





/******************************************
 *                                        *
 *           4. GO GO SERVER!             *
 *                                        *
 ******************************************/

app.listen(PORT, function () {
  console.log('GO GO SERVER!', PORT);
});
