from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["rss"]
collection = db["jobs"]  # Replace with your collection name


async def insert_job(job):
    result = await collection.insert_one(job)
    return result.inserted_id


async def insert_jobs(jobs):
    result = await collection.insert_many(jobs)
    return result.inserted_ids


async def find_jobs(query={}):
    cursor = collection.find(query)
    return await cursor.to_list(length=None)


async def update_job(job_id, update):
    result = await collection.update_one({"_id": job_id}, {"$set": update})
    return result.modified_count


async def delete_job(job_id):
    result = await collection.delete_one({"_id": job_id})
    return result.deleted_count