import logging

from aiogram import BaseMiddleware, Bot, types
from aiogram.fsm.context import FSMContext


class UpdateLastMessageIdMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        state: FSMContext = data.get('state')
        bot: Bot = data.get('bot')

        result = await handler(event, data)

        current_message_id = None
        if isinstance(result, types.Message):
            current_message_id = result.message_id
        elif isinstance(event, types.CallbackQuery):
            current_message_id = event.message.message_id

        if state and current_message_id:
            logging.debug(f"Обновление last_message_id = {current_message_id}")
            await state.update_data(last_message_id=current_message_id)
        return result
