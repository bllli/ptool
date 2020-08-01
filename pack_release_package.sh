#!/usr/bin/env bash

echo "building frontend"

npm --prefix frontend run build

echo "packing...."

rm -rf dist && mkdir dist
mv ./frontend/dist dist/frontend
cp -r ./backend/app dist/app
find dist/app -name '*.pyc' -delete
#cp -r ./nginx/ dist/nginx
cp -r ./supervisor/ dist/supervisor
cp ./requirements.txt dist/requirements.txt
cp ./scripts/install.sh dist/install.sh

zip -r dist_$(date +%s).zip dist
rm -rf dist

find . -type f -name "*dist*"  -maxdepth 1
echo "done!"
