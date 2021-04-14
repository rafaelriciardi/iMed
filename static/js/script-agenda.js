$( document ).ready(function(){
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
  var yyyy = today.getFullYear();

  today = dd + '/' + mm + '/' + yyyy;

	$('select').formSelect();
  $('.datepicker').datepicker({ format: 'dd/mm/yyyy' });
  $('.datepicker').val(today);
	checkUser();
  getConsultas_Medico($('.datepicker').val(), getCookie('id'));
  
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

$(document).on('change','.datepicker', function(){
    console.log('lala')
    getConsultas_Medico($('.datepicker').val(), getCookie('id'));
});

function getConsultas_Medico(date, crm){
  $('.doctor-table tr').remove();
  filter_data = {
    "data": date,
    "crm": crm
  };

  console.log(filter_data)
  
  $.ajax({
        url: 'http://localhost:5000/getconsultas_medico',
        type: 'POST',
        dataType: 'JSON',
        contentType: 'application/json',
        data: JSON.stringify(filter_data), 
        success: function(data) {
          console.log("retorno")
          console.log(data);
          if(data.length > 0){
            for(i = 0; i < data.length; i++){
              $('.doctor-table').append('<tr value='+data[i][1]+'><td><a class="nome-medico military-font">'+data[i][0]+'</a><p class="endereco-medico"><span>Data Nascimento: </span>'+data[i][2]+'</p><p class="site-medico"><span>Telefone: </span>'+data[i][5]+'</p><p class="site-medico"><span>Horário: </span>'+data[i][3]+'</p><p class="site-medico">'+data[i][4]+'</p></td></tr>');
            }
          }
          else{
            $('.doctor-table').append('<tr><td>Você ainda não tem consultas agendadas para esse dia</td></tr>')
          }
          
         },
        error: function (e){
            console.log(JSON.stringify(e));
        }
    });
}

function agendarConsulta(){
  userId = getCookie('id')
  if(userId != ""){
    data = {
      'data': $('.datepicker').val(),
      'horario': $('#horario-select select').val(),
      'cpf': getCookie('id'),
      'crm': $('#crm-value').text()
    }

    console.log(data);
    $.ajax({
          url: 'http://localhost:5000/agendarconsulta',
          type: 'POST',
          dataType: 'JSON',
          contentType: 'application/json',
          data: JSON.stringify(data), 
          success: function(response) {
            console.log(response);
            if (response['insertion'] == 'ok'){
                alert("Consulta agendada com sucesso");
                $('.doctor-content-div').hide();
              }
              else{
                alert(JSON.stringify(response));
              }
           },
          error: function (e){
              console.log(JSON.stringify(e));
          }
      });
  }
  else{
    alert("Voce precisa estar logado para agendar uma consulta")
    window.location.href = "/login"
  }

}


$('#logout').click(function(event) {
  document.cookie = 'name=; expires=Thu, 01 Jan 1970 00:00:00 UTC';
  document.cookie = 'id=; expires=Thu, 01 Jan 1970 00:00:00 UTC';
  document.cookie = 'type=; expires=Thu, 01 Jan 1970 00:00:00 UTC';
  location.reload();
});

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function checkUser(){
    name = getCookie('name');

    if(name != ""){
      $('#boas-vindas-nome').html(name);
      $('#boas-vindas').show();
      $('#boas-vindas').parent().children().eq(0).show();
      $('#boas-vindas').parent().children().eq(1).hide();
      $('#boas-vindas').parent().children().eq(2).hide();
      $('#boas-vindas').parent().children().eq(3).hide();
    }

    else{
      $('#boas-vindas').parent().children().eq(0).hide();
      $('#boas-vindas').parent().children().eq(1).show();
      $('#boas-vindas').parent().children().eq(2).show();
      $('#boas-vindas').parent().children().eq(3).show();
    }
}

function getCookie(cname) {
  const name = `${cname}=`;
  const ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return '';
}