#TODO: 1. Убрать заглушку в сообщении
#TODO: 2. Написать информацию о боте

import config
from parsing import tululu_parser, get_mp3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton


bot = Bot(token=config.token)
dp = Dispatcher(bot)

flag_audiobook_name = False
has_list_of_books = False
books_names = list()
books = list()
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
    global flag_audiobook_name, books_names, has_list_of_books, books
    if has_list_of_books:
        book_name = message.text
        await message.answer("Началось создание аудиокниги")
        get_mp3(book_name, books_names, books)
        
        # TODO отправлять мп3

    if flag_audiobook_name:
        user_search = message.text
        flag_audiobook_name = False
        choose_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        books_names, books = tululu_parser(user_search)
        for i in range(len(books_names)):
            button = KeyboardButton(books_names[i])
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