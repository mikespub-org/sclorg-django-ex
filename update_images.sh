#!/bin/sh
docker build -f Dockerfile -t mikespub/sclorg-flask-ex:centos7-python38 .
docker build -f Dockerfile.c9s -t mikespub/sclorg-flask-ex:c9s-python311 .
docker build -f Dockerfile.f38 -t mikespub/sclorg-flask-ex:f38-python311 .
docker build -f Dockerfile.ubi9 -t mikespub/sclorg-flask-ex:ubi9-python311 .
docker push -a mikespub/sclorg-flask-ex
