# -*- coding: utf-8 -*-

from roboflow import Roboflow
from PIL import Image, ImageDraw, ImageFont
rf = Roboflow(api_key="ukcYHZumokIMpL0mUCZ4")
project = rf.workspace().project("brain-tumor-m4vom")
model = project.version(1).model

# infer on a local image
response = model.predict("/content/back.jpg")
predictions = response.json()


# Output the predictions (optional)
print(predictions['predictions'][0]['predicted_classes'])

# Save the image with predictions (if it's an image classification task)
# Assuming the predictions are in the 'predictions' key of the response dictionary
# Replace 'label' with the key in the predictions dictionary that holds the label you want to draw on the image
label = predictions['predictions'][0]['predicted_classes']

# Open the image using PIL
img = Image.open("/content/back.jpg")

# Draw the predicted label on the image


# Save the image with the predicted label
img.save("prediction.jpg")

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
project = rf.workspace().project("brain-tumor-m4vom")  # Replace with your project name
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

    input_image_path = "/content/back.jpg"
    image.save(input_image_path)

    try:
        predictions = model.predict(input_image_path).json()
        predicted_text = predictions['predictions'][0]['predicted_classes']

        bot.reply_to(message, f"Prediction: {predicted_text}")
    except Exception as e:
        bot.reply_to(message, "An error occurred during image-to-text prediction.")

bot.polling()

import telebot
import requests
from PIL import Image
from io import BytesIO
from roboflow import Roboflow

TelegramBOT_TOKEN = '6351900100:AAE3hywU2AtoeEdbyo-cbe-QupVWni6SIpY'
roboflow_api_key = 'ukcYHZumokIMpL0mUCZ4'
bot = telebot.TeleBot(TelegramBOT_TOKEN)

rf = Roboflow(api_key=roboflow_api_key)

# Function to handle user interaction for selecting the detection type
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! This bot can detect brain tumors and PCOS from images. Please select the detection type:\n"
                          "/brain_tumor - Detect brain tumor\n"
                          "/pcos_detection - Detect PCOS")

# Function to handle brain tumor detection
@bot.message_handler(commands=['brain_tumor'])
def brain_tumor_detection(message):
    bot.reply_to(message, "Please send an image for brain tumor detection.")

    # Set the bot state to "brain_tumor" to remember the user's choice
    bot.register_next_step_handler(message, handle_brain_tumor)

# Function to handle PCOS detection
@bot.message_handler(commands=['pcos_detection'])
def pcos_detection(message):
    bot.reply_to(message, "Please send an image for PCOS detection.")

    # Set the bot state to "pcos_detection" to remember the user's choice
    bot.register_next_step_handler(message, handle_pcos_detection)

# Function to handle brain tumor detection after user input
def handle_brain_tumor(message):
    if message.photo:
        process_image_detection(message, message.photo[-1].file_id, "brain_tumor")
    else:
        bot.reply_to(message, "Please send an image for brain tumor detection.")

# Function to handle PCOS detection after user input
def handle_pcos_detection(message):
    if message.photo:
        process_image_detection(message, message.photo[-1].file_id, "pcos_detection")
    else:
        bot.reply_to(message, "Please send an image for PCOS detection.")

# Function to process the image detection based on user choice
def process_image_detection(message, file_id, detection_type):
    file_id = message.photo[-1].file_id
    photo_info = bot.get_file(file_id)
    photo_url = f"https://api.telegram.org/file/bot{TelegramBOT_TOKEN}/{photo_info.file_path}"
    response = requests.get(photo_url)
    image = Image.open(BytesIO(response.content))



    try:
      if detection_type == "brain_tumor":
            project = rf.workspace().project("brain-tumor-m4vom")  # Replace with your project name
            model = project.version(1).model
            input_image_path = "/content/stream.jpg"
            image.save(input_image_path)
            predictions = model.predict(input_image_path).json()
            predicted_text = predictions['predictions'][0]['predicted_classes']
            bot.reply_to(message, f"Prediction: {predicted_text}")
      else:
        project = rf.workspace().project("detection-of-pcos-classification")
        model = project.version(1).model
        input_image_path = "/content/back.jpg"
        image.save(input_image_path)
        predictions = model.predict(input_image_path).json()
        predicted_text = predictions['predictions'][0]['top']
        predicted_text1 = predictions['predictions'][0]['confidence']

        bot.reply_to(message, f"Prediction: {predicted_text} {predicted_text1}")





    except Exception as e:
        bot.reply_to(message, f"An error occurred during {detection_type.replace('_', ' ')} detection.")

# Start the bot
bot.polling()

