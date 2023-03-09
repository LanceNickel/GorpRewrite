#!/usr/bin/env bash

if [[ $(screen -ls | grep "$1") != "" ]]; then
    echo 1
else
    echo 0
fi