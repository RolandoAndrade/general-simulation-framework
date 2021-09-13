import socketio

sio = socketio.Server(cors_allowed_origins="*", async_mode='threading')
