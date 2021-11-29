#!/usr/bin/bash

sudo docker pull terysy/realtime_web:latest
sudo docker stop realtime_web
sudo docker system prune -f
sudo docker-compose -f /home/ubuntu/docker-composes/docker-compose.yaml up