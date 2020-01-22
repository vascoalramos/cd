# coding: utf-8

import logging
import pickle
import zmq
from utils import *
import random

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


def main(ip, port):
    # create a logger for the client
    logger = logging.getLogger('Cooker')
    # setup zmq
    logger.info('Setup ZMQ')
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://{}:{}'.format(ip, port))

    while True:
        logger.info('Request <Order ready to  Cook> Task')
        p = pickle.dumps({"method": REQ_TASK_COOKER})
        socket.send(p)

        p = socket.recv()
        o = pickle.loads(p)
        while o == False:
            work(2)
            logger.info('Request <Order ready to  Cook> Task')
            p = pickle.dumps({"method": REQ_TASK_COOKER})
            socket.send(p)

            p = socket.recv()
            o = pickle.loads(p)
        logger.info('Received %s', o)

        for typeOfFood,quantity in o[1].items():
            print("%s : %d" % (typeOfFood,quantity))

        work(abs(random.gauss(3, pow(2, 2))))

        logger.info("Order ready to cooking queue")
        p = pickle.dumps({"method": TASK_READY_COOKER, "args": o})
        socket.send(p)

        p = socket.recv()
        o = pickle.loads(p)

        if not o:
            break

    socket.close()
    context.term()

    return 0


if __name__ == '__main__':
    main("127.0.0.1", "5001")
