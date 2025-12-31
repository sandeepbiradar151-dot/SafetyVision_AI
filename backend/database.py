import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_DETAILS = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.safety_vision_db

async def check_db():
    try:
        await client.admin.command('ping')
        print("✅ MongoDB Connection Successful!")
    except Exception as e:
        print(f"❌ MongoDB Failed: {e}")