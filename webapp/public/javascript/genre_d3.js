$(document).ready(function() {
  // Instantiate slider
  var slider = $('.range-slider').slider({
  	formatter: function(beginningYear) {
      endingYear = parseInt(beginningYear) + 10
  		return beginningYear + ' - ' + endingYear;
  	}
  });

  $('.range-button').click(function() {
    $('#genre_chart svg g').empty()
    console.log(slider.slider('getValue'))
    getGenreData(slider.slider('getValue'));
  });

  ////////
  // D3 //
  ////////

  // Chart dimensions
  var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5};
  var width = 960 - margin.right;
  var height = 500 - margin.top - margin.bottom;

  // Bubble dimensions
  var diameter = 960,
      format = d3.format(",d"),
      color = d3.scaleOrdinal(d3.schemeCategory10);

  var bubble = d3.pack()
      .size([diameter, diameter])
      .padding(1.5);

  // Create the SVG container and set the origin
  var svg = d3.select("#genre_chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("class", "wordcloud")
    .append("g")
    .attr("transform", "translate(365,200)");

  // Draw initial data
  getGenreData(1950)

  function getGenreData(beginYear) {
    console.log(beginYear);
    $.post('/genreData', {beginYear: beginYear}, function(data) {
      // Mapping of genre to [song_hotness, count_of_songs] to calculate average hotness
      genre_hotness_map = {};
      // Loop through data to set up mapping of genre to hotness (hotness will be an average)
      for (i = 0; i < data.length; i++) {
        // Loop through each of the genre tags for a song
        song_hotness = parseFloat(data[i].song_hotness);
        if (!isNaN(song_hotness)) {
          song_genres = data[i].artist_mbtags.split(',');
          for (j = 0; j < song_genres.length; j++) {
            if (genre_hotness_map[song_genres[j]]) {
              genre_hotness_map[song_genres[j]][0] += song_hotness
              genre_hotness_map[song_genres[j]][1] += 1;
            }
            else {
              genre_hotness_map[song_genres[j]] = [song_hotness, 1]
            }
          }
        }
      }

      // Calculate average hotness for each genre
      for (var key in genre_hotness_map) {
        genre_hotness_map[key] = genre_hotness_map[key][0] / genre_hotness_map[key][1]
      }

      // Create frequency word list
      frequency_word_list = []
      for (var key in genre_hotness_map) {
        frequency_word_list.push({'text': key, 'size': genre_hotness_map[key] * 70.0})
      }
      console.log(frequency_word_list)

      d3.layout.cloud().size([800, 300])
        .words(frequency_word_list)
        .rotate(0)
        .fontSize(function(d) { return d.size; })
        .on("end", draw)
        .start();

      function draw(words) {
        var words = svg.selectAll("text").data(words)
        words.enter().append("text")
         .style("font-size", function(d) { return d.size + "px"; })
         .style("fill", function(d, i) { return color(i); })
         .attr("transform", function(d) {
             return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
         })
             .text(function(d) { return d.text; });
        words.exit().remove();
       }
    });
  }

});
