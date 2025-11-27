import json
from urllib.parse import quote_plus
from faker import Faker

import pika

from mongoengine import connect, disconnect

from models import Contact

#password = 'Nikolai@'
#encoded_password = quote_plus(password)

#uri = f"mongodb+srv://nnizalov_db_user:{encoded_password}@clustergoit.z5anglb.mongodb.net/?retryWrites=true&w=majority&appName=ClusterGoIT"
# Create a new client and connect to the server
disconnect()
connect(db='hw08_02', host="mongodb://localhost:27017")

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='GOIT08HW02', exchange_type= 'direct')
channel.queue_declare(queue='GOIT08HW02_queue', durable=True)
channel.queue_bind(exchange='GOIT08HW02',queue='GOIT08HW02_queue')

fake = Faker('en-GB')

def create_contacts(nums: int):
    for i in range(nums):
        contact = Contact(fullname=fake.name(),email=fake.email(),message_sent=False)
        contact.save()
        channel.basic_publish(exchange='GOIT08HW02', routing_key='GOIT08HW02_queue', body=json.dumps(str(contact.id)).encode())
#print("[x] sent 'Hello World!'")
    connection.close()

if __name__ =='__main__':
    create_contacts(2)