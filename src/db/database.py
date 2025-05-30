from motor.motor_asyncio import AsyncIOMotorClient

from src.db.config import (DB_NAME, MONGO_URI, RESULTS_COLLECTION,
                           USERS_COLLECTION)


class Database:
    def __init__(self, uri: str = MONGO_URI, db_name: str = DB_NAME, users_collection_name: str = USERS_COLLECTION,
                 results_collection_name: str = RESULTS_COLLECTION):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.users = self.db[users_collection_name]
        self.results = self.db[results_collection_name]

    async def add_new_user(self, user_id: str, current_theory: int = 1, current_test: int = 1,
                           current_practice: int = 2):
        user = await self.users.find_one({"_id": f'{user_id}'})
        if user is None:
            new_user = {
                "_id": f'{user_id}',
                "current_theory": current_theory,
                "current_test": current_test,
                "current_practice": current_practice,
                # средняя оценка за все тесты (считается после прохождения всех тестов)
                "average_score": 0.0
            }
            return await self.users.insert_one(new_user)

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

    async def close(self):
        self.client.close()


db = Database()
