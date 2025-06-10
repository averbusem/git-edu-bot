import logging

from aiogram import BaseMiddleware, Bot, types
from aiogram.fsm.context import FSMContext


async def remove_keyboard(bot: Bot, chat_id: int, message_id: int) -> None:
    try:
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=None
        )
    except Exception as e:
        logging.debug(f"Ошибка при удалении клавиатуры {chat_id}:{message_id}: {e}")


class RemoveLastKeyboardMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        state: FSMContext = data.get("state")
        bot: Bot = data.get("bot")
        last_message_id = None

        # ДО: получаем предыдущий ID
        if state:
            data_storage = await state.get_data()
            last_message_id = data_storage.get("last_message_id")

        # ВЫЗЫВАЕМ хендлер
        result = await handler(event, data)

        # ПОСЛЕ: получаем ID текущего сообщения
        current_message_id = None
        if isinstance(result, types.Message):
            current_message_id = result.message_id
        elif isinstance(event, types.CallbackQuery):
            current_message_id = event.message.message_id

        # Удаляем клавиатуру, если предыдущее сообщение ≠ текущего
        if last_message_id and current_message_id and last_message_id != current_message_id:
            chat_id = (
                event.message.chat.id
                if isinstance(event, types.CallbackQuery)
                else event.chat.id
            )
            await remove_keyboard(bot, chat_id, last_message_id)

        # Обновляем last_message_id
        if state and current_message_id:
            await state.update_data(last_message_id=current_message_id)

        return result
