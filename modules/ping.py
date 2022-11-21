import platform  # For getting the operating system name
import subprocess  # For executing a shell command
import asyncio
import logging
from enum import Enum
from typing import Callable, Awaitable


log = logging.getLogger('ping')
log.setLevel(logging.INFO)


class PingLoopState(Enum):
    RetryPing = 1
    BreakLoop = 2


class PingResponse(Enum):
    OK = True
    ERROR = False
    NODATA = None


def ping_by_port(host: str, port: str):
    # Option for the number of packets as a function of
    # param = '-n' if platform.system().lower() == 'windows' else '-c'

    result_key = None

    if platform.system().lower() == 'windows':
        # command = ['powershell.exe', 'Test-NetConnection', host, '-p', port]
        # result_key = 'TcpTestSucceeded'
        command = ['powershell.exe', 'New-Object', 'System.Net.Sockets.TCPClient', '-ArgumentList', f'{host},{port}']
        result_key = 'Connected'
    else:
        command = ['time', 'timeout', '2', 'nc', '-vz', host, port]

    # Building the command. Ex: "ping -c 1 google.com"

    proccess = subprocess.Popen(command, stdout=subprocess.PIPE)
    proccess.wait()
    log.info(proccess.returncode)
    result = proccess.stdout.read().decode('utf-8')
    if platform.system().lower() == 'windows':
        result_dict = {}
        for line in result.split('\r\n'):
            if ':' in line:
                k, v, *other = line.split(':')
                result_dict[k.strip()] = v.strip()
        return_code = result_dict.get(result_key, False)
        return return_code, result if return_code else None
    else:
        return proccess.returncode == 0, result


def ping_by_host(host: str):
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
    proccess = subprocess.Popen(command, stdout=subprocess.PIPE)
    proccess.wait()
    return proccess.returncode == 0, proccess.stdout.read().decode('utf-8')


def ping(host: str):

    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    try:
        host, port = host.split(':')
        return ping_by_port(host, port)
    except ValueError:
        return ping_by_host(host)


async def infinite_ping(host: str, timeout: int, callbacks: list[Callable[[str, bool, str], Awaitable[str]]] = None):
    while True:
        loop_state = PingLoopState.BreakLoop
        while True:
            is_global, output = ping('google.com')
            is_host, output = ping(host)
            if not is_global:
                result = PingResponse.NODATA
            elif is_host:
                result = PingResponse.OK
            else:
                result = PingResponse.ERROR
            if result == PingResponse.ERROR and loop_state == PingLoopState.BreakLoop:
                loop_state = PingLoopState.RetryPing
            else:
                loop_state = PingLoopState.BreakLoop
            log.info(result)
            if loop_state == PingLoopState.BreakLoop:
                break
            log.info(loop_state)
            await asyncio.sleep(int(timeout/2))

        if callbacks:
            tasks = []
            for callback in callbacks:
                tasks.append(callback(host, result.value, output))
            await asyncio.gather(*tasks)
        await asyncio.sleep(timeout)


if __name__ == '__main__':
    asyncio.run(infinite_ping('94.45.54.166', 2))
