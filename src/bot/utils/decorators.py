import functools
import logging

from aiogram import Bot, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext


async def remove_keyboard(bot: Bot, chat_id: int, message_id: int) -> None:
    try:
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=None
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            logging.debug(f"Клавиатура уже удалена у сообщения {chat_id}:{message_id}")
            return

        logging.error(f"Ошибка при удалении клавиатуры {chat_id}:{message_id}: {e}")
    except Exception as e:
        logging.error(f"Неожиданная ошибка при удалении клавиатуры {chat_id}:{message_id}: {e}")


def remove_last_keyboard(func):
    @functools.wraps(func)
    async def wrapper(event, state: FSMContext, *args, **kwargs):
        data = await state.get_data()
        last_message_id = data.get("last_message_id")
        result = await func(event, state, *args, **kwargs)

        current_message_id = None
        if isinstance(result, types.Message):
            current_message_id = result.message_id
        elif isinstance(result, types.CallbackQuery):
            current_message_id = result.message.message_id

        # Удаляем клавиатуру, только если это новый message_id
        if last_message_id and current_message_id and last_message_id != current_message_id:
            chat_id = (
                event.message.chat.id
                if isinstance(event, types.CallbackQuery)
                else event.chat.id
            )
            await remove_keyboard(event.bot, chat_id, last_message_id)

        if current_message_id:
            await state.update_data(last_message_id=current_message_id)

        return result

    return wrapper
