import platform  # For getting the operating system name
import subprocess  # For executing a shell command
import asyncio


def ping(host: str):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
    proccess = subprocess.Popen(command, stdout=subprocess.PIPE)
    proccess.wait()
    return proccess.returncode == 0, proccess.stdout.read().decode('utf-8')


async def infinite_ping(host: str, timeout: int, callbacks: list[callable] = None):
    while True:
        is_host, output = ping(host)
        is_global, output = ping('google.com')
        if not is_global:
            result = None
        elif is_host:
            result = True
        else:
            result = False
        if callbacks:
            for callback in callbacks:
                try:
                    callback(host, result, output)
                except Exception:
                    continue
        await asyncio.sleep(timeout)


if __name__ == '__main__':
    asyncio.run(infinite_ping('94.45.54.166', 2))
