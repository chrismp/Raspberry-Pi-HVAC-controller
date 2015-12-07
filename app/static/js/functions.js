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

function updateStatus(coolStatusElem, coolCurrentTemperatureElem, heatStatusElem, heatCurrentTemperatureElem, fanStatusElem, lastReadingElem, roomTemperatureElem){
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

			coolTemperature = coolTemperature===null ? 'Not yet set' : coolTemperature;
			heatTemperature = heatTemperature===null ? 'Not yet set' : heatTemperature;

			coolStatusElem.html(coolSwitch);
			coolCurrentTemperatureElem.html(coolTemperature);
			heatStatusElem.html(heatSwitch);
			heatCurrentTemperatureElem.html(heatTemperature);
			fanStatusElem.html(fanSwitch);
			roomTemperatureElem.html(roomTemperature);
			lastReadingElem.html(new Date(timeLastRead*1000));
		}
	);
}