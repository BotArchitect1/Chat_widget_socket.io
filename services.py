from loguru import logger
from models import User, Message

users = {}
rooms = ["lobby", "general", "random"]


# Step 8: Обработчик события join
def join_room(sid, user: User):
    if user.room not in rooms:
        raise ValueError("Room does not exist")
    users[sid] = user
    logger.info(f"User {user.name} joined room {user.room}")
    return {"room": user.room}


# Step 9: Обработчик события move
def move_room(sid, new_room: str):
    if new_room not in rooms:
        raise ValueError("Room does not exist")
    user = users.get(sid)
    if user:
        user.room = new_room
        logger.info(f"User {user.name} moved to room {new_room}")
        return {"room": new_room}
    else:
        raise ValueError("User not found")


# Step 10: Обработчик события leave
def leave_room(sid):
    user = users.pop(sid, None)
    if user:
        logger.info(f"User {user.name} left room {user.room}")


# Step 11: Обработчик события message
def send_message(sid, message: Message):
    user = users.get(sid)
    if user:
        user.messages.append(message)
        logger.info(f"Message from {user.name} in room {user.room}: {message.text}")
    else:
        raise ValueError("User not found")
