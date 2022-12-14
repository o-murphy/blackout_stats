import io
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd

test_data = [
    ['IP', '2022-11-11', '00:18:01', '11:18:04', 'True'],
    ['IP', '2022-11-11', '11:18:04', '13:18:12', 'False'],
    ['IP', '2022-11-11', '13:18:12', '20:18:12', 'True'],
    ['IP', '2022-11-11', '20:18:12', '23:18:12', 'False'],

    ['IP', '2022-11-12', '00:18:01', '10:18:04', 'True'],
    ['IP', '2022-11-12', '10:18:04', '12:18:12', 'True'],
    ['IP', '2022-11-12', '12:18:12', '19:18:12', 'False'],
    ['IP', '2022-11-12', '19:18:12', '23:18:12', 'True'],

    ['IP', '2022-11-13', '00:18:01', '11:18:04', 'True'],
    ['IP', '2022-11-13', '11:18:04', '13:18:12', 'False'],
    ['IP', '2022-11-13', '13:18:12', '20:18:12', 'True'],
    ['IP', '2022-11-13', '20:18:12', '23:18:12', 'True'],

    ['IP', '2022-11-14', '00:18:01', '10:18:04', 'True'],
    ['IP', '2022-11-14', '10:18:04', '12:18:12', 'True'],
    ['IP', '2022-11-14', '12:18:12', '19:18:12', 'None'],
    ['IP', '2022-11-14', '19:18:12', '23:18:12', 'False'],

    ['IP', '2022-11-15', '00:18:01', '11:18:04', 'True'],
    ['IP', '2022-11-15', '11:18:04', '13:18:12', 'True'],
    ['IP', '2022-11-15', '13:18:12', '20:18:12', 'False'],
    ['IP', '2022-11-15', '20:18:12', '23:18:12', 'True'],

    ['IP', '2022-11-16', '00:18:01', '10:18:04', 'True'],
    ['IP', '2022-11-16', '10:18:04', '12:18:12', 'True'],
    ['IP', '2022-11-16', '12:18:12', '19:18:12', 'True'],
    ['IP', '2022-11-16', '19:18:12', '23:18:12', 'True'],

    ['IP', '2022-11-17', '00:18:01', '11:18:04', 'True'],
    ['IP', '2022-11-17', '11:18:04', '13:18:12', 'False'],
    ['IP', '2022-11-17', '13:18:12', '20:18:12', 'True'],
    ['IP', '2022-11-17', '20:18:12', '23:18:12', 'True'],

]

WEEKDAYS = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Friday',
    'Thursday',
    'Saturday',
    'Sunday',
]


def next_days_rows(pre, post, schedule=None):
    # todo: prognoses of future blackouts
    rows = []
    for n in range(-pre + 1, post + 1):
        next_day = datetime.now().date() + timedelta(days=n)
        next_week_day = WEEKDAYS[next_day.weekday()]
        if not schedule:
            rows.append(['None', f'{next_day}', '00:00:00', '00:00:00', ''])
        else:
            week_day_schedule = schedule[next_week_day]
            for period in week_day_schedule:
                period = [f'{t}:00' for t in period]
                rows.append(['None', f'{next_day}', *period, 'SCHEDULE'])
    return rows


def make_plot(data, days=4, schedule=None, show=False):
    data += next_days_rows(days, 3, schedule)
    data = data[::-1]
    df = pd.DataFrame(data, columns=['Ip', 'Date', 'Start', 'End', 'Status'])
    start_time = []
    end_time = []

    today_date = datetime.now()
    pre_date = today_date - timedelta(days=4)
    df['DT'] = pd.to_datetime(df['Date'])
    df = df[df['DT'] >= pre_date]

    for i, row in df.iterrows():

        a = row['Start'].split('.')[0].split(':')
        b = row['End'].split('.')[0].split(':')
        start_hrs = int(a[0]) + (int(a[1]) / 60) + (int(a[2]) / 3600)
        end_hrs = int(b[0]) + (int(b[1]) / 60) + (int(b[2]) / 3600)

        start_time.append(start_hrs)
        end_time.append(end_hrs)

    # df['Start'] = pd.to_datetime(df['Start'])
    # df['End'] = pd.to_datetime(df['End'])

    # df['Start'] = df['Start'].hour + df['Start'].minute / 60
    # df['End'] = df['End'].hour + df['End'].minute / 60

    df['Start'] = start_time
    df['End'] = end_time
    df['Diff'] = df['End'] - df['Start']
    df = df[df.Diff >= 0]

    colors = {"False": "xkcd:black",
              "True": "xkcd:bright blue",
              "None": "xkcd:dark red", "": "xkcd:dark red",
              "SCHEDULE": "xkcd:gold"}
    widths = {"False": 0.2, "True": 0.1, "None": 0.01, "": 0.01, "SCHEDULE": 0.4}

    fig, ax = plt.subplots(dpi=200)
    ax.set_facecolor('xkcd:dark grey blue')
    plt.grid(c='xkcd:navy', linestyle='-', linewidth=0.2)

    w = []

    tasks = enumerate(df.groupby("Date", sort=False))

    for i, task in tasks:
        w.append(task[0])

        for r in task[1].groupby("Status", sort=False):
            data = r[1][["Start", "Diff"]]
            width = widths[r[0]]
            ax.broken_barh(data.values, (i - width / 2, width),
                           color=colors[r[0]], label=r[1]['Status'])

    y_ticks = [t[0] for t in df.groupby("Date", sort=False)]

    ax.set_xlabel("??????")
    ax.set_ylabel("????????")

    plt.yticks(list(range(len(y_ticks))), y_ticks)

    plt.xticks(list(range(24)), [f'{h}:00' for h in range(24)])
    plt.xticks(rotation=90)

    fig.set_figwidth(6)
    fig.set_figheight(len(y_ticks) / 2.5)
    plt.xlim(0, 24)
    plt.tight_layout()
    buf = io.BytesIO()
    if show:
        plt.show()
    plt.savefig(buf, dpi=200, format='png')
    return buf


if __name__ == '__main__':
    from modules.stats import BlackoutState
    import timeit

    b = BlackoutState()
    print(timeit.timeit(b.get_data, number=1))
    data = b.get_data()
    print(timeit.timeit(lambda: make_plot(data, show=True), number=1))
