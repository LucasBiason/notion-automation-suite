#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('NOTION_API_TOKEN')
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Série + 15 episódios
cards = [
    '29b962a7-693c-81f7-8bd9-d74134c72fdd',  # Série principal
    '29b962a7-693c-8119-beb1-d507df52ab97',  # Ep 01
    '29b962a7-693c-8106-8d0c-f80399dcde07',  # Ep 02
    '29b962a7-693c-81b6-9564-d0cc1b51ee28',  # Ep 03
    '29b962a7-693c-816b-b737-fd5d2b1775f2',  # Ep 04
    '29b962a7-693c-8106-9356-e01cd244b5e6',  # Ep 05
    '29b962a7-693c-81d2-a60d-db8e1f0fd4eb',  # Ep 06
    '29b962a7-693c-8111-bd80-e7dad6f21b48',  # Ep 07
    '29b962a7-693c-8187-8ff7-c0035aefc2e4',  # Ep 08
    '29b962a7-693c-812d-ac96-e47b94316bec',  # Ep 09
    '29b962a7-693c-81b7-a318-c8fe08d6fa94',  # Ep 10
    '29b962a7-693c-8167-8cda-ebd71451903a',  # Ep 11
    '29b962a7-693c-8166-9bdc-c5aedb152fd7',  # Ep 12
    '29b962a7-693c-8167-a732-d88088f8ffad',  # Ep 13
    '29b962a7-693c-811c-bc75-c102c3e755ec',  # Ep 14
    '29b962a7-693c-815e-9767-daf56c839b9c',  # Ep 15
]

for i, card_id in enumerate(cards):
    url = f"https://api.notion.com/v1/pages/{card_id}"
    data = {"icon": {"type": "emoji", "emoji": "🛸"}}
    
    response = requests.patch(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        nome = "Série" if i == 0 else f"Ep {i:02d}"
        print(f"✅ 🛸 {nome}")
    else:
        print(f"❌ Erro no card {i}: {response.status_code}")

print("\n🎉 Todos os ícones adicionados!")

