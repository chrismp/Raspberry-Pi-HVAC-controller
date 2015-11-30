$(document).ready(function(){
	var $clock = $('#clock');
	var $roomTemperature = $('#room-temperature');
	var $hvacStatus = $('#hvac-status');
	var $fanStatus = $('#fan-status');
	var $hvacRadioInputArray = $('input:radio[name=hvac]');
	var $fanRadioInputArray = $('input:radio[name=fan]');

	// $(document).ajaxStart(function(){
	// 	do something to show AJAX request is processing
	// }).ajaxStop(function(){
	// 	do something once AJAX request stops
	// });

	$.get('/status',function(data){
		var unixTime = data.unixTime;
		var hvacStatus = data.hvacStatus;
		var fanStatus = data.fanStatus;
		var roomTemperature = data.roomTemperature;
		var cool = data.cool;
		var heat = data.heat;

		$clock.html(new Date(Date.now()));
		$roomTemperature.html(roomTemperature);
		$hvacStatus.html(hvacStatus);
		$fanStatus.html(fanStatus);

		setRadioInputOnLoad($hvacRadioInputArray, hvacStatus)
		setRadioInputOnLoad($fanRadioInputArray, fanStatus)
	});

	$hvacRadioInputArray.click(function(){
		var hvacMode, fanMode, cool, heat;
		var $radioInput = $(this);
		console.log($radioInput.attr('name'));

		// `val` attribute of `input` user clicked.
		// For HVAC: 0 is off, 1 is cool, 2 is heat
		// For fan: 0 is off, 1 is on
		var settingVal = $radioInput.val();


		var dataToSend = {
			'hvacMode': 
		};

		// $.ajax({
		// 	url: '/status',
		// 	type: 'POST',
		// 	data
		// });
	})
});