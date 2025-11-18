import json
import time
import uuid
from datetime import datetime
from threading import Thread

import streamlit as st
import websocket
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

APP_TITLE = 'WebSocket Chat'
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

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'assistant', 'content': "Let's start chatting! 👇"}]


# 初始化 session state
if 'ws' not in st.session_state:
    st.session_state.ws = None
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]
if 'username' not in st.session_state:
    st.session_state.username = f'用户_{st.session_state.user_id}'
if 'message_input' not in st.session_state:
    st.session_state.message_input = ''


def on_close(_wsapp, close_status_code, close_msg):
    """处理 WebSocket 关闭"""
    st.session_state.connected = False
    st.session_state.ws = None
    print('on_close args:')
    if close_status_code or close_msg:
        print('close status code: ' + str(close_status_code))
        print('close message: ' + str(close_msg))


ctx = get_script_run_ctx()


def on_message(_wsapp, message):
    add_script_run_ctx(ctx=ctx)
    """处理接收到的 WebSocket 消息"""
    try:
        data = json.loads(message)
        message_type = data.get('type', '')

        if message_type == 'chat_message':
            # 处理聊天消息
            new_message = {
                'type': 'chat',
                'username': data['username'],
                'content': data['content'],
                'timestamp': data['timestamp'],
                'is_own': data['user_id'] == st.session_state.user_id,
            }
            st.session_state.messages.append(new_message)

        elif message_type == 'user_join':
            # 处理用户加入通知
            st.session_state.messages.append(
                {'type': 'system', 'content': data['message'], 'timestamp': data['timestamp']}
            )
            st.session_state.online_users = data.get('users', [])

        elif message_type == 'user_leave':
            # 处理用户离开通知
            st.session_state.messages.append(
                {'type': 'system', 'content': data['message'], 'timestamp': data['timestamp']}
            )
            st.session_state.online_users = data.get('users', [])

        elif message_type == 'private_message':
            # 处理私信
            st.session_state.messages.append(
                {
                    'type': 'private',
                    'username': data['from_username'],
                    'content': data['content'],
                    'timestamp': data['timestamp'],
                    'is_own': False,
                }
            )

    except Exception as e:
        st.error(f'处理消息时出错: {e}')


def connect_websocket():
    """连接 WebSocket 服务器"""
    if st.session_state.ws and st.session_state.connected:
        return

    try:
        ws_url = f'ws://localhost:8000/ws/{st.session_state.user_id}?username={st.session_state.username}'
        st.session_state.ws = websocket.WebSocketApp(
            ws_url, on_message=on_message, on_close=on_close
        )

        # 在新线程中运行 WebSocket
        def run_ws():
            add_script_run_ctx(ctx=ctx)
            st.session_state.ws.run_forever()

        ws_thread = Thread(target=run_ws, daemon=True)
        # add_script_run_ctx(ws_thread, get_script_run_ctx())
        ws_thread.start()

        # 等待连接建立
        time.sleep(1)
        st.session_state.connected = True
        st.success('连接成功！')

    except Exception as e:
        st.error(f'连接失败: {e}')


def disconnect_websocket():
    """断开 WebSocket 连接"""
    if st.session_state.ws:
        st.session_state.ws.close()
    st.session_state.connected = False
    st.session_state.ws = None


def send_message(message_input):
    """发送消息"""
    if st.session_state.connected and st.session_state.ws and message_input.strip():
        message_data = {
            'type': 'chat_message',
            'content': message_input.strip(),
            'timestamp': datetime.now().isoformat(),
        }

        try:
            st.session_state.ws.send(json.dumps(message_data))
            # 清空输入框
            message_input = ''
        except Exception as e:
            st.error(f'发送消息失败: {e}')


# Config options
with st.sidebar:
    st.header(f'{APP_ICON} {APP_TITLE}')

    new_username = st.text_input('用户名', value=st.session_state.username, key='username_input')
    if new_username != st.session_state.username:
        st.session_state.username = new_username
        if st.session_state.connected:
            st.warning('修改用户名需要重新连接')

    if st.button(':material/chat: New Chat', use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    # 连接控制
    if not st.session_state.connected:
        if st.button('连接聊天室', use_container_width=True):
            connect_websocket()
    else:
        if st.button('断开连接', use_container_width=True):
            disconnect_websocket()

    # 连接状态指示器
    status_color = '🟢' if st.session_state.connected else '🔴'
    st.caption(
        f'{status_color} 连接状态: {"已连接" if st.session_state.connected else "未连接"} | '
        f'用户ID: {st.session_state.user_id}'
    )


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message('user'):
        st.markdown(message['content'])


# Generate new message if the user provided new input
if user_input := st.chat_input():
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    st.chat_message('human').write(user_input)
    # TODO: send websocket message
    send_message(user_input)

    # # Display assistant response in chat message container
    # with st.chat_message('assistant'):
    #     message_placeholder = st.empty()
    #     full_response = ''
    #     assistant_response = 'Hello there! How can I assist you today?'
    #     # Simulate stream of response with milliseconds delay
    #     for chunk in assistant_response.split():
    #         full_response += chunk + ' '
    #         time.sleep(0.05)
    #         # Add a blinking cursor to simulate typing
    #         message_placeholder.markdown(full_response + '▌')
    #     message_placeholder.markdown(full_response)
    # # Add assistant response to chat history
    # st.session_state.messages.append({'role': 'assistant', 'content': full_response})
