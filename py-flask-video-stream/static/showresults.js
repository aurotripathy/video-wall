$(document).ready(function(){

    $("#show").click(function(){
	location.reload(true);
    });


    $("#classify_all").click(function(){
	$.ajax({
            url: "/classify_all"
	}).then(function(data) {
	    $.each(data, function(i, item) {
		console.log(data[i].id + ":" + data[i].label);
		$('.id').append(data[i].id);
		$('.label'+i).append(data[i].label);
	    });
	    $('h1').append(" - Labeled");
	});
	
    });

});
