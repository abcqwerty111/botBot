# -*- coding: utf-8 -*-
import telebot
from telebot import *
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('1046005810:AAG1-tPwvEb5nwEpigoDLuk4vDhuYDULI2M')

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Казахстан')
    markup.add('Мир')
    msg = bot.reply_to(message, 'Привет, я умею только показывать количество заражённых людей в Казахстане и мире', reply_markup=markup)
    bot.register_next_step_handler(msg, process_step)

def process_step(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Казахстан')
    markup.add('Мир')
    if message.text=='Казахстан':
        page_link = 'https://www.coronavirus2020.kz'
        headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        response = requests.get(page_link, headers = headers)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        confirmed = soup.find('span', attrs = {'class': 'number_cov marg_med'}).text
        confirmed = confirmed.replace(' ', '')
        confirmed_city = soup.find('div', attrs = {'class': 'city_cov'}).text
        confirmed_city = confirmed_city.replace(' ', '')
        confirmed_city = confirmed_city.replace('Нур-Султан', 'Астана')
        confirmed_city = confirmed_city.replace('–', ' – ')
        confirmed_city = confirmed_city.replace('аяоб', 'ая об')
        recovered = soup.find('div', attrs = {'class': 'recov_bl'}).text
        recovered = recovered.replace(' ', '')
        recovered = recovered.replace('Выздоровевших:', '')
        for city in soup.find_all('div', attrs = {'class': 'red_line_covid_bl'}):
        	recovered_city = city.find('div', attrs = {'class': 'city_cov'}).text
        recovered_city = recovered_city.replace(' ', '')
        recovered_city = recovered_city.replace('Нур-Султан', 'Астана')
        recovered_city = recovered_city.replace('–', ' – ')
        recovered_city = recovered_city.replace('аяоб', 'ая об')
        deaths = soup.find('div', attrs = {'class': 'deaths_bl'}).text
        for city in soup.find_all('div', attrs = {'class': 'deaths_bl'}):
        	deaths_city = city.find('div', attrs = {'class': 'city_cov'}).text
        deaths = deaths.replace(deaths_city, '')
        deaths = deaths.replace(' ', '')
        deaths = deaths.replace('Летальныхслучаев:', '')
        deaths = deaths.replace('\n', '')
        deaths_city = deaths_city.replace(' ', '')
        deaths_city = deaths_city.replace('Нур-Султан', 'Астана')
        deaths_city = deaths_city.replace('–', ' – ')
        deaths_city = deaths_city.replace('аяоб', 'ая об')
        active = str(int(confirmed) - int(recovered) - int(deaths))
        report = f'''ПОДТВЕРЖДЁННЫХ СЛУЧАЕВ: {confirmed}
	{confirmed_city}
ВЫЗДОРОВЕВШИХ: {recovered}
	{recovered_city}
ЛЕТАЛЬНЫХ СЛУЧАЕВ: {deaths}
	{deaths_city}
АКТИВНЫХ: {active}'''
        bot.send_message(chat_id, report, reply_markup=markup)
    elif message.text=='Мир':
        page_link = 'https://www.worldometers.info/coronavirus'
        response = requests.get(page_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        my_line = soup.find_all('div', class_ = 'maincounter-number')
        wconfirmed = int(my_line[0].text.strip().replace(',', ''))
        wdeaths = int(my_line[1].text.strip().replace(',', ''))
        wrecovered = int(my_line[2].text.strip().replace(',', ''))
        active_cases = wconfirmed - wdeaths - wrecovered
        wreport = f'''ПОДТВЕРЖДЁННЫХ СЛУЧАЕВ (В МИРЕ): {wconfirmed}

ВЫЗДОРОВЕВШИХ (В МИРЕ): {wrecovered}
ЛЕТАЛЬНЫХ СЛУЧАЕВ (В МИРЕ): {wrecovered}
АКТИВНЫХ (В МИРЕ): {active_cases}'''
        bot.send_message(chat_id, wreport, reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Извините, Вы сделали что-то не так', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_echo(message):
	process_step(message)

bot.polling(none_stop = True)
