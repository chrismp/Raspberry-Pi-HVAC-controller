$(document).ready(function(){
	var $clock = $('#clock');
	var $roomTemperature = $('#room-temperature');
	var $hvacStatus = $('#hvac-status');
	var $fanStatus = $('#fan-status');
	var $hvacRadioButtonArray = $('input:radio[name=hvac]');
	var $fanRadioButtonArray = $('input:radio[name=fan]');

	// $(document).ajaxStart(function(){
	// }).ajaxStop(function(){
	// });

	$.get('/status',function(data){
		var unixTime = data.unixTime;
		var hvacStatus = data.hvacStatus;
		var fanStatus = data.fanStatus;
		var roomTemperature = data.roomTemperature;
		var cool = data.cool;
		var heat = data.heat;

		$roomTemperature.html(roomTemperature);
		$hvacStatus.html(hvacStatus);
		$fanStatus.html(fanStatus);

		setRadioInputOnLoad($hvacRadioButtonArray, hvacStatus)
		setRadioInputOnLoad($fanRadioButtonArray, fanStatus)
	});
});