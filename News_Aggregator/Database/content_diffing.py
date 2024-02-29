r"""Fetch the old content from MongoDB.
Fetch the new content from the web page.
Compare the old and new content to identify the differences.
Take action based on the differences (e.g., store the changed items in MongoDB, send notifications).
"""

import asyncio
import aiohttp
import pymongo

async def fetch_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def fetch_old_content_from_mongodb():
    # Connect to MongoDB and fetch the old content
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["mydatabase"]
    collection = db["pages"]
    document = collection.find_one()
    old_content = document.get("content") if document else None
    client.close()
    return old_content

async def monitor_page(url, interval=60):
    old_content = await fetch_old_content_from_mongodb()
    while True:
        try:
            new_content = await fetch_page(url)
            if old_content is not None and old_content != new_content:
                # Content has changed, take action (e.g., store the changed items in MongoDB)
                print("Page content has changed!")
                # Store the new content in MongoDB
                update_mongodb(new_content)
            old_content = new_content
        except Exception as e:
            print(f"Error fetching page: {e}")
        await asyncio.sleep(interval)

def update_mongodb(new_content):
    # Connect to MongoDB and update the content
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["mydatabase"]
    collection = db["pages"]
    # Update the content in MongoDB
    collection.update_one({}, {"$set": {"content": new_content}}, upsert=True)
    client.close()

async def main():
    url = 'https://example.com'  # Replace with the URL of the web page you want to monitor
    await monitor_page(url)

if __name__ == "__main__":
    asyncio.run(main())
