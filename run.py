from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import socketio
from loguru import logger

from user_storage import add_user, get_user, remove_user
from models import User, Message

rooms = {
    "lobby": [],
    "general": [],
    "random": []
}

app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi')
socket_app = socketio.ASGIApp(sio, app)

app.mount("/assets", StaticFiles(directory="assets"))


@sio.on("connect")
async def connect(sid, environ):
    logger.info(f"Client {sid} connected")


@sio.on("disconnect")
async def disconnect(sid):
    logger.info(f"Client {sid} disconnected")


@sio.on("get_rooms")
async def get_rooms(sid, data):
    rooms = sio.rooms(sid)
    return rooms


# Обработчик события join
@sio.on("join")
async def handle_join(sid, data):
    name = data.get("name")
    room = data.get("room")
    if not name or not room:
        await sio.emit("error", {"message": "Имя и комната обязательны"}, room=sid)
        return
    if room not in rooms:
        await sio.emit("error", {"message": "Такой комнаты не существует"}, room=sid)
        logger.info(f"User {name} joined room {room}")
        return

    user = User(name=name, room=room)
    add_user(sid, user)
    rooms[room].append(sid)
    await sio.enter_room(sid, room)
    await sio.emit("move", {"room": room}, room=sid)


@sio.on("move")
async def handle_move(sid, data):
    user = get_user(sid)

    if user:
        user.room = data.room
        await sio.emit("move", {"room": data.room}, room=sid)
        logger.info(f"User {user.name} moved to room {data.room}")


@sio.on("leave")
async def handle_leave(sid, data):
    user = get_user(sid)
    if user:
        room = user.room
        await sio.leave_room(sid, room)
        remove_user(sid)
        await sio.emit("message", {"text": f"{user.name} left the room"}, skip_sid=sid, to=room)
        logger.info(f"User {user.name} left room {user.room}")


@sio.on('send')
async def handle_send(sid, data):
    text = data.get("text")
    if not text:
        await sio.emit("error", {"message": "Сообщение не может быть пустым"}, room=sid)
        return
    user = get_user(sid)
    if user:
        message = Message(text=text, author=user.name)
        await sio.emit("message", {"name": message.author, "text": message.text}, to=user.room)
        logger.info(f"Message from {user.name} in room {user.room}: {message.text}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host='0.0.0.0', port=8000)