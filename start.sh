#!/usr/bin/env bash
docker run --restart always -d -p 8002:8000 --name ptools \
  -v ~/ptools/db:/db \
  -v ~/ptools/tmp:/tmp \
  -v ~/Downloads:/uploads/downloads \
  blllicn/ptools:v0.11
