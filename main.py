import requests
import telepot
from pprint import pprint

import time
from subprocess import call


__author__ = 'Andrew Kuchev (kuchevad@gmail.com)'

TOKEN = 'TOKEN'
bot = telepot.Bot(TOKEN)


def message_handler(msg):
    pprint(msg)
    if 'forward_from' in msg or 'reply_to_message' in msg:
        if 'forward_from' in msg:
            id = msg['forward_from']['id']
            text = msg['text']
        else:
            id = msg['reply_to_message']['from']['id']
            text = msg['reply_to_message']['text']

        photos = bot.getUserProfilePhotos(id)['photos']
        pprint(photos)
        if len(photos) == 0:
            bot.sendMessage(msg['chat']['id'], 'You dont have a photo')
            return

        best_photo = photos[0][-1]
        photo_file = bot.getFile(best_photo['file_id'])
        file = requests.get('https://api.telegram.org/file/bot' + TOKEN + '/' + photo_file['file_path'])
        with open('img', 'wb') as f:
            f.write(file.content)
        make_meme('img', best_photo['height'], best_photo['height'], text.upper())
        with open('img.jpg', 'rb') as f:
            bot.sendPhoto(msg['chat']['id'], f)


def draw_text(filename, height, width, gravity, text, output_filename):
    call(["convert",
          "-gravity", "center",
          "-stroke", "black",
          "-fill", "white",
          "-background", 'transparent',
          "-strokewidth", str(int(width ** 0.18)),
          "-font", "/usr/share/fonts/TTF/impact.ttf",
          "-size", '{}x{}'.format(int(width * 0.9), height // 5),
          'caption:' + text,
          filename,
          "+swap",
          "-gravity", gravity,
          "-composite",
          output_filename])


def make_meme(filename, height, width, text):
    words = text.split()
    if len(words) < 4 or len(text) < 20:
        draw_text(filename, height, width, "south", text, "img.jpg")
    else:
        top_text = ' '.join(words[:len(words) // 2 + 1])
        bottom_text = ' '.join(words[len(words) // 2 + 1:])
        draw_text(filename, height, width, "north", top_text, "img.jpg")
        draw_text("img.jpg", height, width, "south", bottom_text, "img.jpg")


def main():
    bot.message_loop(message_handler)
    print('Listening ...')
    while 1:
        time.sleep(10)


if __name__ == '__main__':
    main()
