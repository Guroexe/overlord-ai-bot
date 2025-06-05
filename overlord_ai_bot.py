import telebot
from telebot import types
import random
import os

# Получаем токен из переменных окружения (безопасно)
BOT_TOKEN = os.getenv('BOT_TOKEN', "7972832759:AAEwXCLf7bXdYguvmx4cJvPCfnfWmslXVW8")
bot = telebot.TeleBot(BOT_TOKEN)

# Базовый URL для файлов Hugging Face
HF_BASE_URL = "https://huggingface.co/guroexe/overlord_bot/resolve/main/"

# Примеры промптов с описаниями (используем ваши файлы)
EXAMPLE_PROMPTS = [
    {
        "image_url": HF_BASE_URL + "00027-1018130080.png",
        "description": "🎨 **Промпт:** 'beautiful anime girl, long flowing hair, magical aura, soft lighting, detailed eyes, fantasy art style, high quality, 4k'\n\n📝 **Описание:** Этот промпт создает красивую аниме девушку с длинными волосами и магической аурой. Ключевые элементы:\n• 'soft lighting' - мягкое освещение\n• 'detailed eyes' - детализированные глаза\n• 'fantasy art style' - фэнтезийный стиль\n• 'high quality, 4k' - высокое качество"
    },
    {
        "image_url": HF_BASE_URL + "00112-2135572718.png", 
        "description": "🎨 **Промпт:** 'cyberpunk warrior, neon armor, futuristic cityscape, rain, dramatic lighting, digital art, cinematic composition'\n\n📝 **Описание:** Киберпанк воин в неоновой броне на фоне футуристического города. Важные элементы:\n• 'neon armor' - неоновая броня\n• 'dramatic lighting' - драматичное освещение\n• 'cinematic composition' - кинематографическая композиция\n• 'rain' - дождь для атмосферы"
    },
    {
        "image_url": HF_BASE_URL + "00138-478166885.png",
        "description": "🎨 **Промпт:** 'mystical forest guardian, ancient tree spirits, glowing mushrooms, ethereal mist, fantasy landscape, magical atmosphere'\n\n📝 **Описание:** Мистический страж леса среди древних духов деревьев. Ключевые слова:\n• 'ancient tree spirits' - древние духи деревьев\n• 'glowing mushrooms' - светящиеся грибы\n• 'ethereal mist' - призрачный туман\n• 'magical atmosphere' - магическая атмосфера"
    },
    {
        "image_url": HF_BASE_URL + "00167-3730156458.png",
        "description": "🎨 **Промпт:** 'steampunk inventor, brass goggles, mechanical workshop, gears and steam, vintage technology, warm lighting, detailed environment'\n\n📝 **Описание:** Стимпанк изобретатель в механической мастерской. Элементы стиля:\n• 'brass goggles' - латунные очки\n• 'gears and steam' - шестерни и пар\n• 'vintage technology' - винтажные технологии\n• 'detailed environment' - детализированное окружение"
    }
]

@bot.message_handler(commands=['start'])
def start_message(message):
    # Отправляем приветственное видео
    video_url = HF_BASE_URL + "IKONA%20-%20ИИ.mp4"  # URL-кодированное название файла
    
    try:
        bot.send_video(message.chat.id, video_url)
    except Exception as e:
        print(f"Ошибка отправки видео: {e}")
        bot.send_message(message.chat.id, "Видео временно недоступно")
    
    # Отправляем описание бота
    description_text = """
🤖 **OVERLORD AI INK (Free Train)**

Добро пожаловать в мир создания изображений с помощью ИИ!

**Что это такое?**
OVERLORD AI INK - это бот для генерации изображений с помощью Stable Diffusion. Вы можете создавать потрясающие артворки, просто описав то, что хотите увидеть.

**Как пользоваться Stable Diffusion:**
1. Опишите изображение на английском языке
2. Используйте детальные описания
3. Добавляйте стилистические теги (например: "digital art", "photorealistic")
4. Экспериментируйте с различными промптами

**Советы для лучших результатов:**
• Будьте конкретными в описаниях
• Используйте художественные термины
• Добавляйте технические параметры качества
• Экспериментируйте со стилями
"""
    
    bot.send_message(message.chat.id, description_text, parse_mode='Markdown')
    
    # Отправляем GIF с Google Colab
    gif_url = HF_BASE_URL + "14.gif"
    colab_text = """
🚀 **Попробуйте прямо сейчас в Google Colab!**

[Открыть Google Colab блокнот](https://colab.research.google.com/drive/your_notebook_link)

Здесь вы можете поэкспериментировать с различными моделями и настройками Stable Diffusion бесплатно!
"""
    
    try:
        bot.send_animation(message.chat.id, gif_url, caption=colab_text, parse_mode='Markdown')
    except Exception as e:
        print(f"Ошибка отправки GIF: {e}")
        bot.send_message(message.chat.id, colab_text, parse_mode='Markdown')
    
    # Создаем главное меню
    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    prompt_btn = types.InlineKeyboardButton("📝 Пример промпта", callback_data="example_prompt")
    pro_btn = types.InlineKeyboardButton("⭐ Полная Версия OVERLORD AI INK PRO", callback_data="pro_version")
    
    markup.add(prompt_btn, pro_btn)
    
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "example_prompt":
        send_example_prompt(call.message.chat.id)
    elif call.data == "pro_version":
        send_pro_version_info(call.message.chat.id)
    elif call.data == "back_to_menu":
        show_main_menu(call.message.chat.id)
    elif call.data.startswith("subscription_"):
        handle_subscription(call.message.chat.id, call.data)

def send_example_prompt(chat_id):
    # Выбираем случайный пример промпта
    example = random.choice(EXAMPLE_PROMPTS)
    
    try:
        # Отправляем изображение с описанием
        bot.send_photo(chat_id, example["image_url"], caption=example["description"], parse_mode='Markdown')
    except Exception as e:
        print(f"Ошибка отправки изображения: {e}")
        bot.send_message(chat_id, f"Изображение временно недоступно\n\n{example['description']}", parse_mode='Markdown')
    
    # Добавляем кнопки для повторного просмотра примеров
    markup = types.InlineKeyboardMarkup(row_width=1)
    another_example_btn = types.InlineKeyboardButton("📝 Еще пример промпта", callback_data="example_prompt")
    back_btn = types.InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_menu")
    markup.add(another_example_btn, back_btn)
    
    bot.send_message(chat_id, "Хотите увидеть еще примеры?", reply_markup=markup)

def send_pro_version_info(chat_id):
    pro_info = """
⭐ **OVERLORD AI INK PRO** - Полная версия

**Отличия от бесплатной версии:**

🎨 **Множество моделей:**
• Realistic Vision
• DreamShaper
• Anything V5
• Waifu Diffusion
• И многие другие!

🔧 **LoRA адаптеры:**
• Стилизация под известных художников
• Специальные эффекты
• Персонажи из игр и аниме

🎭 **Создание собственного стиля:**
• Обучение на ваших изображениях
• Персональные LoRA модели
• Уникальный художественный стиль

🔄 **Регулярные обновления:**
• Новые модели каждый месяц
• Улучшенные алгоритмы
• Эксклюзивные функции

📈 **Расширенные возможности:**
• Высокое разрешение до 4K
• Пакетная генерация
• Приоритетная обработка
• Техническая поддержка 24/7
"""
    
    bot.send_message(chat_id, pro_info, parse_mode='Markdown')
    
    # Показываем варианты подписки
    subscription_text = """
💰 **Выберите подписку через Tribut:**

Безопасные платежи через Telegram с автоматической активацией!
"""
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    month_btn = types.InlineKeyboardButton("📅 Подписка на 1 месяц - 2990₽", callback_data="subscription_month")
    forever_btn = types.InlineKeyboardButton("♾️ Подписка навсегда - 11990₽", callback_data="subscription_forever")
    back_btn = types.InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_menu")
    
    markup.add(month_btn, forever_btn, back_btn)
    
    bot.send_message(chat_id, subscription_text, reply_markup=markup, parse_mode='Markdown')

def handle_subscription(chat_id, subscription_type):
    if subscription_type == "subscription_month":
        price = "2990₽"
        period = "1 месяц"
        tribut_link = "https://tribut.me/your_bot_monthly"  # Замените на реальную ссылку
    else:
        price = "11990₽"
        period = "навсегда"
        tribut_link = "https://tribut.me/your_bot_forever"  # Замените на реальную ссылку
    
    payment_text = f"""
💳 **Оплата подписки**

**Тариф:** {period}
**Цена:** {price}

Для оплаты перейдите по ссылке ниже. После успешной оплаты ваша подписка будет активирована автоматически.

[Оплатить через Tribut]({tribut_link})

⚠️ **Важно:** Не закрывайте бот до завершения оплаты!
"""
    
    markup = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton("⬅️ Назад к подпискам", callback_data="pro_version")
    markup.add(back_btn)
    
    bot.send_message(chat_id, payment_text, reply_markup=markup, parse_mode='Markdown')

# Обработчик для всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    help_text = """
Используйте команду /start чтобы начать работу с ботом.

Или выберите одну из опций в меню ниже:
"""
    bot.send_message(message.chat.id, help_text)
    show_main_menu(message.chat.id)

if __name__ == "__main__":
    print("Бот OVERLORD AI INK запущен...")
    bot.polling(none_stop=True)