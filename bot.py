import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN NÃO ENCONTRADO - verifique o Secret TELEGRAM_BOT_TOKEN")

LINK_AFILIADO = "https://shope.ee/SEU_CODIGO"

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()

    if not texto.startswith("http"):
        await update.message.reply_text("❌ Envie apenas um link.")
        return

    mensagem = f"""
🔥 OFERTA IMPERDÍVEL 🔥

✅ Produto em alta com desconto especial

🔗 {LINK_AFILIADO}

_Aproveite antes que acabe_
"""
    await update.message.reply_text(mensagem.strip())

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

if __name__ == "__main__":
    main()
