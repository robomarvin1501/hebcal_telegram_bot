from config import TOKEN
import telebot, json, datetime, os

bot = telebot.TeleBot(TOKEN)

for id_file in os.listdir("data_gregorian"):
    date_today = datetime.date.today()
    with open(f"data_gregorian/{id_file}", 'r') as f:
        data = json.load(f)
        chat_id = id_file.split('.')[0]
        for reminder_date in data.keys():
            if datetime.date.fromisoformat(reminder_date) == date_today:
                bot.send_message(chat_id, f"Who: {data[reminder_date][0]}\nWhat: {data[reminder_date][1]}")
