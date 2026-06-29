import re

with open('C:/project/HA-michal/dashboard/lovelace.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

# Najdi všechny popup karty kde hash: je bez bg_color hned za ním
# Pattern: hash: "#popup-XXX"\n (bez bg_color na dalším řádku)
pattern = r'(            hash: "#popup-[^"]+"\n)(?!            bg_color:)'
replacement = r'\1            bg_color: "rgb(15, 17, 23)"\n            bg_opacity: 93\n'

new_content, count = re.subn(pattern, replacement, content)
print(f'Přidáno do {count} popup karet')

with open('C:/project/HA-michal/dashboard/lovelace.yaml', 'w', encoding='utf-8') as f:
    f.write(new_content)

# Ověření - spočítej kolik popup karet má bg_color
import yaml
cfg = yaml.safe_load(new_content)
popups = 0
for view in cfg.get('views', []):
    for section in view.get('sections', []):
        for card in section.get('cards', []):
            if card.get('card_type') == 'pop-up':
                if 'bg_color' in card:
                    popups += 1
                else:
                    print(f'CHYBÍ bg_color: {card.get("hash")}')
print(f'Popup karet s bg_color: {popups}')
