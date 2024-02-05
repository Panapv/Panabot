import logging
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from modules import *

# Authentication to manage the bot
TOKEN = os.getenv('TOKEN');
if TOKEN==None:
    print('Lembra indicar a variable TOKEN');
    print('p.ex: docker run --rm TOKEN=token_val Panabot');
    exit(1);

# Show logs in terminal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# This function responds to start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bóas! Son Panabot, en que podo axudarte?")

# Esta función devolde un pequeno parte meteorolóxico da localidade de Portomarín
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_weather()) 

# Esta función devolde a imaxen da nasa do día
async def apod(update: Update, context: ContextTypes.DEFAULT_TYPE):
    res, exp, title = get_apod();
    if res.status_code != 200:
     await context.bot.send_message(chat_id=update.effective_chat.id, text='Non se pudo conectar ca páxina') 
    else:
        img = open('apod.jpg', 'rb')
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=img, caption=f'Título: {title}\n"{exp}"') 
            
# Esta función devolde un pequeno parte meteorolóxico da localidade de Portomarín
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_joke()) 

# Define la función para manejar archivos
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Verifica si el mensaje tiene un documento adjunto
    if update.message.document:
        file = await context.bot.get_file(update.message.document)
        filename = update.message.document.file_name
        await file.download_to_drive(filename)
        if 'csv' in filename:
            answer = get_info(filename);
        filename = convert(filename)
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer) 
    else:
        update.message.reply_text('Por favor, envía un archivo válido.')


if __name__ == '__main__':
    # Start the application to operate the bot
    application = ApplicationBuilder().token(TOKEN).build()

    # Handler to manage the start command
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Handler da api meteoroloxica
    weather_handler = CommandHandler('weather', weather)
    application.add_handler(weather_handler)

    # Handler da api da nasa
    apod_handler = CommandHandler('apod', apod)
    application.add_handler(apod_handler)

    # Handler da api da nasa
    joke_handler = CommandHandler('joke', joke)
    application.add_handler(joke_handler) 

    # Handler de archivos csv y json
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    # Keeps the application running
    application.run_polling()