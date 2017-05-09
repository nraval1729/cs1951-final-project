// Static vars
var KEYUP_DELAY_MS = 500;
var SPOTIFY_SEARCH_ENDPOINT = "https://api.spotify.com/v1/search";

// Globals
var curr_songs = {};
var selected_song = {};
var searchSpotter = true;
  // Delay search until X milliseconds has elapsed from when user stops
  // typing, so as not to get rate-limited by Spotify.
  // https://stackoverflow.com/questions/1909441/how-to-delay-the-keyup-handler-until-the-user-stops-typing
  var delay = (function() {
    var timer = 0;
    return function(callback, ms){
      clearTimeout (timer);
      timer = setTimeout(callback, ms);
    };
  })();

  $(document).ready(function() {
  // On initialization, hide suggestions list
  $("#sugs_list").hide();

  // Listen on search bar to make search query
  $("#song_search").keyup(songSearch);

  // Listen on switch to make corresponding updates to UI based on search type
  $("#search_type").change(function() {
    searchSpotter = $(this).prop('checked'); // if false, search Spotify
    switchSearchPlaceholder(searchSpotter);
  });

  // Listen on the dropdown song (returned from search)
  $('.song_sug').click(function() {
    $('.song_sug').hide();
    $('#song_search').val($(this).text());

    var songId = $(this).attr('song_id');

    if (searchSpotter) {
      // Handle searching initial database. should be same visualization as searching spotify api, but with
      // different features
    } else {
      var spotifyFeatures;
      $.get("/authenticate", function(accessToken) {
        $.ajax({
          url: "https://api.spotify.com/v1/audio-features/" + songId,
          headers: {"Authorization": "Bearer " + accessToken},
          success: function(features) {
            spotifyFeatures = features;
            $.ajax({
              url: "https://api.spotify.com/v1/tracks/" + songId,
              success: function(trackInfo) {
                artistId = trackInfo['album']['artists'][0]['id'];
                songPopularity = trackInfo['popularity'];
                $.ajax({
                  url: "https://api.spotify.com/v1/artists/" + artistId,
                  success: function(artistInfo) {
                    artistPopularity = artistInfo['popularity'];

                    desiredData = {};
                    desiredData.artistPopularity = artistPopularity;
                    desiredData.loudness = spotifyFeatures.loudness;
                    desiredData.tempo = spotifyFeatures.tempo;
                    desiredData.key = spotifyFeatures.key;
                    desiredData.mode = spotifyFeatures.mode;
                    desiredData.duration = spotifyFeatures.duration_ms;
                    desiredData.timeSignature = spotifyFeatures.time_signature;

                    console.log(songPopularity, desiredData);
                    // create d3 bar graph with features as x-axis: artist_hotness, loudness^2, tempo, key, tempo * mode, mode, duration, time_signature
                    createBarGraph(desiredData);

                    // IN HERE, feed spotify data into endpoint that returns
                    // average feature values for each feature
                  }
                });
              }
            });

          }
        });
      });
    }
  });

  function songSearch(e) {
    var keyCode = e.which;
    selected_song = {};
    curr_songs = {};
    if ($("#song_search").val() === "") {
      selected_song = {};
      curr_songs = {};
      $("#sug_list li").hide();
      return;
    }
    if (keyCode != 13) {
      var text = $("#song_search").val();

      if (searchSpotter) {
        $.post("/search", {search: text}, function(result) {
          updateUIWithResult(result, text);
        });
      } else {
        delay(function() {
          // Doc: https://developer.spotify.com/web-api/search-item/
          var spotifySearchType = "track"; // Currently on track (i.e. song) but other options exist (see doc)
          var spotifyLimit = 5; // Get first 5 results
          var spotifySearchParams = {q: text,
            type: spotifySearchType,
            limit: spotifyLimit};

            $.get(SPOTIFY_SEARCH_ENDPOINT, spotifySearchParams, function(spotifyResult) {
              var result = formatSpotifyResult(spotifyResult);
              updateUIWithResult(result, text);
            });
          }, KEYUP_DELAY_MS);
      }
    }
  }

  //  a) song_id: different, depending on if 'Spotter' or 'Spotify' type is
  //     being used
  //  b) song_name: the song name
  //  c) artist_name: the artist name
  function formatSpotifyResult(spotifyResult) {
    var formattedResult = [];

    var items = spotifyResult.tracks.items;

    $.each(items, function(index, elem) {
      var resultObj = {};
      resultObj.song_id = elem.id;
      resultObj.song_name = elem.name;
      resultObj.artist_name = elem.artists[0].name;

      formattedResult.push(resultObj);
    });

    return formattedResult;
  }

  // Assumes input variable 'result' is:
  // 1) an array of objects
  // 2) where each object contains:
  //    a) song_id: different, depending on if 'Spotter' or 'Spotify' type is
  //       being used
  //    b) song_name: the song name
  //    c) artist_name: the artist name
  function updateUIWithResult(result, text) {
    curr_songs = result;
    song_names = [];
    var listItems = $("#sug_list li");
    listItems.each(function(index, li) {
      if (text === '' || result.length === 0) {
        $(this).text("");
        curr_songs = {};
        $(this).hide();
      } else {
        $(this).attr('song_id', result[index].song_id);
        $(this).text(result[index].song_name + " by " + result[index].artist_name);
        $(this).show();
      }
    });
  }

  // * Note: this is currently a placeholder (2meta4me) that doesn't actually
  // make changes to the UI, but can if that's what we want to do. For
  // example, expand Spotify search capabilities to songs, artists, albums,
  // and playlists instead of just songs. This might require changing the
  // placeholderText to "Enter a song, artist, album, or Spotify playlist."
  function switchSearchPlaceholder(searchSpotter) {
    var placeholderText;

    if (searchSpotter) {
      placeholderText = "Enter a song";
    } else {
      placeholderText = "Enter a song";
    }

    $("#song_search").attr("placeholder", placeholderText);
  };

  // Takes in feature data and creates a bar graph that compares the selected song's features to that
  // of the average features of popular and unpopular songs.
  function createBarGraph(data) {
    // Clear chart svg.
    $('.chart').empty();

    ////////////////////
    // NORMALIZE DATA //
    ////////////////////
    var NUMFEATURES = 7
    // Set up arrays for feature labels/values
    var featureLabels = Object.keys(data);
    var featureValues = Object.values(data);

    var DUMMY_DATA = [0.5, 0.3, 0.8];
    // Mapping of feature labels to curr song feature and popular/unpopular
    // feature average (DUMMY DATA)
    var features =  []
    for (var i = 0; i < NUMFEATURES; i++) {
      for (var j = 0; j < 3; j++) {
        var temp = {};
        temp['feature'] = featureLabels[i];
        temp['index'] = j;
        temp['normValue'] = DUMMY_DATA[j];
        temp['value'] = 1000000;
        switch(j) {
          case 0:
            temp['label'] = 'Song Value: '
            break;
          case 1:
            temp['label'] = 'Popular Song Average: '
            break;
          case 2:
            temp['label'] = 'Unpopular Song Average: '
            break;
        }
        features.push(temp);
      }
    }

    console.log(features);

    // TODO: NORMALIZE DATA
    // var normalizedFeatureValues = [];
    // Normalize y-values for each feature
    // for (var i = 0; i < featureValues.length; i++) {
    //   normalizedFeatureValues.push(normalize(featureValues[i], featureValues));
    // };

    ////////
    // D3 //
    ////////

    // Chart dimensions
    var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 50};
    var width = 900 - margin.right;
    var height = 500 - margin.top - margin.bottom;

    // Create the SVG container
    var svg = d3.select(".chart").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr('transform', 'translate(' + margin.left + ',0.0)');

    // Initialize axis
    var x0 = d3.scaleBand()
      .domain(featureLabels)
      .rangeRound([0, width])
      .paddingInner(0.1);
    var x1 = d3.scaleBand()
      .domain([0, 1, 2])
      .rangeRound([0, x0.bandwidth()])
      .padding(0.05)
    var y = d3.scaleLinear()
      .rangeRound([height, 0])
      .domain([0.0, 1.0]);
    var z = d3.scaleOrdinal()
      .range(["#98abc5", "#6b486b", "#ff8c00"]);

    // Tooltip
    var tip = d3.tip().attr('class', 'd3-tip').html(function(d) { return d.label + d.value; });
    svg.call(tip);

    // Create pixel spacing for x-axis for features
    var featureLabelPixels = [];
    var currPixelVal = 0;
    for (var i = 0; i < NUMFEATURES; i++) {
      featureLabelPixels.push(currPixelVal)
      currPixelVal += width / NUMFEATURES;
    }


    svg.append('g')
      .attr('class', 'axis')
      .attr('transform', 'translate(0,' + height + ')')
      .call(d3.axisBottom(x0))
      .selectAll(".tick text")
      .style("text-anchor", "middle");

    // NO NEED TO DRAW Y AXIS.
    // svg.append('g')
    //   .attr('class', 'axis')
    //   .call(d3.axisLeft(y));

    svg.append('g')
      .selectAll('g')
      .data(features)
      .enter().append('g')
        .attr('transform', function(d) {
          return 'translate(' + x0(d.feature) + ',0)';
        })
      .selectAll('rect')
      .data(features)
      .enter().append('rect')
        .attr('x', function(d) {
          return x1(d.index);
        })
        .attr('y', function(d) {
          return y(d.normValue);
        })
        .attr('width', x1.bandwidth())
        .attr('height', function(d) { return height - y(d.normValue); })
        .attr('fill', function(d) { return z(d.index) })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

  };

  // Normalizes data to fit between [0, 1]
  function normalize(currValue, values) {
    return (currValue - Math.min(...values)) / (Math.max(...values) - Math.min(...values));
  };

});
