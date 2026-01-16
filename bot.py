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

def salvar_link(link):
    with open(POSTED_FILE, "a", encoding="utf-8") as f:
        f.write(link + "\n")

def carregar_links_postados():
    if not os.path.exists(POSTED_FILE):
        open(POSTED_FILE, "w").close()
        return set()

    with open(POSTED_FILE, "r", encoding="utf-8") as f:
        return set(l.strip() for l in f.readlines() if l.strip())

# =========================
# BUSCAR PRODUTOS
# =========================

def buscar_produtos(url, usados):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    produtos = []
    cards = soup.select("a.a-link-normal[href*='/dp/']")
    random.shuffle(cards)

    for a in cards:
        href = a.get("href")
        if not href:
            continue

        link_limpo = "https://www.amazon.com.br" + href.split("?")[0]
        if link_limpo in usados:
            continue

        titulo = a.get_text(strip=True)
        if not titulo or len(titulo) < 10:
            continue

        produtos.append({
            "titulo": titulo,
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
        "text": texto,
        "disable_web_page_preview": True
    }
    r = requests.post(url, json=payload, timeout=20)
    print("📡 Telegram:", r.status_code, r.text)

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

hora = datetime.utcnow().hour
categoria_nome, categoria_url = CATEGORIAS[hora % len(CATEGORIAS)]

print("📂 Categoria escolhida:", categoria_nome)
print("🔎 Buscando produtos em:", categoria_url)

links_usados = carregar_links_postados()
print("📁 Links já usados:", len(links_usados))

produtos = buscar_produtos(categoria_url, links_usados)
print("📦 Produtos encontrados:", len(produtos))

if not produtos:
    print("⚠️ Nenhum produto encontrado nesta execução.")
else:
    for p in produtos:
        print("📦 Enviando produto:", p["titulo"])

        link_afiliado = f"{p['link']}?tag={AFILIADO_TAG}"
        mensagem = gerar_mensagem(categoria_nome, p["titulo"], link_afiliado)

        enviar_telegram(mensagem)
        salvar_link(p["link"])
        time.sleep(3)

print("🏁 Execução finalizada com sucesso.")
