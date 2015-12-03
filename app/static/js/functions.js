function setRadioInput(arrayOfElements, statusReceivedFromServer){
	for (var i=0; i<arrayOfElements.length; i++) {
		var radioInput = $(arrayOfElements[i]); // Select the current radio button input using jQuery selector
		var radioInputValue = +radioInput.val(); // Force the radio button's value, which is a string, into an integer
		if(statusReceivedFromServer===radioInputValue){
			radioInput.prop('checked',true);
		}
	}	
}

function getOtherDeviceSetting(arrayOfElements){
	for(var i = 0; i < arrayOfElements.length; i++) {
		var elem = $(arrayOfElements[i]);
		if(elem.prop('checked',true)){
			return +elem.val();
		}
	}
}

function roundInt(num){
	return Math.round(num);
}

function update(lastReadingElem, roomTemperatureElem, coolTemperatureElem, heatTemperatureElem, coolSwitchRadioArray, heatSwitchRadioArray, fanSwitchRadioArray){
	$.get(
		'/status',
		function(data){
			// console.log(data);
			var timeLastRead = data.timeLastRead;
			var roomTemperature = roundInt(data.roomTemperature);
			var coolSwitch = data.coolSwitch;
			var coolTemperature = data.coolTemperature;
			var heatSwitch = data.heatSwitch;
			var heatTemperature = data.heatTemperature;
			var fanSwitch = data.fanSwitch;

			lastReadingElem.html(new Date(timeLastRead*1000));
			roomTemperatureElem.html(roomTemperature);
			coolTemperatureElem.val(coolTemperature)
			heatTemperatureElem.val(heatTemperature);
			setRadioInput(coolSwitchRadioArray, coolSwitch)
			setRadioInput(heatSwitchRadioArray, heatSwitch)
			setRadioInput(fanSwitchRadioArray, fanSwitch)
		}
	);
}