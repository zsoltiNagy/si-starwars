$('#planetDetailModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var planets = button.data('planets').split(",") // Extract the info passed from Flask from data-* attributes
  $('#modal-table').find('td').remove(); // Clean modal table from td leftovers from earlier use
  // For every item in the extracted info make an AJAX request and then put them in the modal-table
  for (var i = 0; i < planets.length; i++) {
    $.getJSON(planets[i].replace("http", "https"), function success(data){
        $("#modal-table").append('<tr><td>'+data.name+'</td><td>'+data.height+'</td><td>'+data.mass+'</td><td>'+data.hair_color+'</td><td>'+data.skin_color+'</td><td>'+data.eye_color+'</td><td>'+data.birth_year+'</td><td>'+data.gender+'</td>')
    });
  };
  // Update the modal's title.
  var modal = $(this)
  modal.find('.modal-title').text('Residents of' + button.parent().closest('tr').children('td.planet-name').text())
});

$('tr').on('click', '.vote-button', function() {
  // We create an empty object for storing data and fill with the username and the planets name
  var dataObj = {};
  dataObj.username = $('#username').text();
  dataObj.planet = $(this).parent().closest('tr').children('td.planet-name').text()
  // Then we pass the collected data with an AJAX POST request to the Flask /votePlanet handler
  $.ajax({
    url: '/votePlanet',
    type: 'POST',
    data: dataObj,
    success: function(response) {
        alert(response); // After succesful request we notify the user with line got from the Flask /votePlanet handler.
    },
    error: function(error) {
        console.log(error); // If there is an error we log it on the console.
    }
  });
});
