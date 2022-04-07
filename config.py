import pymongo
import certifi

# url stored on a variable
mongo_url="mongodb+srv://Arturoexe:Tloz652631@cluster0.dcwf9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# Creates the connection
client=pymongo.MongoClient(mongo_url,tlsCAfile=certifi.where())

# get the data base
db = client.get_database("Youngster_database")