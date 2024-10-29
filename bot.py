import os
from dotenv import load_dotenv
import datetime
import random
from PIL import Image, ImageDraw, ImageFont
from telebot import TeleBot

print('Bot is activated.')

dotenv_path = os.path.join(os.path.dirname(__file__), 'my.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

token_bot = os.getenv('TOKEN')
bot = TeleBot(token_bot)


# обработчик для сообщения содержащего текст
@bot.message_handler(content_types = ['text'])
def text_message(message):
    bot.send_message(message.chat.id, "Привет! Отправьте картинку.")


# обработчик для сообщения содержащего изображение
@bot.message_handler(content_types=['photo'])
def photo_message(message):

    # получаем изображение
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    # cохраняем картинку с правильным именем на компьютер в заранее настроенную папку
    current = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    folder = os.getenv('SAVE_FOLDER')
    #print(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    file_name = f"{current}_{message.chat.id}.jpg"
    path = os.path.join(folder, file_name)
    with open(path, 'wb') as f:
        f.write(downloaded_file)

    # отвечаем картинкой с текстом
    bot.send_message(message.chat.id, 'Обрабатываем...')
    image = add_title(path)
    bot.send_photo(message.chat.id, photo=image)

# функция добавления фразы к изображению
def add_title(path_file):

    # выбираем из файла-сборника случайную подпись
    path = os.getenv("STORAGE_FILE")
    with open(path, encoding='utf-8') as f:
        titles = f.readlines()
    title = random.choice(titles)
    # print(title)

    # рисуем её на картинке пользователя
    img = Image.open(path_file)
    image = ImageDraw.Draw(img)
    path = os.getenv("FONT_FILE")
    font = ImageFont.truetype(path, size=26)
    image.text((int(img.width/2), int(img.height/2)), title, font=font)
    return img


bot.infinity_polling(skip_pending=True)
