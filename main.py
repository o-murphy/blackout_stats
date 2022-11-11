import asyncio
import tomllib
from modules.ping import infinite_ping
from modules.stats import BlackoutState
from modules import bot


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
        CHAT_ID = config['main']['CHAT_ID']
finally:
    pass


async def main():
    blackout = BlackoutState(HOST)
    a, b = await asyncio.gather(*[
        infinite_ping(HOST, TIMEOUT, callback=blackout.save_state),
        bot.run_bot(TOKEN, blackout)
    ])


if __name__ == '__main__':
    asyncio.run(main())
