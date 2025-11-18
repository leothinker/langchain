from datetime import datetime

import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(
    sio, static_files={'/': {'content_type': 'text/html', 'filename': 'index.html'}}
)

connected_users = {}
rooms = {}


@sio.event
def connect(sid, _environ):
    print('connect ', sid)
    connected_users[sid] = {'sid': sid, 'username': None}


@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    if sid in connected_users:
        username = connected_users[sid].get('username')
        print(f'User {username} ({sid}) disconnected')
        del connected_users[sid]

        sio.emit(
            'user_left',
            {
                'username': username,
                'timestamp': datetime.now().isoformat(),
                'message': f'{username} leave the room',
            },
        )


@sio.event
def set_username(sid, data):
    username = data['username']
    connected_users[sid]['username'] = username
    print(f'用户 {sid} 设置用户名为: {username}')

    sio.emit(
        'user_joined',
        {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'message': f'{username} 加入了聊天室',
        },
    )

    # 发送当前在线用户列表
    online_users = [user['username'] for user in connected_users.values() if user['username']]
    sio.emit('online_users', online_users)


@sio.event
def send_message(sid, data):
    user_data = connected_users.get(sid)
    if user_data and user_data['username']:
        message_data = {
            'username': user_data['username'],
            'message': data['message'],
            'timestamp': datetime.now().isoformat(),
        }
        print(f'消息来自 {user_data["username"]}: {data["message"]}')

        sio.emit('receive_message', message_data)


@sio.event
def join_room(sid, data):
    room = data['room']
    if sid in connected_users:
        connected_users[sid]['room'] = room
        sio.enter_room(sid, room)

        if room not in rooms:
            rooms[room] = []
        rooms[room].append(sid)

        print(f'用户 {connected_users[sid]["username"]} 加入了房间 {room}')


@sio.event
def leave_room(sid, data):
    room = data['room']
    if sid in connected_users and 'room' in connected_users[sid]:
        sio.leave_room(sid, room)
        if room in rooms and sid in rooms[room]:
            rooms[room].remove(sid)
        del connected_users[sid]['room']
        print(f'用户 {connected_users[sid]["username"]} 离开了房间 {room}')


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
