$(document).ready(function(){
    $('select').formSelect();

    if(getCookie('type') == 'paciente'){
    $("#page1").attr("href", "/busca")
    $("#page1").html("Buscar médicos")
  }
  else if(getCookie('type') == 'medico'){
    $("#page1").attr("href", "/agenda")
    $("#page1").html("Consultar agenda")
  }
  else{
    $("#page1").hide()
  }
  });


$(document).on('click', '#submit-form', function(e) {
  e.preventDefault();

  if($("#password").val() != $("#password-confirm").val()){
      alert("As senhas não coincidem.")
  }

  else{
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
          if (response['insertion'] == 'ok'){
              window.location.href = "/login";
            }
            else{
              alert(JSON.stringify(response));
            }
        },
        error: function (response){
          alert(JSON.stringify(response));
        }
      });
    }
})

$('#clear').click(function() {
  $('#signin-form').trigger('reset');

});