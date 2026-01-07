from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from openai import OpenAI

import kbrds.InlineKeyboards as kb

client = OpenAI(api_key="sk-3eaa505abf284b9a959ac023b15230ef", base_url="https://api.deepseek.com")
UserPrivateRt = Router()

class States(StatesGroup):
    waiting_for_question_plan = State()
    waiting_for_question_task = State()
    waiting_for_question_termin = State()
    waiting_for_question_TestTask = State()
    waiting_for_question_another = State()

@UserPrivateRt.message(CommandStart())
async def start_cmd(message:Message):
    username = message.from_user.username
    StartText = f'''
    <i>Добро пожаловать, <b>{username}</b> я ваш карманный учитель!</i>

<b>Я помогу вам успешно подготовиться к любой школьной работе:</b>
✅ Объясню сложные темы простыми словами
✅ Помогу составить план подготовки
✅ Решу с вами типовые задачи
✅ Подскажу, как избежать частых ошибок
✅ Отвечу на все ваши учебные вопросы

<b>Навигация ⬇️</b>
    '''
    await message.answer(StartText, parse_mode="HTML", reply_markup=kb.InlineKeyboardStart)

@UserPrivateRt.callback_query(F.data == 'main')
async def start_cmd(callback:CallbackQuery):
    MainText = f'''
<b>Я помогу вам успешно подготовиться к любой школьной работе:</b>
✅ Объясню сложные темы простыми словами
✅ Помогу составить план подготовки
✅ Решу с вами типовые задачи
✅ Подскажу, как избежать частых ошибок
✅ Отвечу на все ваши учебные вопросы

<b>Навигация ⬇️</b>
    '''
    await callback.answer('')
    await callback.message.edit_text(MainText, parse_mode="HTML", reply_markup=kb.InlineKeyboardStart)

@UserPrivateRt.callback_query(F.data == 'help')
async def help_cmd(callback:CallbackQuery):
    HelpText = '''
    📖 <b>Как использовать бота</b>

<b>Вариант 1️⃣ - План подготовки (самое популярное)</b>
<b>Напишите:</b> "Как подготовиться к контрольной по математике?"
<b>Получите:</b> Полный план с темами, задачами и решениями

<b>Вариант 2️⃣ - Объяснений задачи </b>
<b>Напишите свою задачу</b> 
<b>Получите:</b> Пошаговое и понятное объяснение

<b>Вариант 3️⃣ - Определение термина (для уточнения)</b>
<b>Напишите:</b> "Что такое фотосинтез?"
<b>Получите:</b> Краткое определение в 1-2 предложения

<b>Вариант 4️⃣ - Пробные задачи </b>
<b>Напишите:</b> "Составь мне задачи по теме 'гипотенуза'"
<b>Получите:</b> Три, различающихся по сложности, задачи

<b>Что я НЕ могу делать:</b>
❌ Отвечать на вопросы про погоду, кино, спорт
❌ Решать задачи по программированию (вне школьной программы)
❌ Помогать с домашним заданием без объяснения
❌ Давать очень длинные ответы (только по делу!)

<b>Навигация ⬇️</b>
    '''
    await callback.answer('')
    await callback.message.edit_text(HelpText, parse_mode="HTML", reply_markup=kb.InlineKeyboardHelp)

@UserPrivateRt.callback_query(F.data == 'info')
async def info_cmd(callback:CallbackQuery):
    InfoText = '''
    <b>Информация о боте</b>

<b>Что я могу делать:</b>
▪️ Составлять план подготовки
▪️ Объяснять сложные темы и определения
▪️ Предлагать задачи для практики
▪️ Давать пошаговые решения
▪️ Объяснять частые ошибки
▪️ Помогать повторять материал

<b>Как я работаю:</b>
1️⃣ Вы пишите вопрос про учебу
2️⃣ Я анализирую, что вам нужно
3️⃣ Даю краткий и понятный ответ

<b>Типы вопросов:</b>
"Как подготовиться к контрольной по (предмет)?"
<b>Получите полный план подготовки с темами, задачами, решениями</b>

"Что такое интеграл?" / "Кто такой Петр I?"
<b>Получите краткое определение (1-2 предложения)</b>

Вопросы про погоду, спорт, игры и другое (не про учебу)
<b>Вежливо откажу, так как я только учитель по школьным предметам</b>

<b>Навигация ⬇️</b>
    '''
    await callback.answer('')
    await callback.message.edit_text(InfoText, parse_mode="HTML", reply_markup=kb.InlineKeyboardInfo)

@UserPrivateRt.callback_query(F.data == 'type')
async def ask_cmd(callback:CallbackQuery):
    choose = '''
    <b>Выберите тип запроса:</b>
1️⃣ ┌ План подготовки
2️⃣ ├ Объяснение задачи
3️⃣ ├ Определение термина
4️⃣ └ Пробные задачи
'''
    await callback.answer('')
    await callback.message.edit_text(choose, parse_mode="HTML", reply_markup=kb.InlineKeyboardTypes)

@UserPrivateRt.callback_query(F.data == 'plan')
async def plan(callback:CallbackQuery, state:FSMContext):
    await callback.answer('')
    await callback.message.edit_text("<b>🗓 План подготовки\n\nНапишите свой вопрос:</b>", parse_mode="HTML")
    await state.set_state(States.waiting_for_question_plan)

@UserPrivateRt.message(States.waiting_for_question_plan)
async def PlanPrompt(message:Message):
    await message.answer("<b>⏳ Думаю над ответом...</b>", parse_mode="HTML")
    question_plan = message.text
    prompt_plan = f'''
    ты - опытный учитель, который готовит ученика к контрольной работе.

твоя задача составить план подготовки к работе на тему, по которой будет работа у ученика. 

Структура твоего ответа:
1. План подготовки, распиши по пунктам
2. Типовые задачи(2 легких примера, 1 сложный пример)
3. Частые ошибки(3 ошибки, которые допускают ученики)
4. Сделай вывод(1-2 предложения поддержки и мотивации) 

Правила ответа:
1. Пиши кратко и по делу
2. Каждый раздел с новой строки
3. Используй простой язык для школьников
4. Давай конкретные советы
5. Если вопрос ученика не связан с учебой, вежливо откажи ему и скажи что ты учитель
6. Если ученик спрашивает определение термина или просит пробные задачи или просит объяснения задачи, 
тоже откажи и скажи ему выбрать другой тип ответа в меню
7. НЕ используй HTML теги или другое форматирование - пиши обычным текстом

Вопрос ученика: {question_plan}
'''
    response = client.chat.completions.create(
        model = 'deepseek-chat',
        messages=[
            {"role": "system", "content": "Ты опытный учитель"},
            {"role": "user", "content": prompt_plan}
        ],
        timeout=15
    )
    await message.answer(text=response.choices[0].message.content, reply_markup=kb.InlineKeyboardBack)

@UserPrivateRt.callback_query(F.data == 'task')
async def task(callback:CallbackQuery, state:FSMContext):
    await callback.answer('')
    await callback.message.edit_text("<b>🗓 Объяснение задачи\n\nНапишите свою задачю:</b>", parse_mode="HTML")
    await state.set_state(States.waiting_for_question_task)

@UserPrivateRt.message(States.waiting_for_question_task)
async def taskPrompt(message:Message):
    await message.answer("<b>⏳ Думаю над ответом...</b>", parse_mode="HTML")
    question_task = message.text
    prompt_task = f'''
    Ты - опытный школьный учитель, который помогает ученику разобраться в сложной задаче.

Твоя задача объяснить решение задачи ученика.

Структура ответа(если ученик просит объяснить задачу):
1. Анализ задачи: (пару предложений о том, что требуется найти или доказать)
2. Что дано в задаче:
    1) (что дано 1)
    2) (что дано 2)
    3) (что дано 3)
    ... и так далее выписываешь все условия задачи
3. Что надо найти:
    1) (что найти 1)
    2) (что найти 2)
    ... и так далее выписываешь то что требуется найти
4. Решение по шагам:
    Шаг 1: (описание действие) - (решение)
    Шаг 2: (описание действие) - (решение)
    Шаг 3: (описание действие) - (решение)
    ... и так далее сколько нужно шагов для решения задачи
5. Ответ:

Правила ответа:
1. Каждый раздел с новой строки
2. Используй простой язык для школьников
3. Если вопрос ученика не связан с учебой, вежливо откажи ему и скажи что ты учитель(ответ не по структуре)
4. Если ученик спрашивает по школьной теме, но не просит объяснения задачи, а просит определение термина, 
пробные задачи или составить план подготовки, тоже откажи и скажи ему выбрать другой тип ответа в меню.
5. НЕ используй HTML теги или другое форматирование - пиши обычным текстом

Вопрос ученика: {question_task}
'''
    response = client.chat.completions.create(
        model = 'deepseek-chat',
        messages=[
            {"role": "system", "content": "Ты опытный учитель"},
            {"role": "user", "content": prompt_task}
        ],
        timeout=15
    )
    await message.answer(text=response.choices[0].message.content, reply_markup=kb.InlineKeyboardBack)

@UserPrivateRt.callback_query(F.data == 'termin')
async def termin(callback:CallbackQuery, state:FSMContext):
    await callback.answer('')
    await callback.message.edit_text("<b>🗓 Определение термина\n\nНапишите термин:</b>", parse_mode="HTML")
    await state.set_state(States.waiting_for_question_termin)

@UserPrivateRt.message(States.waiting_for_question_termin)
async def terminPrompt(message:Message):
    await message.answer("<b>⏳ Думаю над ответом...</b>", parse_mode="HTML")
    question_termin = message.text
    prompt_termin = f'''
    Ты - опытный учитель, который объясняет сложный или непонятный ученику термин.

Твоя задача состоит в том, что ты даешь определение термину, который не понимает ученик.

Структура твоего ответа:
Название термина - (определение в пару предложений)

Правила ответа:
1. Пиши кратко и по делу
2. Используй простой язык для школьников
3. Если вопрос ученика не связан с учебой, вежливо откажи ему и скажи что ты учитель
4. Если ученик спрашивает по школьной теме, но не просит составить план или не просит подготовить к работе, 
а просит определение термина, пробные задачи или объяснение своей задачи, тоже откажи и скажи ему выбрать другой тип ответа в меню
5. НЕ используй HTML теги или другое форматирование - пиши обычным текстом

Вопрос ученика: {question_termin}
'''
    response = client.chat.completions.create(
        model = 'deepseek-chat',
        messages=[
            {"role": "system", "content": "Ты опытный учитель"},
            {"role": "user", "content": prompt_termin}
        ],
        timeout=15
    )
    await message.answer(text=response.choices[0].message.content, reply_markup=kb.InlineKeyboardBack)

@UserPrivateRt.callback_query(F.data == 'TestTask')
async def termin(callback:CallbackQuery, state:FSMContext):
    await callback.answer('')
    await callback.message.edit_text("<b>🗓 Тестовые задачи\n\nНапишите тему, по которой хотели бы получить задачу:</b>", parse_mode="HTML")
    await state.set_state(States.waiting_for_question_TestTask)

@UserPrivateRt.message(States.waiting_for_question_TestTask)
async def terminPrompt(message:Message):
    await message.answer("<b>⏳ Думаю над ответом...</b>", parse_mode="HTML")
    question_TestTask = message.text
    prompt_TestTask = f'''
    Ты - опытный учитель, дающий ученику пробные задачи по теме, которую скажет ученик.

Структура ответа:
Задача 1:
(текст задачи без решения)
Ответ: (ответ)
Задача 2:
(текст задачи без решения)
Ответ: (ответ)
Задача 3:
(текст задачи без решения)
Ответ: (ответ)

Правила ответа:
1. Придумай 3 задачи и начинай от легко и закончи сложно(задача 1 - легкая, задача 2 - средняя, задача 3 - сложная)
2. Если вопрос ученика не связан с учебой, вежливо откажи ему и скажи что ты учитель
3. Если ученик спрашивает по школьной теме, но не просит задачи, а просит определение термина, 
план подготовки или объяснение своей задачи, тоже откажи и скажи ему выбрать другой тип ответа в меню
4. НЕ используй HTML теги или другое форматирование - пиши обычным текстом

Вопрос ученика: {question_TestTask}
'''
    response = client.chat.completions.create(
        model = 'deepseek-chat',
        messages=[
            {"role": "system", "content": "Ты опытный учитель"},
            {"role": "user", "content": prompt_TestTask}
        ],
        timeout=15
    )
    await message.answer(text=response.choices[0].message.content, reply_markup=kb.InlineKeyboardBack)

@UserPrivateRt.callback_query(F.data == 'another')
async def termin(callback:CallbackQuery, state:FSMContext):
    await callback.answer('')
    await callback.message.edit_text("<b>Ваш вопрос\n\nНапишите свой вопрос, а я отвечу на него:</b>", parse_mode="HTML")
    await state.set_state(States.waiting_for_question_another)

@UserPrivateRt.message(States.waiting_for_question_another)
async def terminPrompt(message:Message):
    await message.answer("<b>⏳ Думаю над ответом...</b>", parse_mode="HTML")
    question_TestTask = message.text
    prompt_TestTask = f'''
    Ты - опытный учитель, отвечающий на любой, но только школьный вопрос школьника.

Правила ответа:
1. Если вопрос ученика не связан с учебой, вежливо откажи ему и скажи что ты учитель
2. НЕ используй HTML теги или другое форматирование - пиши обычным текстом

Вопрос ученика: {question_TestTask}
'''
    response = client.chat.completions.create(
        model = 'deepseek-chat',
        messages=[
            {"role": "system", "content": "Ты опытный учитель"},
            {"role": "user", "content": prompt_TestTask}
        ],
        timeout=15
    )
    await message.answer(text=response.choices[0].message.content, reply_markup=kb.InlineKeyboardBack)

@UserPrivateRt.callback_query(F.data == 'back')
async def back(callback:CallbackQuery, state:FSMContext):
    MainText = f'''
<b>Я помогу вам успешно подготовиться к любой школьной работе:</b>
✅ Объясню сложные темы простыми словами
✅ Помогу составить план подготовки
✅ Решу с вами типовые задачи
✅ Подскажу, как избежать частых ошибок
✅ Отвечу на все ваши учебные вопросы

<b>Навигация ⬇️</b>
'''
    await callback.answer('')
    await callback.message.answer(MainText, parse_mode="HTML", reply_markup=kb.InlineKeyboardStart)
    await state.clear()

@UserPrivateRt.callback_query(F.data == 'EditBack')
async def EditBack(callback:CallbackQuery, state:FSMContext):
    MainText = f'''
<b>Я помогу вам успешно подготовиться к любой школьной работе:</b>
✅ Объясню сложные темы простыми словами
✅ Помогу составить план подготовки
✅ Решу с вами типовые задачи
✅ Подскажу, как избежать частых ошибок
✅ Отвечу на все ваши учебные вопросы

<b>Навигация ⬇️</b>
'''
    await callback.answer('')
    await callback.message.edit_text(MainText, parse_mode="HTML", reply_markup=kb.InlineKeyboardStart)
    await state.clear()
