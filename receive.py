import pika
import json
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.secret_key = "secretkey"
app.config["MONGO_URI"] = "mongodb://localhost:27017/pizza_house"

mongo = PyMongo(app)


def on_message_received(ch,mthod,properties,body):
    print(f"Received new order request : {body}")
    data = json.dumps(body)
    print("order created in consumer")

    if data['method'] == 'Order Created':
        print("Order created")
        order = data['body']
        order_id = mongo.db.orders.insert({'order':order})
        print(f"Order successful ,Order ID - {str(order_id)}")


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue = 'order')
channel.basic_consume(queue='order',auto_ack=True,on_message_callback=on_message_received)
print("Started consuming. To exit print CTRL+C")
channel.start_consuming()
channel.close()