import os
import sys
import json
import time


import pika
from mongoengine import connect, disconnect

from models import Contact

#password = 'Nikolai@'
#encoded_password = quote_plus(password)

##uri = f"mongodb+srv://nnizalov_db_user:{encoded_password}@clustergoit.z5anglb.mongodb.net/?retryWrites=true&w=majority&appName=ClusterGoIT"
# Create a new client and connect to the server
disconnect()
connect(db="hw08_02", host="mongodb://localhost:27017")



def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='GOIT08HW02_queue', durable=True)

    def callback(ch, method, properties, body):
        primary_key = json.loads(body.decode())
        print(f'Sending email to {Contact.objects(id=primary_key).first().fullname}')
        contact = Contact.objects(id=primary_key).first()
        if contact:
            contact.update(message_sent=True)
        contact.reload()
        time.sleep(0.5)
        print(f" [x] Completed{method.delivery_tag} task")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='GOIT08HW02_queue', on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
