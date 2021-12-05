import database.DBCommands
import nlp_wh_py
import random
from bot_init import bot, dispatcher
from keyboards.client_navigator import main_keyboard, hint_keyboard, agreement_keyboard, cancel_kb
from bicycle.quiz_collection import quiz_map, facts_list

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
    agreement = State()
    name = State()
    email = State()
    birthdate = State()
    phone = State()
    education = State()
    desired_area = State()
    check_in_date = State()
    check_out_date = State()
    languages = State()
    experience = State()
    skills = State()
    book = State()
    recommendation = State()
    motivation = State()
    # comments = State()
    video = State()


def register_client_handler(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(test_search, regexp=r'\?$')
    dp.register_message_handler(cm_start, lambda message: 'Зарегистрироваться' in message.text)
    dp.register_message_handler(command_facts, lambda message: 'Интересный факт' in message.text)
    dp.register_message_handler(command_start, lambda message: 'Назад' in message.text)
    dp.register_message_handler(switch_faq, regexp=r'\d+')


async def command_start(message: Message):
    await message.answer(
        "Приветствую тебя, волонтёр! Я помогу вам ответить на ваш вопрос. Вы можете найти ответы в FAQ, а также спросить у меня самостоятельно, для этого поставь «?» в конце предложения. Еще я могу вам рассказать о самих кордонах, и о Камчатке, только нажми на кнопку «интересные факты»\n",
        reply_markup=main_keyboard)


# async def command_register(message: Message): TODO: НЕ ЗАБУДЬ ДОПИЛИТЬ
#     await message.answer(
#         "Заполнить анкету на прохождение обучения в Школе Защитников Природы, ссылка на форму анкеты: \n https://docs.google.com/forms/d/1idhdo4KswngdMijyXZWx_TXGWqJuKn7ySRzjeR0UnsI/edit;")


@dispatcher.message_handler(commands=['fill'], state=None)
async def cm_start(message: Message, state: FSMContext):
    await ClientFSM.next()
    await message.answer(
        'Перед тем как начать, нам нужно знать, согласен ли ты на обработку и передачу персональных данных?',
        reply_markup=agreement_keyboard)


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.agreement)
async def save_client_agreement(message: Message, state: FSMContext):
    if message.text == 'Даю согласие':
        await message.answer('Введи своё ФИО', reply_markup=cancel_kb)
        await ClientFSM.next()
    elif message.text == 'Не даю согласие':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.name)
async def save_client_name(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)

    async with state.proxy() as data:
        data['name'] = message.text
    await ClientFSM.next()
    await message.answer('Теперь мне нужна твоя почта')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.email)
async def save_client_email(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['email'] = message.text
        await ClientFSM.next()
        await message.answer('И еще понадобится дата твоего дня рождения')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.birthdate)
async def save_client_birthdate(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['birthdate'] = message.text
        await ClientFSM.next()
        await message.answer('И еще понадобится номер телефона')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.phone)
async def save_client_phone(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['phone'] = message.text
        await ClientFSM.next()
        await message.answer('На какой территории ты хотел бы поработать?')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.education)
async def save_client_education(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['education'] = message.text
        await ClientFSM.next()
        await message.answer('Какое у тебя образование?')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.desired_area)
async def save_client_desired_area(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['desired_area'] = message.text
        await ClientFSM.next()
        await message.answer('На какую дату заезда ты рассчитываешь?')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.check_in_date)
async def save_client_check_in_date(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['check_in_date'] = message.text
        await ClientFSM.next()
        await message.answer('На какую дату выезда ты рассчитываешь?')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.check_out_date)
async def save_client_check_out_date(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['check_out_date'] = message.text
        await ClientFSM.next()
        await message.answer('Давай поговорим о языках. Какие языки ты знаешь?')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.languages)
async def save_client_languages(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['languages'] = message.text
        await ClientFSM.next()
        await message.answer('Работал уже волонтером? Есть какой-нибудь опыт?')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.experience)
async def save_client_experience(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['experience'] = message.text
        await ClientFSM.next()
        await message.answer('А какими навыками ты владеешь?')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.skills)
async def save_client_skills(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['skills'] = message.text
        await ClientFSM.next()
        await message.answer('А есть ли волонтёрская книжка?')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.book)
async def save_client_book(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['book'] = message.text
        await ClientFSM.next()
        await message.answer('Есть ли у тебя рекомендации?')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.recommendation)
async def save_client_recommendation(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['recommendation'] = message.text
        await ClientFSM.next()
        await message.answer('Самое главное, почему именно ты должен стать волонтером? Можешь и коротко)')


@dispatcher.message_handler(content_types=['text'], state=ClientFSM.motivation)
async def save_client_motivation(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['motivation'] = message.text
        await ClientFSM.next()
        await message.answer('А теперь скинь видео о себе на 1-2 минуты')


# @dispatcher.message_handler(content_types=['text'], state=ClientFSM.comments)
# async def save_client_comment(message: Message, state: FSMContext):
#     if message.text == 'Отмена':
#         await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
#         await cancel_fsm_handler(message, state)
#     else:
#         async with state.proxy() as data:
#             data['comment'] = message.text
#         await ClientFSM.next()
#         await message.answer('')


@dispatcher.message_handler(content_types=['video'], state=ClientFSM.video)
async def save_client_video(message: Message, state=FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Направляю тебя в главное меню :)0', reply_markup=main_keyboard)
        await cancel_fsm_handler(message, state)
    else:
        async with state.proxy() as data:
            data['video'] = message.video.file_id
        async with state.proxy() as data:
            await message.reply(str(data))
        await database.DBCommands.commands.add_volunteer(shit=state)
        await state.finish()


@dispatcher.message_handler(state="*", commands='отмена')
@dispatcher.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_fsm_handler(message: Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await message.answer("Вы вышли из анкетирования", reply_markup=main_keyboard)


async def command_facts(message: Message):
    random_index = random.randrange(len(facts_list))
    await message.answer(facts_list[random_index])


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
    # await message.answer(await database.DBCommands.commands.find_faq(faq_id=int(message.text)))


async def test_search(message: Message):
    await message.answer(nlp_wh_py.get_closest_question(message.text))
