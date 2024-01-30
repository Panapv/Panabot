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


if __name__ == '__main__':
    # Start the application to operate the bot
    application = ApplicationBuilder().token(TOKEN).build()

    # Handler to manage the start command
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Handler da api meteoroloxica
    weather_handler = CommandHandler('weather', weather)
    application.add_handler(weather_handler)    

    # Keeps the application running
    application.run_polling()