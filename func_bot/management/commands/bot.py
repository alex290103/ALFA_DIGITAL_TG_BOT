# from cProfile import run
from tkinter import Message
from django.core.management.base import BaseCommand
from telegram.ext import Updater
from telegram.update import Update
from telegram import InputFile, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import CommandHandler, MessageHandler
from main.models import Bot_Commands, Bot_Buttons, Tg_Users, Hand_sending, Automatization
from main.models import Telegram_bot
from func_bot.bot_send import Send, und_buttons
from telegram.ext.filters import Filters
from datetime import timedelta
import telegram
import requests
import pytz
import pdb

class Command(BaseCommand):
    help = "Конструктор Телеграм-ботов"
    def handle(self,*args,**options):
        bots_dict = {}
        bot = {}
        for tz in pytz.all_timezones:
            print(tz)
        bots_list = list(Telegram_bot.objects.values_list("id","bot_token"))
        for b in bots_list:
            bots_dict[b[0]] = b[1]
        updaters = [Updater(bot[1]) for bot in bots_list]
        dispatchers = {i+1 : updaters[i].dispatcher for i in range(len(updaters))}
        jq = {i+1 : updaters[i].job_queue for i in range(len(updaters))}
        s_handlers = {}
        btn_handlers = {}
        def build_menu(buttons, n_cols,
                    header_buttons=None,
                    footer_buttons=None):
            menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
            if header_buttons:
                menu.insert(0, [header_buttons])
            if footer_buttons:
                menu.append([footer_buttons])
            return menu

        def buttons(btns):
            button_list = [KeyboardButton(btn[1]) for btn in btns]
            reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2))
            return reply_markup

        def button(update: Update, context: CallbackContext):
            for disp, dispatch in dispatchers.items():
                        if dispatch == context.dispatcher:
                            d = disp
                            break;
            com = list(Bot_Commands.objects.filter(bot__id = d, cmd_name=update.message.text[1:]).values_list("bot", "cmd_name", 
                                            "cmd_text", "cmd_file","cmd_foto", "id"))
            btns = list(Bot_Buttons.objects.filter(parent_cmd__bot__id = d).values_list("id","btn_name","btn_text","btn_file","btn_foto","parent_cmd"))
            for btn in btns:
                if update.message.text == btn[1]:
                    try:
                        new_btns = list(Bot_Buttons.objects.filter(parent_btn__id = btn[0]).values_list("id","btn_name","btn_text","btn_file","btn_foto","parent_cmd"))
                        reply = buttons(new_btns)
                        btn_text = btn[2]
                        btn_pic = "media/"+btn[4]
                        btn_file = "media/"+btn[3]
                        Send(update, context, new_btns, reply, btn_text, btn_pic, btn_file)
                    except Exception as ex:
                        new_btns = []
                else: 
                    und_btns = list(Bot_Buttons.objects.filter(parent_btn__id = btn[0]).values_list("id","btn_name","btn_text","btn_file","btn_foto","parent_cmd"))
                    und_buttons(update,context,und_btns)




#ЦИКЛ КОММАНДЫ 
        for disp, dispatcher in dispatchers.items(): 
            #print(dir(dispatcher))
            commands_list = list(Bot_Commands.objects.filter(bot__id = disp).values_list("bot", "cmd_name", 
                                            "cmd_text", "cmd_file", "cmd_foto")) 
            for cmd in commands_list: 
                mes = cmd[2] 
                #MESSAGE
                def message(update, context):
                    name = update.message.chat.first_name
                    for disp, dispatch in dispatchers.items():
                        if dispatch == context.dispatcher:
                            d = disp
                            break;

                    try:
                        user = Tg_Users.objects.get(user_id = update.message.chat.id)
                    except:
                        new_bot = Telegram_bot.objects.get(id=d)
                        new_user = Tg_Users(parent_bot=new_bot,user_id=update.message.chat.id,user_first_name=update.message.chat.first_name,
                                user_last_name=update.message.chat.last_name,username=update.message.chat.username)
                        print(new_user)
                        new_user.save()
                        delt = {}
                        auto_mes = list(Automatization.objects.filter(parent_bot__id=disp).values_list('parent_bot','auto_name','auto_text','auto_file','auto_foto','delta','auto_time','id'))
                        for au in auto_mes:  #АВТОВОРОНКА
                            if au[6] == "минут":
                                delt[au[7]] = timedelta(seconds=int(au[5]))
                            elif au[6] == "часов":
                                delt[au[7]] = timedelta(hours=int(au[5]))
                            elif au[6] == "дней":
                                delt[au[7]] = timedelta(days=int(au[5]))
                            elif au[6] == "недель": 
                                delt[au[7]] = timedelta(weeks=int(au[5]))   
                            print(au[6])
                            print(au[5])
                            def call_auto(context): 
                                print(context.job.context)
                                print(dir(context.user_data))
                                context.bot.send_message(context.job.context[0],text = context.job.context[1])
                                auto_pic = "media/"+ context.job.context[3]
                                auto_file = "media/"+ context.job.context[2]
                                if auto_pic != "media/":                     
                                    inp = InputFile(open(auto_pic, 'rb'))
                                    context.bot.send_photo(chat_id=context.job.context[0], photo=inp)
                                if auto_file != "media/":
                                    inp = InputFile(open(auto_file, 'rb'))
                                    context.bot.send_document(chat_id=context.job.context[0], document=inp)
                            jq[disp].run_once(call_auto,delt[au[7]],context=[update.message.chat_id,au[2],au[3],au[4]])
                            #КОНЕЦ АВТОВОРОНКА
                    com = list(Bot_Commands.objects.filter(bot__id = d, cmd_name=update.message.text[1:]).values_list("bot", "cmd_name", 
                                            "cmd_text", "cmd_file","cmd_foto", "id"))                      
                    btns = []
                    try:
                        #
                        btns = list(Bot_Buttons.objects.filter(parent_cmd__id = com[0][5]).values_list("id","btn_name","btn_text","btn_file","btn_foto","parent_cmd"))
                        reply = buttons(btns)
                    except:
                        btns = []
                    com_text = com[0][2]
                    com_pic = "media/"+com[0][4]
                    com_file = "media/"+com[0][3]
                    print(com_pic)
                    com_text = com_text.replace("{name}",name)
                    Send(update, context, btns, reply, com_text, com_pic, com_file)

                s_handlers[str(cmd[0])+"_"+str(cmd[1])] = CommandHandler(cmd[1], message)
                dispatcher.add_handler(s_handlers[str(cmd[0])+"_"+str(cmd[1])])

            delt = {}
            delt_time = {}
            auto_mes = list(Automatization.objects.filter(parent_bot__id=disp).values_list('parent_bot','auto_name','auto_text','auto_file','auto_foto','delta','auto_time','id','auto_number'))
            for au in auto_mes:  #АВТОВОРОНКА
                if au[6] == "минут":
                    delt[au[7]] = timedelta(seconds=int(au[5]),)
                elif au[6] == "часов":
                    delt[au[7]] = timedelta(hours=int(au[5]))
                elif au[6] == "дней":
                    delt[au[7]] = timedelta(days=int(au[5]))
                elif au[6] == "недель": 
                    delt[au[7]] = timedelta(weeks=int(au[5])) 
                all_users = list(Tg_Users.objects.filter(parent_bot = disp).values("user_id","create_date"))
                print("ALL:------ ",all_users)
                for u in all_users:
                    if au[8] == 1:
                        last_time = u["create_date"]
                        print(last_time.tzinfo)
                        print("last_time: ",last_time)
                        delt_time[f'{au[0]}_{au[8]}']=last_time+delt[au[7]]
                    else:
                        #am = Automatization.objects.get(auto_number=au[8]-1) #Сюда True/False
                        last_time = delt_time[f'{au[0]}_{au[8]-1}']
                        print(last_time.tzinfo)
                        print("last_time: ",last_time)
                        delt_time[f'{au[0]}_{au[8]}']=last_time+delt[au[7]]
                    def call_auto(context): 
                        print(context.job.context)
                        print(dir(context.user_data))
                        context.bot.send_message(context.job.context[0],text = context.job.context[1])
                        auto_pic = "media/"+ context.job.context[3]
                        auto_file = "media/"+ context.job.context[2]
                        if auto_pic != "media/":                     
                            inp = InputFile(open(auto_pic, 'rb'))
                            context.bot.send_photo(chat_id=context.job.context[0], photo=inp)
                        if auto_file != "media/":
                            inp = InputFile(open(auto_file, 'rb'))
                            context.bot.send_document(chat_id=context.job.context[0], document=inp)
                    delt_time[f'{au[0]}_{au[8]}'] = delt_time[f'{au[0]}_{au[8]}'].replace(tzinfo=None)
                    #delt_time[f'{au[7]}_{au[8]}'] = delt_time[f'{au[7]}_{au[8]}'].astimezone(pytz.utc) 
                    time = pytz.timezone('Europe/Moscow').localize(delt_time[f'{au[0]}_{au[8]}'])
                    print("СЛОВАРЬ: ",delt_time)
                    jq[disp].run_once(call_auto,time,context=[u["user_id"],au[2],au[3],au[4]])

                #КОНЕЦ АВТОВОРОНКА 

            btns = list(Bot_Buttons.objects.values_list("id","btn_name","btn_text","btn_file","btn_foto","parent_cmd","parent_cmd__bot__id"))
            for btn in btns:
                btn_handlers[str(btn[5])+"_"+str(btn[1])] = MessageHandler(Filters.all,button)
                dispatcher.add_handler(btn_handlers[str(btn[5])+"_"+str(btn[1])])
            
            def hands_send(update, context):
                for disp, dispatch in dispatchers.items():
                        if dispatch == context.dispatcher:
                            d = disp
                            break;
            
                hands = list(Hand_sending.objects.filter(parent_bot = disp, otpravleno="").values_list("parent_bot", "hand_name", 
                                                "hand_text", "hand_file","hand_foto","id"))
                all_users = list(Tg_Users.objects.filter(parent_bot = disp).values("user_id"))   
                print(all_users)            
                if len(hands) > 0:
                    for h in hands:
                        for u in all_users:
                            bot = telegram.Bot(token=bots_dict[disp])
                            bot.send_message(chat_id=u["user_id"],text=h[2])
                            hand_pic = "media/"+ h[4]
                            hand_file = "media/"+ h[3]
                            if hand_pic != "media/":                     
                                inp = InputFile(open(hand_pic, 'rb'))
                                bot.send_photo(chat_id=u["user_id"], photo=inp)
                            if hand_file != "media/":
                                inp = InputFile(open(hand_file, 'rb'))
                                bot.send_document(chat_id=u["user_id"], document=inp)
                            hand = Hand_sending.objects.get(id=h[5])
                            hand.otpravleno = "отправлено"
                            hand.save()
                            print(h)
            hand_handler = CommandHandler("send", hands_send)
            dispatcher.add_handler(hand_handler)
        

        for updater in updaters:
            updater.start_polling()
        for updater in updaters:
            updater.idle()
        



# {'update_id': 233001592, 
# 'message': {'supergroup_chat_created': False,
#             'chat': {'first_name': 'Александра', 'type': 'private', 'last_name': 'Kaktus', 'username': 'santakaktus', 'id': 1161145491},
#             'date': 1655569390, 'group_chat_created': False,
#             'entities': [{'type': 'bot_command', 'length': 5, 'offset': 0}], 
#             'text': '/help', 'new_chat_photo': [], 'delete_chat_photo': False, 'channel_chat_created': False, 'new_chat_members': [], 'caption_entities': [], 'message_id': 305, 'photo': [], 'from': {'first_name': 'Александра', 'username': 'santakaktus', 'last_name': 'Kaktus', 'id': 1161145491, 'is_bot': False, 'language_code': 'ru'}}}