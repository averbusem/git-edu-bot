import functools
import logging

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext


async def remove_keyboard(bot: Bot, chat_id: int, message_id: int) -> None:
    try:
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=None
        )
    except Exception as e:
        logging.error(f"Ошибка при удалении клавиатуры: {e}")


def clear_last_keyboard(func):
    """Декоратор для удаления инлайн-кнопок у последнего сообщения"""

    @functools.wraps(func)
    async def wrapper(event, state: FSMContext, *args, **kwargs):
        """Обрабатывает как сообщения, так и коллбэки"""

        chat_id = event.chat.id if isinstance(event, types.Message) else event.message.chat.id

        if isinstance(event, types.Message):
            data = await state.get_data()
            last_message_id = data.get("last_message_id")
            if last_message_id:
                await remove_keyboard(event.bot, chat_id, last_message_id)

        elif isinstance(event, types.CallbackQuery):
            chat_id = event.message.chat.id
            data = await state.get_data()
            last_message_id = data.get("last_message_id")
            if last_message_id:
                await remove_keyboard(event.message.bot, chat_id, last_message_id)

        result = await func(event, state, *args, **kwargs)

        if isinstance(result, types.Message):
            await state.update_data(last_message_id=result.message_id)
        elif isinstance(event, types.CallbackQuery):
            await state.update_data(last_message_id=event.message.message_id)

        return result

    return wrapper
