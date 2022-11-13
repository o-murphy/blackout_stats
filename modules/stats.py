from datetime import datetime
import csv


class BlackoutState:
    def __init__(self, host='None', schedule: list = None):
        self.host = host
        self.schedule = schedule
        self.previous = None
        self.last_time = datetime.now()
        self.load_state()

    def load_state(self):
        try:
            with open('stats.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                rows = [row for row in reader]
                self.host, date, start, end, state = rows[-1]
                self.previous = state == 'True'
                self.last_time = datetime.strptime(f'{date} {end}', "%Y-%m-%d %H:%M:%S.%f")
        except IOError as error:
            self.save_state(self.host, False, datetime.now())
        except IndexError as error:
            self.save_state(self.host, False, datetime.now())

    def save_state(self, host, result, output):
        with open('stats.csv', 'a', newline='') as csvfile:
            now = datetime.now()
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([
                host,
                self.last_time.date(),
                self.last_time.time(),
                now.time(),
                result
            ])
            self.previous = result
            self.last_time = now

    def get_last_days(self, days: int):
        def filter_days(item, days):
            self.host, date, start, end, state = item

            start_time = datetime.strptime(start, "%H:%M:%S.%f")
            end_time = datetime.strptime(end, "%H:%M:%S.%f")
            if end_time < start_time:
                return False

            date = datetime.strptime(f'{date}', "%Y-%m-%d")
            delta = date.date() - datetime.now().date()
            if delta.days < days:
                return True
            return False

        try:
            with open('stats.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                data = [row for row in reader]
                data = list(filter(lambda item, days=days: filter_days(item, days), data))
                return data

        except IOError as error:
            return None
        except IndexError as error:
            return None


if __name__ == '__main__':
    blackout = BlackoutState('google.com')
    print(blackout.get_last_days(7))
