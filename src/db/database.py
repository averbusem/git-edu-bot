from motor.motor_asyncio import AsyncIOMotorClient

from src.bot.utils import settings
from src.db.config import (DB_NAME, MONGO_URI, RESULTS_COLLECTION,
                           USERS_COLLECTION)


class Database:
    def __init__(self, uri: str = MONGO_URI, db_name: str = DB_NAME, users_collection_name: str = USERS_COLLECTION,
                 results_collection_name: str = RESULTS_COLLECTION):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.users = self.db[users_collection_name]
        self.results = self.db[results_collection_name]

    async def add_new_user(self, user_id: str, username: str, current_theory: int = 1, current_test: int = 1,
                           current_practice: int = 2, day_points: int = 0, all_points: int = 0):
        user = await self.users.find_one({"_id": f'{user_id}'})
        if user is None:
            new_user = {
                "_id": f'{user_id}',
                "username": username,
                "current_theory": current_theory,
                "current_test": current_test,
                "current_practice": current_practice,
                "day_points": day_points,
                "all_points": all_points,
                # средняя оценка за все тесты (считается после прохождения всех тестов)
                "average_score": 0.0,
                "stickers": [False] * settings.TOTAL_STICKERS,
            }
            return await self.users.insert_one(new_user)

    async def update_points(self, user_id: str, points: int):
        try:
            user = await self.users.find_one({"_id": str(user_id)})
            if not user:
                return

            await self.users.update_one(
                {"_id": str(user_id)},
                {"$inc": {"day_points": points, "all_points": points}}
            )

        except Exception as e:
            print(f"An error occurred while updating points: {e}")

    async def update_current_activity(self, user_id: str, current_theory: int = None, current_test: int = None,
                                      current_practice: int = None):
        user_info = await self.users.find_one({"_id": f'{user_id}'})
        if current_theory:
            if current_theory >= user_info["current_theory"]:
                user_info["current_theory"] = current_theory
        if current_test:
            if current_test >= user_info["current_test"]:
                user_info["current_test"] = current_test
        if current_practice:
            if current_practice >= user_info["current_practice"]:
                user_info["current_practice"] = current_practice

        if user_info:
            return self.users.update_one({"_id": f'{user_id}'}, {"$set": user_info})

    async def start_test(self, user_id: str, test_number: int):
        exists = await self.results.find_one({"user_id": f'{user_id}', "test_number": test_number})
        if exists is None:
            test_doc = {
                "user_id": f'{user_id}',
                "test_number": test_number,
                "answers": {},
                "score": None
            }
            return await self.results.insert_one(test_doc)

    async def get_test_results(self, user_id: str, test_number: int):
        test_info = await self.results.find_one({"user_id": f'{user_id}', "test_number": test_number})
        return test_info["answers"]

    async def tick_question_answer(self, user_id: str, test_number: int,
                                   question_number: int, is_correct: int):
        key = f"answers.{question_number}"
        update_op = {"$set": {key: is_correct}}

        return await self.results.update_one({"user_id": f'{user_id}', "test_number": test_number}, update_op)

    async def set_test_mark(self, user_id: str, test_number: int):
        test_info = await self.results.find_one({"user_id": f'{user_id}', "test_number": test_number})
        answers = test_info.get('answers', {})
        total = len(answers)
        correct_count = sum(1 for v in answers.values() if v)
        score = round((correct_count / total) * 100, 2) if total else 0.0

        return await self.results.update_one({"user_id": f'{user_id}', "test_number": test_number},
                                             {"$set": {"score": score}})

    async def get_test_mark(self, user_id: str, test_number: int):
        test_info = await self.results.find_one({"user_id": f'{user_id}', "test_number": test_number})
        test_result = test_info.get('score')
        return test_result

    async def get_current_activity(self, user_id: str):
        user_info = await self.users.find_one({"_id": f'{user_id}'})
        if not user_info:
            return None

        activities = {"theory": user_info["current_theory"],
                      "test": user_info["current_test"],
                      "practice": user_info["current_practice"]}
        return activities

    async def get_user_statistics(self, user_id: str):
        try:
            user_info = await self.users.find_one({"_id": f'{user_id}'})
            if user_info:
                return {
                    "current_theory": user_info.get("current_theory", 0),
                    "current_test": user_info.get("current_test", 0),
                    "current_practice": user_info.get("current_practice", 0),
                }
            else:
                return None

        except Exception as e:
            print(f"An error occurred while fetching user statistics: {e}")
            return None

    async def get_all_users(self):
        try:
            users_cursor = self.users.find({})
            users_list = await users_cursor.to_list(length=None)
            return users_list
        except Exception as e:
            print(f"An error occurred while fetching all users: {e}")

    async def try_spend_points(self, user_id: str, price: int) -> bool:
        result = await self.users.update_one(
            {"_id": f'{user_id}', "all_points": {"$gte": price}},
            {"$inc": {"all_points": -price}}
        )
        return result.modified_count == 1

    async def get_all_points(self, user_id: str) -> int:
        user = await self.users.find_one({"_id": f'{user_id}'})
        return user.get("all_points", 0)

    async def get_day_points(self, user_id: str) -> int:
        user = await self.users.find_one({"_id": f'{user_id}'})
        return user.get("day_points", 0)

    async def get_current_theory(self, user_id: str) -> int:
        user = await self.users.find_one({"_id": f'{user_id}'})
        return user.get("current_theory", 0)

    async def get_current_test(self, user_id: str) -> int:
        user = await self.users.find_one({"_id": f'{user_id}'})
        return user.get("current_test", 0)

    async def get_current_practice(self, user_id: str) -> int:
        user = await self.users.find_one({"_id": f'{user_id}'})
        return user.get("current_practice", 0)

    async def is_sticker_owned(self, user_id: str, sticker_number: int):
        user = await self.users.find_one({"_id": str(user_id)})
        stickers = user["stickers"]
        return stickers[sticker_number - 1] == True

    async def set_sticker_owned(self, user_id: str, sticker_number: int):
        await self.users.update_one(
            {"_id": str(user_id)},
            {"$set": {f"stickers.{sticker_number - 1}": True}}
        )

    async def are_all_stickers_owned(self, user_id: str) -> bool:
        user = await self.users.find_one({"_id": str(user_id)})
        stickers = user.get("stickers", [])
        return all(stickers)

    async def reset_day_points_all(self):
        print("Resetting day_points for all users...")
        await self.users.update_many({}, {"$set": {"day_points": 0}})

    async def close(self):
        self.client.close()


db = Database()
