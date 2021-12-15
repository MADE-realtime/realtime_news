#!/usr/bin/bash

sudo docker pull terysy/realtime_ml_jobs:latest
sudo docker stop realtime_ml_jobs
sudo docker system prune -f
sudo docker-compose -f /home/ubuntu/docker-composes/docker-compose.yaml up