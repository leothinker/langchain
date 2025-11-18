import queue
from collections import deque

import socketio
import streamlit as st

URL = 'http://localhost:5000'
MSG_LIMIT = 100


if 'msg_queue' not in st.session_state:
    st.session_state.msg_queue = queue.Queue()


if 'sio_client' not in st.session_state:
    st.session_state.sio_client = socketio.Client(reconnection_attempts=3, reconnection_delay=5)
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = deque(maxlen=MSG_LIMIT)

sio = st.session_state.sio_client


def handle_connect(q):
    print('Frontend: Connected to backend.')
    q.put({'event': 'connect'})


def handle_connect_error(q, data):
    print(f'Frontend: Connection error: {data}')
    q.put({'event': 'connect_error'})


def handle_disconnect(q):
    print('Frontend: Disconnected from backend.')
    q.put({'event': 'disconnect'})


def handle_message(q, data):
    print(f'Frontend: Received message: {data}')
    q.put({'event': 'message', 'data': data})


# Handling managers
if 'handlers_registered' not in st.session_state:
    q = st.session_state.msg_queue
    sio.on('connect', lambda: handle_connect(q))
    sio.on('connect_error', lambda data: handle_connect_error(q, data))
    sio.on('disconnect', lambda: handle_disconnect(q))
    sio.on('message', lambda data: handle_message(q, data))
    st.session_state.handlers_registered = True

# Queue events
needs_rerun = False
while not st.session_state.msg_queue.empty():
    msg = st.session_state.msg_queue.get_nowait()
    event_type = msg.get('event')

    if event_type == 'message':
        data = msg.get('data', {})
        u = data.get('user', 'Anonymous')
        t = data.get('text', '')
        bot_name = data.get('bot_name', 'Mistral')
        a = 'User' if u != bot_name else 'Mistral7'
        st.session_state.chat_messages.append({'u': u, 't': t, 'a': a})
        needs_rerun = True
    elif event_type in ['connect', 'disconnect', 'connect_error']:
        needs_rerun = True

if needs_rerun:
    st.rerun()

# UI
st.set_page_config(page_title='LLM Chat', layout='wide')
st.title('Chat with Mistral')


@st.fragment(run_every='1s')
def test():
    if not st.session_state.user_name:
        st.header('Enter your name')
        name = st.text_input('Name', key='name_input')
        if st.button('Join'):
            if name:
                st.session_state.user_name = name
                st.rerun()
            else:
                st.warning('Name is required.')
    else:
        if sio.connected:
            st.success(f'Connected as {st.session_state.user_name}')

            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.chat_messages:
                    with st.chat_message(name=msg['u'], avatar='user'):
                        st.write(msg['t'])

        else:
            st.info('You are not connected to the server.')
            # Disable the button if a connection attempt is in progress
            is_connecting = sio.eio.state == 'connecting'
            if st.button('Connect', disabled=is_connecting):
                try:
                    sio.connect(URL, transports=['websocket'])
                except socketio.exceptions.ConnectionError as e:
                    st.error(f'Connection failed: {e}. Is the backend running?')
                    # No need to rerun here, the event handler will do it.


test()

prompt = st.chat_input('Type a message')
if prompt:
    sio.emit('message', {'user': st.session_state.user_name, 'text': prompt})
