import os
import telebot
from yt_dlp import YoutubeDL

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me a TikTok video link and I will download it for you without a watermark 📥")

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text.strip()
    
    if not ("tiktok.com" in url or "vt.tiktok.com" in url):
        bot.reply_to(message, "Please send a valid TikTok link.")
        return

    msg = bot.reply_to(message, "⏳ Downloading video without watermark...")
    
    output_path = "video.mp4"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'quiet': True,
    }

    try:
        if os.path.exists(output_path):
            os.remove(output_path)

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(output_path, 'rb') as video:
            bot.send_video(message.chat.id, video, reply_to_message_id=message.message_id)
            
        bot.delete_message(message.chat.id, msg.message_id)

        if os.path.exists(output_path):
            os.remove(output_path)

    except Exception as e:
        bot.edit_message_text(f"❌ Error: {e}", message.chat.id, msg.message_id)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    bot.infinity_polling()
