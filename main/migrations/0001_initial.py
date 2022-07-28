# Generated by Django 4.0.4 on 2022-07-11 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Telegram_bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_name', models.CharField(max_length=100, verbose_name='Название бота')),
                ('bot_token', models.CharField(max_length=100, verbose_name='Токен бота')),
                ('bot_link', models.URLField(blank=True, max_length=30, verbose_name='Ссылка на бота')),
            ],
            options={
                'verbose_name': 'Бот',
                'verbose_name_plural': 'Все Боты',
            },
        ),
        migrations.CreateModel(
            name='Tg_Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=10, verbose_name='ID пользователя')),
                ('user_first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя пользователя')),
                ('user_last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Фамилия пользователя')),
                ('username', models.CharField(max_length=100, verbose_name='Username')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('parent_bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.telegram_bot', verbose_name='Бот')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Все Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Hand_sending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hand_name', models.CharField(max_length=500, verbose_name='Название')),
                ('hand_text', models.TextField(max_length=500, verbose_name='Текст сообщения')),
                ('hand_file', models.FileField(blank=True, null=True, upload_to='files/', verbose_name='Прикрепить файл')),
                ('hand_foto', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Прикрепить фото')),
                ('otpravleno', models.CharField(max_length=500, verbose_name='Статус')),
                ('parent_bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.telegram_bot', verbose_name='Бот')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Ручная рассылка',
            },
        ),
        migrations.CreateModel(
            name='Bot_Commands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cmd_name', models.CharField(max_length=500, verbose_name='Название команды')),
                ('cmd_text', models.TextField(blank=True, max_length=500, null=True, verbose_name='Текст сообщения')),
                ('cmd_file', models.FileField(blank=True, null=True, upload_to='files/', verbose_name='Прикрепить файл')),
                ('cmd_foto', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Прикрепить фото')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.telegram_bot', verbose_name='Бот')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
            },
        ),
        migrations.CreateModel(
            name='Bot_Buttons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('btn_name', models.CharField(max_length=500, verbose_name='Название кнопки')),
                ('btn_text', models.TextField(blank=True, max_length=500, verbose_name='Текст сообщения')),
                ('btn_file', models.FileField(blank=True, null=True, upload_to='files/', verbose_name='Прикрепить файл')),
                ('btn_foto', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Прикрепить фото')),
                ('btn_link', models.URLField(blank=True, max_length=30, verbose_name='Добавить ссылку')),
                ('parent_btn', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.bot_buttons', verbose_name='Кнопка')),
                ('parent_cmd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.bot_commands', verbose_name='Кнопка')),
            ],
            options={
                'verbose_name': 'Кнопка',
                'verbose_name_plural': 'Кнопки',
            },
        ),
        migrations.CreateModel(
            name='Automatization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_name', models.CharField(max_length=500, verbose_name='Название')),
                ('auto_text', models.TextField(max_length=500, verbose_name='Текст сообщения')),
                ('auto_file', models.FileField(blank=True, null=True, upload_to='files/', verbose_name='Прикрепить файл')),
                ('auto_foto', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Прикрепить фото')),
                ('delta', models.PositiveIntegerField(verbose_name='После подписки отослать через ')),
                ('auto_time', models.CharField(choices=[('минут', 'минут'), ('часов', 'часов'), ('дней', 'дней'), ('недель', 'недель')], max_length=10, verbose_name='')),
                ('parent_bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.telegram_bot', verbose_name='Бот')),
            ],
            options={
                'verbose_name': 'Автоворонка',
                'verbose_name_plural': 'Автоворонки',
            },
        ),
    ]
