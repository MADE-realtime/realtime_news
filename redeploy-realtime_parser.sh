#!/usr/bin/bash

sudo docker pull terysy/realtime_parser:latest
sudo docker stop realtime_parser
sudo docker system prune -f
sudo docker-compose -f /home/ubuntu/docker-composes/docker-compose.yaml up