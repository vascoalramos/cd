# coding: utf-8

import logging
import pickle
import zmq
from utils import *
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


def main(ip, port):
    # create a logger for the client
    logger = logging.getLogger('Clerk')
    # setup zmq
    logger.info('Setup ZMQ')
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://{}:{}'.format(ip, port))

    while True:
        logger.info('Request <Meal Ready to Deliver> Task')
        p = pickle.dumps({"method": REQ_TASK_CLERK})
        socket.send(p)

        p = socket.recv()
        o = pickle.loads(p)

        while o == False:
            work(2)
            logger.info('Request <Meal Ready to Deliver> Task')
            p = pickle.dumps({"method": REQ_TASK_CLERK})
            socket.send(p)

            p = socket.recv()
            o = pickle.loads(p)
        logger.info('Received %s', o)

        work(3)

        logger.info("Meal Added to Delivery Queue")
        p = pickle.dumps({"method": TASK_READY_CLERK, "args": o})
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
