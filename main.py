# python3 -m venv venv
# source venv/bin/activate
# pip install -r requeriments.txt

import telebot
from telebot import types
import os
import time
import asyncio
from youtube import descargar_youtube
from dotenv import load_dotenv
from facebook import descargar_facebook

load_dotenv()

TOKEN= os.getenv("7486499541:AAFWRRFsAhbXXWPnnSRK-W-8U5qm7aeFcY4") 
bot = telebot.TeleBot(TOKEN)

home = os.path.expanduser("~")
ruta_guardado = os.path.join(home, "Descargas")

def borrar_archivo(ruta_archivo):
    try:
        os.remove(ruta_archivo)
        print(f"Archivo {ruta_archivo} borrado exitosamente.")
    except OSError as e:
        print(f"No se pudo borrar el archivo {ruta_archivo}: {e}")

def es_http_o_https(url):
    return url.startswith("http://") or url.startswith("https://")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hola, bienvenido al bot de prueba")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Hola, bienvenido al bot de prueba")


def descargar_video(message):
    if not es_http_o_https(message.text):
        bot.reply_to(message, f"La url no es válida ({message.chat.id})")
        return

    print("Video a descargar: " + message.text)
    bot.reply_to(message, "Vamos con la descarga...")

    if "facebook" in message.text:
        msg, archivo = descargar_facebook(message.text)
    else:
        msg, archivo = descargar_youtube(message.text)

    if archivo is None:
        bot.reply_to(message, msg)
        return

    print(msg)
            
    chat_id = message.chat.id

    with open(archivo, 'rb') as video_file:
        bot.send_video(chat_id, video_file)
            
    borrar_archivo(archivo)

def mensaje_por_defecto(message):
    # Aquí puedes personalizar el mensaje por defecto
    respuesta = f"¡Hola! No entiendo tu mensaje. Soy un bot simple. 😅 "
    bot.send_message(message.chat.id, respuesta)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    descargar_video(message)


# Ejecuta el bot
if __name__ == "__main__":
    #bot.polling()

    bot.infinity_polling()
