import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# إعداد اللوج
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# قراءة مفاتيح البيئة
TELEGRAM_TOKEN = os.getenv("7971396121:AAF98vmvq3WVZHKnVGi3la9cOta_dGqOjGc")
OPENAI_API_KEY = os.getenv("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")

openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = """
أنت بوت خدمة عملاء فودافون كاش. رد باللهجة المصرية وبأسلوب لبق.
اشرح الخطوات بدقة لو السؤال عن الرصيد، التحويل، السحب أو نسيان الرقم السري.
ما تطلبش أي بيانات حساسة أبداً. لو العميل عايز عمليات حقيقية، وجهه لخدمة العملاء على 7001.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "أهلاً بيك 👋 أنا بوت فودافون كاش الذكي.\n"
        "اسألني عن أي خدمة زي:\n"
        "💰 معرفة الرصيد\n"
        "🔁 التحويل\n"
        "💳 السحب من ATM\n"
        "🔐 نسيان الرقم السري\n\n"
        "اكتب سؤالك بأي طريقة تحبها 😊"
    )
    await update.message.reply_text(text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    logger.info(f"User said: {user_text}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            max_tokens=300,
            temperature=0.3,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = "حصلت مشكلة مؤقتة في الخدمة، جرب تاني بعد شوية 🙏"

    await update.message.reply_text(reply)

async def main():
    if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
        raise SystemExit("⚠️ لازم تضيف TELEGRAM_TOKEN و OPENAI_API_KEY في البيئة")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
