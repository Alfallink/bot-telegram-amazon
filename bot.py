import requests
from bs4 import BeautifulSoup
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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}

# =========================
# CATEGORIAS (ROTAÇÃO POR HORA)
# =========================

CATEGORIAS = [
    ("🔌 Eletrônicos", "https://www.amazon.com.br/gp/bestsellers/electronics"),
    ("🎮 Games & Videogame", "https://www.amazon.com.br/gp/bestsellers/videogames"),
    ("💻 Computadores", "https://www.amazon.com.br/gp/bestsellers/computers"),
    ("🎵 Música", "https://www.amazon.com.br/gp/bestsellers/music")
]

# =========================
# MENSAGENS (COPY ROTATIVA)
# =========================

def gerar_mensagem(categoria, titulo, link):
    modelos = [
        f"""🔥 OFERTA EM ALTA – LOJA PONTO H 🔥

📂 Categoria: {categoria}

📦 {titulo}

✔️ Um dos produtos mais procurados da categoria
✔️ Excelente opção para uso diário ou presente
✔️ Compra segura e entrega rápida pela Amazon

🛒 Garanta o seu agora:
{link}

🏬 Loja Ponto H
Curadoria diária de tecnologia, games e eletrônicos.
""",
        f"""⚡ DESTAQUE DO DIA – LOJA PONTO H ⚡

📂 Categoria: {categoria}

📦 {titulo}

💡 Por que escolher este produto?
✔️ Alta procura
✔️ Ótimo custo-benefício
✔️ Vendido e entregue pela Amazon

👉 Confira a oferta:
{link}

🏬 Loja Ponto H – As melhores oportunidades do dia.
"""
    ]
    return random.choice(modelos)

# =========================
# CONTROLE DE REPETIÇÃO
# =========================

POSTED_FILE = "posted_links.txt"

def carregar_links_postados():
    # Se o arquivo não existir, cria vazio
    if not os.path.exists(POSTED_FILE):
        open(POSTED_FILE, "w").close()
        return set()

    with open(POSTED_FILE, "r") as f:
        return set(l.strip() for l in f.readlines() if l.strip())


# =========================
# BUSCAR PRODUTOS
# =========================

def buscar_produtos(url, usados):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    produtos = []
    itens = soup.select("div.zg-grid-general-faceout")
    random.shuffle(itens)

    for item in itens:
        titulo = item.select_one("div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
        link = item.select_one("a.a-link-normal")

        if not titulo or not link:
            continue

        link_limpo = "https://www.amazon.com.br" + link["href"].split("?")[0]

        if link_limpo in usados:
            continue

        produtos.append({
            "titulo": titulo.get_text(strip=True),
            "link": link_limpo
        })

        if len(produtos) == 3:
            break

    return produtos

# =========================
# ENVIAR TELEGRAM
# =========================

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto
    }
    requests.post(url, json=payload)

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

print("🚀 Bot Loja Ponto H iniciado...")

hora = datetime.utcnow().hour
categoria_nome, categoria_url = CATEGORIAS[hora % len(CATEGORIAS)]

links_usados = carregar_links_postados()
produtos = buscar_produtos(categoria_url, links_usados)

for p in produtos:
    link_afiliado = f"{p['link']}?tag={AFILIADO_TAG}"
    mensagem = gerar_mensagem(categoria_nome, p["titulo"], link_afiliado)

    enviar_telegram(mensagem)
    salvar_link(p["link"])
    time.sleep(random.randint(3, 6))

print("🏁 Execução finalizada com sucesso.")
