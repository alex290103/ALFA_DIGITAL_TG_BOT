from django.db import models
from django.forms import CheckboxInput

class Telegram_bot(models.Model):
    bot_name = models.CharField(max_length=100, verbose_name="Название бота")
    bot_token = models.CharField(max_length=100, verbose_name="Токен бота")
    bot_link = models.URLField(max_length=30, verbose_name="Ссылка на бота", blank=True)

    def __str__(self):
        return f'{self.bot_name} {self.bot_token}'


    class Meta:
        verbose_name = "Бот"
        verbose_name_plural = "Все Боты"




class Bot_Commands(models.Model):
    bot = models.ForeignKey("Telegram_bot", verbose_name="Бот", on_delete=models.CASCADE)
    #text
    cmd_name = models.CharField(max_length=500,verbose_name="Название команды",)
    cmd_text = models.TextField(max_length=500,verbose_name="Текст сообщения",blank=True, null=True)
    #file
    cmd_file = models.FileField(blank=True, null=True, upload_to="files/",verbose_name="Прикрепить файл")
    #foto
    cmd_foto = models.ImageField(blank=True, null=True,upload_to="images/",verbose_name="Прикрепить фото")
    #link na redact knopok
    # cmd_link = models.URLField(max_length=30, verbose_name="", blank=True)

    def __str__(self):
        return f'{self.cmd_name}'


    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"


class Bot_Buttons(models.Model):
    parent_cmd = models.ForeignKey("Bot_Commands", verbose_name="Кнопка", on_delete=models.CASCADE, blank=True, null=True)
    parent_btn = models.ForeignKey("Bot_Buttons", verbose_name="Кнопка", on_delete=models.CASCADE, blank=True, null=True)
    #text
    btn_name = models.CharField(max_length=500,verbose_name="Название кнопки")
    btn_text = models.TextField(max_length=500,verbose_name="Текст сообщения", blank=True)
    #file
    btn_file = models.FileField(blank=True, null=True, upload_to="files/",verbose_name="Прикрепить файл")
    #foto
    btn_foto = models.ImageField(blank=True, null=True,upload_to="images/",verbose_name="Прикрепить фото")
    #link na redact knopok
    btn_link = models.URLField(max_length=30, verbose_name="Добавить ссылку", blank=True)

    def __str__(self):
        return f'{self.btn_name}'


    class Meta:
        verbose_name = "Кнопка"
        verbose_name_plural = "Кнопки"

class Tg_Users(models.Model):
    parent_bot = models.ForeignKey("Telegram_bot", verbose_name="Бот", on_delete=models.CASCADE)   
    user_id = models.CharField(max_length=10, verbose_name="ID пользователя")
    user_first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Имя пользователя")
    user_last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Фамилия пользователя")
    username = models.CharField(max_length=100, verbose_name="Username")
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id} {self.username}'


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Все Пользователи"


class Automatization(models.Model):
    TIME = (
        ('минут', 'минут'),
        ('часов', 'часов'),
        ('дней', 'дней'),
        ('недель', 'недель'),
    )
    parent_bot = models.ForeignKey("Telegram_bot", verbose_name="Бот", on_delete=models.CASCADE)   
    auto_name = models.CharField(max_length=500,verbose_name="Название")
    auto_number = models.IntegerField(verbose_name="Номер")
    auto_text = models.TextField(max_length=500,verbose_name="Текст сообщения")
    #file
    auto_file = models.FileField(blank=True, null=True, upload_to="files/",verbose_name="Прикрепить файл")
    #foto
    auto_foto = models.ImageField(blank=True, null=True,upload_to="images/",verbose_name="Прикрепить фото")
    #link na redact knopok
    delta = models.PositiveIntegerField(verbose_name="После предыдущего сообщения отослать через ")
    auto_time = models.CharField(max_length=10, choices=TIME, verbose_name="")
    
    def __str__(self):
        return f'{self.auto_number} {self.auto_name}'


    class Meta:
        verbose_name = "Автоворонка"
        verbose_name_plural = "Автоворонки"

class Hand_sending(models.Model):
    parent_bot = models.ForeignKey("Telegram_bot", verbose_name="Бот", on_delete=models.CASCADE)   
    hand_name = models.CharField(max_length=500,verbose_name="Название")
    hand_text = models.TextField(max_length=500,verbose_name="Текст сообщения")
    hand_file = models.FileField(blank=True, null=True, upload_to="files/",verbose_name="Прикрепить файл")
    hand_foto = models.ImageField(blank=True, null=True,upload_to="images/",verbose_name="Прикрепить фото")
    otpravleno = models.CharField(max_length=500,verbose_name="Статус")

    def __str__(self):
        return f'{self.hand_name}'


    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Ручная рассылка"




