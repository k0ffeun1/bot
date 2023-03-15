from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN_API, VIDEO_RATE
from ikb import ikb, ikb2, ikb3, ikb4, ikb5, ikb6, ikb7, ikb8, ikb9, ikb10
from datetime import datetime
import time
import sqlite3




bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())


class MyStates(StatesGroup):
        request = State()
        summa = State()


# =================================ПОДГРУЖАЕМ ВИДОСЫ И ИХ ДЛИТЕЛЬНОСТЬ==========================================

videos = [f'videos/video{i}.mp4' for i in range(1, 7)]
video_durations = [6, 27, 23, 20, 60, 19]


async def on_startup(_):
    print('Ваш бот запущен!')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.delete()
    await message.answer(text='Выберите пункт меню ⤵️',
                         reply_markup=ikb)



users_data = {}

# ======================================КОЛЛБЭК ЗАПРОСЫ===============================================

@dp.callback_query_handler()
async def callback_profile(callback: types.CallbackQuery, state: FSMContext):

    

    user_id = callback.from_user.id
    username = callback.from_user.username
    fullname = callback.message.chat.full_name
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # создаем таблицу users с полями id, username и fullname
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY, 
                  username TEXT,
                  fullname TEXT);''')

    # Добавляем данные в таблицу
    cursor.execute("REPLACE INTO users (id, username, fullname) VALUES (?, ?, ?)",
               (user_id, username, fullname))
    conn.commit()

    # закрываем соединение с базой данных
    conn.close()

        # Проверка юзера по user_data
    if user_id not in users_data:
        user_data = users_data.setdefault(user_id, {
            'balance': 0,
            'success': 0,
            'current_video': 0,
            'current_duration': 0,
            'last_watch_time': None,    
            'payment_requested': False,
        })
        
    user_data = users_data.get(user_id)
        

    

    # Обработка коллбэк кнопки "заработать"


    if callback.data == 'work':
        await callback.message.answer(text=(
            f'❗️Не пытайтесь нажимать кнопку "Просмотрено" несколько раз подряд.Вы сможете ее нажать только после того, как будет учтен Ваш просмотр \n'
            f'\n'
            f'❗️Вы можете прервать просмотр видео в любой момент. Заработанные средства автоматически поступят на баланс \n'
            f'\n'
            f'📱 Тариф просмотра: {VIDEO_RATE} лей\n'
            f'✅ Выполнено: {user_data["success"]} из 20\n'
            f'💰 Ваш баланс: {user_data["balance"]} лей'
        ))
        video_index = user_data['current_video']
        user_data['current_duration'] = video_durations[video_index]
        await callback.message.answer_video(video=open(videos[video_index], 'rb'), reply_markup=ikb6)
        user_data['last_watch_time'] = time.time()

    # Обработка коллбэка - "просмотрено"

    elif callback.data == 'watching':
        elapsed_time = time.time() - user_data['last_watch_time']
        if elapsed_time >= user_data['current_duration']:
            user_data['balance'] += VIDEO_RATE
            user_data['success'] += 1
            current_video = user_data['current_video']
            await callback.message.answer(text=(
                f'✅ Просмотр засчитан\n'
                f'Баланс: {user_data["balance"] - VIDEO_RATE} лей → {user_data["balance"]} лей'
            ))
            if 'watched_before' not in user_data:
                user_data['watched_before'] = True
                user_data['balance'] += 200
                await callback.message.answer(text=(
                    f'🎁 Бонус: Новый пользователь!\n'
                    f'\n'
                    f'Баланс: {user_data["balance"] - 200} лей → {user_data["balance"]} лей \n'
                    f'\n'
                    f'Заходите каждый день, чтобы получить больше бонусов от нашей платформы!'
                ))
            if current_video < len(videos)-1:
                user_data['current_video'] += 1
                user_data['current_duration'] = video_durations[current_video+1]
                await callback.message.answer(text=(
                    f'📱 Тариф просмотра: {VIDEO_RATE} лей\n'
                    f' Выполнено: {user_data["success"]} из 20\n'
                    f'💰 Ваш баланс: {user_data["balance"]} лей'
                ))
                await callback.message.answer_video(video=open(videos[current_video+1], 'rb'), reply_markup=ikb6)
                user_data['last_watch_time'] = time.time()
            else:
                await callback.message.answer(text='you watched all the videos!', reply_markup=ikb)
            await callback.message.delete()
        else:
            remaining_time = round(
                user_data['current_duration'] - elapsed_time)
            await callback.answer(f'Wait another {remaining_time} seconds')

    if callback.data == 'stop_watching':
        await callback.message.delete()
        await callback.message.answer(text='Вы уверены, что хотите закончить заработок с просмотра оплачиваемых видеороликов?',
                                      reply_markup=ikb7)

    if callback.data == 'yes_stop':
        await callback.message.delete()
        await callback.message.answer(text=(
            f'🎉 Вы заработали {user_data["balance"]} лей. Приходите снова, что бы заработать больше денег \n'
            f'\n'
            f'❗️Для вас доступен бонус новичка! 200L для новых пользователей ТикТок бота. Для того, чтобы забрать 200L , нажмите кнопку ниже \n'
            f'↓'
        ), reply_markup=ikb8)
    if callback.data == 'no_stop':
        await callback.message.delete()
        await callback.message.answer(text=(
            f'❗️Не пытайтесь нажимать кнопку "Просмотрено" несколько раз подряд.Вы сможете ее нажать только после того, как будет учтен Ваш просмотр \n'
            f'\n'
            f'❗️Вы можете прервать просмотр видео в любой момент. Заработанные средства автоматически поступят на баланс \n'
            f'\n'
            f'📱 Тариф просмотра: {VIDEO_RATE} лей\n'
            f'✅ Выполнено: {user_data["success"]} из 20\n'
            f'💰 Ваш баланс: {user_data["balance"]} лей'
        ))
        video_index = user_data['current_video']
        user_data['current_duration'] = video_durations[video_index]
        await callback.message.answer_video(video=open(videos[video_index], 'rb'), reply_markup=ikb6)
        user_data['last_watch_time'] = time.time()

    if callback.data == 'bonus':
        await callback.message.answer(text=(
            f'👉 Подпишитесь на канал спонсора, и посмотрите последние посты, после чего нажмите кнопку "💰 Получить бонус". Вам будет начислено 500 лей!\n'
            f'\n'
            f'https://t.me/aza10chanel\n'
            f'\n'
            f'Благодаря спонсорам, платформа продолжает функционировать, и развиваться\n'
            f'\n'
            f'❗️ Внимание: если вы отпишитесь от канала спонсора, вы будете заблокированы в нашей системе TikTok Pay на всех устройствах! \n'
        ), reply_markup=ikb9)

    # if callback.data == 'bonus_no':

    if callback.data == 'check_chanel':
        try:
            member = await bot.get_chat_member(chat_id='@aza10chanel', user_id=user_id)
            if member.status == 'member' or member.status == 'creator' or member.status == 'administrator':
                get_bonus = 200
                await callback.message.answer(text=(
                    f'✅ Вам был начислен бонус 200L \n'
                    f'• Баланс: {user_data["balance"]} лей → {user_data["balance"] + get_bonus} лей \n'
                    f'\n'
                    f'💰10 000L+ на канале, на который вы только что подписались, можно забрать сейчас \n'
                    f'• Время изучения информации ~ 3 минуты\n'
                    f'\n'
                    f'@aza10chanel'
                ), reply_markup=ikb10)
                user_data["balance"] = user_data["balance"] + get_bonus
            else:
                await bot.answer_callback_query(callback.id, text='Ты не подписан на канал')
        except Exception as e:
            print(e)
            await bot.answer_callback_query(callback.id, text='Попробуйте чуть позже, пожалуйста!')

    if callback.data == 'no_instructions':
        await callback.message.delete()
        await callback.message.answer(text='Выберите пункт меню ⤵️',
                                      reply_markup=ikb)

    # Обработка коллбэка - "профиль"
    if callback.data == 'profile':
        await callback.message.delete()
        await callback.message.answer(text=(
            f'👤Мой профиль:'
            f'\n'
            f'Имя: {callback.message.chat.full_name}\n'
            f'Username: {callback.message.chat.username}\n'
            f'Баланс: {user_data["balance"]} лей\n'
            f'Просмотрено видео: {user_data["success"]}\n'
            f'Комментариев: 0\n'
            f'Статус: ✅ Верифицирован📊Статистика Бота за {datetime.now().strftime("%d.%m.%Y")}\n'
            f'\n'
            f'Пользователей Бота: 273,853\n'
            f'💰 Заработано Пользователями: 20,140,642L\n'
            f'🧠 Просмотрено видео: 530,016\n'
            f'🧠 Написано комментариев: 30,016\n'
        ), reply_markup=ikb2)

    # Обработка коллбэка - "назад"
    if callback.data == 'btn_back':
        await callback.message.delete()
        await callback.message.answer(text='Выберите пункт меню ⤵️',
                                      reply_markup=ikb)

    # Обработка коллбэка - "вывод"
    if callback.data == 'cash':
        await callback.message.delete()
        await callback.message.answer_video(video=open('cash.mp4', 'rb'),
                                            caption=(
                                                f'Баланс: {user_data["balance"]} лей \n'
                                                f'\n'
                                                f'Вы можете вывести средства, либо заработать дополнительно денег перед выводом\n'
        ), reply_markup=ikb3)

    
    # Обработка коллбэка - "вывод"

    # if callback.data == 'btn_cash_payment':
    #     if user_data['payment_requested']:
    #         await callback.message.answer('Вы уже вводили реквезиты, ожидайте оплаты')
    #         return
    #     await callback.message.answer('Введите ваши реквезиты')
    #     user_data['payment_requested'] = True # обновление состояния
    #     await state.finish() # закрыть предыдущее состояние
    #     await MyStates.request.set()

    # @dp.message_handler(state=MyStates.request)
    # async def request_answer(message: types.Message, state: FSMContext):
    #     answer = message.text
    #     user_id = message.from_user.id
    #     await state.update_data(answer1=answer)
    #     await message.answer('Введите сумму:')
        
    #     await MyStates.next()

    # @dp.message_handler(state=MyStates.summa)
    # async def summa_answer(message: types.Message, state: FSMContext):
    #     data = await state.get_data()
    #     answer1 = (await state.get_data())['answer1']
    #     answer2 = message.text
    #     if not answer2.isdigit():
    #         await message.answer('Введите сумму только в цифрах')
    #         return
    #     if int(answer2) > user_data['balance']:
    #         await message.answer('Ваш баланс меньше указанной суммы, повторите еще раз пожалуйста')
    #         return
    #     await message.answer('Ожидайте оплаты в течение трех дней')
    #     user_data['balance'] = user_data['balance'] - int(answer2)

    #     # Добавление записи в базу данных
    #     session = Session()
    #     payment = Payment(fullname=callback.message.chat.full_name, answer1=answer1, answer2=int(answer2))
    #     session.add(payment)
    #     session.commit()

    #     await state.finish()

    if callback.data == 'btn_cash_payment':
        user_id = callback.from_user.id
        if 'request' not in users_data[user_id]:
            await callback.message.answer(text='Введите реквизиты для выплаты')
            await MyStates.request.set()
        else:
            await callback.message.answer(text='Вы уже ввели реквизиты для выплаты',reply_markup=ikb4)

    @dp.message_handler(state=MyStates.request)
    async def process_request(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        users_data[user_id]['request'] = message.text
        await message.answer('Введите сумму для снятия')
        await MyStates.summa.set()

    @dp.message_handler(state=MyStates.summa)
    async def process_summa(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        user_data = users_data[user_id]
        if 'request' not in user_data:
            await message.answer('Введите реквизиты для выплаты')
            await MyStates.request.set()
            return
        if 'summa' in user_data:
            await message.answer('Вы уже ввели сумму для снятия, ожидайте оплату в течение 3 дней', 
                                 reply_markup=ikb4)
            return

        summa = message.text

        if not summa.isdigit():
            await message.answer('Введите сумму только в цифрах')
            return
        summa = int(message.text)
        if summa < 100:
            await message.answer('Минимальная сумма снятия - 100 лей', reply_markup=ikb4)
            await state.finish()
            return
        if summa > user_data['balance']:
            await message.answer('У вас недостаточно средств для снятия этой суммы', reply_markup=ikb4)
            return
        user_data['summa'] = summa
        user_data['payment_requested'] = True
        user_data['balance'] -= summa  # вычитаем запрошенную сумму из баланса пользователя
        
        # Добавление записи в базу данных
        # Update the database with the user's payment details and requested amount
        conn = sqlite3.connect('payments.db')
        cursor = conn.cursor()

        # создаем таблицу users с полями id, username и fullname
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY, 
                  username TEXT,
                  payment_details TEXT,
                  payment_sum TEXT);''')

        # Добавляем данные в таблицу
        cursor.execute("REPLACE INTO users (id, username, payment_details, payment_sum) VALUES (?, ?, ?, ?)",
               (user_id, fullname, users_data[user_id]['request'], user_data['summa']))
        conn.commit()

        # закрываем соединение с базой данных
        conn.close()
        
        await message.answer(f'Ваш запрос на выплату принят. Ожидайте выплаты. Ваш текущий баланс: {user_data["balance"]} лей')
        
        await state.finish()
    
       
   




    # Обработка коллбэка - "партнеры"
    if callback.data == 'partners':
        await callback.message.delete()
        await callback.message.answer(text=(
            f'💼 Получайте бонусы за приглашённых друзей\n'
            f'\n'
            f'https://t.me/?start=865\n'
            f'\n'
            f'✔️ 100 лей за каждого приглашенного Вами пользователя.\n'
            f'➕ Приглашено человек: 0\n'
        ), reply_markup=ikb5)

    


# ======================================ЗАПУСК БОТА===============================================

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)