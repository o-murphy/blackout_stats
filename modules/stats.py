from datetime import datetime
import csv
from typing import NamedTuple
import logging
from enum import Enum


log = logging.getLogger('stats')
log.setLevel(logging.INFO)


class Statisctics(Enum):
    Skipped = False
    Saved = True


class StatsLine(NamedTuple):
    host: str
    date: str
    start: str
    end: str
    state: str


class BlackoutState:
    def __init__(self, host='None', schedule: list = None):
        self.host = host
        self.schedule = schedule
        self.current = None
        self.cur_time = datetime.now()
        self.previous = ""
        self.prev_time = datetime.now()
        self.load_state()

    def load_state(self):
        try:
            with open('stats.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                rows = [row for row in reader]
                print(rows[-1])
                self.host, date, start, end, state = rows[-1]
                self.previous = state == 'True'
                self.prev_time = datetime.strptime(f'{date} {end}', "%Y-%m-%d %H:%M:%S.%f")
        except IOError as error:
            self.save_state(self.host, False, datetime.now())
        except IndexError as error:
            self.save_state(self.host, False, datetime.now())

    def save_state(self, host, result, output):
        now = datetime.now()
        self.current = result
        self.cur_time = now
        if self.previous != result or self.prev_time.time() > now.time():
            with open('stats.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([
                    host,
                    self.prev_time.date(),
                    self.prev_time.time(),
                    now.time(),
                    result
                ])
                self.previous = result
                self.prev_time = now
            log.info(Statisctics.Saved)
        else:
            log.info(Statisctics.Skipped)

    def get_data(self):
        try:
            with open('stats.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                data = [row for row in reader]
                last_row = data[-1]
                now_row = [
                    last_row[0],
                    self.cur_time.date().strftime('%Y-%m-%d'),
                    self.cur_time.time().strftime("%H:%M:%S.%f"),
                    self.cur_time.time().strftime("%H:%M:%S.%f"),
                    self.current
                ]
                print(now_row)
                data.append(now_row)
                return data

        except IOError as error:
            return None
        except IndexError as error:
            return None


if __name__ == '__main__':
    blackout = BlackoutState('google.com')
    print(blackout.get_data())
