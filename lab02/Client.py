# coding: utf-8

import logging
import pickle
import zmq
from utils import *
import random

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


def createOrder():
    chips = random.randint(1,5)
    drinks = random.randint(1,5)
    burgers = random.randint(1,5)
    return {"hamburger": burgers, "batata": chips, "bebida": drinks}

def main(ip, port):
    # create a logger for the client
    logger = logging.getLogger('Client')
    # setup zmq
    logger.info('Setup ZMQ')
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://{}:{}'.format(ip, port))

    logger.info('Request some food')
    p = pickle.dumps({"method": ORDER, "args": createOrder()})
    socket.send(p)

    p = socket.recv()
    order_id = pickle.loads(p)
    logger.info('Order ID: %s', order_id)

    logger.info('Pickup order %s', order_id)
    p = pickle.dumps({"method": PICKUP, "args": order_id})
    socket.send(p)

    p = socket.recv()
    o = pickle.loads(p)
    while o != order_id:
        work(2)
        logger.info('Pickup order %s', order_id)
        p = pickle.dumps({"method": PICKUP, "args": order_id})
        socket.send(p)

        p = socket.recv()
        o = pickle.loads(p)
    logger.info('Got %s', o)

    socket.close()
    context.term()

    return 0


if __name__ == '__main__':
    main("127.0.0.1", "5001")
