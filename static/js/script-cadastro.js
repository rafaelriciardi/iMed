$(document).on('click', '#confirma_cadastro', function() {


	data = {
		"nome": $("#first_name").val()
	};

	console.log(data)

    $.ajax({
		url: 'http://127.0.0.1:5000/cadastrar',
	    type: 'POST',
	    dataType: 'JSON',
	    contentType: 'application/json',
	    data: JSON.stringify(data),
	    success: function (response){
    	},
    	error: function (response){
    		alert(JSON.stringify(response));
    	}
    });


});