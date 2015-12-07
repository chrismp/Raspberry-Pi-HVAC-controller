$(function(){
	var $clock = $('#clock');
	var $coolStatus = $('#cool-status');
	var $coolCurrentTemperature = $('#cool-current-temperature');
	var $heatStatus = $('#heat-status');
	var $heatCurrentTemperature = $('#heat-current-temperature');
	var $fanStatus = $('#fan-status')
	var $lastReading = $('#last-reading');
	var $roomTemperature = $('#room-temperature');
	var $coolTemperature = $('#coolTemperature');
	var $coolSwitchRadioArray = $('input:radio[name=coolSwitch]');
	var $heatTemperature = $('#heatTemperature');
	var $heatSwitchRadioArray = $('input:radio[name=heatSwitch]');
	var $fanSwitchRadioArray = $('input:radio[name=fanSwitch]');

	// $(document).ajaxStart(function(){
	// 	do something to show AJAX request is processing
	// }).ajaxStop(function(){
	// 	do something once AJAX request stops
	// });

	// Set `input` elements
	$.get(
		'/status',
		function(data){
			var timeLastRead = data.timeLastRead;
			var roomTemperature = roundInt(data.roomTemperature);
			var coolSwitch = data.coolSwitch;
			var coolTemperature = data.coolTemperature;
			var heatSwitch = data.heatSwitch;
			var heatTemperature = data.heatTemperature;
			var fanSwitch = data.fanSwitch;

			$coolTemperature.val(coolTemperature);
			$heatTemperature.val(heatTemperature);
			setRadioInput($coolSwitchRadioArray, coolSwitch)
			setRadioInput($heatSwitchRadioArray, heatSwitch)
			setRadioInput($fanSwitchRadioArray, fanSwitch)
		}
	);

	window.setInterval(
		function(){
			$clock.html(new Date(Date.now()));
		}
	);

	updateStatus(
		$coolStatus,
		$coolCurrentTemperature,
		$heatStatus,
		$heatCurrentTemperature,
		$fanStatus,
		$lastReading, 
		$roomTemperature
	)

	window.setInterval(
		function(){
			updateStatus(
				$coolStatus,
				$coolCurrentTemperature,
				$heatStatus,
				$heatCurrentTemperature,
				$fanStatus,
				$lastReading, 
				$roomTemperature
			)
		},
		10000
	);

	var unitDevicePartsArray = [
		$coolSwitchRadioArray,
		$coolTemperature,
		$heatSwitchRadioArray,
		$heatTemperature,
		$fanSwitchRadioArray
	];

	for (var i=0; i<unitDevicePartsArray.length; i++) {
		unitDevicePartsArray[i].click(function(){
			var $this = $(this);
			var name = $this.attr('name');

			// `val` attribute of `input` user clicked.
			// For HVAC: 0 is off, 1 is cool, 2 is heat
			// For fan: 0 is off, 1 is on
			var switchStatus = $this.val();

			var temperatureType = $this.parent()
				.find('input[type=number]')
				.attr('name');
			var temperature = $this.parent()
				.find('input[type=number]')
				.val();

			var dataToSend = {};
			dataToSend[name] = switchStatus;

			if(temperatureType!=undefined){
				dataToSend[temperatureType] = temperature;
			}
			

			$.ajax({
				url: '/status',
				type: 'POST',
				data: JSON.stringify(dataToSend),
				contentType: 'application/json; charset=utf-8',
				timeout: 20000, // give the A/C 20 seconds
				success: function(data){
					// console.log('got response');
					// console.log(data);
				},
				error: function(error){
					alert('HVAC/fan did not get your request!');
					console.log(error);
				}
			});
		});
	};

});