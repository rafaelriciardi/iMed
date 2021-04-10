$(document).ready(function(){
    $('select').formSelect();
  });

$('#clear').click(function() {
  $('#signin-form').trigger('reset');
});