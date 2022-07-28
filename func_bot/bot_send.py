from telegram import InputFile, KeyboardButton, ReplyKeyboardMarkup
from main.models import Bot_Buttons

def build_menu(buttons, n_cols,
                    header_buttons=None,
                    footer_buttons=None):
            menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
            print(menu)
            #pdb.set_trace()
            if header_buttons:
                menu.insert(0, [header_buttons])
            if footer_buttons:
                menu.append([footer_buttons])
            return menu

def buttons(btns):
    button_list = [KeyboardButton(btn[1]) for btn in btns]
    #print(button_list[0].text)
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2))
    print(reply_markup)
    return reply_markup

def Send(update, context, btns, reply, com_text, com_pic, com_file,):
    if btns != []:
            context.bot.send_message(chat_id=update.effective_chat.id, 
                        text=com_text, reply_markup=reply)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=com_text)
    if com_pic != "media/":                     
        inp = InputFile(open(com_pic, 'rb'))
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=inp)
    if com_file != "media/":
        inp = InputFile(open(com_file, 'rb'))
        context.bot.send_document(chat_id=update.effective_chat.id, document=inp)

def und_buttons(update,context,und_btns):
    for u_btn in und_btns:
        if update.message.text == u_btn[1]:
            try:
                new_btns = list(Bot_Buttons.objects.filter(parent_btn__id = u_btn[0]).values_list("id","btn_name","btn_text","btn_file","btn_foto","parent_cmd"))
                reply = buttons(new_btns)
                btn_text = u_btn[2]
                btn_pic = "media/"+u_btn[4]
                btn_file = "media/"+u_btn[3]
                Send(update, context, new_btns, reply, btn_text, btn_pic, btn_file)
            except Exception as ex:
                new_btns = []
        else:
            und_btns = list(Bot_Buttons.objects.filter(parent_btn__id = u_btn[0]).values_list("id","btn_name","btn_text","btn_file","btn_foto","parent_cmd"))
            und_buttons(update,context,und_btns)