#!/usr/bin/env bash
# sets up web servers for deployment of web_static

sudo apt-get update -y

sudo apt-get install nginx -y

sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/web_static/releases/test/

sudo mkdir -p /data/web_static/shared/

sudo touch /data/web_static/releases/test/index.html

content="\
<html>
   <head>
   </head>
   <body>
      ALX Software Engineering
   </body>
</html>"

echo "$content" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

config="\\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}"

sudo sed -i "/server_name _;/a $config" /etc/nginx/sites-enabled/default

sudo nginx -s reload
