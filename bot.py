import asyncio
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  # for reply keyboard (sends message)
import codecs
import time
import datetime
from datetime import date

BOT_TOKEN = "5726127993:AAEmqkmE569eZ8UrDhGWHScjGA_Q7St1eck"



mates = ["@prikordonye" , "@rprprprrpprp", "@O_Svarog_O"]

used_mates = []
already_used = []

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)
seconds = time.time()



but1 = KeyboardButton('Регистрация')  
but2 = KeyboardButton('Для кого готовить подарок')
but3 = KeyboardButton('Кто принимает участие')
but4 = KeyboardButton('Сколько времени осталось')

first_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(but1).add(but3).add(but4)
second_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(but2).add(but3).add(but4)




@dp.message_handler(regexp='Сколько времени осталось')
async def TimeLeft(message: types.Message):
    now = date.today()
    time = datetime.date(2022, 12, 19)
    o = time-now
    o = o.days
    if message.from_user.mention in mates:
        await message.answer(f"Осталось {o} дней", reply_markup = second_kb)
    else:
        await message.answer(f"Осталось {o} дней", reply_markup = first_kb)

@dp.message_handler(regexp='Кто принимает участие')
async def WhoAttending(message: types.Message):
    mat = ""
    for m in mates:
        mat+= m
        mat+= "\n"
    if message.from_user.mention in mates:
        await message.answer(mat, reply_markup = second_kb)
    else:
        await message.answer(mat, reply_markup = first_kb)





@dp.message_handler(commands=['start'])
async def start_handler(event: types.Message):
    await event.answer(
        f"Привет, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML, reply_markup = first_kb
    )

@dp.message_handler(regexp='Регистрация')
async def Register(message: types.Message):
    mention = message.from_user.mention
    if mention not in mates:
        mates.append(mention)
        await message.answer(f"Регистрация успешная {mention}", reply_markup = second_kb)
    else:
        await message.answer(f"Вы уже зарегестрированны", reply_markup = second_kb)

    



@dp.message_handler(regexp='Для кого готовить подарок')
async def NewMate(message: types.Message):
    m = message.from_user.mention
    if m not in already_used:
        ym = await RandomizeMate(m)
        with codecs.open("mates.txt", "a", "utf-16") as stream:
            stream.write(f"{m} -> {ym}\n")
            stream.close()
        already_used.append(m)
        await message.answer(f"Ты тайный санта {ym}", reply_markup = second_kb)
    else:
        with codecs.open("mates.txt", "r", "utf-16") as stream:
            o = stream.read()
            for line in o.split("\n"):
                if f"{m} ->" in line:
                    await message.answer(f"Ты уже тайный санта {line}", reply_markup = second_kb)
                    return
        
        await message.answer(f"Произогла какая-то ошибка", reply_markup = second_kb)
        


async def RandomizeMate(mention):
    a = random.choice(mates)
    while(a == mention or a in used_mates):
        a = random.choice(mates)
    used_mates.append(a)
    return a


@dp.message_handler(commands=['debug_mates'])
async def start_handler(message: types.Message):
    mat = ""
    for m in mates:
        mat+= m
        mat+= "\n"
    await message.answer(mat, reply_markup = second_kb)

@dp.message_handler(commands=['debug_already_used'])
async def start_handler(message: types.Message):
    mat = ""
    for m in already_used:
        mat+= m
        mat+= "\n"
    await message.answer(mat, reply_markup = second_kb)

@dp.message_handler(commands=['debug_used_mates'])
async def start_handler(message: types.Message):
    mat = ""
    for m in used_mates:
        mat+= m
        mat+= "\n"
    await message.answer(mat, reply_markup = second_kb)


@dp.message_handler(commands=['debug_txt'])
async def start_handler(message: types.Message):
    with codecs.open("mates.txt", "r", "utf-16") as stream:
        mat = ""
        for m in stream:
            mat+= m
            mat+= "\n"
    await message.answer(mat, reply_markup = second_kb)


executor.start_polling(dp)