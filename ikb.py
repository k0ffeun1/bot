from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_data = {
    "start": "work",
    "profile": "profile",
    "cash": "cash",
    "partners": "partners",
    "back": "btn_back",
    "cash_tel": "btn_cash_payment",
    "cash_binance": "btn_cash_payment",
    "cash_paypal": "btn_cash_payment",
    "cash_card": "btn_cash_payment",
    "friends": "friends",
    "watching": "watching",
    "stop_watching": "stop_watching",
    "yes_stop": "yes_stop",
    "no_stop": "no_stop",
    "bonus": "bonus",
    "bonus_no": "bonus_no",
    "chanel": "chanel",
    "check_chanel": "check_chanel",
    "instructions": "instructions",
    "no_instructions": "no_instructions",
    "sum_payment": "sum_payment"
}

button_texts = {
    "start": "Заработок",
    "profile": "Профиль",
    "cash": "Вывод",
    "partners": "Партнерам",
    "back": "Назад",
    "cash_tel": "Телефон",
    "cash_binance": "BINANCE",
    "cash_paypal": "PAY PAL",
    "cash_card": "CARD",
    "friends": "Поделиться с другом",
    "watching": "✅ Просмотрено (+5 лей)",
    "stop_watching": "✋ Закончить",
    "yes_stop": "✅ Да, закончить",
    "no_stop": "👀 Нет, продолжить",
    "bonus": "🎁 Забрать бонус 200 лей",
    "bonus_no": "❌ Отказаться от бонуса",
    "chanel": "📲 Перейти на канал",
    "check_chanel": "☑️ Проверить подписку",
    "instructions": "💰 Инструкция заработка",
    "no_instructions": "❌ Отказываюсь от знаний",
    "sum_payment": "Укажите сумму списания"
}


def create_inline_keyboard(buttons, row_width=1):
    markup = InlineKeyboardMarkup(row_width=row_width)
    for button in buttons:
        text = button_texts.get(button, "")
        callback_data = button_data.get(button, "")
        markup.add(InlineKeyboardButton(text, callback_data=callback_data))
    return markup


ikb = create_inline_keyboard(["start", "profile", "cash", "partners"])
ikb2 = create_inline_keyboard(["start", "back"])
ikb3 = InlineKeyboardMarkup(row_width=2)
ikb3.row(
    InlineKeyboardButton("phone", callback_data="btn_cash_payment"),
    InlineKeyboardButton("BINANCE", callback_data="btn_cash_payment")
)
ikb3.row(
    InlineKeyboardButton("PAY PAL", callback_data="btn_cash_payment"),
    InlineKeyboardButton("CARD", callback_data="btn_cash_payment")
)
ikb3.add(InlineKeyboardButton("back", callback_data="btn_back"))
ikb4 = create_inline_keyboard(["back"])

ikb5 = InlineKeyboardMarkup(row_width=1)
ikb_friend = InlineKeyboardButton('Поделиться с другом', request_contact=True)
ikb_start = InlineKeyboardButton('Заработок', callback_data='work')
ikb_back = InlineKeyboardButton('Назад', callback_data='btn_back')
ikb5.add(ikb_start, ikb_back)

ikb6 = create_inline_keyboard(["watching", "stop_watching"])
ikb7 = create_inline_keyboard(["yes_stop", "no_stop"])
ikb8 = create_inline_keyboard(["bonus", "bonus_no"])

ikb9 = InlineKeyboardMarkup(row_width=1)
ibtn_channel = InlineKeyboardButton('📲 Перейти на канал', url='https://t.me/aza10chanel')
ibtn_check_chanel = InlineKeyboardButton('☑️ Проверить подписку', callback_data='check_chanel')
ikb9.add(ibtn_channel, ibtn_check_chanel)

ikb10 = InlineKeyboardMarkup(row_width=1)
ibtn_instructions = InlineKeyboardButton('💰 Инструкция заработка', url='https://t.me/aza10chanel')
ibtn_no_instructions = InlineKeyboardButton('❌ Отказываюсь от знаний', callback_data='no_instructions')
ikb10.add(ibtn_instructions,ibtn_no_instructions)

ikb11 = InlineKeyboardMarkup()
ikb11_accept = InlineKeyboardButton('Принять', callback_data='accept')
ikb11.add(ikb11_accept)




