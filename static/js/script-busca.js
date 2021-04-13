$( document ).ready(function(){
	$('select').formSelect();
  getFields();
});

$(document).on('click','#filter', function(){
    $('.filter-window').show();
});

$(document).on('click','#cancel-filter', function(){
    $('.filter-window').hide();
});

$(document).on('click','#apply-filter', function(){
    $('.field-table tr').remove();
    $.ajax({
          url: 'http://134.209.114.75/airsoftspot/api/field?name='+$('#nome').val()+'&city='+$('#cidade').val()+'&state='+$('#estado').val(),
          type: 'get',
          success: function(data) {
            console.log(data);
            for(i = 0; i < data.length; i++){
              $('.field-table').append('<tr><td><a class="nome-campo military-font">'+data[i]["name"]+'</a><p class="localizacao-campo"><span class="cidade">'+data[i]["city"]+'</span> - <span class="estado">'+data[i]["state"]+'</span></p><p class="site-campo">'+data[i]["site"]+'</p><div class="id-campo">'+data[i]["fieldid"]+'</div></td></tr>');
            }
           },
          error: function (e){
              console.log(JSON.stringify(e));
          }
      });
    $('.filter-window').hide();
});

$(document).on('click','.close-btn', function(){
    $('.field-content-div').hide();
});

$(document).on('click','.nome-campo', function(){
    var id = $(this).parent().children().last().text();
    console.log(id);
    $.ajax({
          url: 'http://134.209.114.75/airsoftspot/api/field/'+id,
          type: 'get',
          success: function(data) {
            console.log(data);
            $('#field-name').text(data["name"]);
            $('#field-site').text(data["site"]);
            $('#field-address').text(data["address"]);
            $('#field-city').text(data["city"]);
            $('#field-state').text(data["state"]);
            $('#field-description').html(data["about"]);
            $('#field-id').text(data["fieldid"]);
            $('.field-content-div').show();
           },
          error: function (e){
              console.log(JSON.stringify(e));
          }
      });
});

function getFields(){
  $.ajax({
          url: 'http://134.209.114.75/airsoftspot/api/field?name=&city=&state=',
          type: 'get',
          success: function(data) {
            console.log(data);
            for(i = 0; i < data.length; i++){
              $('.field-table').append('<tr><td><a class="nome-campo military-font">'+data[i]["name"]+'</a><p class="localizacao-campo"><span class="cidade">'+data[i]["city"]+'</span> - <span class="estado">'+data[i]["state"]+'</span></p><p class="site-campo">'+data[i]["site"]+'</p><div class="id-campo">'+data[i]["fieldid"]+'</div></td></tr>');
            }
           },
          error: function (e){
              console.log(JSON.stringify(e));
          }
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
      $('#boas-vindas').parent().children().eq(3).show();
    }

    else{
      $('#boas-vindas').parent().children().eq(0).hide();
      $('#boas-vindas').parent().children().eq(1).show();
      $('#boas-vindas').parent().children().eq(2).show();
      $('#boas-vindas').parent().children().eq(3).hide();
    }
}
