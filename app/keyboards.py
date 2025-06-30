from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


main_registred = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Помощь', callback_data='help')],
    [KeyboardButton(text='Мои курсы', callback_data='courses')]],
    resize_keyboard=True) # input_field_placeholder='reply buttons'

main_unregistred = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Регистрация', callback_data='registration'),
    KeyboardButton(text='Помощь', callback_data='help')],
    [KeyboardButton(text='Мои курсы', callback_data='courses')]],
    resize_keyboard=True) # input_field_placeholder='reply buttons'


catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='btn 11', callback_data='btn1')],
    [InlineKeyboardButton(text='btn 22', callback_data='btn2')],
    [InlineKeyboardButton(text='btn 33', callback_data='btn3')]],
                                      resize_keyboard=True)


get_number = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить номер",
    request_contact=True)]],
    resize_keyboard=True)