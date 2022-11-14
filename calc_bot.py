import logging
from config import TOKEN
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOICE, RATIONAL_ONE, RATIONAL_TWO, OPERATIONS_RATIONAL, OPERATIONS_COMPLEX, COMPLEX_ONE, COMPLEX_TWO = range(7)

def start(update, _):
    reply_keyboard = [['Рациональные числа', 'Комплексные числа', 'Выход']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        'Добро пожаловать в калькулятор! Выберите, с какими числами будем работать:', reply_markup=markup_key)
    return CHOICE

def choice(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s: выбор операции: %s", user.first_name, update.message.text)
    user_choice = update.message.text
    if user_choice == 'Рациональные числа':
        update.message.reply_text(
            'Введите первое рациональное число')
        return RATIONAL_ONE
    if user_choice == 'Комплексные числа':
        context. bot.send_message(
            update.effective_chat.id, 'Введите Re и Im первого числа через ПРОБЕЛ:')
        return COMPLEX_ONE
    if user_choice == 'Выход':
        return cancel(update, context)

def rational_one(update, context):
    user = update.message.from_user
    logger. info("Пользователь %s: ввод числа: %s", user.first_name, update.message.text)
    get_rational = update.message.text
    if get_rational.isdigit():
        get_rational = float(get_rational)
        context.user_data['rational_one'] = get_rational
        update.message.reply_text(
            'Введите второе рациональное')
        return RATIONAL_TWO
    else:
        update.message.reply_text(
            'Нужно ввести число')

def rational_two(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s: ввод числа: %s", user.first_name, update.message.text)
    get_rational = update.message.text
    if get_rational.isdigit():
        get_rational = float(get_rational)
        context.user_data['rational_two'] = get_rational
        reply_keyboard = [['+', '-', '*', '/']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            'Выберите операцию с числами', reply_markup=markup_key)
        return OPERATIONS_RATIONAL

def operations_rational(update, context):
    user = update.message.from_user
    logger.info(
        "Пользователь %s: выбор операции: %s", user.first_name, update.message.text)
    rational_one = context.user_data.get('rational_one')
    rational_two = context.user_data.get('rational_two')
    user_choice = update.message.text
    if user_choice == '+':
        result = rational_one + rational_two
    if user_choice == "-":
        result = rational_one - rational_two
    if user_choice == '*':
        result = rational_one * rational_two
    if user_choice == '/':
        try:
            result = rational_one / rational_two
        except:
            update.message.reply_text('Деление на ноль запрещено')
    logger.info(f"Бот-Калькулятор: результат операции: {result}")
    update.message.reply_text(
        f'Результат: {rational_one} {user_choice} {rational_two} = {result}')
    return start(update, context)

def complex_one(update, context):
    user = update.message.from_user
    logger.info(
        "Пользователь %s: ввод числа: %s", user.first_name, update.message.text)
    user_choice = update.message.text
    test = user_choice.replace('-', '')
    if ' ' in test and (test.replace(' ', '')).isdigit():
        user_choice = user_choice.split(' ')
        complex_one = complex(int(user_choice[0], int(user_choice[1])))
        context.user_data['complex_one'] = complex_one
        update.message.reply_text(
            f'Первое число {complex_one}, Введите Re и Im второго числа через ПРОБЕЛ: ')
        return COMPLEX_TWO
    else:
        update.message.reply_text('Ошибка! Введите Re и Im первого числа через ПРОБЕЛ')

def complex_two(update, context):
    user = update.message.from_user
    logger.info(
        "Пользователь %s: ввод числа: %s", user.first_name, update.message.text)
    user_choice = update.message.text
    test = user_choice.replace('-', '')
    if ' ' in test and (test.replace(' ', '')).isdigit():
        user_choice = user_choice.split(' ')
        complex_two = complex(int(user_choice[0], int(user_choice[1])))
        context.user_data['complex_two'] = complex_two
        update.message.reply_text(f'Второе число {complex_two}')
        reply_keyboard = [['+', '-', '*', '/']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            'Выберите операцию с числами', reply_markup=markup_key)
        return OPERATIONS_COMPLEX
    else:
        update.message.reply_text('Ошибка! Введите Re и Im второго числа через ПРОБЕЛ')

def operations_complex(update, context):
    user = update.message.from_user
    logger.info(
        "Пользователь %s: выбор операции: %s", user.first_name, update.message.text)
    complex_one = context.user_data.get('complex_one')
    complex_two = context.user_data.get('complex_two')
    user_choice = update.message.text
    if user_choice == '+':
        result = complex_one + complex_two
    if user_choice == '-':
        result = complex_one - complex_two
    if user_choice == '*':
        result = complex_one * complex_two
    if user_choice == '/':
        try:
            result = complex_one * complex_two
        except:
            update.message.reply_text('Деление на ноль запрещено')
    logger.info(f"Бот-Калькулятор: результат операции: {result}")
    update.message.reply_text(
        f'Результат: {complex_one} {user_choice} {complex_two} = {result}')
    return start(update, context)

def cancel(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s: завершение сеанса", user.first_name)
    update.message.reply_text(
        'Спасибо! Ждём Вас снова!',
    )
    return ConversationHandler.END

if __name__ == "__main__":
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE: [MessageHandler(Filters.text, choice)],
            RATIONAL_ONE: [MessageHandler(Filters.text, rational_one)],
            RATIONAL_TWO: [MessageHandler(Filters.text, rational_two)],
            OPERATIONS_RATIONAL: [MessageHandler(Filters.text, operations_rational)],
            OPERATIONS_COMPLEX: [MessageHandler(Filters.text, operations_complex)],
            COMPLEX_ONE: [MessageHandler(Filters.text, complex_one)],
            COMPLEX_TWO: [MessageHandler(Filters.text, complex_two)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()