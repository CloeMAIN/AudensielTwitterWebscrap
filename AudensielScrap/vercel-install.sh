#!/bin/bash

pip install -r /vercel/path0/AudensielScrap/requirements.txt
python3 -m playwright install
sudo apt update && sudo apt upgrade chromium-browser