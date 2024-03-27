import pymongo
import os
# Connexion à la base de données MongoDB à l'aide du nom du service MongoDB défini dans Docker Compose
# client = pymongo.MongoClient("mongodb+srv://cloe:Webscrap23@cluster0.qnvy73r.mongodb.net/?authMechanism=SCRAM-SHA-1")
client = pymongo.MongoClient(os.getenv('MONGO_URL'))
# Sélection de la base de données
db = client['Tweets']
