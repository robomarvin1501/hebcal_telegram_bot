from config import TOKEN
import telebot
import json, datetime

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "I'm a hebrew calendar reminder bot!\nQuick warning for you, I'm still in alpha, "
                                      "so not everything yet exists, and some things are probably a little broken.\n"
                                      "May I recommend that if any of this data is important, please put it somewhere "
                                      "else as well?\n\n"
                                      "To business. I send reminders at 0900 (Current Israel time) on the day of a "
                                      "reminder (night before reminders hopefully coming soon).\n"
                                      "For assistance on how to set a reminder, and other commands which will be added "
                                      "soon, please type /help.\n"
                                      "You can see this message again by typing /start.\n"
                                      "Leap dates are currently NOT supported")



@bot.message_handler(commands=["add_date"])
def add_reminder(message):
    try:
        with open(f"data_hebrew/{message.chat.id}.json", 'r') as f:
            _ = json.load(f)
    except FileNotFoundError:
        with open(f"data_hebrew/{message.chat.id}.json", 'w') as f:
            json.dump({}, f)
    try:
        with open(f"data_gregorian/{message.chat.id}.json", 'r') as f:
            _ = json.load(f)
    except FileNotFoundError:
        with open(f"data_gregorian/{message.chat.id}.json", 'w') as f:
            json.dump({}, f)

    command = message.text.split()[1:]
    when, who, what = command[0], command[1], ' '.join(command[2:])
    with open(f"data_hebrew/{message.chat.id}.json", 'r') as f:
        hebrew_json_for_person = json.load(f)
        hebrew_json_for_person[when] = [who, what]
    with open(f"data_hebrew/{message.chat.id}.json", 'w') as f:
        json.dump(hebrew_json_for_person, f)
    bot.send_message(message.chat.id, text='-'.join([when, who, what]))
    next_ten_greg = get_next_gregorian_dates(when)

    with open(f"data_gregorian/{message.chat.id}.json", 'r') as f:
        greg_json_for_person = json.load(f)

    for greg_date in next_ten_greg:
        greg_json_for_person[greg_date] = [who, what]

    with open(f"data_gregorian/{message.chat.id}.json", 'w') as f:
        json.dump(greg_json_for_person, f)


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(message.chat.id, "A help message!\n"
                                      "My current commands and their usage:\n"
                                      "/start    => See the start message and explanation.\n"
                                      "/help     => See this message.\n"
                                      "/add_date <when> <who> <what> => Add a reminder, on the set date, for the set "
                                      "person, reminding for the set what. Dates are of the format DD/MM, "
                                      "month 01 = Nisan.\n"
                                      "Leap dates are currently NOT supported")


def get_next_gregorian_dates(hebrew_date):
    with open("dates_jsons/greg_to_hebrew_dates.json", 'r') as f:
        greg_to_hebrew = json.load(f)
    with open("dates_jsons/hebrew_to_greg_dates.json", 'r') as f:
        hebrew_to_greg = json.load(f)
    today = datetime.date.today()
    today_month = str(today.month) if len(str(today.month)) == 2 else '0' + str(today.month)
    today_day = str(today.day) if len(str(today.day)) == 2 else '0' + str(today.day)
    today_greg = '-'.join([str(today.year), str(today_month), str(today_day)])
    today_hebrew = greg_to_hebrew[today_greg]
    months = ["Nisan", "Iyyar", "Sivan", "Tamuz", "Av", "Elul", "Tishrei", "Cheshvan", "Kislev", "Tevet", "Sh'vat",
              "Adar I", "Adar II"]
    word_month = months[int(hebrew_date.split('/')[1]) - 1]

    upcoming_greg_dates = []

    for year in range(int(today_hebrew.split('-')[0]), int(today_hebrew.split('-')[0]) + 4):
        upcoming_hebrew_date = str(year) + '-' + word_month + '-' + hebrew_date.split('/')[0]
        upcoming_greg_dates.append(hebrew_to_greg[upcoming_hebrew_date])

    return upcoming_greg_dates


bot.infinity_polling()
