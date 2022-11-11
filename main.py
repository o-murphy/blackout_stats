import asyncio
import sys

if sys.version_info.minor < 11:
    import tomli as tomllib
else:
    import tomllib
from modules.ping import infinite_ping
from modules.stats import BlackoutState
from modules.bot import BotInstance

HOST = 'google.com'
TIMEOUT = 2
TOKEN = ""
CHAT_ID = 0

try:
    with open('config.toml', 'rb') as fp:
        config = tomllib.load(fp)
        HOST = config['main']['HOST']
        TIMEOUT = config['main']['TIMEOUT']
        TOKEN = config['main']['TOKEN']
        CHAT_IDS = config['main']['CHAT_IDS']
finally:
    pass


async def main():
    blackout = BlackoutState(HOST)
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
