from pyairtable import *
import config


def get_urls(subjects: list):
    urls = Table(config.api_key, config.base_key, 'urls')
    res = urls.all()

    b = []

    for subject in subjects:
        for sub in res:
            if sub['fields']['Предмет'] == subject:
                b.append(sub['fields']['Посилання'])

    return b


def get_timetable(day, day_of_week, base_key):
    timetable = Table(config.api_key, config.base_key, 'timetable')
    res = timetable.get(day)['fields']
    if base_key == 0:
        urls = get_urls([res['0'], res['1'], res['2'], res['3']])

        return f"<strong><pre>..:{config.week[day_of_week]}:..</pre></strong>\n\n" \
               f"1️⃣ <b>{res['0']}</b> <i>8.30-9.50</i>\n" \
               f"{urls[0]}\n\n" \
               f"2️⃣ <b>{res['1']}</b> <i>10.10-11.30</i>\n" \
               f"{urls[1]}\n\n" \
               f"3️⃣ <b>{res['2']}</b> <i>12.00-13.20</i>\n" \
               f"{urls[2]}\n\n" \
               f"4️⃣ <b>{res['3']}</b> <i>13.30-14.50</i>\n" \
               f"{urls[3]}"
    else:
        return f"<strong><pre>..:{config.week[day_of_week]}:..</pre></strong>\n\n" \
               f"1️⃣ <b>{res['0']}</b> <i>8.30-9.50</i>\n\n" \
               f"2️⃣ <b>{res['1']}</b> <i>10.10-11.30</i>\n\n" \
               f"3️⃣ <b>{res['2']}</b> <i>12.00-13.20</i>\n\n" \
               f"4️⃣ <b>{res['3']}</b> <i>13.30-14.50</i>"


def get_urls_to_connect():
    urls = Table(config.api_key, config.base_key, 'urls')
    res = urls.all()

    b = ''

    for r in res:
        b += f"<b>{r['fields']['Предмет']}</b>:\n {r['fields']['Посилання']}\n\n"

    return b


get_urls_to_connect()
