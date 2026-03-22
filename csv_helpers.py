from constants import CSV_FILE, USED_CARDS_FILE
import csv
import json
import os

def load_cards():
    cards = []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cards.append(row)
    return cards

def load_used_cards():
    if not os.path.exists(USED_CARDS_FILE):
        return []
    with open(USED_CARDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_used_cards(used):
    with open(USED_CARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, indent=2)