$(document).ready(function(){
    login_type = 'paciente';

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

$('input[type=radio][name=user-type]').change(function() {
	console.log(this.value)
    if (this.value == 'paciente') {
        $('#user-label').text('CPF');
        login_type = 'paciente';
    }
    else if (this.value == 'medico') {
        $('#user-label').text('CRM');
        login_type = 'medico';
    }
});

$(document).on('click', '#login', function() {

    data = {
      "user": $("#user").val(),
      "password": $("#password").val(),
      "tipo_usuario": login_type
    };
    
    console.log(data)

      $.ajax({
        url: 'http://127.0.0.1:5000/efetuar_login',
        type: 'POST',
        dataType: 'JSON',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (response){
          
          console.log(JSON.stringify(response))
          if (response['login'] == 'ok'){
              name = response['nome']
              id = response['id']

              console.log(response)
              document.cookie = `name=${name}`;
              document.cookie = `id=${id}`;
              document.cookie = `type=${login_type}`;
              if(login_type == "medico"){
                window.location.href = "/agenda";
              }
              else{
                window.location.href = "/busca";
              }
              
          }
          else if(response['login'] == 'bad password'){
            alert("Usuario e senha não coincidem");
          }
          else{
            alert(response);
          }
        },
        error: function (response){
          alert(JSON.stringify(response));
        }
      });
  
  })
