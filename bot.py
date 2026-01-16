import os
import time
import random
import requests

# =========================
# SECRETS (GITHUB ACTIONS)
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SHOPEE_AFILIADO_BASE = os.getenv("SHOPEE_AFILIADO_BASE")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN ausente")

if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID ausente")

if not SHOPEE_AFILIADO_BASE:
    raise ValueError("SHOPEE_AFILIADO_BASE ausente")

# =========================
# CONFIGURAÇÕES
# =========================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://shopee.com.br/",
    "Accept": "application/json"
}

# =========================
# CATEGORIAS + PALAVRAS-CHAVE
# =========================

CATEGORIAS = {
    "📱 Celulares": ["iphone", "samsung galaxy", "xiaomi celular", "motorola celular"],
    "📺 Televisões": ["smart tv", "tv 4k", "android tv"],
    "🎧 Fones de Ouvido": ["fone bluetooth", "headphone", "fone gamer"],
    "⌚ Smartwatch": ["smartwatch", "relogio inteligente"],
    "🛡️ Capinhas e Películas": ["capinha celular", "pelicula vidro"],
    "🔊 Assistentes Virtuais": ["echo dot", "alexa"],
    "💻 Eletrônicos em Geral": ["tablet", "monitor", "notebook"]
}

# =========================
# TELEGRAM
# =========================

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "HTML"
    }
    
    try:
        r = requests.post(url, json=payload, timeout=15)
        print(f"📡 Telegram: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Erro Telegram: {e}")
        return False

# =========================
# GERAR LINK AFILIADO
# =========================

def gerar_link_afiliado(link_produto):
    return f"{SHOPEE_AFILIADO_BASE}?u={link_produto}"

# =========================
# BUSCAR PRODUTOS SHOPEE
# =========================

def buscar_produtos(palavra_chave, limite=1):
    print(f"🔎 Buscando: {palavra_chave}")
    
    url = "https://shopee.com.br/api/v4/search/search_items"
    params = {
        "by": "relevancy",
        "keyword": palavra_chave,
        "limit": limite,
        "newest": 0,
        "order": "desc",
        "page_type": "search"
    }
    
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        
        if r.status_code != 200:
            print(f"⚠️ Status Shopee: {r.status_code}")
            return []
        
        data = r.json()
        produtos = []
        
        for item in data.get("items", []):
            info = item.get("item_basic", {})
            
            titulo = info.get("name", "").strip()
            shopid = info.get("shopid")
            itemid = info.get("itemid")
            
            if not titulo or not shopid or not itemid:
                continue
            
            # Corrigindo formato do link
            link_produto = f"https://shopee.com.br/product/{shopid}/{itemid}"
            link_afiliado = gerar_link_afiliado(link_produto)
            
            produtos.append({
                "titulo": titulo,
                "link": link_afiliado,
                "preco": info.get("price", 0) / 100000 if info.get("price") else 0,
                "vendidos": info.get("historical_sold", 0)
            })
            
            if len(produtos) >= limite:
                break
        
        return produtos
        
    except Exception as e:
        print(f"❌ Erro na busca: {e}")
        return []

# =========================
# GERAR MENSAGEM
# =========================

def gerar_mensagem(categoria, produto):
    titulo = produto["titulo"]
    link = produto["link"]
    
    extras = []
    if produto.get("preco", 0) > 0:
        extras.append(f"💰 Preço: R$ {produto['preco']:,.2f}")
    if produto.get("vendidos", 0) > 0:
        extras.append(f"📊 Vendidos: {produto['vendidos']}+")
    
    info_extras = "\n".join(extras) + "\n" if extras else ""
    
    return f"""🔥 <b>OFERTA EM ALTA – LOJA PONTO H</b> 🔥

📂 <b>Categoria:</b> {categoria}
{info_extras}
📦 <b>Produto:</b> {titulo}

✅ Alta procura
✅ Excelente custo-benefício
✅ Compra segura

🛒 <b>Compre agora:</b>
{link}

🏬 <b>Loja Ponto H</b>
Tecnologia selecionada com qualidade.

⚠️ <i>Ofertas limitadas!</i>
"""

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

def main():
    print("🚀 Bot Shopee iniciado")
    print("=" * 40)
    
    # Quantidade aleatória de produtos
    quantidade = random.randint(2, 4)
    print(f"📦 Enviando {quantidade} produtos")
    
    enviados = 0
    
    for i in range(quantidade):
        print(f"\n🔍 [{i+1}/{quantidade}]")
        
        # Seleciona aleatoriamente
        categoria = random.choice(list(CATEGORIAS.keys()))
        palavra = random.choice(CATEGORIAS[categoria])
        
        print(f"Categoria: {categoria}")
        print(f"Palavra: {palavra}")
        
        # Busca produto
        produtos = buscar_produtos(palavra, limite=1)
        
        if not produtos:
            print("⚠️ Nenhum produto encontrado")
            time.sleep(5)
            continue
        
        # Envia para Telegram
        produto = produtos[0]
        mensagem = gerar_mensagem(categoria, produto)
        
        if enviar_telegram(mensagem):
            enviados += 1
            print(f"✅ Enviado: {produto['titulo'][:50]}...")
        else:
            print("❌ Falha no envio")
        
        # Aguarda entre envios
        if i < quantidade - 1:
            espera = random.randint(15, 25)
            print(f"⏳ Aguardando {espera}s...")
            time.sleep(espera)
    
    print(f"\n🏁 Concluído! {enviados}/{quantidade} enviados")

if __name__ == "__main__":
    main()        print(f"✅ Telegram: Mensagem enviada (status {r.status_code})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro Telegram: {e}")
        return False

# =========================
# GERAR LINK AFILIADO
# =========================

def gerar_link_afiliado(link_produto):
    """Adiciona parâmetros de afiliado ao link"""
    return f"{SHOPEE_AFILIADO_BASE}?u={link_produto}"

# =========================
# BUSCAR PRODUTOS SHOPEE (JSON)
# =========================

def buscar_produtos(palavra_chave, limite=1):
    """Busca produtos na API da Shopee"""
    print(f"🔍 Buscando: '{palavra_chave}'")

    url = "https://shopee.com.br/api/v4/search/search_items"

    params = {
        "by": "relevancy",
        "keyword": palavra_chave,
        "limit": limite,
        "newest": 0,
        "order": "desc",
        "page_type": "search",
        "scenario": "PAGE_GLOBAL_SEARCH",
        "version": 2
    }

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            print(f"⚠️ Shopee status: {response.status_code}")
            return []

        data = response.json()
        
        if "items" not in data:
            print("⚠️ Nenhum produto encontrado")
            return []

    except requests.exceptions.Timeout:
        print("⏱️ Timeout na requisição Shopee")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de requisição: {e}")
        return []
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return []

    produtos = []

    for item in data.get("items", [])[:limite]:
        info = item.get("item_basic", {})

        titulo = info.get("name", "").strip()
        shopid = info.get("shopid")
        itemid = info.get("itemid")

        if not titulo or not shopid or not itemid:
            continue

        # Formata o link do produto
        nome_formatado = titulo.lower().replace(" ", "-")
        link_produto = f"https://shopee.com.br/{nome_formatado}-i.{shopid}.{itemid}"
        link_afiliado = gerar_link_afiliado(link_produto)

        produtos.append({
            "titulo": titulo,
            "link": link_afiliado,
            "preco": info.get("price", 0) / 100000,  # Converter formato do preço
            "vendidos": info.get("historical_sold", 0)
        })

    return produtos

# =========================
# COPY PROFISSIONAL
# =========================

def gerar_mensagem(categoria, produto):
    """Gera mensagem formatada para o produto"""
    titulo = produto["titulo"]
    link = produto["link"]
    
    # Adiciona informações extras se disponíveis
    extras = []
    if "preco" in produto and produto["preco"]:
        extras.append(f"💰 Preço: R$ {produto['preco']:,.2f}")
    if "vendidos" in produto and produto["vendidos"]:
        extras.append(f"📊 Vendidos: {produto['vendidos']}+")
    
    info_extras = "\n".join(extras) + "\n" if extras else ""
    
    return f"""🔥 <b>OFERTA EM ALTA – LOJA PONTO H</b> 🔥

📂 <b>Categoria:</b> {categoria}
{info_extras}
📦 <b>Produto:</b> {titulo}

✅ Alta procura
✅ Excelente custo-benefício
✅ Compra segura pela Shopee

🛒 <b>Garanta o seu agora:</b>
{link}

🏬 <b>Loja Ponto H</b>
Tecnologia e eletrônicos selecionados com qualidade.

⚠️ <i>Ofertas por tempo limitado!</i>
"""

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

def main():
    print("🚀 Bot Shopee Loja Ponto H iniciado")
    print("=" * 50)
    
    QTDE_POR_EXECUCAO = random.randint(3, 5)
    print(f"📦 Quantidade de produtos para esta execução: {QTDE_POR_EXECUCAO}")
    
    enviados = 0
    falhas = 0
    
    for i in range(QTDE_POR_EXECUCAO):
        print(f"\n🔎 ({i+1}/{QTDE_POR_EXECUCAO})")
        
        # Seleciona categoria e palavra-chave aleatórias
        categoria = random.choice(list(CATEGORIAS.keys()))
        palavra = random.choice(CATEGORIAS[categoria])
        
        print(f"Categoria: {categoria}")
        print(f"Palavra-chave: {palavra}")
        
        # Busca produtos
        produtos = buscar_produtos(palavra, limite=1)
        
        if not produtos:
            print("⚠️ Nenhum produto encontrado, tentando novamente...")
            falhas += 1
            time.sleep(10)
            continue
        
        # Envia cada produto encontrado
        for produto in produtos:
            mensagem = gerar_mensagem(categoria, produto)
            if enviar_telegram(mensagem):
                enviados += 1
                print(f"✅ Produto enviado: {produto['titulo'][:50]}...")
            else:
                falhas += 1
        
        # Intervalo entre envios (evita spam)
        if i < QTDE_POR_EXECUCAO - 1:
            intervalo = random.randint(20, 40)
            print(f"⏳ Aguardando {intervalo} segundos...")
            time.sleep(intervalo)
    
    print("\n" + "=" * 50)
    print(f"🏁 Execução finalizada!")
    print(f"📨 Total enviado: {enviados}")
    print(f"❌ Falhas: {falhas}")

if __name__ == "__main__":
    main()    return f"{SHOPEE_AFILIADO_BASE}?u={link_produto}"

# =========================
# BUSCAR PRODUTOS (JSON)
# =========================

def buscar_produtos(palavra_chave, limite=1):
    print(f"🌐 Buscando: {palavra_chave}")

    url = "https://shopee.com.br/api/v4/search/search_items"

    params = {
        "by": "relevancy",
        "keyword": palavra_chave,
        "limit": limite,
        "newest": 0,
        "order": "desc",
        "page_type": "search"
    }

    try:
        r = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=8
        )

        if r.status_code != 200:
            print("⚠️ Shopee status:", r.status_code)
            return []

        data = r.json()

    except requests.exceptions.Timeout:
        print("⏱️ Timeout Shopee")
        return []

    except Exception as e:
        print("❌ Erro Shopee:", e)
        return []

    produtos = []

    for item in data.get("items", []):
        info = item.get("item_basic", {})

        titulo = info.get("name")
        shopid = info.get("shopid")
        itemid = info.get("itemid")

        if not titulo or not shopid or not itemid:
            continue

        link_produto = f"https://shopee.com.br/product/{shopid}/{itemid}"
        link_afiliado = gerar_link_afiliado(link_produto)

        produtos.append({
            "titulo": titulo,
            "link": link_afiliado
        })

        if len(produtos) >= limite:
            break

    return produtos

# =========================
# MENSAGEM
# =========================

def gerar_mensagem(categoria, titulo, link):
    return f"""🔥 OFERTA EM ALTA – LOJA PONTO H 🔥

📂 Categoria: {categoria}

📦 {titulo}

✔️ Alta procura
✔️ Excelente custo-benefício
✔️ Compra segura pela Shopee

🛒 Garanta o seu agora:
{link}

🏬 Loja Ponto H
Tecnologia e eletrônicos selecionados.
"""

# =========================
# EXECUÇÃO
# =========================

print("🚀 Bot Shopee Loja Ponto H iniciado")

QTDE_POR_EXECUCAO = random.randint(3, 5)
print("📦 Produtos nesta execução:", QTDE_POR_EXECUCAO)

for i in range(QTDE_POR_EXECUCAO):
    categoria = random.choice(list(CATEGORIAS.keys()))
    palavra = random.choice(CATEGORIAS[categoria])

    print(f"🔎 ({i+1}/{QTDE_POR_EXECUCAO}) {categoria} | {palavra}")

    produtos = buscar_produtos(palavra, limite=1)

    if not produtos:
        print("⚠️ Nenhum produto retornado")
        continue

    for p in produtos:
        mensagem = gerar_mensagem(categoria, p["titulo"], p["link"])
        enviar_telegram(mensagem)

    if i < QTDE_POR_EXECUCAO - 1:
        time.sleep(15)

print("🏁 Execução finalizada com sucesso")
