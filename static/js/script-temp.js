$( document ).ready(function() {
    console.log( "ready!" );

	var settings = {
		"url": "http://192.168.15.177/",
		"method": "POST",
		"timeout": 0,
		"data": "{command:get_temp&}",
	};

	$.ajax(settings).done(function (response) {
		console.log(response)
		response = JSON.parse(response)
		console.log(response)
		$('#real-temp-value').text(response['temp'].toFixed(2));
		$('#min-temp-value').text(response['minTemp'].toFixed(2));
		$('#max-temp-value').text(response['maxTemp'].toFixed(2))
		$('#target-temp-value').text(response['targetTemp'].toFixed(2));
	});	
});

$(document).on('click', '#update-temp-btn', function() {

	data = "{command:set_temp&minTemp:"+$('#min-temp-value').text()+"&maxTemp:"+$('#max-temp-value').text()+"&targetTemp:"+$('#target-temp-value').text()+"}";

	console.log(data);

	var settings = {
		"url": "http://192.168.15.177/",
		"method": "POST",
		"timeout": 0,
		"data": data,
	};

	$.ajax(settings).done(function (response) {
		console.log(response);
	});	
});

$(document).on('click', '#refresh-temp-btn', function() {

	var settings = {
		"url": "http://192.168.15.177/",
		"method": "POST",
		"timeout": 0,
		"data": "{command:get_temp&}",
	};

	$.ajax(settings).done(function (response) {
		console.log(response)
		response = JSON.parse(response)
		console.log(response)
		$('#real-temp-value').text(response['temp'].toFixed(2));
		$('#min-temp-value').text(response['minTemp'].toFixed(2));
		$('#max-temp-value').text(response['maxTemp'].toFixed(2));
		$('#target-temp-value').text(response['targetTemp'].toFixed(2));
	});	
});