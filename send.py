import pika
import json
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

def publish(method,body):
    #publishing order to RabitMq
    channel.queue_declare(queue='order')
    channel.basic_publish(exchange='', routing_key='order', body= json.dumps(body))
    print(f"Sent the Request---{body}'")
    connection.close()
