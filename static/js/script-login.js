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