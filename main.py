import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton



Api_Token = "8578569004:AAFPIZQ_b0vg-AHdkJ1DPLjM3fh64DvQ-Dg"
Weather_Token = "1b5471bb9ac251f894988f1bf8d4cf4e"


my_bot = Bot(token=Api_Token)

disp = Dispatcher()

# @disp.message(CommandStart())
# async def hello(msg:Message):
#     await msg.answer("Привіт. Я новий бот!")

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Start"), KeyboardButton(text="Clear"), KeyboardButton(text="Clearall")],
        [KeyboardButton(text="ShowWeather"), KeyboardButton(text="Надіслати локацію", request_location=True)]
    ],
    resize_keyboard=True
)

@disp.message(CommandStart())
async def hello_button(msg: Message):
    await msg.answer("Привіт, Я новий бот", reply_markup=main_keyboard)

# Обробка кнопки "Start"
@disp.message(lambda msg: msg.text == "Start")
async def start_button(msg: Message):
    await msg.answer("Ви натиснули кнопку Start!")

# Обробка кнопки "Clear"
@disp.message(lambda msg: msg.text == "Clear")
async def clear_button(msg: Message):
    try:
        await my_bot.delete_message(msg.chat.id, msg.message_id - 1)
    except:
        await msg.answer("Немає повідомлення для видалення.")


# @disp.message(CommandStart())
# async def hello_button(msg:Message):
#     keyb = ReplyKeyboardMarkup(keyboard=[
#     [
#         KeyboardButton(text="Clear"),]
#     ], resize_keyboard=True)
#     await msg.answer("Привіт, Я новий бот",
#                      reply_markup=keyb)
#
#
# @disp.message(Command("clear"))
# async def clear(msg:Message):
#     await my_bot.delete_message(msg.chat.id, msg.message_id-1)

@disp.message(lambda msg: msg.text == "Clearall")
async def clearall(msg:Message):
    for i in range(10):
        try:
            await my_bot.delete_message(msg.chat.id, msg.message_id-i)
        except:
            pass

# Обробка кнопки "ShowWeather"
@disp.message(lambda msg: msg.text == "ShowWeather")
async def show_weather(msg: Message):
    await msg.answer("Будь ласка, надішліть свою локацію кнопкою")

# Обробка отриманої локації
@disp.message(lambda msg: msg.location is not None)
async def get_weather(msg: Message):
    lat = msg.location.latitude
    lon = msg.location.longitude

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={Weather_Token}&units=metric&lang=ua"


    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    if data.get("main"):
        temp = data["main"]["temp"]
        city = data["name"]
        await msg.answer(f"Температура: {temp}°C\n Місто: {city}")
    else:
        await msg.answer("Не вдалося отримати дані про погоду.")


async def start_bot():
    await disp.start_polling(my_bot)

asyncio.run(start_bot())