import pika
import pickle
from rpc import RPC, ORDER
import time
from comida import Hamburger

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#result = channel.queue_declare(queue='batatas', exclusive=True)
#result = channel.queue_declare(queue='hamburger', exclusive=True)
#result = channel.queue_declare(queue='cocacola', exclusive=True)
result = channel.queue_declare(queue='orders', exclusive=True)

print(' [*] Waiting for orders. To exit press CTRL+C')


def callback(ch, method, properties, body):
    order = pickle.load(body)  # Type RPC

    print("%r:%r" % (method.routing_key, order))

    #time.sleep(2)

    if method.routing_key == 'orders':
        channel.basic_publish(exchange='',
                              routing_key=properties.reply_to,
                              properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                              body=pickle.dumps(Hamburger()))


#channel.basic_consume(callback, queue='batatas')
#channel.basic_consume(callback, queue='hamburger')
#channel.basic_consume(callback, queue='cocacola')
channel.basic_consume(callback, queue='orders')

channel.start_consuming()
