from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN_API, VIDEO_RATE
from ikb import ikb, ikb2, ikb3, ikb4, ikb5, ikb6
from datetime import datetime

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Ваш бот запущен!')



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.delete()
    await message.answer(text='Выберите пункт меню ⤵️',
                         reply_markup=ikb)

users_data = {}

@dp.callback_query_handler()
async def callback_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # Check if user exists in the dictionary
    if user_id not in users_data:
        # Initialize the user data
        users_data[user_id] = {
            'balance': 0,
            'success': 0,
        }

    user_data = users_data[user_id]

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
        await callback.message.answer_video(video=open('videos/video1.mp4', 'rb'), reply_markup=ikb6)

    elif callback.data == 'watching':
        user_data['balance'] += VIDEO_RATE
        user_data['success'] += 1

        await callback.message.delete()

        await callback.message.answer(text=(
            f'✅ Просмотр засчитан\n'
            f'Баланс: {user_data["balance"] - VIDEO_RATE} лей ➡️ {user_data["balance"]} лей'
        ))

        await callback.message.answer(text=(
            f'📱 Тариф просмотра: {VIDEO_RATE} лей\n'
            f' Выполнено: {user_data["success"]} из 20\n'
            f'💰 Ваш баланс: {user_data["balance"]} лей'
        ))

        await callback.message.answer_video(video=open('videos/video2.mp4', 'rb'), reply_markup=ikb6)

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
    if callback.data == 'btn_back':
        await callback.message.delete()
        await callback.message.answer(text='Выберите пункт меню ⤵️',
                                      reply_markup=ikb)

    if callback.data == 'cash':
        await callback.message.delete()
        await callback.message.answer_video(video=open('cash.mp4', 'rb'),
                                            caption=(
                                                f'Баланс: {user_data["balance"]} лей \n'
                                                f'\n'
                                                f'Вы можете вывести средства, либо заработать дополнительно денег перед выводом\n'
        ), reply_markup=ikb3)

    if callback.data == 'btn_cash_payment':
        await callback.message.delete()
        await callback.message.answer(text='Введите ваши реквезиты:', reply_markup=ikb4)

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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
