# -*- coding: utf-8 -*-

from roboflow import Roboflow

rf = Roboflow(api_key="ukcYHZumokIMpL0mUCZ4")
project = rf.workspace().project("detection-of-pcos-classification")
model = project.version(1).model

# infer on a local image
predictions=model.predict("/content/stream.jpg").json()
print(predictions['predictions'][0]['top'])
print((predictions['predictions'][0]['confidence'])*100)
# infer on an image hosted elsewhere

# save an image annotated with your predictions
model.predict("/content/stream.jpg").save("prediction.jpg")

!pip install telebot

import telebot
import requests
from PIL import Image
from io import BytesIO
from roboflow import Roboflow

TelegramBOT_TOKEN = '6351900100:AAE3hywU2AtoeEdbyo-cbe-QupVWni6SIpY'
roboflow_api_key = 'ukcYHZumokIMpL0mUCZ4'
bot = telebot.TeleBot(TelegramBOT_TOKEN)

rf = Roboflow(api_key=roboflow_api_key)
project = rf.workspace().project("detection-of-pcos-classification")  # Replace with your project name
model = project.version(1).model

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! This bot can detect brain tumors from images. Please send an image.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    photo_info = bot.get_file(file_id)
    photo_url = f"https://api.telegram.org/file/bot{TelegramBOT_TOKEN}/{photo_info.file_path}"
    response = requests.get(photo_url)
    image = Image.open(BytesIO(response.content))

    input_image_path = "/content/stream.jpg"
    image.save(input_image_path)

    try:
        predictions = model.predict(input_image_path).json()
        predicted_text = predictions['predictions'][0]['top']
        predicted_text1 = predictions['predictions'][0]['confidence']

        bot.reply_to(message, f"Prediction: {predicted_text} {predicted_text1}")
    except Exception as e:
        bot.reply_to(message, "An error occurred during image-to-text prediction.")

bot.polling()
