var curr_songs = {}
var selected_song = {}

$(document).ready(function() {
  $("#sugs_list").hide();
  function auto_func(e) {
      var keyCode = e.which
      selected_song = {}
      curr_songs = {}
      if ($("#song_search").val() === "") {
        selected_song = {}
        curr_songs = {}
        $("#sug_list li").hide()
        return;
      }
      if (keyCode != 13) {
        var text = $("#song_search").val();
        $.post("/search", {search: text},
          function(result){
            curr_songs = result;
            song_names = [];
            var listItems = $("#sug_list li");
            listItems.each(function(index, li) {
                if (text === '' || result.length === 0) {
                    $(this).text("")
                    curr_songs = {}
                    $(this).hide()
                } else {
                    $(this).attr('song_id', result[index].song_id);
                    $(this).text(result[index].song_name + " by " + result[index].artist_name);
                    $(this).show()
                }
            });
          });
      }
  };

  $("#song_search").keyup(auto_func);

  $('.song_sug').click(function() {
    $('.song_sug').hide();
    $('#song_search').val($(this).text());
    console.log('searching');
    $.post('/songLikes', {songId: $(this).attr('song_id')}, function(data) {

      ////////
      // D3 //
      ////////

      var parseStringToDate = d3.timeParse("%Y-%m-%d");
      var parseDateToString = d3.timeFormat("%Y-%m-%d");

      data.forEach(function(d) {
        d.creation_date = parseStringToDate(d.creation_date); // TODO: chop out time and time zone
        d.likes = d.likes;
      });

      var width = 890,
          height = 450

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
  });
});
