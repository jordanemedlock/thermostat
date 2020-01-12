$(function() {
	load_all();

	$("#mode-group.btn-group > .btn").click(function(){
	    $(this).addClass("active").siblings().removeClass("active");
	    set_mode();		
	});

	$('.temp-control').change(function() {
		set_temps();
	})
});

function load_all() {
	load_temperature();
	load_heater();
	load_cooler();
	load_mode();
	load_temps();
}

function load_temperature() {
	$.get('/temperature')
	.done(function(data) {
		$('#temperature-display').text(data)
	})
}


function load_heater() {
	$.get('/heater')
	.done(function(data) {
		$('#heater-display').text(data)
	})
}


function load_cooler() {
	$.get('/cooler')
	.done(function(data) {
		$('#cooler-display').text(data)
	})
}

function load_mode() {
	$.get('/mode')
	.done(function(data) {
		$('[name=mode][value='+data+']').parent().addClass('active')
	});
}

function load_temps() {
	$.get('/temps')
	.done(function(data) {
		var ts = data.split(' ');
		$('[name=lowest]').val(ts[0]);
		$('[name=lower]').val(ts[1]);
		$('[name=upper]').val(ts[2]);
		$('[name=uppest]').val(ts[3]);
	})
}

function set_mode() {
	var mode = $('#mode-group > .active > input').val();
	$.post('/mode/' + mode);
}

function set_temps() {

	var ts = []
	ts.push($('[name=lowest]').val());
	ts.push($('[name=lower]').val());
	ts.push($('[name=upper]').val());
	ts.push($('[name=uppest]').val());
	var msg = ts.join(' ');
	console.log(msg);
	$.post('/temps', msg);
}