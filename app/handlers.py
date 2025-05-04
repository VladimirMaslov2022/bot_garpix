from aiogram import F, Router, exceptions
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


import app.keyboards as kb
import app.database.requests as db
import app.utils as u

router = Router()


class Register(StatesGroup):
    name = State()
    emaili = State()
    number = State()
    u_id = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(u_id=message.from_user.id)
    print(message.from_user.id)
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
async def register_command(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше ФИО')


@router.message(F.text == 'Регистрация')
async def register_text(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше ФИО')


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.emaili)
    await message.answer("Введите вашу почту")


@router.message(Register.emaili)
async def register_email(message: Message, state: FSMContext):
    if await u.valid_email(message.text):
        await state.update_data(emaili=message.text)
        await state.set_state(Register.number)
        await message.answer("Отправьте ваш номер телефона", reply_markup=kb.get_number)
    else:
        await message.answer("Почта введена неправильно, повторите попытку")


@router.message(Register.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f"{data['name']}, регистрация завершена\n"
                         f"contact - {data['number']}\n"
                         f"email - {data['emaili']}")
    await db.register_user(data['name'], data['emaili'], data['number'], data['u_id'])
    await state.clear()
