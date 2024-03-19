import pymongo

# Connexion à la base de données MongoDB à l'aide du nom du service MongoDB défini dans Docker Compose
client = pymongo.MongoClient("mongodb://mongo:27017/")

# Sélection de la base de données
db = client['Tweets']
