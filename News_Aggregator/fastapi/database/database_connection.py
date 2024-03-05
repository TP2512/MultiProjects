from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# MongoDB configuration
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "news_aggregator_db"


# Dependency to get MongoDB database instance
async def get_database() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    return db
