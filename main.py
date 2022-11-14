import asyncio
import sys

if sys.version_info.minor < 11:
    import tomli as tomllib
else:
    import tomllib
from modules.ping import infinite_ping
from modules.stats import BlackoutState
from modules.bot import BotInstance
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)-30s %(levelname)-8s %(message)s")


HOST = 'google.com'
TIMEOUT = 2
TOKEN = ""
CHAT_ID = 0

GROUP = 1
SCHEDULE = None

try:
    with open('config.toml', 'rb') as fp:
        config = tomllib.load(fp)
        main = config['main']
        HOST = main['HOST']
        TIMEOUT = main['TIMEOUT']
        TOKEN = main['TOKEN']
        CHAT_IDS = main['CHAT_IDS']

        GROUP = main['GROUP']
        SCHEDULE = config['schedules'][f'group{GROUP}']
finally:
    pass


async def main():
    blackout = BlackoutState(HOST, SCHEDULE)
    bot = BotInstance(TOKEN, blackout, CHAT_IDS)
    await asyncio.gather(*[
        infinite_ping(HOST, TIMEOUT, callbacks=[
            bot.send_notify,
            blackout.save_state,
        ]),
        bot.run_bot()
    ])


if __name__ == '__main__':
    asyncio.run(main())
