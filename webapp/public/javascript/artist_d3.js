$(document).ready(function() {
  // Instantiate slider
  var slider = $('.range-slider').slider({
  	formatter: function(beginningYear) {
      endingYear = parseInt(beginningYear) + 10
  		return beginningYear + ' - ' + endingYear;
  	}
  });

  $('.range-button').click(function() {
    $('#artist_chart svg g').empty()
    getArtistData(slider.slider('getValue'));
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
  var svg = d3.select("#artist_chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("class", "wordcloud")
    .append("g")
    .attr("transform", "translate(365,200)");

  // Draw initial data
  getArtistData(1950)

  function getArtistData(beginYear) {
    $.post('/artistsData', {beginYear: beginYear}, function(data) {
      // Mapping of artist_id to [artist_name, song_hotness, count_of_songs] to calculate average hotness
      artist_hotness_map = {};
      // Loop through data to set up mapping of genre to hotness (hotness will be an average)
      for (i = 0; i < data.length; i++) {
        // Loop through each of the genre tags for a song
        song_hotness = parseFloat(data[i].song_hotness);
        artist_id = data[i].artist_id;
        artist_name = data[i].artist_name
        if (!isNaN(song_hotness)) {
          if (artist_hotness_map[artist_id]) {
            artist_hotness_map[artist_id][1] += song_hotness;
            artist_hotness_map[artist_id][2] += 1;
          }
          else {
            artist_hotness_map[artist_id] = [artist_name, song_hotness, 1]
          }
        }
      }

      // Calculate average hotness for each genre
      for (var key in artist_hotness_map) {
        artist_hotness_map[key] = [artist_hotness_map[key][0], artist_hotness_map[key][1] / artist_hotness_map[key][2]]
      }

      // Create frequency word list
      frequency_word_list = []
      for (var key in artist_hotness_map) {
        frequency_word_list.push({'text': artist_hotness_map[key][0], 'size': artist_hotness_map[key][1] * 70.0})
      }

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
