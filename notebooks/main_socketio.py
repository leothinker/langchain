# main_socketio.py
import uuid
from datetime import datetime

import socketio
from fastapi import FastAPI

# 创建 Socket.IO 服务器
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()

# 将 Socket.IO 应用挂载到 FastAPI
socket_app = socketio.ASGIApp(sio, app)

# 存储用户信息
users: dict[str, dict] = {}
rooms: dict[str, dict] = {}


@sio.event
async def connect(sid, _environ, _auth):
    print(f'客户端 {sid} 已连接')


@sio.event
async def disconnect(sid):
    if sid in users:
        user_info = users[sid]
        username = user_info['username']
        user_id = user_info['user_id']

        # 通知其他用户该用户已离开
        await sio.emit(
            'user_leave',
            {
                'user_id': user_id,
                'username': username,
                'message': f'{username} 离开了聊天室',
                'timestamp': datetime.now().isoformat(),
                'online_users': len(users),
            },
            skip_sid=sid,
        )

        # 从用户列表中移除
        del users[sid]

    print(f'客户端 {sid} 已断开连接')


@sio.event
async def join_chat(sid, data):
    """用户加入聊天室"""
    user_id = data.get('user_id', str(uuid.uuid4())[:8])
    username = data.get('username', f'用户_{user_id}')

    # 存储用户信息
    users[sid] = {'user_id': user_id, 'username': username, 'joined_at': datetime.now().isoformat()}

    # 通知所有用户有新用户加入
    await sio.emit(
        'user_join',
        {
            'user_id': user_id,
            'username': username,
            'message': f'{username} 加入了聊天室',
            'timestamp': datetime.now().isoformat(),
            'online_users': len(users),
        },
    )

    # 发送当前在线用户列表给新用户
    online_users = [
        {'user_id': info['user_id'], 'username': info['username'], 'joined_at': info['joined_at']}
        for info in users.values()
    ]

    await sio.emit('user_list', {'users': online_users}, room=sid)

    return {'status': 'ok', 'user_id': user_id}


@sio.event
async def send_message(sid, data):
    """发送消息"""
    if sid not in users:
        return {'status': 'error', 'message': '用户未加入聊天室'}

    user_info = users[sid]
    message_data = {
        'type': 'chat_message',
        'user_id': user_info['user_id'],
        'username': user_info['username'],
        'content': data['content'],
        'timestamp': datetime.now().isoformat(),
    }

    # 广播消息给所有用户
    await sio.emit('new_message', message_data)

    return {'status': 'ok'}


@sio.event
async def send_private_message(sid, data):
    """发送私信"""
    if sid not in users:
        return {'status': 'error', 'message': '用户未加入聊天室'}

    target_user_id = data['target_user_id']
    content = data['content']

    # 查找目标用户的 sid
    target_sid = None
    for user_sid, user_info in users.items():
        if user_info['user_id'] == target_user_id:
            target_sid = user_sid
            break

    if not target_sid:
        return {'status': 'error', 'message': '目标用户不在线'}

    user_info = users[sid]
    private_message = {
        'type': 'private_message',
        'from_user_id': user_info['user_id'],
        'from_username': user_info['username'],
        'content': content,
        'timestamp': datetime.now().isoformat(),
    }

    # 发送私信给目标用户
    await sio.emit('private_message', private_message, room=target_sid)

    return {'status': 'ok'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(socket_app, host='0.0.0.0', port=8000)
