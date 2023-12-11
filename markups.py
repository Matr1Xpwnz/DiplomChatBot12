from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnProfile = KeyboardButton("Профиль студента")
btnEditProfile = KeyboardButton("Редактирование профиля")
btnAttendance = KeyboardButton("Посещаемость и успеваемость студента")
btnInstitutes = KeyboardButton("Институты ПГУ")
btnApplicants = KeyboardButton("Поступающим")
btnScience = KeyboardButton("Наука")
btnContacts = KeyboardButton("Контакты ПГУ")
btnNews = KeyboardButton("Новости")
btnFaculty1 = KeyboardButton("Медицинский институт")
btnFaculty2 = KeyboardButton("Юридический институт")
btnFaculty3 = KeyboardButton("Институт экономики и управления")
btnFaculty4 = KeyboardButton("Институт международного сотрудничества")
btnFaculty5 = KeyboardButton("Институт физической культуры и спорта")
btnFaculty6 = KeyboardButton("Политехнический институт")
btnFaculty7 = KeyboardButton("Педагогический институт Им В.Г Белинского")
btnFaculty8 = KeyboardButton("Институт непрерывного образования")
btnBack = KeyboardButton("Назад")
editProfileMenu = KeyboardButton("Редактирование профиля")

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnProfile, btnEditProfile, btnAttendance, btnInstitutes, btnApplicants, btnScience, btnContacts, btnNews)

facultyMenu = ReplyKeyboardMarkup(resize_keyboard=True)
facultyMenu.add(btnFaculty1, btnFaculty2, btnFaculty3, btnFaculty4, btnFaculty5, btnFaculty6, btnFaculty7, btnFaculty8, btnBack)



