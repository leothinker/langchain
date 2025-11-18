# chat_socketio.py
import time
import uuid
from datetime import datetime

import socketio
import streamlit as st

# 全局 Socket.IO 客户端
sio = socketio.Client()

# 页面配置
st.set_page_config(page_title='Socket.IO 聊天室', page_icon='💬', layout='wide')

# 初始化 session state
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]
if 'username' not in st.session_state:
    st.session_state.username = f'用户_{st.session_state.user_id}'
if 'online_users' not in st.session_state:
    st.session_state.online_users = []
if 'message_input' not in st.session_state:
    st.session_state.message_input = ''
if 'connection_error' not in st.session_state:
    st.session_state.connection_error = None


# Socket.IO 事件处理
@sio.event
def connect():
    """连接成功回调"""
    st.session_state.connected = True
    st.session_state.connection_error = None

    # 加入聊天室
    sio.emit(
        'join_chat', {'user_id': st.session_state.user_id, 'username': st.session_state.username}
    )


@sio.event
def disconnect():
    """断开连接回调"""
    st.session_state.connected = False


@sio.event
def connect_error(data):
    """连接错误回调"""
    st.session_state.connected = False
    st.session_state.connection_error = f'连接错误: {data}'


@sio.event
def user_join(data):
    """用户加入事件"""
    st.session_state.messages.append(
        {'type': 'system', 'content': data['message'], 'timestamp': data['timestamp']}
    )
    st.session_state.online_users = data.get('online_users', [])


@sio.event
def user_leave(data):
    """用户离开事件"""
    st.session_state.messages.append(
        {'type': 'system', 'content': data['message'], 'timestamp': data['timestamp']}
    )
    st.session_state.online_users = data.get('online_users', [])


@sio.event
def user_list(data):
    """用户列表事件"""
    st.session_state.online_users = data['users']


@sio.event
def new_message(data):
    """新消息事件"""
    st.session_state.messages.append(
        {
            'type': 'chat',
            'username': data['username'],
            'content': data['content'],
            'timestamp': data['timestamp'],
            'is_own': data['user_id'] == st.session_state.user_id,
        }
    )


@sio.event
def private_message(data):
    """私信事件"""
    st.session_state.messages.append(
        {
            'type': 'private',
            'username': data['from_username'],
            'content': data['content'],
            'timestamp': data['timestamp'],
            'is_own': False,
        }
    )


def connect_socketio():
    """连接 Socket.IO 服务器"""
    if st.session_state.connected:
        return

    try:
        # 重置错误状态
        st.session_state.connection_error = None

        # 连接服务器
        sio.connect('http://localhost:8000', wait_timeout=10)

    except Exception as e:
        st.session_state.connection_error = f'连接失败: {e}'


def disconnect_socketio():
    """断开 Socket.IO 连接"""
    if st.session_state.connected:
        sio.disconnect()
    st.session_state.connected = False


def send_message():
    """发送消息"""
    if st.session_state.connected and st.session_state.message_input.strip():
        try:
            sio.emit('send_message', {'content': st.session_state.message_input.strip()})
            st.session_state.message_input = ''
        except Exception as e:
            st.session_state.connection_error = f'发送消息失败: {e}'


def send_private_message(target_user_id, content):
    """发送私信"""
    if st.session_state.connected and content.strip():
        try:
            sio.emit(
                'send_private_message',
                {'target_user_id': target_user_id, 'content': content.strip()},
            )
            return True
        except Exception as e:
            st.session_state.connection_error = f'发送私信失败: {e}'
            return False
    return False


# 页面标题
st.title('💬 Socket.IO 聊天室')

# 显示连接错误
if st.session_state.connection_error:
    st.error(st.session_state.connection_error)

# 侧边栏 - 用户信息和在线用户
with st.sidebar:
    st.header('用户设置')

    # 用户名设置
    new_username = st.text_input('用户名', value=st.session_state.username, key='username_input')
    if new_username != st.session_state.username:
        st.session_state.username = new_username
        if st.session_state.connected:
            st.warning('修改用户名需要重新连接')

    # 连接控制
    col1, col2 = st.columns(2)
    with col1:
        if not st.session_state.connected:
            if st.button('连接聊天室', use_container_width=True, key='connect_btn'):
                connect_socketio()
        else:
            if st.button('断开连接', use_container_width=True, key='disconnect_btn'):
                disconnect_socketio()

    with col2:
        if st.button('清空聊天', use_container_width=True, key='clear_btn'):
            st.session_state.messages = []

    # 在线用户列表
    st.header(f'在线用户 ({len(st.session_state.online_users)})')
    for user in st.session_state.online_users:
        if user['user_id'] != st.session_state.user_id:
            st.write(f'👤 {user["username"]}')

# 主聊天区域
col1, col2 = st.columns([3, 1])

with col1:
    # 聊天消息显示区域
    chat_container = st.container(height=400, border=True)

    with chat_container:
        for msg in st.session_state.messages[-50:]:
            if msg['type'] == 'system':
                st.markdown(
                    f"<div style='text-align: center; color: #666; font-style: italic; "
                    f'margin: 5px 0; padding: 5px; background-color: #f0f0f0; '
                    f"border-radius: 10px;'>{msg['content']}</div>",
                    unsafe_allow_html=True,
                )
            elif msg['type'] == 'chat' or msg['type'] == 'private':
                message_style = (
                    'text-align: right; background-color: #e3f2fd; margin: 5px 0; '
                    'padding: 8px 12px; border-radius: 10px; margin-left: 20%;'
                    if msg.get('is_own', False)
                    else 'text-align: left; background-color: #f5f5f5; margin: 5px 0; '
                    'padding: 8px 12px; border-radius: 10px; margin-right: 20%;'
                )

                prefix = '🔒 ' if msg['type'] == 'private' else ''
                timestamp = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M:%S')

                st.markdown(
                    f"<div style='{message_style}'>"
                    f'<small><b>{prefix}{msg["username"]}</b> - {timestamp}</small><br/>'
                    f'{msg["content"]}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

with col2:
    # 快速操作区域
    st.header('快捷操作')

    # 私信功能
    if st.session_state.online_users:
        target_users = [
            user
            for user in st.session_state.online_users
            if user['user_id'] != st.session_state.user_id
        ]

        if target_users:
            target_user = st.selectbox(
                '选择私信用户',
                target_users,
                format_func=lambda x: x['username'],
                key='target_user_select',
            )

            private_msg = st.text_area('私信内容', height=100, key='private_msg')
            if st.button('发送私信', key='send_private_btn') and private_msg.strip():
                if send_private_message(target_user['user_id'], private_msg.strip()):
                    st.success('私信发送成功！')
                    # 清空私信输入框
                    st.session_state.private_msg = ''

# 消息输入区域
st.divider()

input_col1, input_col2 = st.columns([4, 1])
with input_col1:
    message_input = st.text_input(
        '输入消息',
        value=st.session_state.message_input,
        key='message_input',
        placeholder='输入消息内容...',
        disabled=not st.session_state.connected,
    )

with input_col2:
    send_btn = st.button(
        '发送',
        use_container_width=True,
        disabled=not st.session_state.connected,
        on_click=send_message,
        key='send_msg_btn',
    )

# 连接状态指示器
status_color = '🟢' if st.session_state.connected else '🔴'
st.caption(
    f'{status_color} 连接状态: {"已连接" if st.session_state.connected else "未连接"} | '
    f'用户ID: {st.session_state.user_id}'
)

# 自动刷新（为了实时接收消息）
if st.session_state.connected:
    time.sleep(0.1)
    st.rerun()

# 使用说明
with st.expander('使用说明'):
    st.markdown("""
    1. **连接聊天室**: 在侧边栏点击"连接聊天室"按钮
    2. **发送消息**: 在下方输入框输入消息并点击发送
    3. **私信功能**: 在右侧选择用户并发送私密消息
    4. **用户管理**: 在侧边栏查看在线用户列表

    **注意**: 确保后端 Socket.IO 服务器正在运行在 `localhost:8000`
    """)
