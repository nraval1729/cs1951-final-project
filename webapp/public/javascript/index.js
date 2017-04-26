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
      $.post('/songLikes', {songId: songId}, function(data) {

        ////////
        // D3 //
        ////////

        var parseStringToDate = d3.timeParse("%Y-%m-%d");
        var parseDateToString = d3.timeFormat("%Y-%m-%d");

        data.forEach(function(d) {
          d.creation_date = parseStringToDate(d.creation_date); // TODO: chop out time and time zone
          d.likes = d.likes;
        });

        var width = 890;
        var height = 450;

        var x = d3.scaleTime()
        .rangeRound([0, width])
        .domain(d3.extent(data, function(d) { return(d.creation_date); }));

        var y = d3.scaleLinear()
        .rangeRound([height, 0])
        .domain(d3.extent(data, function(d) { return d.likes; }));

        // Line to draw
        var line = d3.line()
        .x(function(d) { return x(d.creation_date); })
        .y(function(d) { return y(d.likes); })

        var chart = d3.select('.chart')
        .append('g').attr('transform', 'translate(100, 20)');

        // Hover over (create hover over item)
        var tooltip = d3.select('body')
        .append('div')
        .attr('class', 'hover-over-tooltip')
        .style('opacity', 0)

        // X-axis
        chart.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(x));

        // Y-axis
        chart.append('g')
        .call(d3.axisLeft(y))
        .append('text')
        .attr('fill', '#000')
        .attr('transform', 'rotate(-90)')
        .attr('y', 6)
        .attr('dy', '0.71em')
        .attr('text-anchor', 'end')
        .text('Likes');

        // Draw line data
        chart.append('path')
        .datum(data)
        .attr('fill', 'none')
        .attr('stroke', 'steelblue')
        .attr('stroke-linejoin', 'round')
        .attr('stroke-linecap', 'round')
        .attr('stroke-width', 1.5)
        .attr('d', line);

        // Draw plots
        chart.selectAll('dot')
        .data(data)
        .enter().append('circle')
        .attr('r', 2.5)
        .attr('cx', function(d) { return x(d.creation_date); })
        .attr('cy', function(d) { return y(d.likes); })
        .on('mouseover', function(d) {
          tooltip.transition()
          .duration(200)
          .style('opacity', 1);
          tooltip.html(parseDateToString(d.creation_date) + '<br />' + d.likes + ' likes')
          .style('left', (d3.event.pageX + 5) + 'px')
          .style('top', (d3.event.pageY - 28) + 'px');
        })
        .on('mouseout', function(d) {
          tooltip.transition()
          .duration(600)
          .style('opacity', 0);
        });
      });
    } else {
      var spotifyFeatures;
      $.get("/authenticate", function(accessToken) {
        $.ajax({
          url: "https://api.spotify.com/v1/audio-features/" + songId,
          headers: {"Authorization": "Bearer " + accessToken},
          success: function(features) {
            spotifyFeatures = features;
            console.log(spotifyFeatures); // ask me how to actually get this. code needs some cleaning.
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
  }

});
