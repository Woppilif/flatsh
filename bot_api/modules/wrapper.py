import telegram
from telegram.ext import MessageHandler, Filters, Dispatcher, CommandHandler, CallbackQueryHandler
import logging
from .keyboards import KeyBoards, InLineKeyBoards
from sharing.models import Workers
class Wrapper():
    def __init__(self,json_data):
        self.bot = telegram.Bot(token="705147392:AAFKi_wCIILco9EnoLaykGb3coUWicOueEg")
        self.update = telegram.Update.de_json(json_data,self.bot)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.worker = self.getWorker()

    def start_work(self,bot):
        dispatcher = Dispatcher(bot=bot, update_queue=None, workers=2)
        dispatcher.add_handler(CommandHandler("start", self.start_cmd))
        dispatcher.add_handler(MessageHandler(Filters.photo, photo))
        
        #dispatcher.add_handler(CommandHandler("me", self.getMe))
        return dispatcher

    def start(self):
        sidp = self.start_work(self.bot)
        return sidp.process_update(self.update)

    def start_cmd(self,bot, update):
        return self.sendMessage("Ваш ID: {0}".format(self.update.effective_message.chat_id))
      

    def sendMessage(self,message="",keyboard=None):
        if keyboard is None:
            return self.bot.sendMessage(self.update.effective_message.chat_id,message)
        else:
            return self.bot.sendMessage(self.update.effective_message.chat_id,message,keyboard=keyboard)

    def getWorker(self):
        try:
            return Workers.objects.get(chat_id=self.update.effective_message.chat_id)
        except:
            return None