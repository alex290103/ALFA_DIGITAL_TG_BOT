from django.contrib import admin

# Register your m
from main.models import Telegram_bot,Bot_Commands, Bot_Buttons, Tg_Users, Automatization, Hand_sending

admin.site.register(Tg_Users)

class AutoAdmin(admin.ModelAdmin):
    fields=('parent_bot','auto_name','auto_text','auto_file','auto_foto',('delta','auto_time'),)
    class Meta:
        model = Automatization



class Hand_Admin(admin.ModelAdmin):
    readonly_fields = ('otpravleno',)
    class Meta:
        model = Hand_sending

admin.site.register(Hand_sending, Hand_Admin)


class AutoTabularInline(admin.StackedInline):
    model = Automatization
    classes = ['collapse']
    extra = 0
    show_change_link = True

class CommandsTabularInline(admin.StackedInline):
    model = Bot_Commands
    classes = ['collapse']
    extra = 0
    show_change_link = True

class Btn_BtnTabularInline(admin.StackedInline):
    model = Bot_Buttons
    classes = ['collapse']
    extra = 0
    show_change_link = True
    exclude = ("parent_cmd",)
    

class Btn_CmdTabularInline(admin.StackedInline):
    model = Bot_Buttons
    classes = ['collapse']
    extra = 0
    show_change_link = True
    exclude = ("parent_btn",)
    

class BtnAdmin(admin.ModelAdmin):
    inlines = [Btn_BtnTabularInline]
    class Meta:
        model = Bot_Buttons

class CmdAdmin(admin.ModelAdmin):
    inlines = [Btn_CmdTabularInline]
    class Meta:
        model = Bot_Commands

class TgAdmin(admin.ModelAdmin):
    inlines = [CommandsTabularInline, AutoTabularInline]
    class Meta:
        model = Telegram_bot

admin.site.register(Telegram_bot, TgAdmin)
admin.site.register(Bot_Commands, CmdAdmin)
admin.site.register(Bot_Buttons, BtnAdmin)
admin.site.register(Automatization,AutoAdmin)
