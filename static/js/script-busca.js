$( document ).ready(function(){
	$('select').formSelect();
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

$(document).on('click','.nome-medico', function(){
    var id = $(this).parent().children().last().text();
    console.log(id);
    $.ajax({
          url: 'http://134.209.114.75/airsoftspot/api/doctor/'+id,
          type: 'get',
          success: function(data) {
            console.log(data);
            $('#doctor-name').text(data["name"]);
            $('#doctor-site').text(data["site"]);
            $('#doctor-address').text(data["address"]);
            $('#doctor-city').text(data["city"]);
            $('#doctor-state').text(data["state"]);
            $('#doctor-description').html(data["about"]);
            $('#doctor-id').text(data["fieldid"]);
            $('.doctor-content-div').show();
           },
          error: function (e){
              console.log(JSON.stringify(e));
          }
      });
});

function retornaBusca(){
  filter_data = {
    "nome": $("#nome").val(),
    "cidade": $("#drop_list_cidades").val(),
    "especialidade": $("#drop_list_especialidade").val(),
    "convenio": ""
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
            $('.doctor-table').append('<tr><td><a class="nome-medico military-font">'+data[i][1]+'</a><p class="localizacao-medico"><span class="cidade">'+data[i][2]+'</span> - <span class="estado">'+data[i][3]+'</span></p><p class="site-medico">'+data[i][4]+'</p><div class="id-medico">'+data[i][5]+'</div></td></tr>');
          }
         },
        error: function (e){
            console.log(JSON.stringify(e));
        }
    });
}

function getMedicos(){
  $.ajax({
          url: 'http://localhost:5000/teste',
          type: 'get',
          success: function(data) {
            console.log(data);
            for(i = 0; i < data.length; i++){
              $('.doctor-table').append('<tr><td><a class="nome-medico military-font">'+data[i]["name"]+'</a><p class="localizacao-medico"><span class="cidade">'+data[i]["city"]+'</span> - <span class="estado">'+data[i]["state"]+'</span></p><p class="site-medico">'+data[i]["site"]+'</p><div class="id-medico">'+data[i]["fieldid"]+'</div></td></tr>');
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

$('#logout').click(function(event) {
  document.cookie = 'name=; expires=Thu, 01 Jan 1970 00:00:00 UTC';
  document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC';
  location.reload();
});


}

$('#logout').click( function(event) {
  document.cookie = "name=; expires=Thu, 01 Jan 1970 00:00:00 UTC";
  document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC";
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