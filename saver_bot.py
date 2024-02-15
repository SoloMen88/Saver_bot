"""
Бот предназначен для сохранения пересланных сообщений на диск.
Поддерживается сохранение фото как в виде документа, так и в пережатом
качестве, видео, любых других типов вайлов, так же может сохранять текст
в отдельные файлы.
Поддерживает разделение папок по пользователям.
Есть возможность изменять основные настройки по команде /start.

Настройки в файле settings.ini:
        DEL_MSG - удалять принятое сообщение после его сохранения
        DIFFERENT_DIR - сохранять принятые данные в одной папке с разделением
        по пользователям: set_dir-/-user1-/-photo
                                  /       /-txt etc..
                                  /-user2-/-photo
                                          /-txt etc..
        либо можно каждому пользователю задать свой путь.
        WORK_DIR - папка куда сохранять данные если DIFFERENT_DIR == False
        TOKEN - токен от бота
        LOG_LEVEL - уровень логирования

Версия 1.0
Автор @SoloMen88
"""
import configparser
import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

config = configparser.ConfigParser()
if os.path.isfile('settings.ini'):
    config.read('settings.ini', encoding="utf-8")
else:
    config['BASE'] = {
        'DEL_MSG': 'True',
        'DIFFERENT_DIR': 'No',
        'WORK_DIR': '/patch/to/save/for/all/',
        'TOKEN': 'you_bot_token',
        'LOG_LEVEL': 'WARNING'
    }
    config['USERS'] = {
        'user1': 'fist + last name user1',
        'user2': 'fist + last name user2 and other user etc...'
    }
    config['USERS_URL'] = {
        'user1_url': '/patch/to/save/for/user1/',
        'user2_url': '/patch/to/save/for/user2/etc...'
    }
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

DEL_MSG = config.getboolean('BASE', 'DEL_MSG')
DIFFERENT_DIR = config.getboolean('BASE', 'DIFFERENT_DIR')
WORK_DIR = config.get('BASE', 'WORK_DIR')
LOG_LEVEL = config.get('BASE', 'LOG_LEVEL')
TOKEN = config.get('BASE', 'TOKEN')

PHOTO_EXTENSION = ['jpg', 'png', 'gif', 'bmp']

log_level_info = {'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  }
log_level_from_config = config['BASE']['LOG_LEVEL']
log_level = log_level_info.get(log_level_from_config, logging.ERROR)

logging.basicConfig(
    format='%(asctime)s: %(levelname)s: %(funcName)s:%(lineno)s - %(message)s',
    filename='log.log',
    filemode='a',
    level=log_level,
    encoding="UTF-8")


def delete_msg(update, context, msg):
    """Удаляет последнее сообщение и отправляет текст"""
    if DEL_MSG is True:
        try:
            context.bot.delete_message(message_id=update.message.message_id,
                                       chat_id=update.message.chat_id)
            logging.info('Соощбщение удалено')
        except Exception:
            logging.exception('Не удалось удалить сообщение')
    update.message.reply_text(msg)
    logging.info(f'Соощбщение "{msg}" отправтено')


def save_txt(dir, text, file_name):
    """Сохраняет текст в файл с полученным именем по указанному пути"""
    if not os.path.isdir(dir + '/txt'):
        os.mkdir(dir + '/txt')
        logging.info('Папки txt небыло, пришлось создать')
    dir += '/txt'
    try:
        with open(f'{dir}/{file_name}.txt', 'w', encoding='utf-8') as file:
            file.write(f'{text}\n')
        logging.info(f'Текст {file_name} сохранен')
    except Exception:
        logging.exception('Не удалось записать файл, он кем-то открыт')


def get_data(update, context):
    """Определяет тип сообщения и в зависимости от типа сохраняет
    данные на диск"""
    user = update.message.chat.full_name
    dir = WORK_DIR
    if DIFFERENT_DIR:
        for user_ in config['USERS']:
            if config['USERS'][user_] == user:
                # dir = 'Z:/мое/telegram'
                dir = config['USERS_URL'][f'{user_}_url']
    elif not os.path.isdir(dir + '/' + user):
        os.mkdir(dir + '/' + user)
        dir = dir + '/' + user
    else:
        dir = dir + '/' + user
    if update._effective_message.document:
        files = update._effective_message.document.file_id
        file_name = update._effective_message.document.file_name
        dir_name = file_name.split('.')[-1]
        if dir_name in PHOTO_EXTENSION:
            dir_name = 'photo'
        logging.info(f'Прислан документ {file_name}')
    elif update._effective_message.photo:
        files = update._effective_message.photo[-1].file_id
        file_name = f'{update._effective_message.photo[-1].file_unique_id}.jpg'
        dir_name = 'photo'
        logging.info(f'Прислано фото {file_name}')
    elif update._effective_message.text:
        if update._effective_message.forward_from_chat:
            file_name = f'''Переслано от {
                update._effective_message.forward_from_chat.title}. {
                    update._effective_message.text[0:20]}'''
        else:
            file_name = update._effective_message.text[0:25]
        text = update._effective_message.text_markdown
        logging.info(f'Прислан текст {file_name}')
        save_txt(dir, text, file_name)
        delete_msg(update, context, msg='Текст сохранен.')
        return
    elif update._effective_message.video:
        size = update._effective_message.video.file_size
        if size >= 20000000:
            delete_msg(update, context,
                       msg='Видео больше 20 Мб, бот такое не скачает...((')
            logging.warning(f'''Видео больше 20 Мб не поддерживаются ботаим,
                            размер этого видео = {size}''')
            return
        files = update._effective_message.video.file_id
        file_name = f'{update._effective_message.video.file_unique_id}.mp4'
        dir_name = 'video'
        logging.info(f'Прислано видео {file_name}')
    else:
        delete_msg(update, context, msg='Не шли больше мне такое!')
        logging.info('Неподдерживаемый тип сообщения.')
        return
    path_dir = os.path.join(dir, dir_name)
    path_file = os.path.join(path_dir, file_name)
    if os.path.isfile(path_file):
        msg = f'Хмм.."{file_name}"..уже есть такой...'
        delete_msg(update, context, msg)
        logging.info('Повтор')
        return
    if not os.path.isdir(path_dir):
        os.mkdir(path_dir)
        logging.info(f'Папки {dir_name} небыло, пришлось создать')
    file = context.bot.getFile(files)
    try:
        file.download(custom_path=path_file)
        logging.info(f'Файл {file_name} получен')
    except Exception:
        logging.warning(f'Не удалось получить файл {file_name}')
    delete_msg(update, context,
               msg=f'{file_name} загружен в папку {dir_name}')
    logging.info(f'Файл {file_name} сохранен в папке {dir_name}')


def start(update, context):
    """Запускает диалог настроек"""
    if DEL_MSG:
        del_msg = '[x]'
    else:
        del_msg = '[_]'
    if DIFFERENT_DIR:
        dif_dir = '[x]'
    else:
        dif_dir = '[_]'
    keyboard = [
        [InlineKeyboardButton(
            f'{del_msg} Удаление сообщений.', callback_data='del_msg')],
        [InlineKeyboardButton(
            f'{dif_dir} Раздельные папки для пользователей.',
            callback_data='dif_dir')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        update.message.reply_text('Что настраиваем:',
                                  reply_markup=reply_markup)
        logging.info('Открыты настройки')
    except Exception:
        logging.exception('Не удалось отправть сообщение')


def settings_chg(update, context):
    """Изменяет настройки"""
    global DEL_MSG
    global DIFFERENT_DIR
    query = update.callback_query
    variant = query.data
    query.answer()
    if variant == 'del_msg':
        DEL_MSG = not DEL_MSG
        config.set('BASE', 'DEL_MSG', str(DEL_MSG))
        logging.info(f'Изменен параметр DEL_MSG на {DEL_MSG}')
    elif variant == 'dif_dir':
        DIFFERENT_DIR = not DIFFERENT_DIR
        config.set('BASE', 'DIFFERENT_DIR', str(DIFFERENT_DIR))
        logging.info(f'Изменен параметр DIFFERENT_DIR на {DIFFERENT_DIR}')
    with open('settings.ini', 'w', encoding="utf-8") as config_file:
        config.write(config_file)
        logging.info('Настройки записаны')
    if DEL_MSG:
        del_msg = '[x]'
    else:
        del_msg = '[_]'
    if DIFFERENT_DIR:
        dif_dir = '[x]'
    else:
        dif_dir = '[_]'
    keyboard = [
        [InlineKeyboardButton(
            f'{del_msg} Удаление сообщений.', callback_data='del_msg')],
        [InlineKeyboardButton(
            f'{dif_dir} Раздельные папки для пользователей.',
            callback_data='dif_dir')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        query.edit_message_text('Что настраиваем:', reply_markup=reply_markup)
    except Exception:
        logging.exception('Не удалось отредактировать сообщение настроек')


def main():
    try:
        updater = Updater(token=TOKEN)
    except Exception as error:
        logging.error(f'Токен не верный, работа невозможна {error}')
        raise
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, get_data))
    updater.dispatcher.add_handler(CallbackQueryHandler(settings_chg))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
