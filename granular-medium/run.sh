#!/bin/bash

rm -rf ./inputs/*
rm -rf ./outputs/*
python scripts/generate_inputs.py > /dev/null 2>&1
mvn clean package > /dev/null 2>&1
python scripts/run_all.py