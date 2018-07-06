import common

from telegram.ext import  (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging

password = 'BINANCE123456'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
#command handlers
def subscribe(bot, update,args):
	if update.message.chat_id not in common.subscribers:
		clave = args[0]
		if clave == password:
			common.subscribers.append(update.message.chat_id)
			bot.sendMessage(update.message.chat_id, text='REGISTRADO!')
			common.saveSubscribers(common.subscribers)
		else: 
			bot.sendMessage(update.message.chat_id, text="Clave invalida")
	else:
		bot.sendMessage(update.message.chat_id, text='YA ESTAS REGISTRADO!')

def posicion(bot, update,args):
	if update.message.chat_id in common.subscribers: 
		resp = common.updatePosicion(args)
		full_resp = "Posicion recibida, parametros actuales: " + str(resp)
		bot.sendMessage(update.message.chat_id,text = full_resp)
	else:
		bot.sendMessage(update.message.chat_id,text = "No tienes permiso para usar este comando")

def unsubscribe(bot, update):
	if update.message.chat_id in common.subscribers:
		common.subscribers.remove(update.message.chat_id)
		bot.sendMessage(update.message.chat_id, text='ADIOS!')
		common.saveSubscribers(common.subscribers)
	else:
		bot.sendMessage(update.message.chat_id, text='NO ESTAS REGISTRADO')
def inicio(bot,update):
    bot.sendMessage(update.message.chat_id, text=
	
	"""Bienvenidos al Bot de Binance, los comandos disponibles son : \n 
	/registrar - Para registrar usuario, manda el comando mas la contraseña
	/suprimir - Para suprimir cuenta.
	/posicion - Para colocar posiciones, manda el comando mas la posicion Ej: 0.012
	/info - Para ver informacion general del bot
	"""   
	
)



def bot_main(bot_token=""):
	# Create the EventHandler and pass it your bot's token.
	updater = Updater(bot_token)

	
	common.bot = updater.bot
	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("registrar", subscribe,pass_args = True))
	dp.add_handler(CommandHandler("suprimir", unsubscribe))
	dp.add_handler(CommandHandler("posicion",posicion,pass_args= True))
	dp.add_handler(CommandHandler('start',inicio))
	# Start the Bot
	updater.start_polling(timeout=5)

	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()
	return common.bot