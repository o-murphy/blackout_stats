from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from .plot import make_plot
from .stats import BlackoutState


class BotInstance:
    def __init__(self, token: str, blackout: BlackoutState,
                 target_chats: list[int] = None):
        self.token = token
        self.blackout = blackout
        self.target_chats = target_chats
        self.bot = Bot(token=self.token, parse_mode='html')
        # loop = asyncio.get_event_loop()
        # self.dp = Dispatcher(self.bot, loop=loop)
        self.dp = Dispatcher(self.bot)

    async def run_bot(self):

        await self.dp.bot.set_my_commands(commands=[types.BotCommand('stats', 'Get statistics'),
                                                    types.BotCommand('now', 'Get state')])
        self.dp.register_message_handler(lambda msg, bk=self.blackout: self.send_stats(msg), commands=['stats'])
        self.dp.register_message_handler(lambda msg, bk=self.blackout: self.get_state(msg), commands=['now'])

        try:
            await self.dp.skip_updates()
            await self.dp.start_polling(self.dp)
        finally:
            await self.bot.session.close()

    async def send_stats(self, message: types.Message):
        await message.answer('Очікуйте будь ласка, розраховуємо статистику')
        data = self.blackout.get_data()
        buf = make_plot(data, 4, self.blackout.schedule)
        legend = [
            "<b>Статистика</b>",
            "",
            "🟦 Електропостачання в нормі",
            "⬛ Електропостачання відсутнє",
            "🟨 Можливе відключення за графіком",
            "🟥 Немає даних",
        ]
        await message.answer_photo(buf.getvalue(), caption='\n'.join(legend))

    async def get_state(self, message: types.Message):
        await message.answer(f'{self.get_state_text()}\n<i>Останнє оновлення: {self.get_time_stamp()}</i>')

    def get_time_stamp(self):
        return self.blackout.last_time.strftime("%d.%m.%Y %H:%M")

    def get_state_text(self):
        if self.blackout.previous is None:
            return "<b>⚠ Немає з'єднання, спробуйте пізніше</b>"
        elif self.blackout.previous:
            return "<b>💡 Електропостачання в нормі</b>"
        else:
            return "<b>🕯️ Електропостачання відсутнє</b>"

    @staticmethod
    def get_notify_text(result):
        if result:
            return "<b>⚠Увага!⚠</b>\n💡 Електропостачання відновлено!"
        else:
            return "<b>⚠Увага!⚠</b>\nМожливі проблеми з електропостачанням!\nДістаємо: 🔦🕯️"

    async def send_notify(self, host, result, output):
        if self.target_chats and self.blackout.previous != result and result is not None:
            for uid in self.target_chats:
                await self.bot.send_message(
                    uid,
                    f'{self.get_notify_text(result)}\n<i>Останнє оновлення: {self.get_time_stamp()}</i>',
                    disable_notification=True
                )


if __name__ == '__main__':
    pass
