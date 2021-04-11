$(document).ready(function(){
    $('select').formSelect();
  });

$('#clear').click(function() {
  $('#signin-form').trigger('reset');
});

$(document).on('click', '#submit-form', function() {

  data = {
    "nome": $("#name").val(),
    "crm": $("#crm").val(),
    "birthday": $("#birthday").val(),
    "address": $("#address").val(),
    "cidade": $("#cidade").val(),
    "estado": $("#estado").val(),
    "phone": $("#phone").val(),
    "email": $("#email").val(),
    "convenio": $("#drop_list_convenio").val(),
    "especialidade": $("#especialidade").val(),
    "password": $("#password").val()
  };

    $.ajax({
      url: 'http://127.0.0.1:5000/cadastrar_medico',
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

})