# -*- coding: utf-8 -*-
import telebot
from telebot import *
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('1046005810:AAG1-tPwvEb5nwEpigoDLuk4vDhuYDULI2M')

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Показать')
    msg = bot.reply_to(message, 'Привет, я умею только показывать количество заражённых людей в Казахстане', reply_markup=markup)
    bot.register_next_step_handler(msg, process_step)

def process_step(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Показать')
    if message.text=='Показать':
        page_link = 'https://www.coronavirus2020.kz/ru'
        headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        response = requests.get(page_link, headers = headers)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        confirmed = soup.find('span', attrs = {'class': 'number_cov marg_med'}).text
        confirmed = confirmed.replace(' ', '')
        deaths = soup.find('div', attrs = {'class': 'deaths_bl'}).text
        deaths = deaths.replace('Летальных случаев:', '')
        deaths = deaths.replace(' ', '')
        deaths = deaths.replace('\n', '')
        recovered = soup.find('div', attrs = {'class': 'recov_bl'}).text
        recovered = recovered.replace('Выздоровевших:', '')
        recovered = recovered.replace(' ', '')
        active = str(int(confirmed) - int(deaths) - int(recovered))
        city = soup.find('div', attrs = {'class': 'city_cov'}).text
        city = city.replace('  ', ' ')
        city = city.replace('  ', ' ')
        city = city.replace('  ', ' ')
        city = city.replace('  ', ' ')
        report = f'''Подтверждённых случаев: {confirmed}
Летальных случаев: {deaths}
Выздоровевших: {recovered}
Активных: {active}

Информация по областям:{city}'''
        bot.send_message(chat_id, report, reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Извините, Вы сделали что-то не так', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_echo(message):
	process_step(message)

bot.polling(none_stop = True)
