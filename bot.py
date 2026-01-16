import requests
import os
import time
import random
from datetime import datetime

# =========================
# SECRETS
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AFILIADO_TAG = os.getenv("AFILIADO_TAG")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Token ou Chat ID do Telegram não definidos")

if not AFILIADO_TAG:
    raise ValueError("AFILIADO_TAG não definido nos Secrets do GitHub")

# =========================
# BUSCAS ATUALIZADAS (SEM BLOQUEIO)
# =========================

BUSCAS = [
    ("🔌 Eletrônicos", "https://www.amazon.com.br/s?k=eletronicos"),
    ("🎮 Games & Videogame", "https://www.amazon.com.br/s?k=video+game"),
    ("💻 Computadores", "https://www.amazon.com.br/s?k=computador"),
    ("🎧 Fones de Ouvido", "https://www.amazon.com.br/s?k=fone+de+ouvido"),
    ("🖥️ Periféricos", "https://www.amazon.com.br/s?k=mouse+teclado"),
    ("🎵 Música", "https://www.amazon.com.br/s?k=musica")
]

# =========================
# MENSAGEM (SEM IMAGEM)
# =========================

def gerar_mensagem(categoria, link_busca):
    link_afiliado = f"{link_busca}&tag={AFILIADO_TAG}"

    return f"""🔥 OFERTAS EM ALTA – LOJA PONTO H 🔥

📂 Categoria: {categoria}

💡 Seleção atualizada com os produtos mais procurados:
✔️ Preços em tempo real
✔️ Entrega rápida Amazon
✔️ Compra segura

🛒 Confira os produtos aqui:
{link_afiliado}

🏬 Loja Ponto H
Curadoria diária de tecnologia, games e eletrônicos.
"""

# =========================
# ENVIAR TELEGRAM (SÓ TEXTO + LINK)
# =========================

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto
        # NÃO usar disable_web_page_preview
    }
    r = requests.post(url, json=payload, timeout=20)
    print("📡 Telegram:", r.status_code)

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

print("🚀 Bot Loja Ponto H iniciado")

# 🔁 Quantos links por execução (5 = 5 por hora)
QTDE_POR_EXECUCAO = 5

for i in range(QTDE_POR_EXECUCAO):
    categoria, link_busca = random.choice(BUSCAS)

    print(f"🔗 Enviando link {i+1}/{QTDE_POR_EXECUCAO} – {categoria}")

    mensagem = gerar_mensagem(categoria, link_busca)
    enviar_telegram(mensagem)

    # ⏳ Intervalo humano: 3 a 6 minutos
    if i < QTDE_POR_EXECUCAO - 1:
        time.sleep(random.randint(180, 360))

print("🏁 Execução finalizada com sucesso.")
