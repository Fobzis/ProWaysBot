import config
import logging
import datetime
import asyncio
import tracemalloc
tracemalloc.start()
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from sqlite import (db_start, create_profile, edit_profile, user_info, create_order, change_language, change_style, change_topic1,
                    change_topic, additional_wishes, check_st, check_wishes, send_file, change_status, send_message, done_status)
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

async def on_startup(_):
    await db_start()

logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())



async def on_button_click(callback_query: types.CallbackQuery):
    # Отримуємо дані з callback_query
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    # Редагуємо повідомлення для видалення кнопки
    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)


@dp.message_handler(commands=['stop'])
async def start_command(message: types.Message):
    if message.from_user.id == 1306948850:
        await done_status()
        await bot.send_message(message.chat.id, "Done")


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Далі", callback_data="delete_button")
    markup.add(button)
    img=open('pro.png', 'rb')
    await bot.send_photo(message.chat.id, img, "Привіт, я бот зза допомогою якого ти можеш замовити презентацію, реферат та інше.",reply_markup=markup)
    await create_profile(user_id=message.from_user.id, username=message.from_user.username)


@dp.callback_query_handler(text="menu")
async def artwork_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton("1", callback_data="delete_button")
    button2 = types.InlineKeyboardButton("2", callback_data="m_2")
    button3 = types.InlineKeyboardButton("3", callback_data="m_3")
    markup.add(button1, button2, button3)
    button4 = types.InlineKeyboardButton("Техпідтримка", callback_data="m_5")
    button5 = types.InlineKeyboardButton("Інше", callback_data="m_10")
    markup.add(button4, button5)


    await bot.send_message(callback_query.from_user.id,
                               "Обери що ти хочеш \n1  -  Реферат, презентація, твір\n2  -  Виконання дз\n"
                               "3  -  Пояснення теми з математики",
                               reply_markup=markup)



@dp.callback_query_handler(text="m_2")
async def artwork_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton("1", callback_data="d_1")
    button2 = types.InlineKeyboardButton("2", callback_data="d_2")
    button3 = types.InlineKeyboardButton("3", callback_data="d_3")
    markup.add(button1, button2, button3)
    button4 = types.InlineKeyboardButton("4", callback_data="d_4")
    button5 = types.InlineKeyboardButton("5", callback_data="d_5")
    button6 = types.InlineKeyboardButton("6", callback_data="d_6")
    markup.add(button4, button5, button6)
    button7 = types.InlineKeyboardButton("7", callback_data="d_7")
    button8 = types.InlineKeyboardButton("Назад", callback_data="menu")
    markup.add(button7, button8)



    await bot.send_message(callback_query.from_user.id,
                               "Обери з якого предмету ти хочеш купити вирішення дз \n1 - Українська мова"
                               "\n2 - Українська література\n3 - Англійська мова\n4 - Зарубіжня література"
                               "\n5 - Історія України\n6 - Всесвітня історія\n7 - Правознавство",
                               reply_markup=markup)



@dp.callback_query_handler(text="delete_button")
async def delete_button_callback(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    markup1 = types.InlineKeyboardMarkup(row_width=1)

    button1 = types.InlineKeyboardButton("Презентація", callback_data="order_presentation")
    markup1.add(button1)
    button2 = types.InlineKeyboardButton("Реферат", callback_data="order_essay")
    markup1.add(button2)
    button4 = types.InlineKeyboardButton("Твір", callback_data="order_artwork")
    button_st = types.InlineKeyboardButton("Меню", callback_data="menu")
    markup1.add(button4, button_st)


    await callback_query.answer("Обирай")
    await bot.send_message(callback_query.from_user.id, "Обери що ти хочеш замовити)", reply_markup=markup1)


@dp.callback_query_handler(text="st_order")
async def delete_button_callback(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    markup1 = types.InlineKeyboardMarkup(row_width=1)

    button1 = types.InlineKeyboardButton("Презентація", callback_data="order_presentation")
    markup1.add(button1)
    button2 = types.InlineKeyboardButton("Реферат", callback_data="order_essay")
    markup1.add(button2)
    button4 = types.InlineKeyboardButton("Твір", callback_data="order_artwork")
    button_st = types.InlineKeyboardButton("Назад", callback_data="menu")
    markup1.add(button4, button_st)


    await callback_query.answer("Обирай")
    await bot.send_message(callback_query.from_user.id, "Обери що ти хочеш замовити)", reply_markup=markup1)


@dp.callback_query_handler(text="order_another")
async def another_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Інше", amount=50 * 100)


    await bot.send_invoice(callback_query.from_user.id,
                           title="Інше",
                           description="Ти вибрав(-ла) інше. Щоб оплатити натисни кнопку нижче.\n\nПісля сплати потрібно вказати що саме ти хочеш.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Інше")



@dp.callback_query_handler(text="order_artwork")
async def artwork_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton("1", callback_data="a_1")
    button2 = types.InlineKeyboardButton("2", callback_data="a_2")
    markup.add(button1, button2)
    button3 = types.InlineKeyboardButton("3", callback_data="a_3")
    button4 = types.InlineKeyboardButton("5", callback_data="a_5")
    markup.add(button3, button4)
    button5 = types.InlineKeyboardButton("10", callback_data="a_10")
    button_st = types.InlineKeyboardButton("Назад", callback_data="st_order")
    markup.add(button5, button_st)


    await bot.send_message(callback_query.from_user.id,
                               "Обери розмір твору (в сторінках А4, розмір шрифту 11-12)\n1  -  20 грн\n2  -  30 грн\n"
                               "3  -  40 грн\n5  -  50 грн\n10  -  80 грн",
                               reply_markup=markup)



@dp.callback_query_handler(text="a_1")
async def essay_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Твір 1 сторінка", amount=20 * 100)


    await bot.send_invoice(callback_query.from_user.id,
                           title="Твір",
                           description="Ти вибрав(-ла) твір розміром 1 сторінка. Щоб оплатити натисни кнопку нижче.\n"
                                       "\nПісля сплати можна внести додаткові побажання, обрати стиль презентації та "
                                       "мову.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Твір 1 сторінка")



@dp.callback_query_handler(text="a_2")
async def essay_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Твір 2 сторінки", amount=30 * 100)


    await bot.send_invoice(callback_query.from_user.id,
                           title="Твір",
                           description="Ти вибрав(-ла) твір розміром 2 сторінки. Щоб оплатити натисни кнопку нижче.\n"
                                       "\nПісля сплати можна внести додаткові побажання, обрати стиль презентації та "
                                       "мову.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Твір 2 сторінки")



@dp.callback_query_handler(text="a_3")
async def essay_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Твір 3 сторінки", amount=40 * 100)


    await bot.send_invoice(callback_query.from_user.id,
                           title="Твір",
                           description="Ти вибрав(-ла) твір розміром 3 сторінки. Щоб оплатити натисни кнопку нижче.\n"
                                       "\nПісля сплати можна внести додаткові побажання, обрати стиль презентації та "
                                       "мову.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Твір 3 сторінки")



@dp.callback_query_handler(text="a_5")
async def essay_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Твір 5 сторінки", amount=50 * 100)


    await bot.send_invoice(callback_query.from_user.id,
                           title="Твір",
                           description="Ти вибрав(-ла) твір розміром 5 сторінки. Щоб оплатити натисни кнопку нижче.\n"
                                       "\nПісля сплати можна внести додаткові побажання, обрати стиль презентації та"
                                       " мову.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Твір 5 сторінки")



@dp.callback_query_handler(text="a_10")
async def essay_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Твір 10 сторінки", amount=80 * 100)

    await bot.send_invoice(callback_query.from_user.id,
                           title="Твір",
                           description="Ти вибрав(-ла) твір розміром 10 сторінки. Щоб оплатити натисни кнопку нижче.\n"
                                       "\nПісля сплати можна внести додаткові побажання, обрати стиль презентації "
                                       "та мову.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Твір 10 сторінки")



@dp.callback_query_handler(text="order_essay")
async def essay_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton("1", callback_data="e_1")
    button2 = types.InlineKeyboardButton("2", callback_data="e_2")
    markup.add(button1, button2)
    button3 = types.InlineKeyboardButton("3", callback_data="e_3")
    button4 = types.InlineKeyboardButton("5", callback_data="e_5")
    markup.add(button3, button4)
    button5 = types.InlineKeyboardButton("10", callback_data="e_10")
    button_st = types.InlineKeyboardButton("Назад", callback_data="st_order")
    markup.add(button5, button_st)

    await bot.send_message(callback_query.from_user.id,
                               "Обери розмір реферату (в сторінках А4, розмір шрифту 11-12)\n1  -  5 грн"
                               "\n2  -  8 грн\n3  -  10 грн\n5  -  15 грн\n10  -  30 грн",
                               reply_markup=markup)



@dp.callback_query_handler(text="e_1")
async def essay_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Реферат 1 сторінка", amount=5 * 100)


    await bot.send_invoice(callback_query.from_user.id,
                           title="Реферат",
                           description="Ти вибрав(-ла) реферат розміром 1 сторінка. Щоб оплатити натисни кнопку нижче.\n"
                                       "\nПісля сплати можна внести додаткові побажання, обрати стиль презентації "
                                       "та мову.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Реферат 1 сторінка")



@dp.callback_query_handler(text="e_2")
async def essay_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Реферат 2 сторінки", amount=8 * 100)

    await bot.send_invoice(callback_query.from_user.id,
                           title="Реферат",
                           description="Ти вибрав(-ла) реферат розміром 2 сторінки. Щоб оплатити натисни кнопку нижче.\n"
                                       "\nПісля сплати можна внести додаткові побажання, обрати стиль презентації"
                                       " та мову.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Реферат 2 сторінки")



@dp.callback_query_handler(text="e_3")
async def essay_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Реферат 3 сторінки", amount=10 * 100)

    await bot.send_invoice(callback_query.from_user.id,
                           title="Реферат",
                           description="Ти вибрав(-ла) реферат розміром 3 сторінки. Щоб оплатити натисни кнопку нижче."
                                       "\n\nПісля сплати можна внести додаткові побажання, обрати стиль презентації "
                                       "та мову.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Реферат 3 сторінки")



@dp.callback_query_handler(text="e_5")
async def essay_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Реферат 5 сторінок", amount=15 * 100)

    await bot.send_invoice(callback_query.from_user.id,
                               title="Реферат",
                               description="Ти вибрав(-ла) реферат розміром 5 сторінок. Щоб оплатити натисни кнопку "
                                           "нижче.\n\nПісля сплати можна внести додаткові побажання, обрати стиль "
                                           "презентації та мову.",
                               provider_token=config.PAYMENTS_TOKEN,
                               currency="uah",
                               is_flexible=False,
                               prices=[PRICE],
                               start_parameter="order",
                               payload="Реферат 5 сторінок")



@dp.callback_query_handler(text="e_10")
async def essay_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Реферат 10 сторінок", amount=30 * 100)

    await bot.send_invoice(callback_query.from_user.id,
                               title="Реферат",
                               description="Ти вибрав(-ла) реферат розміром 10 сторінок. Щоб оплатити натисни кнопку "
                                           "нижче.\n\nПісля сплати можна внести додаткові побажання, обрати стиль "
                                           "презентації та мову.",
                               provider_token=config.PAYMENTS_TOKEN,
                               currency="uah",
                               is_flexible=False,
                               prices=[PRICE],
                               start_parameter="order",
                               payload="Реферат 10 сторінок")



@dp.callback_query_handler(text="order_presentation")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton("10", callback_data="p_10")
    button2 = types.InlineKeyboardButton("15", callback_data="p_15")
    markup.add(button1, button2)
    button3 = types.InlineKeyboardButton("20", callback_data="p_20")
    button4 = types.InlineKeyboardButton("30", callback_data="p_30")
    markup.add(button3, button4)
    button_st = types.InlineKeyboardButton("Назад", callback_data="st_order")
    markup.add(button_st)

    await bot.send_message(callback_query.from_user.id, "Обери розмір презентації(в слайдах)\n10  -  20 грн"
                                                        "\n15  -  25 грн\n20  -  30 грн\n30  -  40 грн",
                           reply_markup=markup)



@dp.callback_query_handler(text="p_10")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Презентація 10 слайдів", amount=20 * 100)


    await bot.send_invoice(callback_query.from_user.id,
                           title="Презентація",
                           description="Ти вибрав(-ла) презентацію розміром 10 слайдів. Щоб оплатити натисни кнопку "
                                       "нижче.\n\nПісля сплати можна внести додаткові побажання, обрати стиль "
                                       "презентації та мову.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Презентація 10 слайдів")



@dp.callback_query_handler(text="p_15")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Презентація 15 слайдів", amount=25 * 100)


    await bot.send_invoice(callback_query.from_user.id,
                           title="Презентація",
                           description="Ти вибрав(-ла) презентацію розміром 15 слайдів. Щоб оплатити натисни кнопку "
                                       "нижче.\n\nПісля сплати можна внести додаткові побажання, обрати стиль "
                                       "презентації та мову.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Презентація 15 слайдів")



    @dp.callback_query_handler(text="p_20")
    async def presentation_choice(callback_query: types.CallbackQuery):
        await on_button_click(callback_query)

        PRICE = types.LabeledPrice(label="Презентація 20 слайдів", amount=30 * 100)

        await bot.send_invoice(callback_query.from_user.id,
                               title="Презентація",
                               description="Ти вибрав(-ла) презентацію розміром 20 слайдів. Щоб оплатити натисни "
                                           "кнопку нижче.\n\nПісля сплати можна внести додаткові побажання, обрати "
                                           "стиль презентації та мову.",
                               provider_token=config.PAYMENTS_TOKEN,
                               currency="uah",
                               is_flexible=False,
                               prices=[PRICE],
                               start_parameter="order",
                               payload="Презентація 20 слайдів")


@dp.callback_query_handler(text="p_20")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Презентація 20 слайдів", amount=30 * 100)


    await bot.send_invoice(callback_query.from_user.id,
                           title="Презентація",
                           description="Ти вибрав(-ла) презентацію розміром 20 слайдів. Щоб оплатити натисни кнопку "
                                       "нижче.\n\nПісля сплати можна внести додаткові побажання, обрати стиль "
                                       "презентації та мову.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Презентація 20 слайдів")



    @dp.callback_query_handler(text="p_20")
    async def presentation_choice(callback_query: types.CallbackQuery):
        await on_button_click(callback_query)

        PRICE = types.LabeledPrice(label="Презентація 20 слайдів", amount=30 * 100)

        await bot.send_invoice(callback_query.from_user.id,
                               title="Презентація",
                               description="Ти вибрав(-ла) презентацію розміром 20 слайдів. Щоб оплатити натисни "
                                           "кнопку нижче.\n\nПісля сплати можна внести додаткові побажання, обрати "
                                           "стиль презентації та мову.",
                               provider_token=config.PAYMENTS_TOKEN,
                               currency="uah",
                               is_flexible=False,
                               prices=[PRICE],
                               start_parameter="order",
                               payload="Презентація 20 слайдів")

@dp.callback_query_handler(text="p_30")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    PRICE = types.LabeledPrice(label="Презентація 30 слайдів", amount=40 * 100)


    await bot.send_invoice(callback_query.from_user.id,
                           title="Презентація",
                           description="Ти вибрав(-ла) презентацію розміром 30 слайдів. Щоб оплатити натисни кнопку "
                                       "нижче.\n\nПісля сплати можна внести додаткові побажання, обрати стиль "
                                       "презентації та мову.",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="uah",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="order",
                           payload="Презентація 30 слайдів")


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
  await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)



@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    sf=[]
    print("УСПІШНА ОПЛАТА")
    payment_info = message.successful_payment.to_python()
    print(payment_info)
    for k, v in payment_info.items():
        sf.append(v)
    print(sf)

    await create_order(user_id=message.from_user.id, order_id=sf[3], type_order=sf[2])
    await bot.send_message(message.chat.id,
                           "Замовлення сплачене")

    if 'Презентація' in sf[2]:
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Англійська", callback_data="language_english")
        button2 = types.InlineKeyboardButton("Українська", callback_data="language_ukrainian")
        markup.add(button2)
        markup.add(button)
        await bot.send_message(message.chat.id,
                             "Вкажи мову для презентації",
                             reply_markup=markup)

    elif 'Реферат' in sf[2]:
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Англійська", callback_data="Rlanguage_english")
        button2 = types.InlineKeyboardButton("Українська", callback_data="Rlanguage_ukrainian")
        markup.add(button2)
        markup.add(button)
        await bot.send_message(message.chat.id,
                             "Вкажи мову для презентації",
                             reply_markup=markup)

    elif 'Твір' in sf[2]:
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Англійська", callback_data="Tlanguage_english")
        button2 = types.InlineKeyboardButton("Українська", callback_data="Tlanguage_ukrainian")
        markup.add(button2)
        markup.add(button)
        await bot.send_message(message.chat.id,
                             "Вкажи мову для презентації",
                             reply_markup=markup)


@dp.callback_query_handler(text="Tlanguage_english")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    await change_language(user_id=callback_query.from_user.id, language='Англійська')
    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему твору")


@dp.callback_query_handler(text="Tlanguage_ukrainian")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    await change_language(user_id=callback_query.from_user.id, language='Українська')
    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему твору")


@dp.callback_query_handler(text="Rlanguage_english")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    await change_language(user_id=callback_query.from_user.id, language='Англійська')
    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему реферату")


@dp.callback_query_handler(text="Rlanguage_ukrainian")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    await change_language(user_id=callback_query.from_user.id, language='Українська')
    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему реферату")

@dp.callback_query_handler(text="Rlanguage_english")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    await change_language(user_id=callback_query.from_user.id, language='Англійська')
    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему реферату")


@dp.callback_query_handler(text="Rlanguage_ukrainian")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)

    await change_language(user_id=callback_query.from_user.id, language='Українська')
    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему реферату")


@dp.callback_query_handler(text="language_english")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("1", callback_data="p_style_1")
    button2 = types.InlineKeyboardButton("2", callback_data="p_style_2")
    button3 = types.InlineKeyboardButton("3", callback_data="p_style_3")
    button4 = types.InlineKeyboardButton("4", callback_data="p_style_4")
    markup.add(button1, button2, button3)
    button5 = types.InlineKeyboardButton("5", callback_data="p_style_5")
    button6 = types.InlineKeyboardButton("6", callback_data="p_style_6")
    button7 = types.InlineKeyboardButton("7", callback_data="p_style_7")
    button8 = types.InlineKeyboardButton("8", callback_data="p_style_8")
    markup.add(button4, button5, button6)
    markup.add(button7, button8)

    img = open('p_1.png', 'rb')
    img2 = open('p_2.png', 'rb')
    await bot.send_photo(callback_query.from_user.id, img)
    await bot.send_photo(callback_query.from_user.id, img2, "Вибери стиль презентації з показаних вище",
                         reply_markup=markup)
    await change_language(user_id=callback_query.from_user.id, language='Англійська')


@dp.callback_query_handler(text="language_ukrainian")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("1", callback_data="p_style_1")
    button2 = types.InlineKeyboardButton("2", callback_data="p_style_2")
    button3 = types.InlineKeyboardButton("3", callback_data="p_style_3")
    button4 = types.InlineKeyboardButton("4", callback_data="p_style_4")
    markup.add(button1, button2, button3)
    button5 = types.InlineKeyboardButton("5", callback_data="p_style_5")
    button6 = types.InlineKeyboardButton("6", callback_data="p_style_6")
    button7 = types.InlineKeyboardButton("7", callback_data="p_style_7")
    button8 = types.InlineKeyboardButton("8", callback_data="p_style_8")
    markup.add(button4, button5, button6)
    markup.add(button7, button8)

    img = open('p_1.png', 'rb')
    img2 = open('p_2.png', 'rb')
    await bot.send_photo(callback_query.from_user.id, img)
    await bot.send_photo(callback_query.from_user.id, img2, "Вибери стиль презентації з показаних вище",
                         reply_markup=markup)
    await change_language(user_id=callback_query.from_user.id, language='Українська')





@dp.callback_query_handler(text="p_style_1")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    await change_style(user_id=callback_query.from_user.id, order_style='1')

    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему для презентації")

@dp.callback_query_handler(text="p_style_2")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    await change_style(user_id=callback_query.from_user.id, order_style='2')

    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему для презентації")

@dp.callback_query_handler(text="p_style_3")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    await change_style(user_id=callback_query.from_user.id, order_style='3')

    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему для презентації")

@dp.callback_query_handler(text="p_style_4")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    await change_style(user_id=callback_query.from_user.id, order_style='4')

    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему для презентації")

@dp.callback_query_handler(text="p_style_5")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    await change_style(user_id=callback_query.from_user.id, order_style='5')

    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему для презентації")

@dp.callback_query_handler(text="p_style_6")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    await change_style(user_id=callback_query.from_user.id, order_style='6')

    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему для презентації")

@dp.callback_query_handler(text="p_style_7")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    await change_style(user_id=callback_query.from_user.id, order_style='7')

    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему для презентації")

@dp.callback_query_handler(text="p_style_8")
async def presentation_choice(callback_query: types.CallbackQuery):
    await on_button_click(callback_query)
    await change_style(user_id=callback_query.from_user.id, order_style='8')
    await change_topic(user_id=callback_query.from_user.id, topic="key//empety//topic")
    await bot.send_message(callback_query.from_user.id, "Напиши тему для презентації")



@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def save_last_message(message: types.Message):
    last_message = message.text
    if message.from_user.id == 1306948850:
        if "/sendorder" in last_message:
            id = last_message[10:]
            await change_status(id, 'send')
        else:
            await send_message(last_message)
    else:
        if last_message != None:
            #heck = check_st(user_id=message.from_user.id, stt='пепе')
            check = change_topic1(user_id=message.from_user.id, topic=last_message)
            asyncio.create_task(check)


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def save_last_message(message: types.Message):
    if message.from_user.id == 1306948850:
        try:
            file_id = message.document.file_id
            await send_file(file_id)
        except(AttributeError):
            await bot.send_message(message.chat.id, 'Це не файл')


if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)