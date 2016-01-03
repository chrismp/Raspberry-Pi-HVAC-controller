import requests
import random
import sys
import datetime
import time
import json
import os
import dotenv
import RPi.GPIO as GPIO
import Adafruit_DHT

def dht22Reading():
    # Sensor should be set to Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
    sensor = Adafruit_DHT.DHT22
    pin = os.environ.get('DHT22_PIN')

    # Try to grab a sensor reading.  
    # Use the read_retry method which will retry up to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    rawReading = {
        'humidity': humidity,
        'temperature': temperature  # Raw temperature reading is in Celsius
    }

    return rawReading

def currentTemperatureRaw():
    rawReading = dht22Reading()
    return rawReading['temperature']

def convertToC(tempF):
    return ((tempF - 32.0) / 9.0) * 5.0  # Convert Fahrenheit to Celsius. Remember to add '.0' after numbers to make them floats. We want this to be a float.

def currentHumidityRaw():
    rawReading = dht22Reading()
    return rawReading['humidity']

def sendCurrentStatus():
    dataToSend = {
        'roomTemperature': currentTemperatureRaw(),
        'humidity': currentHumidityRaw(),
        'coolSwitch': currentStatus['coolSwitch'],
        'coolTemperature': currentStatus['coolTemperature'],
        'heatSwitch': currentStatus['heatSwitch'],
        'heatTemperature': currentStatus['heatTemperature'],
        'fanSwitch': currentStatus['fanSwitch']
    }
    
    url = baseURL+'/add-hvac-status'
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }

    r = requests.post(
        url,
        data = json.dumps(dataToSend),
        headers = headers,
        timeout = 20
    )
    rJSON = r.json() # Desired status, as returned by '/add-hvac-status' route

    coolSwitch = rJSON['coolSwitch']
    coolTemperature = rJSON['coolTemperature']
    heatSwitch = rJSON['heatSwitch']
    heatTemperature = rJSON['heatTemperature']
    fanSwitch = rJSON['fanSwitch']
    
    setStatus(coolSwitch, coolTemperature, heatSwitch, heatTemperature, fanSwitch)

def setStatus(coolSwitch, coolTemperature, heatSwitch, heatTemperature, fanSwitch):
    # For testing/debugging only!
##        coolSwitch = 0
##        coolTemperature = convertToC(85)
##        heatSwitch = 1
##        heatTemperature = convertToC(80)
##        fanSwitch = 1

    # May need to replace next four lines with some other code for getting and evaluating min/max temperature settings
    # Maybe get min/max settings from user/frontend?
    minTemp = float( os.environ.get('MINIMUM_TEMPERATURE') )
    maxTemp = float( os.environ.get('MAXIMUM_TEMPERATURE') )
    minTemp = convertToC(minTemp)
    maxTemp = convertToC(maxTemp)

    # Example of how `tempBuffer` is used: If COOL is set to 23.889C (about 75F), it will not turn on if tempF is 23.89, but only when it reaches 24.444 (about 76F)
    tempBuffer = float( os.environ.get('TEMPERATURE_BUFFER') ) # One degree change in Fahrenheit is about 0.555 in Celsius. So if I want the temperature buffer to be one degree Fahrenheit, set this to 0.555 Celsius.
    roomTemperature = currentTemperatureRaw()
    # print roomTemperature  # debugging

    if inTemperatureRange(minTemp, maxTemp, coolTemperature)==False:
        coolTemperature = None

    if inTemperatureRange(minTemp, maxTemp, heatTemperature)==False:
        heatTemperature = None

    if coolSwitch==1:
        if inTemperatureRange(minTemp, maxTemp, coolTemperature)==False:
            print 'Cool temperature out of range'
            coolSwitch = 0
            coolTemperature = None
        else:
            if coolSwitch==1 and heatSwitch==1:
                    coolSwitch = 1
                    heatSwitch = 0

            if roomTemperature > float(coolTemperature)+tempBuffer:
                    coolSwitch = 1
                    print 'Room temperature too high. Cooling...'
            else:
                    coolSwitch = 0
                    print 'Room temp cool, turning off cool.'
    else:
            coolSwitch = 0
            print 'cool switched off'

    if heatSwitch==1:
        if inTemperatureRange(minTemp, maxTemp, heatTemperature)==False:
            print 'Heat temp out of range'
            heatSwitch = 0
            heatTemperature = None
        else:
            if coolSwitch==1 and heatSwitch==1:
                    coolSwitch = 0
                    heatSwitch = 1

            if roomTemperature < float(heatTemperature)-tempBuffer:
                    heatSwitch = 1
                    print 'Room temp too cold. Heating...'
            else:
                    heatSwitch = 0
                    print 'Room temp warm. Turning off heat.'
    else:
        heatSwitch = 0
        print 'heat switched off'


    if fanSwitch==0:
        GPIO.output(fanPin, GPIO.HIGH)
        print 'fan switched on'
    elif fanSwitch==1:
        GPIO.output(fanPin, GPIO.LOW)
        fanSwitch = 0
        print 'fan switched off'

    if coolSwitch==0:
        GPIO.output(coolPin, GPIO.HIGH)
    elif coolSwitch==1:
        GPIO.output(coolPin, GPIO.LOW)
            
    if heatSwitch==0:
        GPIO.output(heatPin, GPIO.HIGH)
    elif heatSwitch==1:
        GPIO.output(heatPin, GPIO.LOW)                

    currentStatus['coolSwitch'] = coolSwitch
    currentStatus['coolTemperature'] = coolTemperature
    currentStatus['heatSwitch'] = heatSwitch
    currentStatus['heatTemperature'] = heatTemperature
    currentStatus['fanSwitch'] = fanSwitch
    print currentStatus # for debugging
    print '================'

def inTemperatureRange(minTemp, maxTemp, temperature):
    if temperature==None or temperature=='':
        return False

    if int(temperature)<minTemp or int(temperature)>maxTemp:
        return False



if __name__=='__main__':
    # Setting up environmental variables
    # See https://github.com/theskumar/python-dotenv
    dotenvPath = os.path.join(
        os.path.dirname(__file__),
        '.env'
    )
    dotenv.load_dotenv(dotenvPath)



    # Pin Definitons:
    coolPin = int( os.environ.get('COOL_PIN') )
    heatPin = int( os.environ.get('HEAT_PIN') )
    fanPin = int( os.environ.get('FAN_PIN') )
    hvacPinArray = [
        coolPin,
        heatPin,
        fanPin
    ]

    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    for pin in hvacPinArray:
        GPIO.setup(pin, GPIO.OUT) # When Pi interacts with pin, it is to send data from Pi to whatever is attached to pin
        GPIO.output(pin,GPIO.HIGH) # Set pin to 'HIGH', which means 'off'

    # Get current status
    baseURL = os.environ.get('BASE_URL')
    statusURL = baseURL+'/status'
    statusURLResponse = requests.get(
        statusURL
    )

    startupStatus = statusURLResponse.json()
    startupStatusDictionary = startupStatus['Status']
    
    if startupStatusDictionary==None:
        currentStatus = {
            'coolSwitch': 0,
            'coolTemperature': None,
            'heatSwitch': 0,
            'heatTemperature': None,
            'fanSwitch': 0
        }
    else:
        currentStatus = {
            'coolSwitch': startupStatusDictionary['coolSwitch'],
            'coolTemperature': startupStatusDictionary['coolTemperature'],
            'heatSwitch': startupStatusDictionary['heatSwitch'],
            'heatTemperature': startupStatusDictionary['heatTemperature'],
            'fanSwitch': startupStatusDictionary['fanSwitch']
        }

    try:
        while True:
            preConnect = datetime.datetime.now()
            sendCurrentStatus()
            lastConnect = datetime.datetime.now()
            time.sleep(1)
    except Exception as e:
        GPIO.cleanup() # cleanup all GPIO, which will turn off everything attached to GPIO pins
        raise
