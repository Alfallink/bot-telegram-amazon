import os
import time
import random
import requests
import json

# =========================
# SECRETS
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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    "Referer": "https://shopee.com.br/",
    "Origin": "https://shopee.com.br",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

# =========================
# CATEGORIAS + PALAVRAS-CHAVE SIMPLIFICADAS
# =========================

CATEGORIAS = {
    "📱 Celulares": ["iphone", "samsung", "xiaomi", "motorola"],
    "📺 Televisões": ["smart tv", "tv 4k", "tv led"],
    "🎧 Fones de Ouvido": ["fone bluetooth", "headphone", "fone sem fio"],
    "⌚ Smartwatch": ["smartwatch", "relogio inteligente"],
    "💻 Notebooks": ["notebook", "laptop", "computador portatil"]
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
# BUSCAR PRODUTOS SHOPEE (API ATUALIZADA)
# =========================

def buscar_produtos(palavra_chave, limite=3):
    """Busca produtos na Shopee com API atualizada"""
    print(f"🔍 Buscando: '{palavra_chave}'")
    
    # URL da API oficial da Shopee
    url = "https://shopee.com.br/api/v4/search/search_items"
    
    # Parâmetros otimizados
    params = {
        "by": "relevancy",
        "keyword": palavra_chave,
        "limit": 50,  # Busca mais para ter opções
        "newest": 0,
        "order": "desc",
        "page_type": "search",
        "scenario": "PAGE_GLOBAL_SEARCH",
        "version": 2,
        "locations": "",
    }
    
    try:
        # Faz a requisição
        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=20
        )
        
        print(f"📡 Status API: {response.status_code}")
        
        if response.status_code != 200:
            print(f"⚠️ Erro na API: {response.status_code}")
            # Tentar uma abordagem alternativa
            return buscar_produtos_alternativo(palavra_chave, limite)
        
        data = response.json()
        
        # Debug: mostrar estrutura da resposta
        print(f"📦 Itens na resposta: {len(data.get('items', []))}")
        
        produtos = []
        
        for item in data.get("items", []):
            if len(produtos) >= limite:
                break
                
            info = item.get("item_basic", {})
            
            # Extrair informações
            nome = info.get("name", "").strip()
            shop_id = info.get("shopid")
            item_id = info.get("itemid")
            preco_min = info.get("price_min", 0)
            preco_max = info.get("price_max", 0)
            vendidos = info.get("historical_sold", 0)
            avaliacao = info.get("item_rating", {}).get("rating_star", 0)
            
            if not nome or not shop_id or not item_id:
                continue
            
            # Formatar preço
            if preco_min:
                preco_real = preco_min / 100000
            else:
                preco_real = 0
            
            # Gerar link do produto
            nome_slug = nome.lower().replace(" ", "-").replace(",", "").replace(".", "")
            link_produto = f"https://shopee.com.br/{nome_slug}-i.{shop_id}.{item_id}"
            link_afiliado = f"{SHOPEE_AFILIADO_BASE}?u={link_produto}"
            
            produtos.append({
                "titulo": nome[:80],  # Limitar tamanho
                "link": link_afiliado,
                "preco": preco_real,
                "vendidos": vendidos,
                "avaliacao": round(avaliacao, 1)
            })
        
        return produtos[:limite]  # Retornar apenas o limite pedido
        
    except requests.exceptions.Timeout:
        print("⏱️ Timeout na requisição")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de rede: {e}")
        return []
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return []

def buscar_produtos_alternativo(palavra_chave, limite=2):
    """Método alternativo de busca se o principal falhar"""
    print(f"🔄 Tentando busca alternativa: '{palavra_chave}'")
    
    # Tentar uma API diferente ou método
    url = "https://shopee.com.br/api/v4/search/search_items"
    
    # Parâmetros diferentes
    params = {
        "by": "pop",
        "keyword": palavra_chave,
        "limit": 30,
        "newest": 0,
        "order": "desc",
        "page_type": "search",
    }
    
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            produtos = []
            
            for item in data.get("items", []):
                if len(produtos) >= limite:
                    break
                    
                info = item.get("item_basic", {})
                nome = info.get("name", "").strip()
                shop_id = info.get("shopid")
                item_id = info.get("itemid")
                
                if nome and shop_id and item_id:
                    link_produto = f"https://shopee.com.br/product/{shop_id}/{item_id}"
                    link_afiliado = f"{SHOPEE_AFILIADO_BASE}?u={link_produto}"
                    
                    produtos.append({
                        "titulo": nome[:60],
                        "link": link_afiliado,
                        "preco": info.get("price", 0) / 100000 if info.get("price") else 0
                    })
            
            return produtos
        else:
            return []
            
    except Exception:
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
    if produto.get("avaliacao", 0) > 0:
        extras.append(f"⭐ Avaliação: {produto['avaliacao']}/5")
    
    info_extras = "\n".join(extras)
    
    mensagem = f"""🔥 <b>OFERTA RECOMENDADA - LOJA PONTO H</b> 🔥

<b>{categoria}</b>

{info_extras}

📦 <b>{produto['titulo']}</b>

✅ Produto em alta demanda
✅ Compra segura via Shopee
✅ Entrega para todo Brasil

🛒 <b>Clique para ver a oferta:</b>
{produto['link']}

🏬 <b>Loja Ponto H</b>
Selecionamos as melhores ofertas para você!

#Oferta #Shopee #Eletronicos
"""
    return mensagem

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

def main():
    print("🚀 Bot Shopee Loja Ponto H - INICIADO")
    print("=" * 50)
    
    # Quantidade de produtos a enviar
    quantidade = 3  # Fixo para testes
    print(f"🎯 Meta: Enviar {quantidade} produtos\n")
    
    enviados = 0
    
    for i in range(quantidade):
        print(f"\n{'='*30}")
        print(f"📦 PRODUTO {i+1}/{quantidade}")
        
        # Selecionar categoria e palavra-chave
        categoria = random.choice(list(CATEGORIAS.keys()))
        palavra = random.choice(CATEGORIAS[categoria])
        
        print(f"Categoria: {categoria}")
        print(f"Palavra-chave: {palavra}")
        
        # Buscar produtos
        produtos = buscar_produtos(palavra, limite=2)
        
        if not produtos:
            print("⚠️ Nenhum produto encontrado. Tentando alternativa...")
            # Tentar com palavra-chave mais genérica
            produtos = buscar_produtos("celular", limite=2)
        
        if produtos:
            produto = produtos[0]
            print(f"✅ Produto encontrado: {produto['titulo'][:50]}...")
            
            # Gerar e enviar mensagem
            mensagem = gerar_mensagem(categoria, produto)
            
            if enviar_telegram(mensagem):
                enviados += 1
                print(f"📨 Enviado com sucesso!")
            else:
                print("❌ Falha no envio para Telegram")
        else:
            print("❌ Nenhum produto disponível")
        
        # Aguardar entre buscas
        if i < quantidade - 1:
            espera = random.randint(10, 20)
            print(f"⏳ Aguardando {espera} segundos...")
            time.sleep(espera)
    
    print(f"\n{'='*50}")
    print(f"🏁 RESULTADO FINAL: {enviados}/{quantidade} enviados")
    
    if enviados == 0:
        print("⚠️ ATENÇÃO: Nenhuma mensagem foi enviada.")
        print("Verifique:")
        print("1. Conexão com a API da Shopee")
        print("2. Configuração dos secrets no GitHub")
        print("3. Palavras-chave utilizadas")

if __name__ == "__main__":
    main()            itemid = info.get("itemid")
            
            if titulo and shopid and itemid:
                link_produto = f"https://shopee.com.br/product/{shopid}/{itemid}"
                produtos.append({
                    "titulo": titulo,
                    "link": gerar_link_afiliado(link_produto)
                })
                
            if len(produtos) >= limite:
                break
                
        return produtos
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return []

def gerar_mensagem(categoria, produto):
    return f"""🔥 <b>OFERTA EM ALTA</b> 🔥

📂 <b>Categoria:</b> {categoria}
📦 <b>Produto:</b> {produto['titulo']}

✅ Alta procura
✅ Excelente custo-benefício

🛒 <b>Compre agora:</b>
{produto['link']}

🏬 <b>Loja Ponto H</b>
Tecnologia selecionada.
"""

# =========================
# EXECUÇÃO PRINCIPAL
# =========================

def main():
    print("🚀 Bot iniciado")
    
    quantidade = random.randint(2, 3)
    print(f"📦 Enviando {quantidade} produtos")
    
    enviados = 0
    
    for i in range(quantidade):
        categoria = random.choice(list(CATEGORIAS.keys()))
        palavra = random.choice(CATEGORIAS[categoria])
        
        print(f"\n🔍 [{i+1}/{quantidade}] {categoria} - {palavra}")
        
        produtos = buscar_produtos(palavra, 1)
        
        if produtos:
            mensagem = gerar_mensagem(categoria, produtos[0])
            if enviar_telegram(mensagem):
                enviados += 1
            
            if i < quantidade - 1:
                time.sleep(random.randint(10, 20))
    
    print(f"\n🏁 Concluído! {enviados}/{quantidade} enviados")

if __name__ == "__main__":
    main()
