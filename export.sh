#!/usr/bin/env bash

./build.sh

docker save pobotri | gzip -c > /data/ATLAS22_POBOTRI.tar.gz
