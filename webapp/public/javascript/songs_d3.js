// Chart dimensions
var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5};
var width = 960 - margin.right;
var height = 500 - margin.top - margin.bottom;

// Various scales
var xScale = d3.scaleLog().domain([300, 1e5]).range([0, width]),
  yScale = d3.scaleLinear().domain([10, 85]).range([height, 0]),
  radiusScale = d3.scaleSqrt().domain([0, 5e8]).range([0, 40]),
  colorScale = d3.scaleOrdinal(['red', 'blue', 'green', 'teal', 'brown', 'pink', 'purple']);

// The x & y axes
var xAxis = d3.axisBottom(xScale).ticks(12, d3.format(",d")),
  yAxis = d3.axisLeft(yScale);

// Create the SVG container and set the origin
var svg = d3.select("#chart").append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Add overlay for mouse movement
var overlay = svg.append("rect");
overlay.attr('class', 'overlay')
  .attr('x', 504)
  .attr('y', 246)
  .attr('width', 436)
  .attr('height', 233.5);


function getGenreData() {

}

// Grabs database for song
function getSongSpotterData() {

  $.post('/songLikes', {songId: $(this).attr('song_id')}, function(data) {

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

}
