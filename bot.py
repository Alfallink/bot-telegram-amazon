import requests
import os
import time
import random

# =========================
# SECRETS
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AFILIADO_TAG = os.getenv("AFILIADO_TAG")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Token ou Chat ID do Telegram não definidos")

if not AFILIADO_TAG:
    raise ValueError("AFILIADO_TAG não definido")

# =========================
# CATEGORIAS + PALAVRAS-CHAVE
# =========================
# 🔥 AQUI ESTÁ A CORREÇÃO PRINCIPAL

CATEGORIAS = {
    "🔌 Eletrônicos": [
        "smart tv",
        "fone bluetooth",
        "caixa de som",
        "carregador usb"
    ],
    "🎮 Games": [
        "controle ps4",
        "controle xbox",
        "headset gamer",
        "jogo ps5"
    ],
    "💻 Computadores": [
        "notebook",
        "mouse gamer",
        "teclado mecanico",
        "monitor"
    ],
    "🎧 Áudio": [
        "fone de ouvido",
        "headphone bluetooth",
        "soundbar"
    ]
}

# =========================
# MENSAGEM
# =========================

def gerar_mensagem(categoria, palavra, link):
    return f"""🔥 OFERTA EM ALTA – LOJA PONTO H 🔥

📂 Categoria: {categoria}
🔎 Produto: {palavra.title()}

💡 Seleção com os modelos mais vendidos do momento:
✔️ Preços atualizados
✔️ Entrega rápida Amazon
✔️ Compra segura

🛒 Ver produtos:
{link}

🏬 Loja Ponto H
Tecnologia, games e eletrônicos selecionados.
"""

# =========================
# ENVIAR TELEGRAM
# =========================

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto
    }
    r = requests.post(url, json=payload, timeout=20)
    print("📡 Telegram:", r.status_code)

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

QTDE_POR_EXECUCAO = 5  # 5 links por hora

for i in range(QTDE_POR_EXECUCAO):
    categoria = random.choice(list(CATEGORIAS.keys()))
    palavra = random.choice(CATEGORIAS[categoria])

    # 🔗 LINK DE BUSCA CORRETO (COM PRODUTOS)
    query = palavra.replace(" ", "+")
    link_busca = f"https://www.amazon.com.br/s?k={query}&tag={AFILIADO_TAG}"

    print(f"🔗 Enviando: {categoria} | {palavra}")

    mensagem = gerar_mensagem(categoria, palavra, link_busca)
    enviar_telegram(mensagem)

    if i < QTDE_POR_EXECUCAO - 1:
        time.sleep(random.randint(180, 360))  # 3 a 6 minutos

print("🏁 Execução finalizada com sucesso.")
