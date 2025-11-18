import uuid
from datetime import datetime

import socketio
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

APP_TITLE = 'Socket.IO Chat'
APP_ICON = '💬'
USER_ID_COOKIE = 'user_id'


def get_or_create_user_id() -> str:
    """Get the user ID from session state or URL parameters, or create a new one if it doesn't exist."""
    # Check if user_id exists in session state
    if USER_ID_COOKIE in st.session_state:
        return st.session_state[USER_ID_COOKIE]

    # Try to get from URL parameters using the new st.query_params
    if USER_ID_COOKIE in st.query_params:
        user_id = st.query_params[USER_ID_COOKIE]
        st.session_state[USER_ID_COOKIE] = user_id
        return user_id

    # Generate a new user_id if not found
    user_id = str(uuid.uuid4())

    # Store in session state for this session
    st.session_state[USER_ID_COOKIE] = user_id

    # Also add to URL parameters so it can be bookmarked/shared
    st.query_params[USER_ID_COOKIE] = user_id

    return user_id


st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    menu_items={},
)

# Hide the streamlit upper-right chrome
st.html(
    """
    <style>
    [data-testid="stStatusWidget"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
        }
    </style>
    """,
)
if st.get_option('client.toolbarMode') != 'minimal':
    st.set_option('client.toolbarMode', 'minimal')
    st.rerun()

# Get or create user ID
user_id = get_or_create_user_id()
if 'sio_client' not in st.session_state:
    st.session_state.sio_client = socketio.Client(reconnection_attempts=3, reconnection_delay=5)
sio = st.session_state.sio_client
ctx = get_script_run_ctx()

if 'thread_id' not in st.session_state:
    thread_id = st.query_params.get('thread_id')
    if not thread_id:
        thread_id = str(uuid.uuid4())
        messages = []
    else:
        try:
            messages = []
        except Exception:
            st.error('No message history found for this Thread ID.')
            messages = []
    st.session_state.messages = messages
    st.session_state.thread_id = thread_id

if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'online_users' not in st.session_state:
    st.session_state.online_users = []
if 'current_room' not in st.session_state:
    st.session_state.current_room = 'general'


@sio.event
def connect():
    add_script_run_ctx(ctx=ctx)
    st.session_state.connected = True
    print('连接到服务器')


@sio.event
def disconnect():
    add_script_run_ctx(ctx=ctx)
    st.session_state.connected = False
    print('与服务器断开连接')


@sio.event
def receive_message(data):
    add_script_run_ctx(ctx=ctx)

    message_data = {
        'username': data['username'],
        'message': data['message'],
        'timestamp': data['timestamp'],
        'type': 'received',
    }
    st.session_state.messages.append(message_data)


@sio.event
def user_joined(data):
    add_script_run_ctx(ctx=ctx)
    message_data = {
        'username': '系统',
        'message': data['message'],
        'timestamp': data['timestamp'],
        'type': 'system',
    }
    st.session_state.messages.append(message_data)


@sio.event
def user_left(data):
    add_script_run_ctx(ctx=ctx)
    message_data = {
        'username': '系统',
        'message': data['message'],
        'timestamp': data['timestamp'],
        'type': 'system',
    }
    st.session_state.messages.append(message_data)


@sio.event
def online_users(data):
    add_script_run_ctx(ctx=ctx)
    st.session_state.online_users = data


def connect_to_server():
    """连接到 SocketIO 服务器"""
    try:
        if not st.session_state.connected:
            sio.connect('http://localhost:2024/socket.io/')
            if st.session_state.username:
                sio.emit('set_username', {'username': st.session_state.username})
                sio.emit('join_room', {'room': st.session_state.current_room})
    except Exception as e:
        st.error(f'连接失败: {e}')


def disconnect_from_server():
    """断开与服务器的连接"""
    if st.session_state.connected:
        sio.disconnect()


def send_message(message):
    """发送消息"""
    # message = st.session_state.message_input
    if message and st.session_state.connected:
        sio.emit('send_message', {'message': message})


def join_room(room_name):
    """加入房间"""
    if st.session_state.connected:
        sio.emit('join_room', {'room': room_name})
        st.session_state.current_room = room_name


# Config options
with st.sidebar:
    st.header(f'{APP_ICON} {APP_TITLE}')

    if st.button(':material/chat: New Chat', use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    with st.popover(':material/settings: Settings', use_container_width=True):
        # Display user ID (for debugging or user information)
        st.text_input('User ID (read-only)', value=user_id, disabled=True)

    username = st.text_input(
        'Username', value=st.session_state.username, placeholder='Please enter your username'
    )

    if username != st.session_state.username:
        st.session_state.username = username
        if st.session_state.connected and username:
            sio.emit('set_username', {'username': username})

    if st.button(
        'Connect', type='primary', disabled=st.session_state.connected, use_container_width=True
    ):
        connect_to_server()

    if st.button('断开', disabled=not st.session_state.connected, use_container_width=True):
        disconnect_from_server()

    if st.session_state.connected:
        st.success('✅ Connected')
    else:
        st.error('❌ Not connected')


@st.fragment(run_every='1s')
def draw_messages():
    for msg in st.session_state.messages:
        if msg['type'] == 'sent':
            with st.chat_message('user', avatar='👤'):
                st.write(f'**{msg["username"]}**')
                st.write(msg['message'])
                st.caption(
                    f'发送于 {datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")}'
                )

        elif msg['type'] == 'received':
            with st.chat_message('human', avatar='👥'):
                st.write(f'**{msg["username"]}**')
                st.write(msg['message'])
                st.caption(
                    f'发送于 {datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")}'
                )

        elif msg['type'] == 'system':
            with st.chat_message('assistant', avatar='ℹ️'):
                st.info(msg['message'])
                st.caption(
                    f'系统消息 {datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")}'
                )


draw_messages()


# Generate new message if the user provided new input
if user_input := st.chat_input():
    send_message(user_input)
