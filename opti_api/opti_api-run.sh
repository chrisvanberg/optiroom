#!/usr/bin/env bash

#Optiroom opti_api run command (Local Dev)
docker stop opti_api
docker rm opti_api
docker build -t  opti_api .
clear
echo "Build finished, launching the container"
docker run --name opti_api -e JWT_SECRET_KEY="optiroom" -e MYSQL_HOST="dev.optiroom.net" -e MYSQL_USER="opti_api" -e MYSQL_PASSWORD="YFdcxYJS:ng3PcvndfGeIeRxhuOYiP" -e MYSQL_DB="optiroom" -e DEBUG="True" -p 5000:5000 opti_api


#sleep 5
#sudo docker ps --filter "name=opti_api" -a
