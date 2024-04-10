#!/usr/bin/env bash
# Setting up a web server to deploy web static.
# Author: Bismark-K

# installing updates and nginx
apt update -y
apt install -y nginx

# creating the directory and file location for my web static files
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# writing to that file, a test html
echo "<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <p>Testing Nginx server</p>
  </body>
</html>" | tee /data/web_static/releases/test/index.html

# creating a symbolic link to the html file
ln -sf /data/web_static/releases/test/ /data/web_static/current

# changing ownership
chown -R ubuntu:ubuntu /data
sudo sed -i '39 i\ \tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n' /etc/nginx/sites-enabled/default

# restarting nginx
sudo service nginx restart
