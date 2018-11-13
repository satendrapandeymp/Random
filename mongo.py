import pymongo

# connecting to the mongo database
mongo = pymongo.MongoClient("mongodb://localhost:27017")

# printing database names
print mongo.list_database_names()

# now I'm going to use myTests Database
mydb = mongo["myTests"]

# will find my customer columns
mycol = mydb["customers"]

# will insert single document
mydoc = {"name" : "Satyendra", "address" : "Kanpur, India, 208016"}
mycol.insert_one(mydoc)

# Will insert many data in database
mydoc =    [{"name" : "Ram", "address" : "Kanpur, India, 208016"}, \
            {"name" : "Narendra", "address" : "Kanpur, India, 208016"}, \
            {"name" : "Shyam", "address" : "Kanpur, India, 208016"}, \
            {"name" : "Mohan", "address" : "Kanpur, India, 208016"}, ]

mycol.insert_many(mydoc)

# update one row
mycol.update_one({"name" : {"$regex" : "^S.+$"}} , {"$set": {"address" : "Delhi India...."}})

# will query to find existing columns in there shorted by name
for i in mycol.find({"name" : {"$regex" : "^.+$"}, "address": {"$regex" : "^.{11}.+$"}}, {"_id" : 0 }).sort("name"):
    print i


# to delete all the data from the column
mycol.delete_many({})