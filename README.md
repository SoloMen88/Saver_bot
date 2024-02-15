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

[![Telegram-bot](https://img.shields.io/badge/-Telegram-bot-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://core.telegram.org/bots/)
[![Telegram-bot-API](https://img.shields.io/badge/-Telegram-bot-API-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://core.telegram.org/bots/api/)
[![Logging](https://img.shields.io/badge/-Logging-464646?style=flat&color=008080)](https://docs.python.org/3/library/logging.html/)


## Запуск приложения
1. Переименовать файл settings — exemple.ini в settings.ini
2. Указать настройки в файле settings.ini:
        DEL_MSG - удалять принятое сообщение после его сохранения
        DIFFERENT_DIR - сохранять принятые данные в одной папке с разделением
        по пользователям: set_dir-/-user1-/-photo
                                  /       /-txt etc..
                                  /-user2-/-photo
                                          /-txt etc..
        set_dir должен уже существовать!
        либо можно каждому пользователю задать свой путь в разделах USERS и USERS_URL.
        WORK_DIR - папка куда сохранять данные если DIFFERENT_DIR == False
        TOKEN - токен от бота
        LOG_LEVEL - уровень логирования
3. Создать виртуальное окружение: python -m venv venv
4. Запустить виртуальное окружение:source venv/Scripts/activate
5. Установить зависимости: pip install -r requirements.txt
6. Запустить файл saver_bot.py


## Создание бота
```
Начните диалог с ботом @BotFather: нажмите кнопку Start («Запустить»). Затем отправьте команду /newbot и укажите параметры нового бота:
имя (на любом языке), под которым ваш бот будет отображаться в списке контактов;
техническое имя вашего бота, по которому его можно будет найти в Telegram. Имя должно оканчиваться на слово bot в любом регистре, например Saver_bot, SaverBOT. Имена ботов должны быть уникальны.
@BotFather поздравит вас и отправит в чат токен для работы с Bot API. Токен выглядит примерно так: 123456:ABC-FFGgfgG3-fghfgfh4564gdfj46.
```

## Версия 
1.0

## Автор
Станислав Кучеренко @SoloMen88