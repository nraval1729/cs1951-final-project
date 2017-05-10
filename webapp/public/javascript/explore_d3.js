var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5};
var width = 600;//960 - margin.right;
var height = 600 - margin.top - margin.bottom;//500 - margin.top - margin.bottom;

var ARTIST_HOTNESS_DOMAIN = [0, 1.08]; // 0, 1.08
var DURATION_DOMAIN = [0, 1000]; // 0.68, 992.05
var KEY_DOMAIN = [0, 10]; // 0, 9
var LOUDNESS_DOMAIN = [-1, 5]; // -0.18, 4.32
var MODE_DOMAIN = [0, 1]; // 0, 1
var SONG_HOTNESS_DOMAIN = [0, 1]; // 0.19, 1.00
var TEMPO_DOMAIN = [0, 100]; // 0.00, 99.99
var TIME_SIGNATURE_DOMAIN = [0, 10]; // 0, 7

function getFeatureDomain(feature) {
  if (feature === 'artist_hotness') {
    return ARTIST_HOTNESS_DOMAIN;
  } else if (feature === 'duration') {
    return DURATION_DOMAIN;
  } else if (feature === 'key') {
    return KEY_DOMAIN;
  } else if (feature === 'loudness') {
    return LOUDNESS_DOMAIN;
  } else if (feature === 'mode') {
    return MODE_DOMAIN;
  } else if (feature === 'song_hotness') {
    return SONG_HOTNESS_DOMAIN;
  } else if (feature === 'tempo') {
    return TEMPO_DOMAIN;
  } else {
    return TIME_SIGNATURE_DOMAIN;
  }
}

function getFeatureLabel(feature) {
  if (feature === 'artist_hotness') {
    return 'Artist Hotness';
  } else if (feature === 'duration') {
    return 'Duration';
  } else if (feature === 'key') {
    return 'Key';
  } else if (feature === 'loudness') {
    return 'Loudness';
  } else if (feature === 'mode') {
    return 'Mode';
  } else if (feature === 'song_hotness') {
    return 'Song Hotness';
  } else if (feature === 'tempo') {
    return 'Tempo';
  } else {
    return 'Time Signature';
  }
}

function colorDot(dot) {
  dot.attr('stroke', 'black')
     .attr('stroke-width', 1)
     .attr('fill', function(d) {
        var isPopular = parseFloat(d.song_hotness) > 0.55;
        if (isPopular) {
          console.log('red')
          return 'gold';
        } else {
          console.log('blue')
          return 'mediumblue'
        }
     })
     .attr('fill-opacity', 0.5);
}

$(document).ready(function() {
  var slider = $('.range-slider').slider({
    formatter: function(n) {
      return n;
    }
  });

  $('.range-button').click(function() {
    $('#artist_chart svg g').empty()
    getArtistData(slider.slider('getValue'));
  });

  $('#generate').on('click', function() {
    var sampleSize = $('#sample-size').val();

    $.post('/classifier/exploreSpotter', {sampleSize: sampleSize}, function(data) {
      var parsedData = [];
      for (var key in data) {
        parsedData.push(data[key]);
      }
      data = parsedData;

      var featureX = $('#feature-x').val();
      var featureY = $('#feature-y').val();

      var xScale = d3.scaleLinear().domain(getFeatureDomain(featureX)).range([0, width]);
      var yScale = d3.scaleLinear().domain(getFeatureDomain(featureY)).range([height, 0]);
      var colorScale = d3.scaleOrdinal([0, 1, 2, 3, 4, 5, 6]);

      var xAxis = d3.axisBottom(xScale);
      var yAxis = d3.axisLeft(yScale);

      d3.select('#vis').selectAll('svg').remove();

      var svg = d3.select('#vis').append('svg')
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom)
          .append('g')
          .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

      svg.append('g')
        .attr('transform', 'translate(0, ' + height + ')')
        .call(xAxis);
      svg.append('g')
        .call(yAxis);

      var xAxisLabel = svg.append('text')
                          .attr('class', 'label')
                          .attr('transform', 'translate(' + (width - 100) + ', ' + (height-10) + ')')
                          .text(getFeatureLabel(featureX));
      var yAxisLabel = svg.append('text')
                          .attr('class', 'label')
                          .attr('transform', 'translate(10, 100)rotate(270)')
                          .text(getFeatureLabel(featureY));

      var dot = svg.append('g')
                .selectAll('g')
                .data(data)
                .enter()
                .append('circle')
                .call(colorDot);

      function position(dot, featureX, featureY) {
        dot.attr('cx', function(d) { return xScale(d[featureX]); })
           .attr('cy', function(d) { return yScale(d[featureY]); })
           .attr('r', function(d) { return 5; });
      }

      position(dot, featureX, featureY);

    });
  });
});
