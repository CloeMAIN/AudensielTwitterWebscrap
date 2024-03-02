#!/bin/bash

# Installer les dépendances Python
pip install -r /vercel/path0/AudensielScrap/requirements.txt

# Installer Playwright
python -m playwright install

# Installer les dépendances de Playwright
python -m playwright install-deps

# Lancer la construction de déploiement
npm run build