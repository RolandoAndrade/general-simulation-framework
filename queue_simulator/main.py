from typing import List, Dict

import eventlet
import socketio

from dynamic_system.future_event_list import Scheduler
from experiments.experiment_builders import DiscreteEventExperiment
from queue_simulator.source import Source
from test.mocks.dynamic_system_mock import DynamicSystemMock

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

serial = 0


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    session: Dict[str, List]
    with sio.session(sid) as session:
        session['experiment'] = []


@sio.event
def CREATE_NODE(sid, data):
    print('message ', sid, data)
    session: Dict[str, List]
    with sio.session(sid) as session:
        session['experiment'].append(data)
        print(session)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 4000)), app)
