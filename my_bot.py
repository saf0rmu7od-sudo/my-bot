import telebot
import os
from telebot import types
from dotenv import load_dotenv # Импортируем защитник

# Эта команда находит твой файл .env и загружает токен в память программы
load_dotenv()

# Теперь это сработает на 100% и на ноутбуке, и потом на сервере!
TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)


# 1. Срабатывает на команду /start и создает кнопки
@bot.message_handler(commands=['start'])
def welcome(message):
    # Создаем красивую клавиатуру, которая подстраивается под экран телефона
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Создаем две кнопки
    btn_calc = types.KeyboardButton("🧮 Посчитать зарплату")
    btn_info = types.KeyboardButton("ℹ️ О программе")
    
    # Добавляем кнопки в нашу клавиатуру
    markup.add(btn_calc, btn_info)
    
    # Отправляем сообщение вместе с кнопками
    bot.send_message(message.chat.id, "Привет, брат! Выбери нужное действие на кнопках внизу:", reply_markup=markup)


# 2. Логика обработки нажатия на кнопки
@bot.message_handler(content_types=['text'])
def handle_buttons(message):
    if message.text == "🧮 Посчитать зарплату":
        # Если нажали на калькулятор, спрашиваем смены и ждем ввода числа
        msg = bot.send_message(message.chat.id, "Напиши мне цифрами, сколько смен ты отработал в этом месяце?")
        bot.register_next_step_handler(msg, calculate_salary)
        
    elif message.text == "ℹ️ О программе":
        # Если нажали на инфо, рассказываем про автора
        bot.send_message(message.chat.id, "🤖 Этот бот был создан студентом 2 курса МТУСИ Сафар в 2026 году.\n\nЦель проекта — помочь сотрудникам быстро и честно рассчитывать свой доход чистыми!")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используй кнопки на клавиатуре внизу. Нажми /start, если они пропали.")


# 3. Функция самого расчета зарплаты
def calculate_salary(message):
    try:
        shifts = int(message.text)
        salary_per_shift = 3732
        total_money = salary_per_shift * shifts
        
        if shifts > 25:
            total_money = total_money + 10000
            response = f"Ты отлично поработал! Тебе положена премия 10 000 рублей. 🏆\nИтого к выплате: {total_money} рублей чистыми!"
        else:
            response = f"Твой чистый доход за этот месяц: {total_money} рублей. 👍"
            
        bot.send_message(message.chat.id, response)
        
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Нужно ввести именно число. Нажми кнопку '🧮 Посчитать зарплату' ещё раз.")

# Бесконечный запуск
print("Профессиональный бот с кнопками успешно запущен...")
bot.polling(none_stop=True)
