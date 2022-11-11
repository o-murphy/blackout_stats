import asyncio
import tomllib
from modules.ping import infinite_ping
from modules.stats import BlackoutState


HOST = 'google.com'
TIMEOUT = 2


try:
    with open('config.toml', 'rb') as fp:
        config = tomllib.load(fp)
        HOST = config['main']['HOST']
        TIMEOUT = config['main']['TIMEOUT']
finally:
    pass


blackout = BlackoutState(HOST)


if __name__ == '__main__':
    asyncio.run(
        infinite_ping(HOST, TIMEOUT, callback=blackout.save_state)
    )