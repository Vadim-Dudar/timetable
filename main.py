import telebot
import config
import time
import datetime
import airtable
import zamina


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def wellcome(mes):

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2).add('📘 Розклад на сьогодні', '📗 Розклад на завтра', '📚 Розклад на тиждень', '🧾 Коди до підключення', '📝 Заміни', '🔧 Налаштування', '☕ Купи мені кави!')

    bot.send_message(mes.chat.id, '<b>Привіт друже❕</b>\nТи повинен бути з групи <b>П-23</b>, щоб користуватися цим ботом. Не засмучуйся, просто напиши моєму творцю<i>(@h0opsy)</i>.\nВін обов\'язково візьме до уваги!'.format(mes.from_user, bot.get_me()), parse_mode='html')
    time.sleep(3)
    bot.send_message(mes.chat.id, 'Тут розібрались❕\nЯ створений для полегшення життя студента, від тепер ти не мусиш шукати розклад, коди до підключення, заміни.'.format(mes.from_user, bot.get_me()), parse_mode='html')
    time.sleep(3)
    bot.send_message(mes.chat.id, 'Ну що❕\nГоді лірики, почнімо, тиць що хочеш❕'.format(mes.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

    config.base[mes.chat.id] = 0


@bot.message_handler(regexp='📘 Розклад на сьогодні')
def today(mes):

    day_of_week = datetime.datetime.today().weekday()

    if day_of_week >= 5:
        bot.send_message(mes.chat.id, 'Ти в курсі, що сьогодні вихідний? Ну так і бути лови розклад на понеділок!')
        timetable = airtable.get_timetable(config.numbering[0], 0, config.base[mes.chat.id])
        bot.send_message(mes.chat.id, timetable.format(mes.from_user, bot.get_me()), parse_mode='html')
    else:
        timetable = airtable.get_timetable(config.numbering[day_of_week], day_of_week, config.base[mes.chat.id])
        bot.send_message(mes.chat.id, timetable.format(mes.from_user, bot.get_me()), parse_mode='html')


@bot.message_handler(regexp='📗 Розклад на завтра')
def tomorrow(mes):

    day_of_week = datetime.datetime.today().weekday()+1

    if day_of_week == 5:
        bot.send_message(mes.chat.id, 'Ти в курсі, що сьогодні вихідний? Ну так і бути лови розклад на понеділок!')
        timetable = airtable.get_timetable(config.numbering[0], 0, config.base[mes.chat.id])
        bot.send_message(mes.chat.id, timetable.format(mes.from_user, bot.get_me()), parse_mode='html')
    elif day_of_week == 6:
        timetable = airtable.get_timetable(config.numbering[0], 0, config.base[mes.chat.id])
        bot.send_message(mes.chat.id, timetable.format(mes.from_user, bot.get_me()), parse_mode='html')
    else:
        timetable = airtable.get_timetable(config.numbering[day_of_week], day_of_week, config.base[mes.chat.id])
        bot.send_message(mes.chat.id, timetable.format(mes.from_user, bot.get_me()), parse_mode='html')
    

@bot.message_handler(regexp='📚 Розклад на тиждень')
def week(mes):

    for day in range(5):
        timetable = airtable.get_timetable(config.numbering[day], day, config.base[mes.chat.id])
        bot.send_message(mes.chat.id, timetable.format(mes.from_user, bot.get_me()), parse_mode='html')


@bot.message_handler(regexp='🧾 Коди до підключення')
def urls(mes):
    bot.send_message(mes.chat.id, airtable.get_urls_to_connect().format(mes.from_user, bot.get_me()), parse_mode='html')


@bot.message_handler(regexp='☕ Купи мені кави!')
def cup_of_coffee(mes):

    bot.send_message(mes.chat.id, 'Якщо маєш бажання підтримати автора, оплатити хостинг, тоді ось номера карток:\n<pre>4441114417095161 Монобанк\n4790729935625038 Ощадбанк\n5168755909495026 Приватбанк</pre>'.format(mes.from_user, bot.get_me()), parse_mode='html')
    time.sleep(1.3)
    bot.send_message(mes.chat.id, 'Якщо ти всетаки наважився<i>(-лась)</i>, <b>величезне дякую тобі 🥰</b>. Це мотивує працювати, якщо є якісь пропозиції <b>пиши</b> <i>(@h0opsy)</i>!'.format(mes.from_user, bot.get_me()), parse_mode='html')


@bot.message_handler(regexp='📝 Заміни')
def zamina_send(mes):

    m = bot.send_message(mes.chat.id, '🕐 Необхідно трішечки зачекати, прояви терпіння!')
    zamina.save_img()
    with open('img.png', 'rb') as img:
        bot.send_photo(mes.chat.id, img, caption='http://bcpep.org.ua/rozklad-ta-zamina/zamina-urokiv')
    bot.delete_message(mes.chat.id, m.message_id)


@bot.message_handler(regexp='🔧 Налаштування')
def settings(mes):

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    if config.base[mes.chat.id] == 0:
        button = telebot.types.InlineKeyboardButton('Off 🕹', callback_data='switch')
        markup.add(button)
    elif config.base[mes.chat.id] == 1:
        button = telebot.types.InlineKeyboardButton('On 🕹', callback_data='switch')
        markup.add(button)
    bot.send_message(mes.chat.id, 'Коди до підключення в розкладі:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def switch(call):

    if config.base[call.message.chat.id] == 1:
        config.base[call.message.chat.id] = 0
    elif config.base[call.message.chat.id] == 0:
        config.base[call.message.chat.id] = 1


bot.polling(none_stop=True)
