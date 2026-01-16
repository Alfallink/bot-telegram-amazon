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
    "📱 Celulares": ["iphone", "samsung", "xiaomi"],
    "📺 Televisões": ["smart tv", "tv led"],
    "🎧 Fones de Ouvido": ["fone bluetooth", "headphone"],
    "⌚ Smartwatch": ["smartwatch"],
    "💻 Notebooks": ["notebook", "laptop"]
}

# =========================
# TELEGRAM
# =========================

def enviar_telegram(texto):
    """Envia mensagem para o Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        r = requests.post(url, json=payload, timeout=15)
        print(f"✅ Telegram: Status {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Erro Telegram: {e}")
        return False

# =========================
# BUSCAR PRODUTOS SHOPEE
# =========================

def buscar_produtos(palavra_chave, limite=1):
    """Busca produtos na Shopee"""
    print(f"🔍 Buscando: '{palavra_chave}'")
    
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
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️ Status: {response.status_code}")
            return []
        
        data = response.json()
        produtos = []
        
        for item in data.get("items", []):
            info = item.get("item_basic", {})
            
            nome = info.get("name", "").strip()
            shop_id = info.get("shopid")
            item_id = info.get("itemid")
            
            if not nome or not shop_id or not item_id:
                continue
            
            link_produto = f"https://shopee.com.br/product/{shop_id}/{item_id}"
            link_afiliado = f"{SHOPEE_AFILIADO_BASE}?u={link_produto}"
            
            preco_min = info.get("price_min")
            preco = preco_min / 100000 if preco_min else 0
            
            produtos.append({
                "titulo": nome[:100],
                "link": link_afiliado,
                "preco": preco,
                "vendidos": info.get("historical_sold", 0)
            })
            
            if len(produtos) >= limite:
                break
        
        return produtos
        
    except requests.exceptions.Timeout:
        print("⏱️ Timeout na requisição")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de rede: {e}")
        return []
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return []

# =========================
# GERAR MENSAGEM
# =========================

def gerar_mensagem(categoria, produto):
    """Gera mensagem formatada para Telegram"""
    
    extras = []
    if produto.get("preco", 0) > 0:
        extras.append(f"💰 Preço: R$ {produto['preco']:,.2f}")
    if produto.get("vendidos", 0) > 0:
        extras.append(f"📊 Vendidos: {produto['vendidos']}+")
    
    info_extras = "\n".join(extras)
    
    mensagem = f"""🔥 <b>OFERTA RECOMENDADA</b> 🔥

<b>{categoria}</b>

{info_extras}

📦 <b>{produto['titulo']}</b>

✅ Produto em alta demanda
✅ Compra segura via Shopee
✅ Entrega rápida

🛒 <b>Clique para ver:</b>
{produto['link']}

🏬 <b>Loja Ponto H</b>
As melhores ofertas para você!
"""
    return mensagem

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

def main():
    print("🚀 Bot Shopee Loja Ponto H")
    print("=" * 50)
    
    quantidade = 3
    print(f"🎯 Enviando {quantidade} produtos\n")
    
    enviados = 0
    
    for i in range(quantidade):
        print(f"\n📦 Produto {i+1}/{quantidade}")
        
        categoria = random.choice(list(CATEGORIAS.keys()))
        palavra = random.choice(CATEGORIAS[categoria])
        
        print(f"Categoria: {categoria}")
        print(f"Palavra: {palavra}")
        
        produtos = buscar_produtos(palavra, limite=1)
        
        if not produtos:
            print("⚠️ Nada encontrado, tentando termo genérico...")
            produtos = buscar_produtos("celular", limite=1)
        
        if produtos:
            produto = produtos[0]
            print(f"✅ Encontrado: {produto['titulo'][:50]}...")
            
            mensagem = gerar_mensagem(categoria, produto)
            
            if enviar_telegram(mensagem):
                enviados += 1
                print(f"📨 Enviado!")
            else:
                print("❌ Falha no envio")
        else:
            print("❌ Nenhum produto disponível")
        
        # CORREÇÃO: Esta linha deve estar DENTRO do loop for, mas FORA do if/else
        if i < quantidade - 1:
            espera = random.randint(8, 15)
            print(f"⏳ Aguardando {espera}s...")
            time.sleep(espera)
    
    print(f"\n{'='*50}")
    print(f"🏁 Concluído: {enviados}/{quantidade} enviados")

# =========================
# INICIAR O BOT
# =========================

if __name__ == "__main__":
    main()
