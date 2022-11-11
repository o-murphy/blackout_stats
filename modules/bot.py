from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from .stats import BlackoutState
from .plot import make_plot


async def run_bot(token, blackout: BlackoutState):
    bot = Bot(token=token, parse_mode='html')
    dp = Dispatcher(bot)

    await dp.bot.set_my_commands(commands=[types.BotCommand('stats', 'Get statistics'),
                                           types.BotCommand('now', 'Get state')])
    dp.register_message_handler(lambda msg, bk=blackout: send_stats(msg, bk), commands=['stats'])
    dp.register_message_handler(lambda msg, bk=blackout: get_state(msg, bk), commands=['now'])

    try:
        await dp.skip_updates()
        await dp.start_polling(dp)
    finally:
        await bot.session.close()


async def send_stats(message: types.Message, blackout: BlackoutState):
    data = blackout.get_last_days(7)
    buf = make_plot(data)
    await message.answer_photo(buf.getvalue())


async def get_state(message: types.Message, blackout: BlackoutState):
    await message.answer(f'{blackout.last_time}, {blackout.previous}')


if __name__ == '__main__':
    pass
