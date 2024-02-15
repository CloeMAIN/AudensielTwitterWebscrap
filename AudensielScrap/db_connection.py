import pymongo

url = "mongodb+srv://cloe:Webscrap23@cluster0.qnvy73r.mongodb.net/?authMechanism=SCRAM-SHA-1"
client = pymongo.MongoClient(url)

db = client['TestNicoco']