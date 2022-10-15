import telebot
from constants import token

tbot = telebot.TeleBot(token)

elementsList = (
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V',
    'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br',
    'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag',
    'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr',
    'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
    'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi',
    'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U')

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
    tbot.send_photo(message.chat.id, open('images/blue_thermal.jpg', 'rb'))
    # tbot.send_photo(open('blue_thermal.jpg', 'rb'))


# File downloading
@tbot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    # chat_id = message.chat.id
    file_info = tbot.get_file(message.document.file_id).file_path
    downloaded_file = tbot.download_file(file_info)
    src = 'C:/katja/Uni/5_Sem/pythonProject/Bot_three/files/' + message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    tbot.reply_to(message, "I will take it with me")


# Ask for the two elements and a file
@tbot.message_handler(commands=['element'])
def send_instruction(message):
    tbot.reply_to(message, "Please input first element")
    tbot.register_next_step_handler(message, first_elem)


def first_elem(message):
    first = message.text

    # Check if the users text is an element
    first_lower = first.lower()
    is_in_list = first_lower in (string.lower() for string in elementsList)

    if is_in_list:
        tbot.send_message(message.chat.id, "Your first element is " + first)

        tbot.send_message(message.chat.id, "Please input second element")
        tbot.register_next_step_handler(message, second_elem)
    else:
        tbot.reply_to(message, "It is no an element")
        tbot.send_message(message.chat.id, "Please input an element")
        tbot.register_next_step_handler(message, first_elem)


def second_elem(message):
    second = message.text

    # Check if the users text is an element
    second_lower = second.lower()
    is_in_list = second_lower in (string.lower() for string in elementsList)

    if is_in_list:
        tbot.send_message(message.chat.id, "Your second element is " + second)

        tbot.send_message(message.chat.id, "Please give us file")
        tbot.register_next_step_handler(message, handle_docs)
    else:
        tbot.reply_to(message, "It is no an element")
        tbot.send_message(message.chat.id, "Please input an element")
        tbot.register_next_step_handler(message, second_elem)


def handle_docs(message):
    # chat_id = message.chat.id
    file_info = tbot.get_file(message.document.file_id).file_path
    downloaded_file = tbot.download_file(file_info)
    src = 'C:/katja/Uni/5_Sem/pythonProject/Bot_three/files/' + message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    tbot.reply_to(message, "I will take it with me, thanks")

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

async def main():
    # use in for delete with the necessary scope and language_code if necessary
    tbot.delete_my_commands(scope=None, language_code=None)

    tbot.set_my_commands(
        commands=[
            telebot.types.BotCommand("command1", "command1 description"),
            telebot.types.BotCommand("command2", "command2 description")
        ],
        #scope=telebot.types.BotCommandScopeChat(12345678)  # use for personal command menu for users
        scope=telebot.types.BotCommandScopeAllPrivateChats()  # use for all private chats
    )

    cmd = tbot.get_my_commands(scope=None, language_code=None)
    print([c.to_json() for c in cmd])

"""""
@dp.message_handler(commands=['button'])
async def button()
"""""

"""""
Language change
"""""


def main():
    tbot.polling()


if __name__ == '__main__':
    main()

#      executor.start_polling(dp, skip_updates=True)
#
# executor.start_polling(tbot)
