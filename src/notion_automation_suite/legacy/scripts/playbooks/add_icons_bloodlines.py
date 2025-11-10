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

cards = [
    '29b962a7-693c-8124-bca0-d787fb787ece',  # Série
    '29b962a7-693c-81b4-9748-f2691e8baa19',  # Ep 01
    '29b962a7-693c-81f3-9c26-cfed52e1ca6f',  # Ep 02
    '29b962a7-693c-81fb-9438-ffa5f034b506',  # Ep 03
    '29b962a7-693c-8188-a547-d978c470f313',  # Ep 04
    '29b962a7-693c-815c-836b-faf44fcb9a97',  # Ep 05
    '29b962a7-693c-8171-9f81-d78970c55a85',  # Ep 06
    '29b962a7-693c-8180-b0b7-e1242de8cacd',  # Ep 07
    '29b962a7-693c-8111-8051-f3bbf45aad07',  # Ep 08
    '29b962a7-693c-818a-a5fe-cd7b2a58b0b7',  # Ep 09
    '29b962a7-693c-81ee-a630-ef7680c94e7e',  # Ep 10
    '29b962a7-693c-81cc-a903-fa8428afa615',  # Ep 11
    '29b962a7-693c-816f-832a-c5bb285f51a5',  # Ep 12
    '29b962a7-693c-8182-b1bc-d9859b6a8c3a',  # Ep 13
    '29b962a7-693c-814a-aec3-eee04ea69d37',  # Ep 14
    '29b962a7-693c-819c-bd73-fca8da2a2239',  # Ep 15
]

for i, card_id in enumerate(cards):
    url = f"https://api.notion.com/v1/pages/{card_id}"
    data = {"icon": {"type": "emoji", "emoji": "🧛"}}
    
    response = requests.patch(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        nome = "Série" if i == 0 else f"Ep {i:02d}"
        print(f"✅ 🧛 {nome}")

print("\n🎉 Vampire Bloodlines completo!")

