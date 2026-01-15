from amazon_paapi import AmazonApi
import os
import time

# ==============================
# PEGAR SECRETS DO GITHUB
# ==============================

ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY")
SECRET_KEY = os.getenv("AMAZON_SECRET_KEY")
PARTNER_TAG = os.getenv("AMAZON_PARTNER_TAG")

print("ACCESS_KEY existe?", bool(ACCESS_KEY))
print("SECRET_KEY existe?", bool(SECRET_KEY))
print("PARTNER_TAG =", PARTNER_TAG)

# ==============================
# CRIAR OBJETO DA AMAZON
# ==============================

amazon = AmazonApi(
    ACCESS_KEY,
    SECRET_KEY,
    PARTNER_TAG,
    "BR"
)

# ==============================
# BUSCAR PRODUTO (TESTE)
# ==============================

items = amazon.search_items(
    keywords="Echo Dot",
    item_count=1
)

# ==============================
# MOSTRAR RESULTADO
# ==============================

for item in items:
    print("TÍTULO:", item.item_info.title.display_value)
    print("PREÇO:", item.offers.listings[0].price.display_amount)
    print("IMAGEM:", item.images.primary.large.url)
    time.sleep(5)  # evita bloqueio

print("🏁 Finalizado.")
