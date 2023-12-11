from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
import logging
import markups as nav
from db import Database
from datetime import datetime

import markups

import requests
from bs4 import BeautifulSoup

TOKEN = "5732063079:AAHkoHewxztujteKTh8QUWEqwqsBQN624a8"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = Database('database.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Введите ваше ФИО:")
        db.set_signup_status(message.from_user.id, "setfio")
    else:
        await bot.send_message(message.from_user.id, "Вы уже зарегистрированы!", reply_markup=nav.mainMenu)


@dp.message_handler()
async def handle_text_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Профиль студента':
            fio = db.get_fio(message.from_user.id)
            birthdate = db.get_birthdate(message.from_user.id)
            contacts = db.get_contacts(message.from_user.id)
            faculty = db.get_faculty(message.from_user.id)
            nickname = db.get_nickname(message.from_user.id)

            if fio:
                await bot.send_message(message.from_user.id, f"ФИО: {fio}")
            else:
                await bot.send_message(message.from_user.id, "ФИО не задано")

            if birthdate:
                await bot.send_message(message.from_user.id, f"Дата рождения: {birthdate}")
            else:
                await bot.send_message(message.from_user.id, "Дата рождения не задана")

            if contacts:
                await bot.send_message(message.from_user.id, f"Контакты: {contacts}")
            else:
                await bot.send_message(message.from_user.id, "Контакты не заданы")

            if faculty:
                await bot.send_message(message.from_user.id, f"Факультет: {faculty}")
            else:
                await bot.send_message(message.from_user.id, "Факультет не задан")

            if nickname:
                await bot.send_message(message.from_user.id, f"Никнейм: {nickname}")
            else:
                await bot.send_message(message.from_user.id, "Никнейм не задан")

            await bot.send_message(message.from_user.id, "Что вы хотите сделать?", reply_markup=nav.studentProfileMenu)

        elif db.get_signup_status(message.from_user.id) == "setfio":
            db.set_fio(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id, "Введите вашу дату рождения (в формате ДД.ММ.ГГГГ):")
            db.set_signup_status(message.from_user.id, "setbirthdate")
        elif db.get_signup_status(message.from_user.id) == "setbirthdate":
            db.set_birthdate(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id, "Введите ваши контакты (номер телефона, email и т.д.):")
            db.set_signup_status(message.from_user.id, "setcontacts")
        elif db.get_signup_status(message.from_user.id) == "setcontacts":
            db.set_contacts(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id, "Введите ваш факультет:")
            db.set_signup_status(message.from_user.id, "setfaculty")
        elif db.get_signup_status(message.from_user.id) == "setfaculty":
            db.set_faculty(message.from_user.id, message.text)
            await bot.send_message(message.from_user.id, "Введите ваш никнейм:")
            db.set_signup_status(message.from_user.id, "setnickname")
        elif db.get_signup_status(message.from_user.id) == "setnickname":
            if len(message.text) > 60:
                await bot.send_message(message.from_user.id, "Превышено максимальное количество символов!")
            elif '@' in message.text or '/' in message.text:
                await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ!")
            else:
                db.set_nickname(message.from_user.id, message.text)
                db.set_signup_status(message.from_user.id, "done")
                await bot.send_message(message.from_user.id, "Регистрация прошла успешно!", reply_markup=nav.mainMenu)
        elif message.text == 'Редактирование профиля':
            await bot.send_message(message.from_user.id, "Выберите, что хотите отредактировать:",
                                   reply_markup=nav.editProfileMenu)

        elif message.text == 'Редактировать ФИО':
            await bot.send_message(message.from_user.id, "Введите новое ФИО:")
            db.set_signup_status(message.from_user.id, "editfio")
        elif message.text == 'Редактировать дату рождения':
            await bot.send_message(message.from_user.id, "Введите новую дату рождения (в формате ДД.ММ.ГГГГ):")
            db.set_signup_status(message.from_user.id, "editbirthdate")
        elif message.text == 'Редактировать контакты':
            await bot.send_message(message.from_user.id, "Введите новые контакты:")
            db.set_signup_status(message.from_user.id, "editcontacts")
        elif message.text == 'Редактировать факультет':
            await bot.send_message(message.from_user.id, "Введите новый факультет:")
            db.set_signup_status(message.from_user.id, "editfaculty")
        elif message.text == 'Редактировать никнейм':
            await bot.send_message(message.from_user.id, "Введите новый никнейм:")
            db.set_signup_status(message.from_user.id, "editnickname")

        elif db.get_signup_status(message.from_user.id) == "editfio":
            db.set_fio(message.from_user.id, message.text)
            db.set_signup_status(message.from_user.id, "done")
            await bot.send_message(message.from_user.id, "ФИО успешно обновлено!", reply_markup=nav.studentProfileMenu)
        elif db.get_signup_status(message.from_user.id) == "editbirthdate":
            db.set_birthdate(message.from_user.id, message.text)
            db.set_signup_status(message.from_user.id, "done")
            await bot.send_message(message.from_user.id, "Дата рождения успешно обновлена!",
                                   reply_markup=nav.studentProfileMenu)
        elif db.get_signup_status(message.from_user.id) == "editcontacts":
            db.set_contacts(message.from_user.id, message.text)
            db.set_signup_status(message.from_user.id, "done")
            await bot.send_message(message.from_user.id, "Контакты успешно обновлены!",
                                   reply_markup=nav.studentProfileMenu)
        elif db.get_signup_status(message.from_user.id) == "editfaculty":
            db.set_faculty(message.from_user.id, message.text)
            db.set_signup_status(message.from_user.id, "done")
            await bot.send_message(message.from_user.id, "Факультет успешно обновлен!",
                                   reply_markup=nav.studentProfileMenu)
        elif db.get_signup_status(message.from_user.id) == "editnickname":
            if len(message.text) > 60:
                await bot.send_message(message.from_user.id, "Превышено максимальное количество символов!")
            elif '@' in message.text or '/' in message.text:
                await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ!")
            else:
                db.set_nickname(message.from_user.id, message.text)
                db.set_signup_status(message.from_user.id, "done")
                await bot.send_message(message.from_user.id, "Никнейм успешно обновлен!",
                                       reply_markup=nav.studentProfileMenu)

        elif message.text == 'Посещаемость и успеваемость студента':
            await bot.send_message(message.from_user.id,
                                   "Здесь вы можете узнать о своей посещаемости и успеваемости, зафиксировать какие у вас есть задолжности, так же узнать расписание и курсы текущего семестра: [ссылка](https://moodle.pnzgu.ru/)",
                                   parse_mode='Markdown')
        elif message.text == 'Институты ПГУ':
            week_number = datetime.now().isocalendar()[1]
            current_week = "Первая неделя" if week_number % 2 == 1 else "Вторая неделя"
            schedule_text = f"Текущая неделя: {current_week}\n\nВыберите институт:"
            await bot.send_message(message.from_user.id, schedule_text, reply_markup=nav.facultyMenu)
        elif message.text == 'Поступающим':

            await bot.send_message(message.from_user.id,
                                   "Здесь вы найдите ифнормацию для поступающих: [ссылка](https://pnzgu.ru/Abitur/abitur_2023)",
                                   parse_mode='Markdown')
            file_path = 'C:\\Users\\zelen\\OneDrive\\Документы\\pravila_priema_bs_2023.pdf'
            with open(file_path, 'rb') as file:
                await message.reply_document(file)
        elif message.text == 'Наука':
            await bot.send_message(message.from_user.id,
                                   "Здесь вы можете получить множество полезных ресурсов, ссылок на различные сайты помогающие в обучении, а так же конкурсы, гранты, на иновационные проекты, множество научных изадний, мероприятий на справочные и научные материалы и на НИИФиПИ: [ссылка](https://science.pnzgu.ru/)",
                                   parse_mode='Markdown')
        elif message.text == 'Контакты ПГУ':
            contacts_text = "Контакты ПГУ:\n\nE-mail: cnit@pnzgu.ru\nТелефон: +7 (8412) 66-64-19\nАдрес: 440026, г. Пенза, ул. Красная, 40\nСоциальная сеть Вконтаке: https://vk.com/pnzgu\n\nСсылка на местоположение объекта в приложении 2gis: [ссылка](https://2gis.ru/penza/geo/5911958058440784/45.003972351551056,53.18122453061585)"
            await bot.send_message(message.from_user.id, contacts_text, parse_mode='Markdown')
        elif message.text == 'Медицинский институт':
            await bot.send_message(message.from_user.id, "Открываю веб-сайт Медицинский институт: [ссылка](https://i_med.pnzgu.ru)",
                                   parse_mode='Markdown')
        elif message.text == 'Юридический институт':
            await bot.send_message(message.from_user.id, "Открываю веб-сайт Юридический институт: [ссылка](https://fyur.pnzgu.ru)",
                                   parse_mode='Markdown')
        elif message.text == 'Институт экономики и управления':
            await bot.send_message(message.from_user.id, "Открываю веб-сайт Институт экономики и управления: [ссылка](https://feiu.pnzgu.ru)",
                                   parse_mode='Markdown')
        elif message.text == 'Институт международного сотрудничества':
            await bot.send_message(message.from_user.id, "Открываю веб-сайт Институт международного сотрудничества: [ссылка](https://ims.pnzgu.ru)",
                                   parse_mode='Markdown')
        elif message.text == 'Институт физической культуры и спорта':
            await bot.send_message(message.from_user.id, "Открываю веб-сайт Институт физической культуры и спорта: [ссылка](https://ffkis.pnzgu.ru)",
                                   parse_mode='Markdown')
        elif message.text == 'Политехнический институт':
            await bot.send_message(message.from_user.id, "Открываю веб-сайт Политехнический институт: [ссылка](https://politeh.pnzgu.ru)",
                                   parse_mode='Markdown')
        elif message.text == 'едагогический институт Им В.Г Белинского':
            await bot.send_message(message.from_user.id, "Открываю веб-сайт Педагогический институт Им В.Г Белинского: [ссылка](https://ppi.pnzgu.ru)",
                                   parse_mode='Markdown')
        elif message.text == 'Институт непрерывного образования':
            await bot.send_message(message.from_user.id, "Открываю веб-сайт Институт непрерывного образования: [ссылка](https://iito.pnzgu.ru)",
                                   parse_mode='Markdown')
        elif message.text == 'Назад':
            await bot.send_message(message.from_user.id, 'Вы вернулись в главное меню.', reply_markup=markups.mainMenu)
        elif message.text == 'Новости':
            await get_news(message.from_user.id)
        else:
            await bot.send_message(message.from_user.id, 'Неизвестная команда.')
    else:
        await bot.send_message(message.from_user.id, 'Привет! Я работаю только в личных сообщениях.')
@dp.message_handler()
async def get_news(user_id: int):
    url = "https://pnzgu.ru/news"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        news_list = soup.find_all('div', class_='news-list-item')

        if news_list:
            for news in news_list:
                title = news.find('div', class_='news-list-item-title').text.strip()
                date = news.find('div', class_='news-list-item-date').text.strip()
                link = news.find('a', class_='news-list-item-link')['href']

                message_text = f"📰 {title}\n📅 {date}\n🔗 {link}"
                await bot.send_message(user_id, message_text)
        else:
            await bot.send_message(user_id, "Первая новость: [ссылка](https://pnzgu.ru/news/2023/06/8/13532086)", parse_mode='Markdown')
            await bot.send_message(user_id,
                                   "Вторая новость: [ссылка](https://pnzgu.ru/news/2023/06/8/10100259)",parse_mode='Markdown')
            await bot.send_message(user_id,
                                   "Третья новость: [ссылка](https://pnzgu.ru/news/2023/06/8/9192897)",parse_mode='Markdown')

    except requests.exceptions.RequestException as e:
        await bot.send_message(user_id, "Ошибка при получении новостей.")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

