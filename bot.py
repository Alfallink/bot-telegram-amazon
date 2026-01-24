from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Envie o produto neste formato:\n\n"
        "CHAMADA | PRODUTO | PREÇO_ANTIGO | PREÇO_ATUAL | LINK | OBSERVAÇÃO"
    )

async def gerar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    partes = texto.split("|")

    if len(partes) != 6:
        await update.message.reply_text(
            "❌ Formato inválido.\n\n"
            "Use:\n"
            "CHAMADA | PRODUTO | PREÇO_ANTIGO | PREÇO_ATUAL | LINK | OBSERVAÇÃO"
        )
        return

    chamada, produto, preco_antigo, preco_atual, link, obs = [p.strip() for p in partes]

    mensagem = f"""
{chamada}

✅ {produto}

DE ~R$ {preco_antigo}~
🔥 POR R$ {preco_atual} 🔥

🔗 {link}

_{obs}_
"""

    await update.message.reply_text(mensagem.strip())

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gerar))

    app.run_polling()

if __name__ == "__main__":
    main()
