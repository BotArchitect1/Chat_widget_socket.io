from models import User, Message
from run import sio
from loguru import logger

from services import leave_room, rooms, join_room, move_room, send_message


@sio.on("connect")
async def connect(sid, environ):
    logger.info(f"Client {sid} connected")


# Обработчик отключения WebSocket
@sio.on("disconnect")
async def disconnect(sid):
    logger.info(f"Client {sid} disconnected")
    leave_room(sid)


# Обработчик события get_rooms
@sio.on("get_rooms")
async def get_rooms(sid, data):
    return rooms


# Обработчик события join
@sio.on("join")
async def handle_join(sid, data: User):
    try:
        return join_room(sid, data)
    except ValueError as e:
        return str(e)


# Обработчик события move
@sio.on("move")
async def handle_move(sid, data: str):
    try:
        return move_room(sid, data)
    except ValueError as e:
        return str(e)


# Обработчик события leave
@sio.on("leave")
async def handle_leave(sid, data):
    leave_room(sid)


# Обработчик события message
@sio.on("send_message")
async def handle_message(sid, data: Message):
    try:
        return await send_message(sid, data)
    except ValueError as e:
        return str(e)