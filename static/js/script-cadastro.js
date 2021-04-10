$(document).ready(function(){
    $('select').formSelect();
  });


$(document).on('click', '#submit-form', function() {

  data = {
    "nome": $("#name").val(),
    "cpf": $("#cpf").val(),
    "birthday": $("#cpf").val(),
    "genre": $("#drop_list_genre").val(),
    "phone": $("#phone").val(),
    "email": $("#email").val(),
    "convenio": $("#drop_list_convenio").val(),
    "password": $("#password").val()
  };

    $.ajax({
      url: 'http://127.0.0.1:5000/cadastrar',
      type: 'POST',
      dataType: 'JSON',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function (response){
        console.log(JSON.stringify(response))
      },
      error: function (response){
        alert(JSON.stringify(response));
      }
    });



$('#clear').click(function() {
  $('#signin-form').trigger('reset');

});