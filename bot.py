from amazon_paapi import AmazonApi
import os

ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY")
SECRET_KEY = os.getenv("AMAZON_SECRET_KEY")
PARTNER_TAG = os.getenv("AMAZON_PARTNER_TAG")


amazon = AmazonApi(
    ACCESS_KEY,
    SECRET_KEY,
    PARTNER_TAG,
    "BR"
)

items = amazon.search_items(
    keywords="Echo Dot",
    item_count=1
)

print("ACCESS_KEY existe?", bool(ACCESS_KEY))
print("SECRET_KEY existe?", bool(SECRET_KEY))
print("PARTNER_TAG =", PARTNER_TAG)




    time.sleep(5)  # evita bloqueio

print("🏁 Finalizado.")
