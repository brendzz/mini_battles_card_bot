import schedule
import time
from csv_helpers import load_cards, load_used_cards
from discord_helpers import pick_card, send_card
from constants import TIME_TO_POST

def daily_task():
    cards = load_cards()
    used = load_used_cards()
    card = pick_card(cards, used)
    send_card(card)
    print(f"Sent card: {card['Name']} (CardNumber {card['CardNumber']})")

schedule.every().day.at(TIME_TO_POST).do(daily_task)

print("Daily CSV card bot running...")

while True:
    schedule.run_pending()
    time.sleep(1)
