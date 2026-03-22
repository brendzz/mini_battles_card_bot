import csv
import json
import os
import random
import schedule
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

load_dotenv()
webhookUrl = os.environ.get("DISCORD_WEBHOOK_URL")
if not webhookUrl:
    raise ValueError("DISCORD_WEBHOOK_URL is missing or not loaded from .env")

cardsFile = "cards.csv"
usedCardsFile = "used_cards.json"
imagesFolder = "images"  # Folder where your PNGs live
timeToPost = "14:00"

def load_cards():
    cards = []
    with open(cardsFile, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cards.append(row)
    return cards

def load_used_cards():
    if not os.path.exists(usedCardsFile):
        return []
    with open(usedCardsFile, "r", encoding="utf-8") as f:
        return json.load(f)

def save_used_cards(used):
    with open(usedCardsFile, "w", encoding="utf-8") as f:
        json.dump(used, f, indent=2)

def pick_card(cards, used):
    unused = [c for c in cards if c["CardNumber"] not in used]

    if not unused:
        used.clear()
        unused = cards

    card = random.choice(unused)
    used.append(card["CardNumber"])
    save_used_cards(used)
    return card

def send_card(card):
    webhook = DiscordWebhook(url=str(webhookUrl))

    stat_block = f"""
**Faction:** {card.get("Faction", "")}
**Designer:** {card.get("Designer", "")}
**ID:** {card.get("CardNumber", "")}
"""

    if card.get("Tags"):
        stat_block += f"**Tags:** {card['Tags']}\n"

    full_description = stat_block

    embed = DiscordEmbed(
        title=card["Name"],
        description=full_description,
        color=0xbf7d36
    )

    image_path = os.path.join(imagesFolder, f"{card['CardNumber']}.png")

    if os.path.exists(image_path):
        with open(image_path, "rb") as img:
            webhook.add_file(file=img.read(), filename=f"{card['CardNumber']}.png")
        embed.set_image(url=f"attachment://{card['CardNumber']}.png")
    else:
        print(f"No image found for CardNumber {card['CardNumber']}")

    webhook.add_embed(embed)
    webhook.execute()

def daily_task():
    cards = load_cards()
    used = load_used_cards()
    card = pick_card(cards, used)
    send_card(card)
    print(f"Sent card: {card['Name']} (CardNumber {card['CardNumber']})")

schedule.every().day.at(timeToPost).do(daily_task)

print("Daily CSV card bot running...")
while True:
    schedule.run_pending()
    time.sleep(1)
