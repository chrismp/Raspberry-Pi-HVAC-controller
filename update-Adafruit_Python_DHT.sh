#!/bin/bash

mkdir -p Adafruit_Python_DHT # Make directory if not exists

# Get git submodule, update it
git submodule init
git submodule update