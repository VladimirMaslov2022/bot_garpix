from aiogram import F, Router, exceptions
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart


import app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!',reply_markup=kb.main)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Помощь')


@router.message(Command('catalog'))
async def cmd_help(message: Message):
    await message.reply('buttons', reply_markup=kb.catalog)


@router.callback_query(F.data)
async def cmd_btn1(callback: CallbackQuery):
    try:
        match callback.data:
            case 'btn1': 
                await callback.message.edit_text(text='buttons (btn1 pressed)', 
                                                reply_markup=kb.catalog)
            case 'btn2': 
                await callback.message.edit_text(text='buttons (btn2 pressed)', 
                                                reply_markup=kb.catalog)
            case 'btn3': 
                await callback.message.edit_text(text='buttons (btn3 pressed)', 
                                                reply_markup=kb.catalog)
        await callback.answer('')
    except exceptions.TelegramBadRequest: 
        await callback.answer('')


@router.message(Command('register'))
async def register(message: Message):
    await message.answer('What is your name?')