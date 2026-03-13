import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os

# ✅ محاولة قراءة التوكن من المتغيرات البيئية (وهو ما نضيفه في Railway)
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# إذا لم يتم العثور على التوكن، سيعرض خطأ واضحاً
if not BOT_TOKEN:
    raise ValueError("لم يتم العثور على BOT_TOKEN. تأكدي من إضافته في متغيرات البيئة.")

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    file = None
    # إذا كانت الرسالة تحتوي على ملف أو فيديو
    if msg.document:
        file = msg.document
    elif msg.video:
        file = msg.video
    # إذا كانت الرسالة معاد توجيهها من قناة
    elif msg.forward_from_chat and msg.forward_from_message_id:
        try:
            original_msg = await context.bot.get_chat_message(msg.forward_from_chat.id, msg.forward_from_message_id)
            file = original_msg.document or original_msg.video
        except:
            pass
    if not file:
        await msg.reply_text("أرسل ملف فيديو أو أعد توجيه رسالة من القناة.")
        return
    try:
        f = await context.bot.get_file(file.file_id)
        file_path = f.file_path
        direct_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        await msg.reply_text(f"✅ الرابط المباشر:\n{direct_link}")
    except Exception as e:
        await msg.reply_text(f"❌ خطأ: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
