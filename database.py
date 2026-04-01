import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client['rss_bot']
users_col = db['users']
feeds_col = db['feeds']

async def is_sudo(user_id: int) -> bool:
    if user_id == int(os.getenv("OWNER_ID")):
        return True
    user = await users_col.find_one({"user_id": user_id})
    return bool(user and user.get("role") == "sudo")

async def add_sudo(user_id: int):
    await users_col.update_one({"user_id": user_id}, {"$set": {"role": "sudo"}}, upsert=True)

async def remove_sudo(user_id: int):
    await users_col.delete_one({"user_id": user_id})

async def add_feed(url: str, chat_id: int, added_by: int):
    await feeds_col.update_one(
        {"url": url, "chat_id": chat_id},
        {"$set": {"last_link": None, "added_by": added_by}},
        upsert=True
    )

async def remove_feed(url: str, chat_id: int):
    await feeds_col.delete_one({"url": url, "chat_id": chat_id})

async def get_all_feeds():
    return await feeds_col.find().to_list(length=None)

async def get_feeds_by_chat(chat_id: int):
    return await feeds_col.find({"chat_id": chat_id}).to_list(length=None)

async def update_last_link(url: str, chat_id: int, last_link: str):
    await feeds_col.update_one(
        {"url": url, "chat_id": chat_id},
        {"$set": {"last_link": last_link}}
    )