import telebot

token = ('5411588162:AAGHrl2GOjG6Uz1F2DxlTmrs6PQ_Z4JAIuM')
tbot = telebot.TeleBot(token)

# Greetnings command

@tbot.message_handler(commands=['start'])
def send_welcome(message):
    tbot.reply_to(message, "Hello")


@tbot.message_handler(commands=['help'])
def send_help(message):
    tbot.send_message(message.chat.id, "Some information")


# Image sending by URL

@tbot.message_handler(commands=['image'])
def send_photo(message):
    tbot.send_photo(message.chat.id, "https://www.python.org/static/community_logos/python-powered-h-140x182.png")


# Image sending by file path

@tbot.message_handler(commands=['image2'])
def welcome(message):
    tbot.send_photo(message.chat.id, open('blue_thermal.jpg', 'rb'))
    # tbot.send_photo(open('blue_thermal.jpg', 'rb'))


# File downloading
@tbot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    # chat_id = message.chat.id
    file_info = tbot.get_file(message.document.file_id).file_path
    downloaded_file = tbot.download_file(file_info)
    src = 'C:/katja/Uni/5_Sem/pythonProject/Bot_three/' + message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    tbot.reply_to(message, "I will take it with me")


# Language selection

# answers = []
#
# lang1 = KeyboardButton('English 👍')
# lang2 = KeyboardButton('russian 💪')
# lang3 = KeyboardButton('Other language 🤝')
# lang_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(lang1).add(lang2).add(lang3)
#
#
# @dp.message_handler(commands=['language'])
# async def welcome(message: types.Message):
#     await message.answer('Choose lang', reply_markup=lang_kb)
#
#
# en_options1 = KeyboardButton('Selection one')
# en_options2 = KeyboardButton('Selection two')
# en_options3 = KeyboardButton('Selection three')
# en_options4 = KeyboardButton('Selection four')
# en_options_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(en_options1).add(en_options2).add(
#     en_options3).add(en_options4)
#
#
# #### selecting what you need
# @dp.message_handler(regexp='English 👍')
# async def english(message: types.Message):
#     answers.append(message.text)
#     await message.answer('What do you need?', reply_markup=en_options_kb)
#
#
# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text)


"""""
@dp.message_handler(commands=['button'])
async def button()
"""""

"""""
Language change
"""""

tbot.infinity_polling()

# if __name__ == '__main__':
#      executor.start_polling(dp, skip_updates=True)
#
# executor.start_polling(tbot)
