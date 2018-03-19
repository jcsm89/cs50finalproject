$(document).ready(function() {

  $("#form_movie").submit(function() {

    // on movie name submission trigger a GET request to search for the movie of interest
    $.getJSON("/search", {name: $("#movie_name").val()}, function(data) {
      alert(data.rat);
    });

    return false;
  });

  $('#movie .typeahead').typeahead({
    hint: true,
    highlight: true,
    minLength: 1
  },
  {
    name: 'movies',
    source: function (value, callback) {
    $.getJSON('/autocomplete', {
        q: value
      }, function (data) {
          callback(data.data || [])
      })
    },
  });

});
