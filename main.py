import telebot
import requests
import re

# Telegram bot token (replace with your own token)
TOKEN = ''

# Create an instance of the TeleBot class
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "ℹ მოგესალმებით! გთხოვთ შეიყვანეთ გაჩერების ID.")

@bot.message_handler(func=lambda message: True)
def get_arrival_times(message):
    # Extract the stop ID from the message text using regular expressions
    stop_id = re.findall(r'\d+', message.text)
    if stop_id:
        stop_id = stop_id[0]

    url = f"http://transfer.ttc.com.ge:8080/otp/routers/ttc/stopArrivalTimes?stopId={stop_id}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the XML response
        xml_data = response.text

        # Process the XML response to extract desired data
        data = xml_data.replace('{"ArrivalTime":[', '').replace('{"RouteNumber"', '🚌').replace('"DestinationStopName"', ' ➡').replace('"ArrivalTime"', ' ⏱').replace('}]}', '').replace('\\"', '').replace('},', '\n').replace(']}', '⚠ შეყვანილია გაჩერების არასწორი ID').replace(':', ': ')

        # Send the processed data as a message
        bot.send_message(message.chat.id, data)
    else:
        bot.send_message(message.chat.id, "Request failed with status code: " + str(response.status_code))

# Start the bot
bot.polling()
