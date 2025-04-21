from motor.motor_asyncio import AsyncIOMotorClient

from src.db.config import COLLECTION_NAME, DB_NAME, MONGO_URI


class Database:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    async def add_new_user(self, user_id: int, current_theory: int = 1, current_test: int = 1,
                           current_practice: int = 1):
        user = await self.collection.find_one({"_id": user_id})

        if user is None:
            task = {
                "_id": user_id,
                "current_theory": current_theory,
                "current_test": current_test,
                "current_practice": current_practice,
                "tests_marks": {}  # хранение оценок для каждого теста
            }
            return await self.collection.insert_one(task)

    async def update_current_activity(self, user_id: int, current_theory: int = None, current_test: int = None,
                                      current_practice: int = None):
        update_data = {}
        if current_theory:
            update_data["current_theory"] = current_theory
        if current_test:
            update_data["current_test"] = current_test
        if current_practice:
            update_data["current_practice"] = current_practice

        if update_data:
            return self.collection.update_one({"_id": user_id}, {"$set": update_data})

    async def tick_question_answer(self, user_id: int, test_number: int,
                                   question_number: int, is_correct: int):
        key = f"tests_marks.test{test_number}.{question_number}"
        update_op = {"$set": {key: is_correct}}

        return await self.collection.update_one({"_id": user_id}, update_op)

    async def set_test_mark(self, user_id: int, test_number: int):
        user_info = await self.collection.find_one({"_id": user_id})
        test_answers_dict = user_info["tests_marks"][f"test{test_number}"]
        score_sum = 0
        for i in range(1, 8):
            score_sum += test_answers_dict[str(i)]
        mark = round(float(score_sum) / 7 * 100, 2)
        key = f"tests_marks.test{test_number}.mark"
        update_op = {"$set": {key: mark}}

        return await self.collection.update_one({"_id": user_id}, update_op)

    async def get_test_mark(self, user_id: int, test_number: int):
        user_info = await self.collection.find_one({"_id": user_id})
        test_result = user_info["tests_marks"][f"test{test_number}"]["mark"]
        return test_result

    async def get_current_activity(self, user_id: int, activity: str):
        user_info = await self.collection.find_one({"_id": user_id})
        if activity == "theory":
            return user_info["current_theory"]
        elif activity == "test":
            return user_info["current_test"]
        elif activity == "practice":
            return user_info["current_practice"]

    async def close(self):
        self.client.close()


db = Database(MONGO_URI, DB_NAME, COLLECTION_NAME)
