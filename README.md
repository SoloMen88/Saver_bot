# Saver_bot
Telegram бот который умеет сохранять сообщения на диск.

## Описание 

Бот предназначен для сохранения пересланных сообщений на диск.
Поддерживается сохранение фото как в виде документа, так и в пережатом
качестве, видео, любых других типов вайлов, так же может сохранять текст
в отдельные файлы.
Поддерживает разделение папок по пользователям.
Есть возможность изменять основные настройки по команде /start.

## Технологический стек

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
![Static Badge](https://img.shields.io/badge/Telegram-bot-API?style=flat&logo=Telegram-bot-API&logoColor=56C0C0&color=008080&link=https%3A%2F%2Fcore.telegram.org%2Fbots%2FAPI)
[![Logging](https://img.shields.io/badge/-Logging-464646?style=flat&color=008080)](https://docs.python.org/3/library/logging.html/)


## Запуск приложения
1. Переименовать файл settings — exemple.ini в settings.ini
2. Указать настройки в файле settings.ini:
   
         DEL_MSG - удалять принятое сообщение после его сохранения
         WORK_DIR - папка куда сохранять данные если DIFFERENT_DIR == False, либо можно каждому пользователю задать свой путь в разделах USERS и USERS_URL.
         DIFFERENT_DIR - сохранять принятые данные в одной папке с разделением по пользователям:

               WORK_DIR-|-user1-|-photo
                        |       |-txt etc..
                        |
                        |-user2-|-photo
                                |-txt etc..
           
           WORK_DIR должен уже существовать!
           TOKEN - токен от бота
           LOG_LEVEL - уровень логирования.
   
4. Создать виртуальное окружение: python -m venv venv
5. Запустить виртуальное окружение:source venv/Scripts/activate
6. Установить зависимости: pip install -r requirements.txt
7. Запустить файл saver_bot.py


## Создание бота
Начните диалог с ботом @BotFather: нажмите кнопку Start («Запустить»). Затем отправьте команду /newbot и укажите параметры нового бота:
   
имя (на любом языке), под которым ваш бот будет отображаться в списке контактов;

техническое имя вашего бота, по которому его можно будет найти в Telegram. 

Имя должно оканчиваться на слово bot в любом регистре, например Saver_bot, SaverBOT. Имена ботов должны быть уникальны.

@BotFather поздравит вас и отправит в чат токен для работы с Bot API. Токен выглядит примерно так: 123456:ABC-FFGgfgG3-fghfgfh4564gdfj46.


## Версия 
1.0

## Автор
Станислав Кучеренко @SoloMen88
