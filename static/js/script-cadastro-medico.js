$(document).ready(function(){
    $('select').formSelect();
  });

$('#clear').click(function() {
  $('#signin-form').trigger('reset');
});

$(document).on('click', '#submit-form', function(e) {
  e.preventDefault();

  if($("#password").val() != $("#password-confirm").val()){
      alert("As senhas não coincidem.")
  }

  else{
      data = {
        "nome": $("#name").val(),
        "crm": $("#crm").val(),
        "birthday": $("#birthday").val(),
        "address": $("#address").val(),
        "cidade": $("#cidade").val(),
        "estado": $("#estado").val(),
        "phone": $("#phone").val(),
        "email": $("#email").val(),
        "convenios_atendidos": $("#convenios_atendidos").val(),
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
