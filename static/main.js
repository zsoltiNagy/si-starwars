$('#myModal').on('show.bs.modal', function (event) {
  debugger;
  var button = $(event.relatedTarget) // Button that triggered the modal
  var planets = button.data('planets').split(",") // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  $('#modal-table').find('td').remove();
  debugger;
  for (var i = 0; i < planets.length; i++) {
    debugger;
    $.getJSON(planets[i], function success(data){
        $("#modal-table").append('<tr><td>'+data.name+'</td><td>'+data.height+'</td><td>'+data.mass+'</td><td>'+data.hair_color+'</td><td>'+data.skin_color+'</td><td>'+data.eye_color+'</td><td>'+data.birth_year+'</td><td>'+data.gender+'</td>')
    });
  };
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('Residents of' + button.parent().closest('tr').children('td.planet-name').text())
  
});

$('tr').on('click', '.vote-button', function() {
  debugger;
  var dataObj = {};
  dataObj.username = $('#username').text();
  dataObj.planet = $(this).parent().closest('tr').children('td.planet-name').text()
  $.ajax({
    url: '/votePlanet',
    type: 'POST',
    data: dataObj,
    success: function(response) {
        alert(response);
        debugger;
    },
    error: function(error) {
        console.log(error);
    }
  });
});

/*
$('#voteStat').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var voteStat = button.data(); // Extract info from data-* attributes
  var x = voteStat[0]
  debugger;
  $('#voteStat-table').find('td').remove();
  for (var i = 0; i < voteStat.length; i++) {
        voteStat[i]
        //$("#voteStat-table").append('<tr><td>'+data.name+'</td><td>'+data.height+'</td><td>'+data.mass+'</td><td>'+data.hair_color+'</td><td>'+data.skin_color+'</td><td>'+data.eye_color+'</td><td>'+data.birth_year+'</td><td>'+data.gender+'</td>')
    };
  });
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
//  var modal = $(this)
//  modal.find('.modal-title').text('Residents of' + button.parent().closest('tr').children('td.planet-name').text())*/
//});