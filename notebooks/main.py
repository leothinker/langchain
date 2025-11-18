import json
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.user_connections: dict[str, WebSocket] = {}
        self.users: dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, user_id: str, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_connections[user_id] = websocket
        self.users[user_id] = {
            'username': username,
            'user_id': user_id,
            'connected_at': datetime.now().isoformat(),
        }

        join_message = {
            'type': 'user_join',
            'user_id': user_id,
            'username': username,
            'message': f'{username} 加入了聊天室',
            'timestamp': datetime.now().isoformat(),
            'online_users': len(self.active_connections),
        }
        await self.broadcast(join_message)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id in self.user_connections:
            del self.user_connections[user_id]

        if user_id in self.users:
            username = self.users[user_id]['username']
            leave_message = {
                'type': 'user_leave',
                'user_id': user_id,
                'username': username,
                'message': f'{username} 离开了聊天室',
                'timestamp': datetime.now().isoformat(),
                'online_users': len(self.active_connections),
            }
            del self.users[user_id]
            return leave_message
        return None

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

    async def send_to_user(self, message: dict, target_user_id: str):
        if target_user_id in self.user_connections:
            await self.user_connections[target_user_id].send_text(json.dumps(message))


manager = ConnectionManager()


@app.get('/')
async def get():
    return {'message': 'WebSocket Chat Server is running'}


@app.websocket('/ws/{user_id}')
async def websocket_endpoint(websocket: WebSocket, user_id: str, username: str = '匿名用户'):
    await manager.connect(websocket, user_id, username)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            if message_data['type'] == 'chat_message':
                broadcast_message = {
                    'type': 'chat_message',
                    'user_id': user_id,
                    'username': username,
                    'content': message_data['content'],
                    'timestamp': datetime.now().isoformat(),
                }
                await manager.broadcast(broadcast_message)

            elif message_data['type'] == 'private_message':
                private_message = {
                    'type': 'private_message',
                    'from_user_id': user_id,
                    'from_username': username,
                    'content': message_data['content'],
                    'timestamp': datetime.now().isoformat(),
                }
                await manager.send_to_user(private_message, message_data['target_user_id'])

    except WebSocketDisconnect:
        leave_message = manager.disconnect(websocket, user_id)
        if leave_message:
            await manager.broadcast(leave_message)
