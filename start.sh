#!/usr/bin/env bash
# docker run --restart always -d -p 8009:5000 -e SERVER_MODE=${SERVER_MODE} --name `basename $(pwd)` -v $(pwd):/momedia -v $(pwd)/../molib:/molib -v /var/web/dynamic.static/:/var/web/dynamic.static/ moremom/momedia
docker run --restart always -d -p 8080:8000 --name `basename $(pwd)` \
  -v $(pwd)/tmp/docker/tmp:/tmp \
  -v $(pwd)/tmp/docker/uploads:/uploads \
  bt_publisher:latest
