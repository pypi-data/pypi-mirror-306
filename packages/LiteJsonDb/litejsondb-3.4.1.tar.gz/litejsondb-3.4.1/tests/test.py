import LiteJsonDb

# Initialize the database with encryption enabled
db = LiteJsonDb.JsonDB(crypted=True)

db.export_to_csv("users")