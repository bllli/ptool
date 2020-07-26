mkdir -p /var/web/ptools/log
mkdir -p /var/web/ptools/db

# todo stop services
unzip /var/web/ptools/update.zip -d /var/web/ptools/
rm -rf /var/web/ptools/app_backup
mv -f /var/web/ptools/app /var/web/ptools/app_backup
mv -f /var/web/ptools/dist /var/web/ptools/app

#cp nginx/nginx.conf /usr/local/etc/nginx
# todo nginx update
# todo supervisor update

rm -rf /var/web/ptools/app/app/uploads/
ln -s /uploads /var/web/ptools/app/app/uploads
