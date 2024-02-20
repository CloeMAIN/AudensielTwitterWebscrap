#!/bin/bash

# Installer les dépendances Python
pip install -r /vercel/path0/AudensielScrap/requirements.txt

# Installer Playwright
playwright install

#Installer dépendances 
playwright install-deps