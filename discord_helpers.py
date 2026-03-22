from discord_webhook import DiscordWebhook, DiscordEmbed
from csv_helpers import save_used_cards
from constants import IMAGES_FOLDER
import random, os, re, requests
from dotenv import load_dotenv

load_dotenv()

webhookUrl = os.environ.get("DISCORD_WEBHOOK_URL")
if not webhookUrl:
    raise ValueError("DISCORD_WEBHOOK_URL is missing or not loaded from .env")

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
    
    gradient_str = card.get("Background", "")

    embed = DiscordEmbed(
        title=card["Name"],
        description=full_description,
        color=extract_color_from_gradient(gradient_str)
    )

    image_url = f"{IMAGES_FOLDER}/{card['CardNumber']}.png"

    if github_image_exists(image_url):
        embed.set_image(url=image_url)
    else:
        print(f"No image found for CardNumber {card['CardNumber']}")

    webhook.add_embed(embed)
    webhook.execute()
    
def extract_color_from_gradient(gradient_str):

    if not gradient_str:
        return 0x595959

    match = re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+)', gradient_str)
    if not match:
        return 0x595959 

    r, g, b = map(int, match.groups())

    return (r << 16) + (g << 8) + b

def github_image_exists(url):
    response = requests.head(url)
    return response.status_code == 200