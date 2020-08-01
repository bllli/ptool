mkdir -p /var/web/ptools/log
mkdir -p /var/web/ptools/db

rm -rf /var/web/ptools/app_backup
mv -f /var/web/ptools/app /var/web/ptools/app_backup
mv -f /var/web/ptools/dist /var/web/ptools/app

#cp nginx/nginx.conf /usr/local/etc/nginx
# todo nginx update
# todo supervisor update

rm -rf /var/web/ptools/app/app/uploads/
ln -s /uploads /var/web/ptools/app/app/uploads
