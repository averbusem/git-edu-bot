import logging

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, IndexModel

from src.db.config import (DB_NAME, MONGO_URI, RESULTS_COLLECTION,
                           USERS_COLLECTION)


async def init_db():
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[DB_NAME]

        existing_collections = await db.list_collection_names()
        if USERS_COLLECTION not in existing_collections:
            logging.info(f"Создаём коллекцию {USERS_COLLECTION}...")
            await db.create_collection(USERS_COLLECTION)
        else:
            logging.info(f"Коллекция {USERS_COLLECTION} уже существует")

            await db[USERS_COLLECTION].create_indexes([IndexModel([("user_id", ASCENDING)])])

        if RESULTS_COLLECTION not in existing_collections:
            logging.info(f"Создаём коллекцию {RESULTS_COLLECTION}...")
            await db.create_collection(RESULTS_COLLECTION)
            unique_test_index = IndexModel([("user_id", ASCENDING), ("test_number", ASCENDING)],
                                           unique=True)
            user_index = IndexModel([("user_id", ASCENDING)])
            await db[RESULTS_COLLECTION].create_indexes([unique_test_index, user_index])
        else:
            logging.info(f"Коллекция {RESULTS_COLLECTION} уже существует")
    except Exception as e:
        logging.error(f"Ошибка при подключении или работе с базой данных: {e}")
    finally:
        client.close()
