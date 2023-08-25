import sqlite3 as sq
import config
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.contrib.middlewares.logging import LoggingMiddleware
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

def kff(text):
    if len(text) > 4:
        l = len(text)
        s = l - 4
        result = text[:-(s)]
    else:
        result = text
    return result

async def db_start():
    global db, cur

    db = sq.connect('new.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, username TEXT, data_join TEXT, number TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS orderpro(user_id TEXT, order_id TEXT, status TEXT, time_order TEXT, type_order TEXT, language TEXT, order_style TEXT, topic TEXT, additional_wishes TEXT)")

    db.commit()

async def change_status(order_id, order_status):
    cur.execute("UPDATE orderpro SET status = '{key2}' WHERE order_id = '{key}'".format(key=order_id, key2=order_status))
    db.commit()

async def done_status():
    cur.execute("UPDATE orderpro SET status = '{key2}' WHERE status = '{key}'".format(key='send', key2='done'))
    db.commit()

async def send_file(file_id):
    st = cur.execute(
        "SELECT user_id FROM orderpro WHERE status = '{key}'".format(key='send')).fetchone()
    if st != None:
        st = str(st)
        st = st[:-3][2:]
        print(st)
        await bot.send_document(st, file_id)
    else:
        await bot.send_message(1306948850, "Файл не надісланий, такого користувача не знайдено")


async def send_message(message):
    st = cur.execute(
        "SELECT user_id FROM orderpro WHERE status = '{key}'".format(key='send')).fetchone()
    if st != None:
        st = str(st)
        st = st[:-3][2:]
        print(st)
        await bot.send_message(st, message)
    else:
        await bot.send_message(1306948850, "Повідомлення не надіслано, такого користувача не знайдено")


async def change_language(user_id, language):
    cur.execute("UPDATE orderpro SET language = '{key2}' WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id, key2=language)).fetchone()
    db.commit()


async def change_topic(user_id, topic):
    cur.execute("UPDATE orderpro SET topic = '{key2}' WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id, key2=topic)).fetchone()

    db.commit()

async def change_topic1(user_id, topic):
    st = cur.execute(
        "SELECT topic FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id)).fetchone()
    st2 = cur.execute("SELECT additional_wishes FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(
        key=user_id)).fetchone()
    order_id1 = cur.execute(
        "SELECT order_id FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(
            key=user_id)).fetchone()

    order_id = str(order_id1)
    order_id = order_id[:-(3)][2:]

    if st != None:
        if "key//empety//topic" in st:

            cur.execute(
                "UPDATE orderpro SET topic = '{key2}' WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id,
                                                                                                             key2=topic)).fetchone()
            type_order = cur.execute(
                "SELECT type_order FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(
                    key=user_id)).fetchone()
            print(type_order)
            st = cur.execute(
                "SELECT topic FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id)).fetchone()

            type = kff(type_order)
            print(type)
            if type == "('Пр":
                await bot.send_message(user_id, f"Тепер напиши додаткові побажання, наприклад: шрифт, ваше ім'я (для вказування вас як автора).")

            elif type == "('Ре":
                await bot.send_message(user_id,
                                       f"Тепер напиши додаткові побажання, наприклад: шрифт, ваше ім'я (для вказування вас як автора).")

            elif type == "('Тв":
                await bot.send_message(user_id,
                                       f"Тепер Напиши вид твору, наприклад: Твір роздум, опис, розповідь. Та додаткові побажання\n(Одним повідомленням)")

            else:
                await bot.send_message(user_id,
                                       f"Тепер напиши додаткові побажання\n(Одним повідомленням)")

            cur.execute(
                "UPDATE orderpro SET additional_wishes = '{key2}' WHERE user_id = '{key}' AND status = 'filling'".format(
                    key=user_id, key2='key//empety//wishes')).fetchone()

        elif 'key//empety//wishes' in st2:
            cur.execute(
                "UPDATE orderpro SET additional_wishes = '{key2}' WHERE user_id = '{key}' AND status = 'filling'".format(
                    key=user_id, key2=topic)).fetchone()

            st2 = cur.execute(
                "SELECT additional_wishes FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id)).fetchone()
            await bot.send_message(user_id, f"Дякю за замовлення №{order_id}, Робота буде виконана протягом 24 годин.")

            print(f'{user_id}: {topic}')


            time_order = cur.execute(
                "SELECT time_order FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id)).fetchone()
            type_order = cur.execute(
                "SELECT type_order FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id)).fetchone()
            language = cur.execute(
                "SELECT language FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id)).fetchone()
            order_style = cur.execute(
                "SELECT order_style FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id)).fetchone()
            topic = cur.execute(
                "SELECT topic FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id)).fetchone()
            additional_wishes = cur.execute(
                "SELECT additional_wishes FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id)).fetchone()
            username = cur.execute(
                "SELECT username FROM profile WHERE user_id = '{key}'".format(key=user_id)).fetchone()
            await bot.send_message(1306948850, f"Нове замовлення!\nID: {order_id}\nЧас: {time_order}\n"
                                               f"Тип: {type_order}\nМова: {language}\nСтиль: {order_style}\nТема: {topic}\n"
                                               f"Додаткові побажання{additional_wishes}\nUserName: {username}\nВієправити замовлення - /sendorder{order_id}")

            cur.execute(
                "UPDATE orderpro SET status = 'open' WHERE user_id = '{key}' AND status = 'filling'".format(
                    key=user_id)).fetchone()


        else:
            print(f'{user_id}:  {topic}')
    else:
        print(f'{user_id}:  {topic}')
    db.commit()


async def additional_wishes(user_id, wishes):
    cur.execute("UPDATE orderpro SET additional_wishes = '{key2}' WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id, key2=wishes)).fetchone()
    db.commit()


async def check_st(user_id, stt):
    st = cur.execute("SELECT topic FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id)).fetchone()
    st2 = cur.execute("SELECT additional_wishes FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id)).fetchone()
    print(st)
    print(st2)
    if 's' in st:
        print("if")
        cur.execute(
            "UPDATE orderpro SET topic = '{key2}' WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id, key2=stt)).fetchone()
        cur.execute(
            "UPDATE orderpro SET additional_wishes = '{key2}' WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id,
                                                                                                         key2="s")).fetchone()
        return 'True'

    elif st2 == ('s',):
        print("elif")
        cur.execute(
            "UPDATE orderpro SET additional_wishes = '{key2}' WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id,
                                                                                                         key2=stt)).fetchone()
        cur.execute(
            "UPDATE orderpro SET additional_wishes = '{key2}' WHERE user_id = '{key}' AND status = 'filling'".format(
                key=user_id,
                key2="s")).fetchone()
    else:
        print("else")
        print('f')

    db.commit()

async def check_wishes(user_id):
    st = cur.execute("SELECT additional_wishes FROM orderpro WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id)).fetchone()
    db.commit()
    if st == "('s',)":
        return True
    else:
        return False




async def change_style(user_id, order_style):
    cur.execute("UPDATE orderpro SET order_style = '{key2}' WHERE user_id = '{key}' AND status = 'filling'".format(key=user_id, key2=order_style))
    db.commit()
async def create_order(user_id, order_id, type_order):
    now = str(datetime.datetime.now())[:-7]
    cur.execute("INSERT INTO orderpro VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, order_id, 'filling', now, type_order, '', '', '', ''))
    db.commit()

async def create_profile(user_id, username):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        now = str(datetime.datetime.now())[:-7]
        cur.execute("INSERT INTO profile VALUES(?, ?, ?, ?)", (user_id, username, now, ''))
        db.commit()

async def user_info(user_id):
  user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
  if not user:
      return "Такого коритувача не існує"

  else:

    username = cur.execute("SELECT username FROM profile WHERE user_id = {key}".format(key=user_id)).fetchone()

  db.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE profile SET photo = '{}', age = '{}', description = '{}', name = '{}' WHERE user_id == '{}'".format(
            data['photo'], data['age'], data['description'], data['name'], user_id))
        db.commit()