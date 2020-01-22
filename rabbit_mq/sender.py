import pika
import uuid
import pickle
from rpc import RPC, ORDER

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# create anonymous queue
result = channel.queue_declare(exclusive=True)
callback_queue = result.method.queue


def callback(ch, method, properties, body):
    if method.routing_key == 'orders':
        print("Got my order {}".format(pickle.load(body)))


channel.basic_consume(callback,
                      queue=callback_queue,
                      no_ack=True)

channel.basic_publish(exchange='',
                      routing_key='orders',
                      properties=pika.BasicProperties(reply_to=callback_queue,
                                                      correlation_id=str(uuid.uuid1())),
                      body=pickle.dumps(RPC(ORDER, {'hamburger': 2})))
print("Order placed")

channel.start_consuming()

connection.close()
