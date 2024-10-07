#!/bin/bash

rm -rf ./static/*
rm -rf ./output/*
python scripts/generate_static.py
mvn clean package > /dev/null 2>&1
java -jar target/coupledMain.jar static/*
python scripts/amplitude_analysis.py