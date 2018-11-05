$(document).ready(function(){

    $("#start_loop").hide();
    
    interval = setInterval(function(){
	console.log('invoked showproxy');
	window.location.href=window.location;
    }, 20000);


    $("#stop_loop").click(function(){
	clearInterval(interval);
	// Toggle button slowly
	$("#stop_loop").hide();
	$("#start_loop").show();
    });

    $("#start_loop").click(function(){
	location.reload(true);
    });
    
    
});
