# Utiliser une image de base avec Python
FROM python:3.8
### Plus besoin parceque playwright je suppose
# # Installation de Chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
# RUN apt-get update && apt-get install -y google-chrome-stable

###Test sans
# # Installation du Chrome WebDriver
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# # Installation de Node.js et npm
# RUN apt-get update && apt-get install -y nodejs npm
# RUN apt-get update && apt-get install -y xvfb

###Added to requirements.txt
# # Installation de Playwright
# RUN npm install -g playwright

# # Installation des navigateurs requis par Playwright
# RUN playwright install

# Configuration du répertoire de travail
WORKDIR /AudensielTwitterWebscrap

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt .
COPY AudensielScrap/ .

# Installation des dépendances Python
RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps

# Expose port 8000 for Django app
EXPOSE 8000

# Define the command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]