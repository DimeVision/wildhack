from bot_init import bot, dispatcher
from keyboards.client_navigator import main_keyboard, quiz_keyboard, hint_keyboard
from bicycle.quiz_collection import quiz_map

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command

from aiogram.dispatcher.filters.state import State, StatesGroup


class ClientFSM(StatesGroup):
    name = State()
    email = State()
    birthdate = State()
    phone = State()
    education = State()


#     TODO: Дописать пункты для анкеты

def register_client_handler(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_faq, commands=['FAQ'])
    dp.register_message_handler(command_register, commands=['Зарегистрироваться'])
    dp.register_message_handler(command_facts, commands=['Интересные'])
    dp.register_message_handler(command_ask, commands=['Задать'])
    # dp.register_message_handler() TODO: Для редиректа на
    # dp.register_message_handler(command_register, commands=['Отмена'])


async def command_faq(message: Message):
    await message.answer("Факт №1:\n"
                         "Камчатка крутое место")


async def command_ask(message: Message):
    await message.answer("Ну давай, рискни")


async def command_start(message: Message):
    await message.answer("Тратата\n", reply_markup=main_keyboard)


async def command_register(message: Message):
    await message.answer("Здесь должна быть ссылка на GForms")


async def command_facts(message: Message):
    await message.answer(f"{quiz_map.keys()}", reply_markup=hint_keyboard)


@dispatcher.message_handler(commands=['fill'], state=None)
async def fill_volunteer_data(message: Message):
    await ClientFSM.name.set()
    await message.reply('Введи своё ФИО')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.name)
async def save_client_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await ClientFSM.next()
    await message.reply('Теперь email')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.email)
async def save_client_email(message: Message, state=FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await ClientFSM.next()
    await message.reply('Дата рождения')

#     TODO: добавить обработку других полей. Для обработки видео в data['video'] укажи message.video[].file_id

#     TODO: РЕДИРЕКТ НА AI
