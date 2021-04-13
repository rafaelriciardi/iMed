$( document ).ready(function(){
	$('select').formSelect();
  $('.datepicker').datepicker({ format: 'dd-mm-yyyy' });
	checkUser();
  retornaBusca();
  preencheFiltros();
});

$(document).on('click','#filter', function(){
    $('.filter-window').show();
});

$(document).on('click','#cancel-filter', function(){
    $('.filter-window').hide();
});

$(document).on('click','#apply-filter', function(){
  $('.doctor-table tr').remove();
  retornaBusca();
  $('.filter-window').hide();
});

$(document).on('click','.close-btn', function(){
    $('.doctor-content-div').hide();
});

$(document).on('click','#agendar-consulta', function(){
  if ($('.datepicker').val() != "" && $('select').val() != ""){
    agendarConsulta();
  }
  else{
    alert("Escolha um dia e horario de consulta");
  }
  
});

$(document).on('click','.doctor-table tr', function(){
    var id = $(this).attr('value');
    console.log($(this).find('.nome-medico').text())

    $('.datepicker').val('');
    $('select').prop('selectedIndex',0);
    $('select').formSelect();
    
    $('#doctor-name').text($(this).find('.nome-medico').text());
    $('#doctor-site').html("CRM: <span id='crm-value'>"+id+"</span>");
    $('#doctor-address').text($(this).find('.endereco-medico').text());
    $('#doctor-city').text($(this).find('.cidade').text());
    $('#doctor-state').text($(this).find('.estado').text());
    $('#doctor-especialidade').text($(this).find('.site-medico').text());
    $('#doctor-convenios').text($(this).find('.convenio-medico').text());
    $('.doctor-content-div').show();

});

$(document).on('change','.datepicker', function(){
    console.log($('.datepicker').val());
    getHorarios($('.datepicker').val(), $('#crm-value').text());
});

function getHorarios(date, crm){
  filter_data = {
    "data": date,
    "crm": crm
  };

  console.log(filter_data)
  
  $.ajax({
        url: 'http://localhost:5000/gethorarios',
        type: 'POST',
        dataType: 'JSON',
        contentType: 'application/json',
        data: JSON.stringify(filter_data), 
        success: function(data) {
          for(i = 0; i < data.length; i++){
            $('#horario-select option[value="'+data[i]+'"]').attr("disabled", true);;
          }
          $('select').formSelect();
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

$(document).on('click','#clear-filter', function(){
  console.log('Função Clear Filter')
  $("#nome").val("");
  //TODO - RESETAR OS COMBO BOXES PARA A PRIMEIRA OPÇÃO
  //$("#drop_list_cidades").val("");
  //$("#drop_list_especialidade").val("");
  //$("#drop_list_convenios").val("")
})

function retornaBusca(){
  filter_data = {
    "nome": $("#nome").val(),
    "cidade": $("#drop_list_cidades").val(),
    "especialidade": $("#drop_list_especialidade").val(),
    "convenio": $("#drop_list_convenios").val()
  };

  console.log(filter_data)
  
  $.ajax({
        url: 'http://localhost:5000/realizarbusca',
        type: 'POST',
        dataType: 'JSON',
        contentType: 'application/json',
        data: JSON.stringify(filter_data), 
        success: function(data) {
          console.log(data);
          for(i = 0; i < data.length; i++){
            $('.doctor-table').append('<tr value='+data[i][0]+'><td><a class="nome-medico military-font">'+data[i][1]+'</a><p class="localizacao-medico"><span class="cidade">'+data[i][2]+'</span> - <span class="estado">'+data[i][3]+'</span></p><p class="endereco-medico">'+data[i][5]+'</p><p class="site-medico">'+data[i][4]+'</p><div class="convenio-medico">'+data[i][6]+'</div></td></tr>');
          }
         },
        error: function (e){
            console.log(JSON.stringify(e));
        }
    });
}

function preencheFiltros(){
    $.ajax({
        url: 'http://localhost:5000/getespecialidades',
        type: 'get',
        success: function(data) {
          console.log(data);
          for(i = 0; i < data.length; i++){
            $('#drop_list_especialidade').append('<option value="'+data[i][0]+'">'+data[i][0]+'</option>');
          }
          $('#drop_list_especialidade').formSelect();
         },
        error: function (e){
            console.log(JSON.stringify(e));
        }
    });

    $.ajax({
        url: 'http://localhost:5000/getcidades',
        type: 'get',
        success: function(data) {
          console.log(data);
          for(i = 0; i < data.length; i++){
            $('#drop_list_cidades').append('<option value="'+data[i][0]+'">'+data[i][0]+'</option>');
          }
          $('#drop_list_cidades').formSelect();
         },
        error: function (e){
            console.log(JSON.stringify(e));
        }
    });

    $.ajax({
      url: 'http://localhost:5000/getconvenios',
      type: 'get',
      success: function(data) {
        console.log(data);
        for(i = 0; i < data.length; i++){
          $('#drop_list_convenios').append('<option value="'+data[i][0]+'">'+data[i][0]+'</option>');
        }
        $('#drop_list_convenios').formSelect();
       },
      error: function (e){
          console.log(JSON.stringify(e));
      }
  });
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