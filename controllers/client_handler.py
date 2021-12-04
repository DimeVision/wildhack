import nlp_wh_py
from bot_init import bot, dispatcher
from keyboards.client_navigator import main_keyboard, quiz_keyboard, hint_keyboard, question_keyboard
from bicycle.quiz_collection import quiz_map

import re
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command

from aiogram.dispatcher.filters.state import State, StatesGroup

dick = list(quiz_map.values())
accaptable = ['Зарегистрироваться', 'Интересные факты', 'Интересные факты', 'Задать вопрос', 'Назад', 'start']


class ClientFSM(StatesGroup):
    name = State()
    email = State()
    birthdate = State()
    phone = State()
    education = State()


#     TODO: Дописать пункты для анкеты

def register_client_handler(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(test_search, regexp=r'\?$')
    dp.register_message_handler(command_register, lambda message: 'Зарегистрироваться' in message.text)
    dp.register_message_handler(command_facts, lambda message: 'Интересные факты' in message.text)
    dp.register_message_handler(command_ask, lambda message: 'Задать вопрос' in message.text)
    dp.register_message_handler(command_start, lambda message: 'Назад' in message.text)
    dp.register_message_handler(switch_faq, regexp=r'\d+')
    # dp.register_message_handler() TODO: Для редиректа на нейросеть


async def command_ask(message: Message):
    await message.answer("Напиши появившийся вопрос", reply_markup=question_keyboard)


async def command_start(message: Message):
    await message.answer("Отлично! В предложенном меню ты можешь выбрать интересующие пункты.\n",
                         reply_markup=main_keyboard)


async def command_register(message: Message):
    await message.answer("Здесь должна быть ссылка на GForms")


async def command_facts(message: Message):
    await message.answer("Факт №1:\n"
                         "TODO: заполнить список фактов")


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

@dispatcher.message_handler(lambda message: 'FAQ' in message.text)
async def command_faq(message: Message):
    text = ""
    count = 0
    for key in quiz_map:
        count += 1
        text += f"<b>{count}) " + key + "</b>\n"

    await message.answer(f"{text}", reply_markup=hint_keyboard)


async def switch_faq(message: Message):
    await message.answer(f"{dick[int(message.text) - 1]}")


async def test_search(message: Message):
    await message.answer("Response: " + nlp_wh_py.get_closest_question(message.text))
