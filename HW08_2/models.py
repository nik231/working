from urllib.parse import quote_plus

from mongoengine import *


password = 'Nikolai@'
encoded_password = quote_plus(password)

uri = f"mongodb+srv://nnizalov_db_user:{encoded_password}@clustergoit.z5anglb.mongodb.net/?retryWrites=true&w=majority&appName=ClusterGoIT"
# Create a new client and connect to the server
connect(db="hw_08_02", host=uri)

class Contact(Document):
    fullname = StringField(max_length=150)
    email = StringField(max_length=150)
    message_sent = BooleanField(default=False)
    meta = {"collection":"Contacts" }
