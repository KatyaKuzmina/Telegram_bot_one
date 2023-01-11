# -*- coding: utf-8 -*-
"""
bot_edann_1.py:
Contains the main part of the application.

translations.py:
Contains dictionary for main part.

ann_model_for_K-Zn-O_2.h5:
Contains ANN model for calculations.
The ANN model was provided by the EXAFS Laboratory of the Institute of Solid State Physics, University of Latvia.

Author: Katerina Kuzmina, kk20156
Title: Telegram bot
The program was created: 20.09.2022
"""

# Import additional libraries
import os
from keras.models import load_model
from scipy.interpolate import CubicSpline
import numpy as np
import matplotlib.pyplot as plt

# Library for telegram bot
import telebot
from telebot import types
from telebot import apihelper

# Import dictionary
from translations import engList, latList, ruList

# A middleware handler is a function that allows modifying requests or the bot context
# as they pass through the Telegram to the bot
# Middleware processing is disabled by default
apihelper.ENABLE_MIDDLEWARE = True

# Telegram bot token that is required to control the bot
token = '5800016315:AAFt3MJx7ZSPclTNLRWTTypWkxcejMqog2w'
tbot = telebot.TeleBot(token)

# List with the chemical elements
elementsList = [
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V',
    'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br',
    'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag',
    'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr',
    'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
    'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi',
    'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U']

# List with the absorption edges
edgesList = ('K', 'L1', 'L2', 'L3')

# List with the available power k_power for k^k_power in the EXAFS formula
powerList = ('1', '2', '3')

# Preventing tensorflow from polluting standard error
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

first_element = ''
second_element = ''
edge_element = ''
ann_model = ''
src_exp = ''

k_power = 2

language = engList  # default language

# List with the available commands
command = ['start', 'lang', 'help', 'edann', 'image']


# Gaussian window function for Fourier Transform
def windowgauss(x):
    ka = (x[0] + x[-1]) / 2.0
    kw = (x[-1] - x[0]) ** 2 / 9.210340372
    w = np.exp(-(x - ka) * (x - ka) / kw)
    return w


# Fourier Transform
def sft(fl, n, x, yr, yi, nn, t, fr, fi):
    con = np.sqrt(2.0 / np.pi)
    for jj in range(1, nn):
        r = 2.0 * t[jj]

        sn = np.sin(r * x) * fl
        cs = np.cos(r * x)
        wr = yr * cs - yi * sn
        wi = yr * sn + yi * cs

        r1 = 0.0
        r2 = 0.0
        for ii in range(1, n - 1):
            dx = (x[ii + 1] - x[ii]) / 2.0
            r1 = r1 + dx * (wr[ii + 1] + wr[ii])
            r2 = r2 + dx * (wi[ii + 1] + wi[ii])

        fr[jj] = r1 * con
        fi[jj] = r2 * con


# Modifying the message before it reaches any other handler
@tbot.middleware_handler(update_types=['message'])
def modify_message(bot_instance, message):
    # To let the user know what to do next
    if len(command) != 0:  # if list is empty then another function is running
        messages = message.text.strip('/')  # every command in telegram bot starts with a '/'
        messages.lower()
        # Checks if users input is a command
        if messages not in (string.lower() for string in command):
            tbot.reply_to(message, language['unknown'] + '"' + messages + '"'
                          + '\n\n' + language['commands'] + ': /help /lang /start /edann')


# Telegram bot will respond to some commands
# Using decorator we are handling filters that a message must pass
@tbot.message_handler(commands=['start'])
def start(message):
    # 'reply_to' - built-in method that allows the bot to respond
    # with a replying to a message that was sent by the user and passed to the function
    # language['some text'] - dictionary that stores phrases in different languages
    tbot.reply_to(message, language['welcome'])
    lang(message)  # calls function with languages


#  Displays the built-in keyboard with the languages to the user
@tbot.message_handler(commands=['lang'])
def lang(message):
    # creating a built-in keyboard with three buttons
    # callback_data is data that will be sent to query when button is pressed
    markup = types.InlineKeyboardMarkup(row_width=3)
    en = types.InlineKeyboardButton('English', callback_data="en")
    lv = types.InlineKeyboardButton('Latviešu', callback_data="lv")
    ru = types.InlineKeyboardButton('Русский', callback_data="ru")
    markup.add(en, lv, ru)  # adding buttons to the inline keyboard

    # Sending message with inline keyboard
    tbot.send_message(message.chat.id, language['language'], reply_markup=markup)


# Decorator accepts an anonymous function that returns True
@tbot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global language
    req = call.data  # The value of a callback

    # Declaring a dictionary based on the user's choice
    if req == 'en':
        language = engList
    elif req == 'lv':
        language = latList
    elif req == 'ru':
        language = ruList

    tbot.send_message(call.message.chat.id, language['welcome'])


# Display available commands
@tbot.message_handler(commands=['help'])
def help_line(message):
    tbot.send_message(message.chat.id, language['commands'] + ': /start /help /lang /edann')


# Main script with data analysis
@tbot.message_handler(commands=['edann'])
def edann(message):
    global command
    command.clear()

    print(message.chat.id)
    tbot.reply_to(message, language['first element'])

    # Built-in method that helps to register users next message and call next function
    tbot.register_next_step_handler(message, first_elem)


# Define the first element
def first_elem(message):
    global first_element

    first = message.text

    if first.lower() == 'stop':
        tbot.send_message(message.chat.id, language['terminate'])
        return

    # Checks if the users text is an element by casting the string from the user to lowercase
    # and comparing it to the lowercase elements of the given array
    first_lower = first.lower()
    is_in_list = first_lower in (string.lower() for string in elementsList)
    first = first.capitalize()  # Built-in function that capitalizes the first letter of a string

    # If user gave an element move to the next function.
    # Else the request for the first element is repeated
    if is_in_list:
        tbot.send_message(message.chat.id, language['first element answer'] + first)
        first_element = first

        tbot.send_message(message.chat.id, language['second element'])
        tbot.register_next_step_handler(message, second_elem)
    else:
        tbot.reply_to(message, language['not element'])
        tbot.send_message(message.chat.id, language['correct element'])
        tbot.register_next_step_handler(message, first_elem)


# Define the second element
def second_elem(message):
    global second_element

    second = message.text

    if second.lower() == 'stop':
        tbot.send_message(message.chat.id, language['terminate'])
        return

    # Checks if the users text is an element by casting the string from the user to lowercase
    # and comparing it to the lowercase elements of the given array
    second_lower = second.lower()
    is_in_list = second_lower in (string.lower() for string in elementsList)
    second = second.capitalize()

    # If user gave an element move to the next function.
    # Else the request for the second element is repeated
    if is_in_list:
        tbot.send_message(message.chat.id, language['second element answer'] + second)
        second_element = second

        tbot.send_message(message.chat.id, language['edge'])
        tbot.register_next_step_handler(message, edge_elem)
    else:
        tbot.reply_to(message, language['not element'])
        tbot.send_message(message.chat.id, language['correct element'])
        tbot.register_next_step_handler(message, second_elem)


# Define the absorption edge of the first element
def edge_elem(message):
    global edge_element

    edge = message.text

    if edge.lower() == 'stop':
        tbot.send_message(message.chat.id, language['terminate'])
        return

    # Check if the users text is an element
    edge_lower = edge.lower()
    is_in_list = edge_lower in (string.lower() for string in edgesList)
    edge = edge.capitalize()

    if is_in_list:
        tbot.send_message(message.chat.id, language['first element edge'] + edge + '.')
        edge_element = edge

        tbot.send_message(message.chat.id, language['power'])
        tbot.register_next_step_handler(message, power_k)
    else:
        tbot.reply_to(message, language['not edge'])
        tbot.send_message(message.chat.id, language['correct edge'])
        tbot.register_next_step_handler(message, edge_elem)


# k_power for k^k_power in the EXAFS formula
def power_k(message):
    global k_power_n

    k_power_n = message.text

    if k_power_n.lower() == 'stop':
        tbot.send_message(message.chat.id, language['terminate'])
        return

    is_in_list = k_power_n in powerList

    if is_in_list:
        tbot.send_message(message.chat.id, language['multiplication'] + k_power_n + ".")

        tbot.send_message(message.chat.id, language['file'])
        tbot.register_next_step_handler(message, main_part)
    else:
        tbot.reply_to(message, language['not power'])
        tbot.send_message(message.chat.id, language['power'])
        tbot.register_next_step_handler(message, power_k)


# Main part of the script
def main_part(message):
    global first_element
    global second_element
    global edge_element
    global src_exp
    global ann_model
    global k_power_n
    global command

    # Checks if user's input is a file anf if it is a stop word
    if message.content_type != 'document':
        if message.text.lower() == 'stop':
            tbot.send_message(message.chat.id, language['terminate'])
            return
        else:
            tbot.send_message(message.chat.id, language['not file'])  # if not a file, ask for the file again
            tbot.register_next_step_handler(message, main_part)
    else:
        file_info = tbot.get_file(message.document.file_id).file_path

        downloaded_file = tbot.download_file(file_info)

        src_exp = message.document.file_name
        with open(src_exp, 'wb') as new_file:
            new_file.write(downloaded_file)

        print()
        print('********************************************')
        print('*                                          *')
        print('*                  EDA-NN                  *')
        print('*                   v1.0                   *')
        print('*                                          *')
        print('*              Telegram bot                *')
        print('*                                          *')
        print('********************************************')
        print()

        first_element_index = elementsList.index(first_element) + 1
        second_element_index = elementsList.index(second_element) + 1

        print('First element: ' + first_element + '  Z=' + str(first_element_index))
        print('Second element: ' + second_element + '  Z=' + str(second_element_index))
        print('The absorption edge of the first element (' + first_element + ') is: ' + edge_element)
        print()

        ann_model = 'ann_model_for_' + edge_element + '-' + first_element + '-' + second_element + '_' + k_power_n + '.h5'

        nmaxdata = 1000


        #  Load experimental EXAFS spectrum
        print('Reading experimental EXAFS spectrum: ' + src_exp)
        print()

        filename = src_exp

        data = np.loadtxt(filename, comments='#', skiprows=0)

        ke = data[:, 0]  # All the first column of the dataset

        xte = data[:, 1]  # All the second column of the dataset

        # Show experimental EXAFS spectrum
        plt.clf()  # Clears the entire current figure with all its axes
        plt.plot(ke, xte, 'r')  # Draws a line in a red color
        plt.title('Experimental EXAFS spectrum')
        plt.xlabel('Wavenumber k')
        plt.ylabel('EXAFS chi(k)k^' + k_power_n)
        plt.savefig('exp_exafs.png')

        print()

        #   RDF g(r) in R-space
        dR = 0.02

        r = np.arange(1, 4, dR)  # Array creation with 0.02 interval between 1 and 4
        nr = r.size
        print('Number of points in R-space: ', nr, '  Step dR=', dR)
        print()

        g = np.empty(shape=nr)
        g.fill(0)


        #  EXAFS k-space
        dk = 0.05
        kmin = 2.5
        kmax = 16.0


        # Check range in k-space
        if kmin < ke[0]:
            if int(ke[0] * 10) / 10 == ke[0]:
                kmin = ke[0]
            else:
                kmin = int(ke[0] * 10) / 10 + 0.05
        if kmin < ke[0]:
            kmin = kmin + 0.05

        if kmax > ke[-1]:
            if int(ke[-1] * 10) / 10 == ke[-1]:
                kmax = ke[-1]
            else:
                kmax = int(ke[-1] * 10) / 10 + 0.05
        if kmax > ke[-1]:
            kmax = kmax - 0.05

        x = np.arange(kmin, kmax, dk)  # Array creation with 0.05 interval
        n = x.size
        print('Number of points in k-space: ', n, '  Step dk=', dk)
        print('Range in k-space:')
        print('  Kmin=', kmin)
        print('  Kmax=', kmax)
        print()

        w = np.empty(shape=n)
        w.fill(0)

        # Window 10%Gauss function for FT
        w = windowgauss(x)

        # FT r-space
        dr = 0.02
        t = np.arange(0, 4, dr)
        nt = t.size

        print('Number of points in r-space: ', nt, '  Step dr=', dr)
        print()

        # creating arrays and filling with 0
        fi = np.empty(shape=nt)
        fi.fill(0)

        fr = np.empty(shape=nt)
        fr.fill(0)

        ft = np.empty(shape=(nmaxdata, nt))
        ft.fill(0)

        ftchi = np.empty(shape=(1, nt))
        ftchi.fill(0)

        yi = np.empty(shape=n)
        yi.fill(0)
        yr = np.empty(shape=n)
        yr.fill(0)

        y = np.empty(shape=(nmaxdata, n))
        y.fill(0)

        chi = np.empty(shape=(1, n))
        chi.fill(0)

        fty = np.empty(shape=(n + nt))
        fty.fill(0)
        ftychi = np.empty(shape=(n + nt))
        ftychi.fill(0)

        print('The ANN model name: ' + ann_model)
        print()

        # Check if ANN model exists
        if not os.path.exists(ann_model):
            print("The ANN model does not exist.\n\n")
            tbot.send_message(message.chat.id, language['not ann'])

        else:
            print('The ANN model exists!')
            tbot.send_message(message.chat.id, language['ann'])

        print()

        # Load model
        # Reload a fresh Keras model from the saved model
        model = load_model(ann_model)

        print("Loading the ANN model ...")
        print()
        tbot.send_message(message.chat.id, language['loading'])

        ff = CubicSpline(ke, xte, bc_type='natural')
        chi[0, :] = ff(x)

        # Show experimental EXAFS spectrum before and after interpolation
        plt.clf()
        plt.plot(ke, xte, 'ro')
        plt.plot(x, chi[0, :], 'b')
        plt.title('Experimental EXAFS spectrum before (red) and after (blue) interpolation')
        plt.xlabel('Wavenumber k')
        plt.ylabel('EXAFS chi(k)k^' + k_power_n)
        plt.savefig('exp_exafs.png')
        #    plt.show()
        photo = open('exp_exafs.png', 'rb')
        tbot.send_photo(message.chat.id, photo)

        yi.fill(0)
        yr = chi[0, :] * w

        # Calculate Fourier transform of the experimental EXAFS spectrum
        sft(-1, n, x, yr, yi, nt, t, fr, fi)
        ftchi[0, :] = np.sqrt(fr * fr + fi * fi)

        fltype = 2

        if fltype == 0:
            ftychi = chi

        if fltype == 1:
            ftychi = ftchi

        if fltype == 2:
            ftychi = np.concatenate((chi, ftchi), axis=1)

        print("Predicting RDF ...")
        print()
        tbot.send_message(message.chat.id, language['rdf'])

        g.fill(0)

        # Result
        g = model.predict(ftychi)

        with open('rdf_' + src_exp, 'w') as f:
            for i in range(0, nr):
                f.write(str(r[i]) + ' ' + str(g[0, i]))
                f.write('\n')
        f.close()

        # plot the predicted RDF
        plt.clf()
        plt.plot(r, g[0, :], 'b')
        plt.title('Predicted RDF')
        plt.xlabel('Distance R')
        plt.ylabel('Predicted RDF g(R)')
        plt.savefig('predicted_rdf.png')
        #    plt.show()

        photo = open('predicted_rdf.png', 'rb')
        tbot.send_photo(message.chat.id, photo)

        photo = open('rdf_' + src_exp, 'rb')
        tbot.send_document(message.chat.id, photo)

        print("Done.")
        print()

        tbot.send_message(message.chat.id, language['done'])

        command = ['start', 'lang', 'help', 'edann', 'image']


tbot.infinity_polling()  # to launch the bot
