import telebot
from telebot import types
import random
import os
import requests
from io import BytesIO
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN', "7972832759:AAEwXCLf7bXdYguvmx4cJvPCfnfWmslXVW8")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='Markdown')

# URL для медиафайлов
MEDIA_URLS = {
    "video": "https://huggingface.co/guroexe/overlord_bot/resolve/main/IKONA%20-%20%D0%98%D0%98.mp4?download=true",
    "gif": "https://huggingface.co/guroexe/overlord_bot/resolve/main/14.gif?download=true"
}

# Заголовки для запросов к Hugging Face
HEADERS = {
    'User-Agent': 'TelegramBot/1.0'
}

# Функция для загрузки файлов с обработкой ошибок
def download_media(url):
    try:
        response = requests.get(url, headers=HEADERS, stream=True)
        response.raise_for_status()
        
        # Создаем файлоподобный объект
        file_like = BytesIO()
        for chunk in response.iter_content(chunk_size=8192):
            file_like.write(chunk)
        file_like.seek(0)
        
        return file_like
    except Exception as e:
        logger.error(f"Ошибка загрузки медиа: {e}")
        return None

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        # Отправляем видео
        send_welcome_video(message.chat.id)
        
        # Отправляем описание бота
        send_bot_description(message.chat.id)
        
        # Отправляем GIF с Google Colab
        send_colab_gif(message.chat.id)
        
        # Показываем главное меню
        show_main_menu(message.chat.id)
        
    except Exception as e:
        logger.error(f"Ошибка в команде /start: {e}")
        bot.send_message(message.chat.id, "⚠️ Произошла ошибка при загрузке медиафайлов. Пожалуйста, попробуйте позже.")

def send_welcome_video(chat_id):
    try:
        video = download_media(MEDIA_URLS["video"])
        if video:
            # Определяем MIME-тип по расширению файла
            video.name = "welcome_video.mp4"
            bot.send_video(chat_id, video, caption="🎬 *Демонстрация возможностей OVERLORD AI INK*")
        else:
            bot.send_message(chat_id, "🎬 *Демонстрация возможностей OVERLORD AI INK*\n\nВидео временно недоступно.")
    except Exception as e:
        logger.error(f"Ошибка отправки видео: {e}")
        bot.send_message(chat_id, "🎬 *Демонстрация возможностей OVERLORD AI INK*\n\nВидео временно недоступно.")

def send_colab_gif(chat_id):
    colab_text = """
🚀 **Попробуйте прямо сейчас в Google Colab!**

[Открыть Google Colab блокнот](https://colab.research.google.com/drive/your_notebook_link)

Здесь вы можете поэкспериментировать с различными моделями и настройками Stable Diffusion бесплатно!
"""
    
    try:
        gif = download_media(MEDIA_URLS["gif"])
        if gif:
            gif.name = "colab_demo.gif"
            bot.send_animation(chat_id, gif, caption=colab_text)
        else:
            bot.send_message(chat_id, colab_text)
    except Exception as e:
        logger.error(f"Ошибка отправки GIF: {e}")
        bot.send_message(chat_id, colab_text)

# Остальные функции остаются без изменений
def send_bot_description(chat_id):
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
    bot.send_message(chat_id, description_text)

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    prompt_btn = types.InlineKeyboardButton("📝 Пример промпта", callback_data="example_prompt")
    pro_btn = types.InlineKeyboardButton("⭐ Полная Версия OVERLORD AI INK PRO", callback_data="pro_version")
    
    markup.add(prompt_btn, pro_btn)
    
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

# Остальные обработчики остаются без изменений
# ...

if __name__ == "__main__":
    logger.info("Бот OVERLORD AI INK запущен...")
    bot.infinity_polling()
