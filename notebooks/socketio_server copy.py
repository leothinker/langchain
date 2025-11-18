import os

import eventlet
import requests
import socketio

print('Backend starting...')

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# OLLAMA_API_URL = 'http://ollama:11434/api/chat'
# MODEL_NAME = os.getenv('MODEL_NAME', 'mistral')


# def llm_res(prompt):
#     try:
#         print(f'Sending to Ollama: {prompt}')
#         body = {
#             'model': MODEL_NAME,
#             'messages': [{'role': 'user', 'content': prompt}],
#             'stream': False,
#         }
#         response = requests.post(OLLAMA_API_URL, json=body, timeout=120)
#         response.raise_for_status()
#         data = response.json()
#         return data.get('message', {}).get('content', 'No response from model.')
#     except requests.exceptions.RequestException as e:
#         print(f'Error talking to Ollama: {e}')
#         return 'Error: LLM backend not responding.'


@sio.event
def connect(sid, environ):
    print(f'Client connected: {sid}')
    sio.emit('message', {'user': 'System', 'text': 'A new user has joined the chatroom.'}, room=sid)


@sio.event
def message(sid, data):
    print(f'Message from {sid}: {data}')
    user = data.get('user', 'Anonymous')
    prompt = data.get('text', '')

    if not prompt:
        print('Empty prompt. Ignored.')
        return

    sio.emit('message', {'user': user, 'text': prompt})
    # response = llm_res(prompt)
    # bot_name = MODEL_NAME.capitalize()
    # sio.emit('message', {'user': bot_name, 'text': response, 'bot_name': bot_name})


@sio.event
def disconnect(sid):
    print(f'Client disconnected: {sid}')


if __name__ == '__main__':
    print('Server running on port 5000...')
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
