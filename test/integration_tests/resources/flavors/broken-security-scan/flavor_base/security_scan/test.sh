#!/usr/bin/env bash

echo Simulating running security scan ...
mkdir -p $1
echo Report 123 >> "$1/report.txt"
exit 1 # Fail the security scan