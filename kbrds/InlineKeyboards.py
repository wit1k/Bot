from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

InlineKeyboardHelp = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📍 Главное меню', callback_data='main'), InlineKeyboardButton(text='📖 Информация', callback_data='info')],
    [InlineKeyboardButton(text='❓ Выбрать тип вопроса ', callback_data='type')]
])

InlineKeyboardStart = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❔ Помощь', callback_data='help'), InlineKeyboardButton(text='📖 Информация', callback_data='info')],
    [InlineKeyboardButton(text='❓ Выбрать тип вопроса ', callback_data='type')]
])

InlineKeyboardInfo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📍 Главное меню', callback_data='main'), InlineKeyboardButton(text='❔ Помощь', callback_data='help')],
    [InlineKeyboardButton(text='❓ Выбрать тип вопроса ', callback_data='type')]
])

InlineKeyboardResponse = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📍 Главное меню", callback_data="MainResp")]
])

InlineKeyboardTypes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1️⃣', callback_data="plan"),
    InlineKeyboardButton(text='2️⃣', callback_data="task"),
    InlineKeyboardButton(text='3️⃣', callback_data="termin"),
    InlineKeyboardButton(text='4️⃣', callback_data="TestTask")],
    [InlineKeyboardButton(text='Другой вопрос', callback_data="another")],
    [InlineKeyboardButton(text='⬅️ Назад в меню', callback_data="EditBack")]
])

InlineKeyboardBack = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back")]
])