#!/usr/bin/env bash

./build.sh

docker save pobotri | gzip -c > /data/POBOTRI.tar.gz
