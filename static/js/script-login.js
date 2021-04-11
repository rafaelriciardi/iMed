$(document).ready(function(){
    login_type = 'paciente';
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
        },
        error: function (response){
          alert(JSON.stringify(response));
        }
      });
  
  })
