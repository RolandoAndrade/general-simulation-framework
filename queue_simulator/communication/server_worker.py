import threading

import zmq


class ServerWorker(threading.Thread):
    """ServerWorker"""

    def __init__(self, context):
        threading.Thread.__init__(self)
        self.context = context

    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        print('Worker started')
        while True:
            ident, msg = worker.recv_multipart()
            print('Worker received %s from %s' % (msg, ident))
            worker.send_multipart([ident, msg])

        worker.close()