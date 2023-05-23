#TODO: 1. Убрать заглушку в сообщении
#TODO: 2. Написать информацию о боте
#TODO: 3. Заменить на использование функции после считывания автра и названия
#TODO: 4. Заменить массив на корректный

import config
from parsing import tululu_parser, get_mp3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton


bot = Bot(token=config.token)
dp = Dispatcher(bot)

flag_audiobook_name = False
has_list_of_books = False
books_names = list()
#Создание приветственного сообщения и клавиатуры
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    button1 = KeyboardButton("Получить аудиокнигу 📖")
    button2 = KeyboardButton("Инфо 🔎")
    button3 = KeyboardButton("Поддержать создателей 💸")
    button4 = KeyboardButton("Инфо")
    main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(button1,button2).row(button3,button4)
    # 1.
    await message.reply("Заглушка", reply_markup=main_keyboard)


#Получение аудиокниги, 
@dp.message_handler()
async def getter_audiobook(message: types.Message):
    global flag_audiobook_name, books_names, has_list_of_books
    if has_list_of_books:
        book_name = message.text
        get_mp3(book_name, books_names, books)
        # TODO отправлять мп3

    if flag_audiobook_name:
        #3.
        user_search = message.text
        await message.reply(message.text + "аа")
        flag_audiobook_name = False
        choose_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        #4. 
        # a = ["Мастер и Маргарита М. А. Булгаков", "Герой нашего времени М. Ю. Лермонтов"]
        books_names, books = tululu_parser(user_search)
        for i in range(len(books)):
            button = KeyboardButton(books[i])
            choose_keyboard.row(button)
        choose_keyboard.row("Нет подходящего варианта")
        has_list_of_books = True
        await message.answer("Выберите один из представленных вариантов", reply_markup=choose_keyboard)

    if message.text == "Получить аудиокнигу 📖":
        flag_audiobook_name = True
        await message.reply("Введите автора и название произведения")
    if message.text == "Инфо 🔎" or message.text.lower() == "инфо" or message.text == "/help":
        #2.
        await message.reply("Здесь содержиться информация о боте")


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)