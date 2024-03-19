# Utiliser une image de base avec Python
FROM python:3.8

WORKDIR /AudensielTwitterWebscrap

# Copier les fichiers nécessaires dans le conteneur
COPY AudensielScrap/requirements.txt .
COPY AudensielScrap/ .

# Installation des dépendances Python
RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps

# Expose port 8000 for Django app
EXPOSE 8000

# Define the command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]