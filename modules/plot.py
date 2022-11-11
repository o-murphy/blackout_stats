import matplotlib.pyplot as plt
import pandas as pd
import io
from datetime import datetime, timedelta

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
        ['IP', '2022-11-14', '12:18:12', '19:18:12', 'True'],
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


def next_days_rows(n):
    # todo: prognoses of future blackouts
    rows = []
    for n in range(1, n + 1):
        rows.append(['None', f'{datetime.now().date() + timedelta(days=n)}', '00:00:00', '00:00:00', ''])
    return rows


def make_plot(data):
    data += next_days_rows(3)
    data = data[::-1]
    df = pd.DataFrame(data, columns=['Ip', 'Date', 'Start', 'End', 'Status'])
    start_time = []
    end_time = []
    for i, row in df.iterrows():
        a = row['Start'].split('.')[0].split(':')
        b = row['End'].split('.')[0].split(':')
        start_hrs = int(a[0]) + (int(a[1]) / 60) + (int(a[2]) / 3600)
        end_hrs = int(b[0]) + (int(b[1]) / 60) + (int(b[2]) / 3600)

        start_time.append(start_hrs)
        end_time.append(end_hrs)


    df['Start'] = start_time
    df['End'] = end_time
    df['Diff'] = df['End'] - df['Start']
    color = {"False": "crimson", "True": "turquoise", "None": "white", "": "white"}
    fig, ax = plt.subplots(dpi=200)

    w = []

    tasks = enumerate(df.groupby("Date", sort=False))

    for i, task in tasks:
        w.append(task[0])

        for r in task[1].groupby("Status", sort=False):
            data = r[1][["Start", "Diff"]]
            width = 0.3 if r[0] != 'True' else 0.1
            ax.broken_barh(data.values, (i - width / 2, width),
                           color=color[r[0]], label=r[1]['Status'])

    y_ticks = [t[0] for t in df.groupby("Date", sort=False)]
    print(y_ticks)
    # y_ticks.reverse()
    # y_ticks.insert(0, '0')
    # ax.set_yticklabels(y_ticks)

    ax.set_xlabel("Час")
    ax.set_ylabel("Дата")

    plt.yticks(list(range(len(y_ticks))), y_ticks)

    plt.xticks(list(range(24)), [f'{h}:00' for h in range(24)])
    plt.xticks(rotation=90)

    fig.set_figwidth(10)
    fig.set_figheight(len(y_ticks))
    plt.xlim(0, 24)
    plt.tight_layout()
    plt.grid()
    buf = io.BytesIO()

    plt.savefig(buf, dpi=200, format='png')
    return buf


if __name__ == '__main__':
    make_plot(test_data)
