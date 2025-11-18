from datetime import datetime

import socketio
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

# 初始化 SocketIO 客户端
sio = socketio.Client()
ctx = get_script_run_ctx()


def initialize_session_state():
    """初始化 session state"""
    if 'connected' not in st.session_state:
        st.session_state.connected = False
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'online_users' not in st.session_state:
        st.session_state.online_users = []
    if 'current_room' not in st.session_state:
        st.session_state.current_room = 'general'


# SocketIO 事件处理
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
    """接收消息事件"""
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
    """用户加入事件"""
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
    """用户离开事件"""
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
    """更新在线用户列表"""
    st.session_state.online_users = data


def connect_to_server():
    """连接到 SocketIO 服务器"""
    try:
        if not st.session_state.connected:
            sio.connect('http://localhost:5000')
            # 设置用户名
            if st.session_state.username:
                sio.emit('set_username', {'username': st.session_state.username})
                # 加入默认房间
                sio.emit('join_room', {'room': st.session_state.current_room})
    except Exception as e:
        st.error(f'连接失败: {e}')


def disconnect_from_server():
    """断开与服务器的连接"""
    if st.session_state.connected:
        sio.disconnect()


def send_message():
    """发送消息"""
    message = st.session_state.message_input
    if message and st.session_state.connected:
        sio.emit('send_message', {'message': message})
        # 添加到本地消息列表
        message_data = {
            'username': st.session_state.username,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'type': 'sent',
        }
        st.session_state.messages.append(message_data)
        st.session_state.message_input = ''


def join_room(room_name):
    """加入房间"""
    if st.session_state.connected:
        sio.emit('join_room', {'room': room_name})
        st.session_state.current_room = room_name


def main():
    st.set_page_config(page_title='实时聊天室', page_icon='💬', layout='wide')

    initialize_session_state()

    st.title('💬 实时聊天室')

    # 侧边栏 - 用户信息和在线用户
    with st.sidebar:
        st.header('用户设置')

        # 用户名输入
        username = st.text_input(
            '用户名', value=st.session_state.username, placeholder='请输入您的用户名'
        )

        if username != st.session_state.username:
            st.session_state.username = username
            if st.session_state.connected and username:
                sio.emit('set_username', {'username': username})

        # 连接/断开连接按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button('连接', type='primary', disabled=st.session_state.connected):
                connect_to_server()
        with col2:
            if st.button('断开', disabled=not st.session_state.connected):
                disconnect_from_server()

        # 连接状态
        if st.session_state.connected:
            st.success('✅ 已连接')
        else:
            st.error('❌ 未连接')

        # 房间选择
        st.header('房间')
        rooms = ['general', 'tech', 'random', 'help']
        for room in rooms:
            if st.button(
                f'#{room}', key=f'room_{room}', disabled=room == st.session_state.current_room
            ):
                join_room(room)

        # 在线用户
        st.header('在线用户')
        for user in st.session_state.online_users:
            st.write(f'👤 {user}')

    # 主聊天区域
    col1, col2 = st.columns([3, 1])

    with col1:
        # 聊天消息显示区域
        st.header(f'聊天室: #{st.session_state.current_room}')

        # 消息容器
        messages_container = st.container(height=400)

        with messages_container:
            for msg in st.session_state.messages:
                # 根据消息类型设置不同的样式
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

        # 消息输入区域
        col_input, col_send = st.columns([4, 1])
        with col_input:
            st.text_input(
                '输入消息',
                key='message_input',
                placeholder='输入消息后按回车或点击发送',
                on_change=send_message,
                disabled=not st.session_state.connected,
            )
        with col_send:
            st.button('发送', on_click=send_message, disabled=not st.session_state.connected)

    with col2:
        st.header('聊天信息')
        st.metric('在线用户', len(st.session_state.online_users))
        st.metric('消息总数', len(st.session_state.messages))

        # 清空聊天记录按钮
        if st.button('清空聊天记录', type='secondary'):
            st.session_state.messages = []
            st.rerun()


if __name__ == '__main__':
    main()
