# Étape de construction du frontend
FROM node:14 as build

WORKDIR /app

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ ./

RUN npm run build

# Étape de construction du backend
FROM python:3.8

WORKDIR /app

COPY --from=build /app/build ./static
COPY AudensielScrap/requirements.txt .

RUN pip install -r requirements.txt

COPY AudensielScrap/ .

EXPOSE 8000

CMD ["python", "manage.py runserver"]