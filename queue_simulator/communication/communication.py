import json
import zmq
import os
import random

# Define the port you want to use
port = os.getenv("zmq_output", default="4001")
# Define the connection type your want to use (tcp, ipc...)
connection_type = os.getenv("connection_type", default="tcp")
# Define the host. Default is to publish on all.
host = os.getenv("host", default="*")
# Set the topic of the stream
topicfilter = os.getenv("topic", default="rand")
Publishport = connection_type + "://" + host + ":" + port

# Create and bind to the Publishport
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(Publishport)
# A little bit of logging
print("Sending on topic:" + topicfilter, flush=True)

if __name__ == "__main__":
    while (True):
        # Create a random number
        msg = {"num": random.randint(0, 10)}
        # Send this string
        socket.send_string("%s %s" % (topicfilter, json.dumps(msg)))