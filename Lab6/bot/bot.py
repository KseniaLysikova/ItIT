import telebot
from telebot import types
import psycopg2

conn = psycopg2.connect(database="bot",
                        user="postgres",
                        password="123456",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

token = "5633966217:AAGzoZwRY0yyR9pbuLfCNh7XTAXGryLBVQM"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()

    keyboard.row("Понедельник", "Вторник", "Среда")
    keyboard.row("Четверг", "Пятница", "Суббота")
    keyboard.row("Текущая неделя", "Следующая неделя")

    bot.send_message(
        message.chat.id,
        "Привет! Хочешь узнать свежую информацию о МТУСИ?",
        reply_markup=keyboard
    )


@bot.message_handler(commands=["week"])
def week_command(message):
    cursor.execute("SELECT curr_week FROM bot_info")
    current_week = list(cursor.fetchone())
    bot.send_message(
        message.chat.id,
        "Сейчас идет " + ("нечётная" if int(current_week[0]) % 2 else "чётная") + " неделя")


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "Я умею сообщать вам расписание и информацию о текущей неделе; предоставлять вам ссылку на официальный сайт "
        "МТУСИ\n\n"
        "/help — получить список доступных команд\n"
        "/week - получить информацию о том, является четной ли или нет текущая неделя\n"
        "/mtuci — получить ссылку на официальный сайт МТУСИ"
    )


@bot.message_handler(commands=["mtuci"])
def mtuci_command(message):
    bot.send_message(
        message.chat.id,
        "Официальный сайт МТУСИ доступен по адресу https://mtuci.ru/"
    )


def get_schedule(next_week):
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    cursor.execute("SELECT tt.day_name, s.subject_name, tt.room_numb, tt.start_time, "
                   "tr.full_name FROM subject s, timetable tt, teacher tr WHERE s.subject_id = tr.subject "
                   "AND s.subject_id = tt.subject AND tt.week = " +
                   ("((SELECT curr_week FROM bot_info) + 1)" if next_week else "(SELECT curr_week FROM bot_info)") +
                   " order by tt.id")

    result = {day: [] for day in days}
    for i in cursor.fetchall():
        if i[0] == 'Понедельник':
            result["Понедельник"].append(
                str(i[1]) + ", " + str(i[2]) + ", " + str(i[3]) + ", " + str(i[4]) + "\n")
        elif i[0] == 'Вторник':
            result["Вторник"].append(
                str(i[1]) + ", " + str(i[2]) + ", " + str(i[3]) + ", " + str(i[4]) + "\n")
        elif i[0] == 'Среда':
            result["Среда"].append(
                str(i[1]) + ", " + str(i[2]) + ", " + str(i[3]) + ", " + str(i[4]) + "\n")
        elif i[0] == 'Четверг':
            result["Четверг"].append(
                str(i[1]) + ", " + str(i[2]) + ", " + str(i[3]) + ", " + str(i[4]) + "\n")
        elif i[0] == 'Пятница':
            result["Пятница"].append(
                str(i[1]) + ", " + str(i[2]) + ", " + str(i[3]) + ", " + str(i[4]) + "\n")
        elif i[0] == 'Суббота':
            result["Суббота"].append(
                str(i[1]) + ", " + str(i[2]) + ", " + str(i[3]) + ", " + str(i[4]) + "\n")
    return result


@bot.message_handler(content_types=["text"])
def answer(message):
    text = message.text
    if text == "Текущая неделя":
        for i in get_schedule(0):
            bot.send_message(message.chat.id, i + "\n_______\n" + get_schedule(0)[i][0] +
                             (get_schedule(0)[i][1] if len(get_schedule(0)[i]) > 1 else "") +
                             (get_schedule(0)[i][2] if len(get_schedule(0)[i]) > 2 else "") +
                             (get_schedule(0)[i][3] if len(get_schedule(0)[i]) > 3 else "") + "\n_______\n")
    elif text == "Следующая неделя":
        for i in get_schedule(1):
            bot.send_message(message.chat.id, i + "\n_______\n" + get_schedule(0)[i][0] +
                             (get_schedule(1)[i][1] if len(get_schedule(1)[i]) > 1 else "") +
                             (get_schedule(1)[i][2] if len(get_schedule(1)[i]) > 2 else "") +
                             (get_schedule(1)[i][3] if len(get_schedule(1)[i]) > 3 else "") + "\n_______\n")
    elif text in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]:
        bot.send_message(message.chat.id, text + "\n_______\n" + get_schedule(0)[text][0] +
                         (get_schedule(0)[text][1] if len(get_schedule(0)[text]) > 1 else "") +
                         (get_schedule(0)[text][2] if len(get_schedule(0)[text]) > 2 else "") +
                         (get_schedule(0)[text][3] if len(get_schedule(0)[text]) > 3 else "") + "\n_______\n")
    elif text == "sus?":
        bot.send_message(message.chat.id, "ඞ")
    elif text == "Хочу":
        bot.send_message(message.chat.id, 'Тогда тебе сюда - https://mtuci.ru/')
    else:
        bot.send_message(message.chat.id, "Извините, я Вас не понял")


bot.infinity_polling()
