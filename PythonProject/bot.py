import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

TOKEN = ""  # Вставь свой токен

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Списки подарков для разных рулеток
GIFT_POOLS = {
    "cheap": [
        ("Наклейка", 50),
        ("Чашка кофе", 30),
        ("Шоколадка", 20)
    ],
    "expensive": [
        ("iPhone 15 Pro", 5),
        ("MacBook Air", 10),
        ("Наушники AirPods", 20),
        ("Футболка", 65)
    ]
}

# Словарь для хранения выбранной рулетки пользователем
user_choices = {}


@dp.message(Command("start"))
async def start(message: Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎰 Выбрать рулетку", callback_data="select_roulette")]
    ])
    await message.answer("Привет! Выбери рулетку и попробуй свою удачу!", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "select_roulette")
async def select_roulette(callback_query: CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="💰 Дешевая рулетка", callback_data="roulette_cheap")],
        [types.InlineKeyboardButton(text="💎 Дорогая рулетка", callback_data="roulette_expensive")]
    ])
    await callback_query.message.edit_text("Выбери рулетку:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data.startswith("roulette_"))
async def set_roulette(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    choice = callback_query.data.split("_")[1]  # cheap или expensive
    user_choices[user_id] = choice  # Запоминаем выбор пользователя

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎲 Испытать удачу", callback_data="spin")]
    ])

    await callback_query.message.edit_text(
        f"Ты выбрал {'💰 Дешевую' if choice == 'cheap' else '💎 Дорогую'} рулетку! Нажми, чтобы крутить:",
        reply_markup=keyboard
    )


@dp.callback_query(lambda c: c.data == "spin")
async def spin_wheel(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in user_choices:
        await callback_query.answer("Сначала выбери рулетку!", show_alert=True)
        return

    selected_pool = GIFT_POOLS[user_choices[user_id]]
    gift = random.choices([g[0] for g in selected_pool], weights=[g[1] for g in selected_pool])[0]

    await callback_query.message.edit_text(f"🎁 Поздравляем! Ты выиграл: {gift}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

