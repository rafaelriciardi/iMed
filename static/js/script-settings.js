$( document ).ready(function() {
    console.log( "ready!" );

	var settings = {
		"url": "http://192.168.15.177/",
		"method": "POST",
		"timeout": 0,
		"data": "{command:get_time&}",
	};

	$.ajax(settings).done(function (response) {
		console.log(response)
		$('#real-time-value').text(response);
	});	
});

$(document).on('click', '#update-time-btn', function() {

	time_array = $('#real-time-value').text().split(":");

	data = "{command:set_time&h:"+time_array[0]+"&m:"+time_array[1]+"&s:00}";

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