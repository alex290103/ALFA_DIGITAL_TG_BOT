import telebot
import pdb
from main.models import Bot_Commands


def bot_commands(bots):
    commands_list = list(Bot_Commands.objects.values_list("bot", "cmd_name", "cmd_text", "cmd_file", "cmd_foto"))
    print(commands_list)
    for key,value in bots.items():
        commands_list = list(Bot_Commands.objects.filter(bot__id = key).values_list("bot", "cmd_name", "cmd_text", "cmd_file", "cmd_foto"))
        print(commands_list)
        for comm in commands_list:
            print(comm[1])
            print(bots[key])
            @bots[key].message_handler(content_types='text')
            def command_message(message):
                # user_markup = telebot.types.ReplyKeyboardMarkup()
                # user_markup.row('comm[2]')
                for comm in commands_list:  
                    if message.text == comm[1]:
                        bots[key].send_message(message.chat.id, comm[2])
            print('Нужна помощь')
            # @bots[key].message_handler(commands=["help"])
            # def command_message(message):
            #     user_markup = telebot.types.ReplyKeyboardMarkup()
            #     user_markup.row('start')              
            #     bots[key].send_message(message.chat.id, 'Нужна помощь')
    #for key,value in bots.items():
            bots[key].polling()
            bots[key].stop_polling()
    # for b in commands_list:
    #     bot[b[0]] = telebot.TeleBot(b[1])
    # print(bot)
            