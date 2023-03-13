from telegram import Update, Bot
from telegram.ext import CommandHandler, CallbackContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatMemberUpdated
from config import TOKEN_API, VIDEO_RATE
from ikb import ikb, ikb2, ikb3, ikb4, ikb5, ikb6, ikb7, ikb8, ikb9
from datetime import datetime
import time
import sqlite3

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

# =================================ПОДГРУЖАЕМ ВИДОСЫ И ИХ ДЛИТЕЛЬНОСТЬ==========================================

videos = [f'videos/video{i}.mp4' for i in range(1, 7)]
video_durations = [6, 27, 23, 20, 60, 19]


async def on_startup(_):
    print('Ваш бот запущен!')

    # Connect to the database
    conn = sqlite3.connect('bot.db')

    # Create a table to store the user data if it does not already exist
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY)''')
    conn.commit()

    # Close the database connection
    conn.close()

# ======================================СОЗДАЕМ КНОПКУ СТАРТ===============================================

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.delete()
    await message.answer(text='Выберите пункт меню ⤵️',
                         reply_markup=ikb)

# ======================================ПОДКЛЮЧАЕМ К БД АЙДИ ЮЗЕРА===============================================

    # Connect to the database
    conn = sqlite3.connect('bot.db')

    # Insert the user ID into the users table if it does not already exist
    user_id = message.from_user.id
    conn.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (user_id,))
    conn.commit()

    # Close the database connection
    conn.close()

users_data = {}

# ======================================КОЛЛБЭК ЗАПРОСЫ===============================================

@dp.callback_query_handler()
async def callback_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # Проверка юзера по user_data
    if user_id not in users_data:
        users_data[user_id] = {
            'balance': 0,
            'success': 0,
            'current_video': 0,
            'current_duration': 0,
            'last_watch_time': None,
        }
    user_data = users_data[user_id]

    #Обработка коллбэк кнопки "заработать"

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
                await callback.message.answer(text='Вы посмотрели все видео!', reply_markup=ikb)
            await callback.message.delete()
        else:
            remaining_time = round(user_data['current_duration'] - elapsed_time)
            await callback.answer(f'Подождите еще {remaining_time} секунд')

    if callback.data == 'stop_watching':    
        await callback.message.answer(text='Вы уверены, что хотите закончить заработок с просмотра оплачиваемых видеороликов?',
                                      reply_markup=ikb7)
    if callback.data == 'yes_stop':    
        await callback.message.answer(text=(   
                                    f'🎉 Вы заработали {user_data["balance"]} лей. Приходите снова, что бы заработать больше денег \n'
                                    f'\n'
                                    f'❗️Для вас доступен бонус новичка! 200L для новых пользователей ТикТок бота. Для того, чтобы забрать 200L , нажмите кнопку ниже \n'
                                    f'↓'
                                    ), reply_markup=ikb8)
    if callback.data == 'no_stop':    
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
        ),reply_markup=ikb9)

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

    # Обработка коллбэка - "способов оплаты"
    if callback.data == 'btn_cash_payment':
        await callback.message.delete()
        await callback.message.answer(text='Введите ваши реквезиты:', reply_markup=ikb4)

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

    # Establish a connection to the database
    db = sqlite3.connect('bot_db.sqlite')
    cursor = db.cursor()

    # Create the bot_actions table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS bot_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    action TEXT NOT NULL,
                    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                );''')

    # Commit the changes and close the database connection
    db.commit()
    db.close()

