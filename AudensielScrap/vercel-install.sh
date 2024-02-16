#!/bin/bash

# Installer les dépendances Python
pip install -r /vercel/path0/AudensielScrap/requirements.txt

# Installer Playwright
PLAYWRIGHT_BROWSERS_PATH python -m playwright install