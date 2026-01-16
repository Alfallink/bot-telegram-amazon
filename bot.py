import os
import time
import random
import requests

# =========================
# SECRETS
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SHOPEE_AFILIADO_BASE = os.getenv("SHOPEE_AFILIADO_BASE")

# Validação
if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, SHOPEE_AFILIADO_BASE]):
    raise ValueError("Variáveis de ambiente ausentes")

# =========================
# CONFIGURAÇÕES
# =========================

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://shopee.com.br/"
}

CATEGORIAS = {
    "📱 Celulares": ["iphone", "samsung galaxy", "xiaomi celular"],
    "📺 Televisões": ["smart tv", "tv 4k"],
    "🎧 Fones de Ouvido": ["fone bluetooth", "headphone"]
}

# =========================
# TELEGRAM - FUNÇÃO CORRIGIDA
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
        r.raise_for_status()
        print(f"✅ Telegram: Mensagem enviada (status {r.status_code})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro Telegram: {e}")
        return False

# =========================
# FUNÇÕES AUXILIARES
# =========================

def gerar_link_afiliado(link_produto):
    return f"{SHOPEE_AFILIADO_BASE}?u={link_produto}"

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
            return []
        
        data = r.json()
        produtos = []
        
        for item in data.get("items", []):
            info = item.get("item_basic", {})
            titulo = info.get("name", "").strip()
            shopid = info.get("shopid")
            itemid = info.get("itemid")
            
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
