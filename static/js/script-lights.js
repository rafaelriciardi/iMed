$( document ).ready(function() {
    console.log( "ready!" );
    getLights()
	getSchedule();
});

$(document).on('click', '#change-lights-btn', function() {

	data = "";

	$( ".color-slider" ).each( function( index, element ){
		valor = $( this ).val();
		valor = map(valor, 0, 100, 0, 255);
		data += valor + "-";
	});

	data = data.substring(0, data.length-1);

	data = "{command:set_lights&value:"+data+"}";

	console.log(data);

	var settings = {
		"url": "http://192.168.15.177/",
		"method": "POST",
		"timeout": 0,
		"data": data,
	};

	console.log(settings)

	$.ajax(settings).done(function (response) {
		console.log(response);
	});	
});

$(document).on('change', '.color-slider', function() {
	$(this).parent().parent().children().find('.color-pct').text($(this).val()+'%');
});

$(document).on('click', '#new-schedule-btn', function() {
	$('#schedule-table').append('<tr><td>00:00</td><td>0%</td><td>0%</td><td>0%</td><td><a class="confirm-schedule-btn"><img src="/static/img/confirm.png"></a></td></tr>');
	$('#schedule-table').children().children().last().children().eq(0).attr('contenteditable','true');
	$('#schedule-table').children().children().last().children().eq(1).attr('contenteditable','true');
	$('#schedule-table').children().children().last().children().eq(2).attr('contenteditable','true');
	$('#schedule-table').children().children().last().children().eq(3).attr('contenteditable','true');
});

$(document).on('click', '.delete-schedule-btn', function() {
	if(confirm('Whould you like to delete this scheduled time? This actions cannot be undone.')){
		var time = $(this).parent().parent().children().eq(0).text();
		deleteSchedule(time);
		$(this).parent().parent().remove();
	}
});

$(document).on('click', '.edit-schedule-btn', function() {
	$(this).parent().parent().children().eq(0).attr('contenteditable','true');
	$(this).parent().parent().children().eq(1).attr('contenteditable','true');
	$(this).parent().parent().children().eq(2).attr('contenteditable','true');
	$(this).parent().parent().children().eq(3).attr('contenteditable','true');
	$(this).parent().parent().children().eq(4).html('<a class="confirm-schedule-btn"><img src="/static/img/confirm.png"></a>');
});

$(document).on('click', '.confirm-schedule-btn', function() {
	var time = $(this).parent().parent().children().eq(0).text();
	var white = $(this).parent().parent().children().eq(1).text().replace('%', '');
	var blue = $(this).parent().parent().children().eq(2).text().replace('%', '');
	var violet = $(this).parent().parent().children().eq(3).text().replace('%', '');

	setSchedule(time, white, blue, violet)

	$(this).parent().parent().children().eq(0).attr('contenteditable','false');
	$(this).parent().parent().children().eq(1).attr('contenteditable','false');
	$(this).parent().parent().children().eq(2).attr('contenteditable','false');
	$(this).parent().parent().children().eq(3).attr('contenteditable','false');
	$(this).parent().parent().children().eq(4).html('<a class="edit-schedule-btn"><img src="/static/img/edit.png"></a><a class="delete-schedule-btn"><img src="/static/img/delete.png"></a>');
});

function getLights(){
	var settings = {
		"url": "http://192.168.15.177/",
		"method": "POST",
		"timeout": 0,
		"data": "{command:get_lights&}",
	};

	$.ajax(settings).done(function (response) {
		console.log(response)
		response = JSON.parse(response)
		var white_value = map(response['white'], 0, 255, 0, 100);
		var blue_value = map(response['blue'], 0, 255, 0, 100);
		var violet_value = map(response['violet'], 0, 255, 0, 100);
		$( ".color-slider" ).eq(0).val(white_value);
		$( ".color-slider" ).eq(1).val(blue_value);
		$( ".color-slider" ).eq(2).val(violet_value);
		$( ".color-pct" ).eq(0).text(white_value+'%');
		$( ".color-pct" ).eq(1).text(blue_value+'%');
		$( ".color-pct" ).eq(2).text(violet_value+'%');
	});	
}

function getSchedule(){
	var table = document.getElementById("schedule-table");
	$.ajax({
	    url: 'https://smart-reef.herokuapp.com/select_all',
	    type: 'GET',
	    success: function (response){
	    	console.log(response)
	    	for (var i = 0; i < response.length; i++) {
	    		$('#schedule-table').append('<tr><td>'+response[i][0]+'</td><td>'+response[i][1]+'%</td><td>'+response[i][2]+'%</td><td>'+response[i][3]+'%</td><td><a class="edit-schedule-btn"><img src="/static/img/edit.png"></a><a class="delete-schedule-btn"><img src="/static/img/delete.png"></a></td></tr>');
	    	}
		    sortTable('schedule-table');
		    generateChart();
    	},
    	error: function (response){
    		alert(JSON.stringify(response));
    	}
    });
}

function setSchedule(time, white, blue, violet){
	var table = document.getElementById("schedule-table");

	data = {
		"time": time,
		"white": white,
		"blue": blue,
		"violet":violet
	}

	console.log(data);

	$.ajax({
	    url: 'https://smart-reef.herokuapp.com/insert',
	    type: 'POST',
	    dataType: 'JSON',
	    contentType: 'application/json',
	    data: JSON.stringify(data),
	    success: function (response){
	    	response = JSON.stringify(response);

	    	if(response == '{"insertion":"ok"}'){
	    		sortTable('schedule-table');
		   		generateChart();
	    	}
	    	else{
	    		alert(response);
	    	}
		    
    	},
    	error: function (response){
    		alert(JSON.stringify(response));
    	}
    });
}

function deleteSchedule(time){
	var table = document.getElementById("schedule-table");

	data = {
		"time": time
	}

	$.ajax({
	    url: 'https://smart-reef.herokuapp.com/delete',
	    type: 'POST',
	    dataType: 'JSON',
	    contentType: 'application/json',
	    data: JSON.stringify(data),
	    success: function (response){
	    	response = JSON.stringify(response);

	    	if(response == '{"deletion":"ok"}'){
	    		sortTable('schedule-table');
		   		generateChart();
	    	}
	    	else{
	    		alert(response);
	    	}
		    
    	},
    	error: function (response){
    		alert(JSON.stringify(response));
    	}
    });

}

function generateChart(){
	var table = document.getElementById("schedule-table");
	var time = [];
	var white = [];
	var blue = [];
	var violet = [];
	for (var i = 1, row; row = table.rows[i]; i++) {
    //iterate through rows
    //rows would be accessed using the "row" variable assigned in the for loop
	    for (var j = 0, col; col = row.cells[j]; j++) {
		    //iterate through columns
		    if(j == 0){
		    	time.push(col.innerHTML);
		    }
		    else if (j == 1){
		    	white.push(col.innerHTML.replace('%', ''));
		    }
		    else if (j == 2){
		    	blue.push(col.innerHTML.replace('%', ''));
		    }
		    else if (j == 3){
		    	violet.push(col.innerHTML.replace('%', ''));
		    }
		    

		    //columns would be accessed using the "col" variable assigned in the for loop
		}  
	}

	for (var k = time.length-1; k > 0; k--){
		time.splice(k, 0, time[k]);
		white.splice(k, 0, white[k-1]);
		blue.splice(k, 0, blue[k-1]);
		violet.splice(k, 0, violet[k-1]);
	}

	plotChart(time, white, blue, violet)

}





function plotChart(time, white, blue, violet){
	var white_trace = {
		x: time,
		y: white,
		type: 'scatter',
		line: {
			color: 'rgb(0, 0, 0)'
		}
	};

	var blue_trace = {
		x: time,
		y: blue,
		type: 'scatter',
		line: {
			color: 'rgb(0, 116, 236)'
		}
	};

	var violet_trace = {
		x: time,
		y: violet,
		type: 'scatter',
		line: {
			color: 'rgb(128, 0, 128)'
		}
	};

	var data = [white_trace, blue_trace, violet_trace];

	Plotly.newPlot('chart-div', data);
}



function sortTable(table_id) {
	var table, rows, switching, i, x, y, shouldSwitch;
	table = document.getElementById(table_id);
	switching = true;
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[0];
      y = rows[i + 1].getElementsByTagName("TD")[0];
      // Check if the two rows should switch place:
      if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
        // If so, mark as a switch and break the loop:
        shouldSwitch = true;
        break;
    }
}
if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
  }
}
}

function map(x, in_min, in_max, out_min, out_max){
	return Math.round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min);
}