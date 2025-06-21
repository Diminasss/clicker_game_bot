import telebot
import os
from logger import initialize_logger
from loaders import JSONLoader
from dotenv import load_dotenv

load_dotenv()
LOGGER = initialize_logger(__name__)
JSON_LOADER = JSONLoader()
PREV_TEXT: str = ""


def bot():

    bot: telebot.TeleBot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
    lottery_markup: telebot.types.InlineKeyboardMarkup = telebot.types.InlineKeyboardMarkup(row_width=2).add(telebot.types.InlineKeyboardButton(text="Клик👆", callback_data="lottery"), telebot.types.InlineKeyboardButton(text="Счёт📈", callback_data="score"))
    lottery_data: dict[str, int | dict[str, int]] = JSON_LOADER.load_score()
    boost_x2: list[int] = JSON_LOADER.load_booster_x2()
    boost_names: str = JSON_LOADER.get_boost_names(boost_x2, lottery_data)
    admin_id: int = int(os.getenv('ADMIN_ID'))
    player_id: int = int(os.getenv('PLAYER_ID'))

    bot.send_message(chat_id=player_id, text="Нажми, чтобы играть «Клик»", reply_markup=lottery_markup)

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call: telebot.types.CallbackQuery):
        if call.data == "lottery":
            LOGGER.info(f"{call.from_user.id}")

            user_id = str(call.from_user.id)
            if user_id not in lottery_data:
                lottery_data[user_id] = {"score": 1, "name": call.from_user.first_name}
                lottery_data["counter"] += 1
            else:
                if call.from_user.id not in boost_x2:
                    lottery_data[user_id]["score"] += 1
                    lottery_data["counter"] += 1
                else:
                    lottery_data[user_id]["score"] += 2
                    lottery_data["counter"] += 2

            if lottery_data["counter"] % 5 == 0:
                JSON_LOADER.update_score(lottery_data)

                # Исключение элемента с ключом "counter"
                filtered_lottery_data = {k: v for k, v in lottery_data.items() if k != "counter"}

                # Сортировка словаря по значению ключа "score" в порядке убывания
                sorted_lottery_data = sorted(
                    filtered_lottery_data.items(), key=lambda item: item[1]["score"], reverse=True
                )

                # Получение 10 первых позиций
                top_players = sorted_lottery_data[:10]

                text = "<b>Топ мест:</b>\n\n"
                for x in range(len(top_players)):
                    text += f"{x + 1}.{top_players[x][1]['name']} - {top_players[x][1]['score']}\n"

                text += boost_names
                global PREV_TEXT
                if text != PREV_TEXT:
                    PREV_TEXT = text
                    bot.edit_message_text(
                        text=text,
                        message_id=call.message.message_id,
                        chat_id=call.message.chat.id,
                        reply_markup=lottery_markup,
                        parse_mode="HTML",
                    )

        elif call.data == "score":
            bot.answer_callback_query(
                callback_query_id=call.id,
                text=f'Ваш счёт на данный момент - {lottery_data[str(call.from_user.id)]["score"]}!',
            )

    while True:
        try:
            bot.polling(non_stop=True)
        except Exception as e:
            LOGGER.error(f"{e}")
            bot.send_message(chat_id=admin_id, text=f"Пизда рулю и седлу {e}")


if __name__ == "__main__":
    bot()
