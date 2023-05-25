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

# Создание приветственного сообщения и клавиатуры
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    global flag_audiobook_name, has_list_of_books
    flag_audiobook_name = False
    has_list_of_books = False
    button1 = KeyboardButton("Получить аудиокнигу 📖")
    button2 = KeyboardButton("Инфо 🔎")
    button3 = KeyboardButton("Поддержать создателей 💸")
    main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(button1).row(button2, button3)
    await message.answer("Воспользуйтесь кнопками 👇", reply_markup=main_keyboard)


# Получение аудиокниги
@dp.message_handler()
async def getter_audiobook(message: types.Message):
    global flag_audiobook_name, books_names, has_list_of_books, books

    if message.text.lower() == "меню":
        await send_welcome(message)

    if has_list_of_books: # пользователь ввёл название книги
        book_name = message.text
        if book_name == "Нет подходящего варианта":
            has_list_of_books = False
            flag_audiobook_name = True
            await message.answer("Попробуйте ввести название книги как-нибудь по-другому", reply_markup=types.ReplyKeyboardRemove())
        elif book_name not in books_names:
            await message.answer("Используйте кнопки, чтобы выбрать подходящий вариант")
        else:
            await message.answer(
                "Началось создание аудиокниги. Пожалуйста, подождите, этот процесс может занять длительное время", 
                reply_markup=types.ReplyKeyboardRemove()
            )
            mp3_dir = get_mp3(book_name, books_names, books)
            audio = open(mp3_dir, 'rb')
            await bot.send_audio(message.chat.id, audio)
            await send_welcome(message)

    if flag_audiobook_name: # пользователь ввёл Получить аудиокнигу
        user_search = message.text
        if user_search != "Нет подходящего варианта":
            flag_audiobook_name = False
            choose_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            books_names, books = tululu_parser(user_search)
            if len(books_names) == 0:
                has_list_of_books = False
                flag_audiobook_name = True
                await message.answer("Попробуйте ввести название книги как-нибудь по-другому", reply_markup=types.ReplyKeyboardRemove())
            else:
                for i in range(len(books_names)):
                    button = KeyboardButton(books_names[i])
                    choose_keyboard.row(button)
                choose_keyboard.row("Нет подходящего варианта")
                has_list_of_books = True
                await message.answer("Выберите один из представленных вариантов", reply_markup=choose_keyboard)

    if message.text == "Получить аудиокнигу 📖":
        flag_audiobook_name = True
        has_list_of_books = False
        await message.answer("Введите автора и название произведения", reply_markup=types.ReplyKeyboardRemove())
    
    if message.text == "Инфо 🔎" or message.text.lower() == "инфо" or message.text == "/help":
        flag_audiobook_name = False
        has_list_of_books = False
        await message.answer("Я создан, чтобы создавать аудиокниги по Вашему запросу. " + 
                            "Нажимайте на кнопки, чтобы воспользоваться мной. " +
                            'Напишите "меню", чтобы вызвать кнопки главного меню')
        
    if message.text == "Поддержать создателей 💸":
        await message.answer("Вот ссылка для перевода денежных средств: https://www.donationalerts.com/id8359254\n" +
                             "Спасибо за оказанную поддержку!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
