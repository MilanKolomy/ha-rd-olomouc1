# Projekt Vizualizace a ovládání domácnosti na Home Assistant & KNX/EIB

## Budeme pracovat na PC Green s HA OS zapojený do místní LAN
Green běží na: http://192.168.40.144:8123/
API token: .token-ha-api
SSH: login uzivatel-ssh-api, heslo v ssh-config

## Vzorové projekt
priklad-projektu-1.yaml
* komerční budova budova
* spíše snaha o systémové načítání konfigurací
* zobrazovat spíše data
* přehledy textové, tabulkové
* ovládání místností spíše funkční

priklad-projektu-2.yaml
* rodinný dům
* kladen důraz spíše na design
* grafické přehledy
* ovládání místnosít grafické

## Tabulka popisu místností a KNX skupinových adres
DB\mistnosti.csv

## Téma v HA
/config/themes/glass_dark.yaml

# Systémové instrukce
* Ukládej prosím veškeré své režijní nastavení a paměť přímo sem do projektu, aby se dal projekt přenést na jiné PC a byl uchovaný kontext viz KONTEXT.md
* Před každým ukončením práce Tě vyzvu k uložení kontextu, tak prosím uložit kontext - aby se dalo plynule navázat