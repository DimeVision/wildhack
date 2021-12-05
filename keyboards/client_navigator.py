from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

main_b1 = KeyboardButton('FAQ')
main_b2 = KeyboardButton('Интересный факт')
main_b3 = KeyboardButton('Зарегистрироваться')

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(main_b1).add(main_b2).insert(main_b3)

hint_b1 = KeyboardButton('1')
hint_b2 = KeyboardButton('2')
hint_b3 = KeyboardButton('3')
hint_b4 = KeyboardButton('4')
hint_b5 = KeyboardButton('5')
hint_b6 = KeyboardButton('6')
hint_b7 = KeyboardButton('7')
hint_b8 = KeyboardButton('8')
hint_b9 = KeyboardButton('9')
hint_b10 = KeyboardButton('10')
hint_b11 = KeyboardButton('11')
hint_b12 = KeyboardButton('12')
hint_b13 = KeyboardButton('13')
hint_b14 = KeyboardButton('14')
hint_b15 = KeyboardButton('15')
hint_back = KeyboardButton('Назад')

hint_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
hint_keyboard.add(hint_b1, hint_b2, hint_b3, hint_b4, hint_b5, hint_b6, hint_b7, hint_b8, hint_b9, hint_b10, hint_b11,
                  hint_b12, hint_b13, hint_b14, hint_b15).insert(hint_back)

agreement_b1 = KeyboardButton('Даю согласие')
agreement_b2 = KeyboardButton('Не даю согласие')

agreement_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
agreement_keyboard.add(agreement_b1, agreement_b2)

cancel_bt = KeyboardButton('Отмена')
cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_kb.add(cancel_bt)