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
});