# Kontext projektu — stav k 2026-06-29

## Co bylo uděláno

### Git & GitHub (2026-06-29)
- Vytvořen `.gitignore` — ignoruje `.claude/`, `.local/`, `DB/`, `KNX-Adresy/`, `dashboard/*.png/jpg/jpeg`, tokeny
- Inicializován git repozitář, initial commit
- Repozitář na GitHub: https://github.com/MilanKolomy/ha-rd-olomouc1
- `dashboard/Dashboard-návrh.png` odebrán z gitu (přesunut do `.local/`)
- Vytvořen `README.md` s přehledem projektu, tabulkami KNX skupin, strukturou, deploy příkazy
- Přidán screenshot dashboardu `themes/screenshot.jpg` — zobrazuje se v README na GitHubu

### Připojení na HA Green
- Ověřeno připojení na Home Assistant Green
- HA API běží na: `http://192.168.40.144:8123/api/` ✓
- API token uložen v: `.token-ha-api`
- SSH přihlašovací údaje: viz `ssh-config`
- HA je čerstvá instalace — žádná KNX integrace, žádné dashboardy

### Analýza podkladů
- `DB/mistnosti.csv` — 22 místností s KNX skupinovými adresami
- `KNX-Adresy/KNX-adresy.csv` — kompletní mapa KNX skupin
- KNX adresové skupiny zmapovány:
  - 3/1/x = světla (switch binary)
  - 3/2/x = stmívací světla obývák (dim + hodnota)
  - 3/3/x = ventilace
  - 4/0/x = měřená teplota (6 místností)
  - 4/1/x = topení Komfort
  - 4/2/x = topení Standby
  - 4/3/x = topení Noc/Útlum
  - 4/5/x = přepínač Topení/Klima
  - 2/1/x = kontakty oken a dveří
  - 2/2/x = motory vrat
  - 2/3/x = tlačítka vrat (impulz)

### Vytvořené soubory
- `knx-config/knx.yaml` — kompletní KNX entity (30 světel + 2 stmívací, 6 teplotních senzorů, 18 topení spínačů, 4 klima přepínače, 16 kontaktů oken/dveří, 2 ventilace, 2 tlačítka vrat)
- `dashboard/lovelace.yaml` — kompletní Lovelace dashboard (4 views)
- `INSTALACE.md` — postup instalace
- `knx-dummy/knx_dummy.yaml` — dummy entity package (77 entit pro testování bez KNX)

### Stav dashboardu
**Views:**
1. **Domov** — čas/datum, teploty (venkovní + sklep), rychlé přepínače (topení/větrání/světla), kamera, bloky 10 místností + pop-up detaily pro každou
2. **Topení** — přehled a ovládání všech topení módů
3. **Kamery** — 2 kamery (entity: camera.kamera_01, camera.kamera_02)
4. **Nastavení** — ventilace, stavy kontaktů

**Styl:** Glassmorphism (rgba(255,255,255,0.07), backdrop-filter:blur) z priklad-projektu-1 + layout bloků místností z priklad-projektu-2

**Pop-up místnosti (bubble-card v3.2+ standalone):**
- Obývací pokoj, Kuchyň, Dětský pokoj 1, Dětský pokoj 2
- Ložnice, Pracovna, Koupelna 2NP, Garáž, Terasa, Sklep, Kotelna, Vchod
- + globální pop-up pro Topení, Ventilaci, Světla

### Nahrávání na HA (workflow) — AKTUÁLNÍ
Upload YAML + WebSocket save (2 kroky):
```
pscp -pw "Jidl*dEgleo598" -P 22 -hostkey "ssh-ed25519 255 SHA256:ww4XIIQ0SEk3H7YjMwiawiZSN0v8Me5aqcZHKGILOyU" dashboard/lovelace.yaml uzivatel-ssh-api@192.168.40.144:/tmp/lovelace_new.yaml
plink ... "echo 'PASS' | sudo -S python3 /tmp/ws_lovelace_save.py"
```
- Python script `/tmp/update_lovelace.py` — přímý zápis do storage (NEFUNGUJE pro live update)
- Python script `/tmp/ws_lovelace_save.py` — WebSocket API save (funguje ✓)

### Dashboard URL
- Dashboard url_path: `dashboard-dashboard`
- Domov view path: `domov`
- Plná URL: `http://192.168.40.144:8123/dashboard-dashboard/domov`

---

## Aktuální stav řešení (2026-06-24)

### Co funguje ✓
- Glassmorphism styling bloků místností
- Layout 2 místnosti na řadu (grid_options columns: 12)
- Navigation při kliknutí na blok — URL se změní na `#popup-obyvak`, `#popup-topeni` atd.
- Quick-switch tlačítka (Topení/Větrání/Světla) navigují na správný hash
- **Pop-upy fungují** — Bubble Card v3.2 standalone, hash detekce OK
- **Pop-up background tmavý** — bg_color: "rgb(15, 17, 23)", bg_opacity: 93 na každém popup
- **Backdrop tmavý** — CSS var bubble-backdrop-background-color v tématu
- JS chyba `ButtonCardJSTemplateError` opravena — entity?.state místo entity.state
- Bubble Card `bubble-modules.yaml` vytvořen v `/config/www/bubble/`

### Vyřešené technické problémy
- **Pop-up neviditelný**: `bubble-modules.yaml` chybělo → 404 error. Vytvořeno `{}`.
- **Pop-up bílý background**: Bubble Card nastavuje bg inline přes JS (ne CSS). Fix: přidat `bg_color` a `bg_opacity` do každé popup karty v lovelace.yaml.
- **Backdrop šedý**: Bubble Card nastavuje `--bubble-default-backdrop-background-color` inline na body. Fix: nastavit `--bubble-backdrop-background-color` (bez "default") v tématu — ta má CSS prioritu.
- **HA neloaduje config z disku**: HA drží Lovelace config v paměti. Fix: WebSocket API `lovelace/config/save` místo přímého zápisu do storage souboru.
- **JS error ButtonCardJSTemplateError**: `entity.state` bez `?.` v popup-ventilace kartách. Opraveno na `entity?.state`.

### Dummy entity (pro testování bez KNX)
- `/config/packages/knx_dummy.yaml` — 77 dummy entit:
  - 32 `light.*` (template lights backed by input_boolean)
  - 24 `switch.*` (template switches: topení, ventilace, režim)
  - 8 `sensor.*` (teploty, statické hodnoty)
  - 13 `binary_sensor.*` (okna, dveře)
- `configuration.yaml` upraven: `homeassistant: packages: !include_dir_named packages`
- `knx: !include knx-config/knx.yaml` zakomentováno (KNX není nainstalováno)

### Témata — glass_dark.yaml
Přidané proměnné pro Bubble Card (na konci souboru):
```yaml
bubble-pop-up-background-color: "rgba(15, 17, 23, 0.93)"
bubble-secondary-background-color: "rgba(20, 22, 35, 0.88)"
bubble-pop-up-border: "0.5px solid rgba(255, 255, 255, 0.11)"
bubble-pop-up-border-radius: "28px"
bubble-border: "0.5px solid rgba(255, 255, 255, 0.11)"
bubble-border-radius: "28px"
bubble-default-backdrop-background-color: "rgba(0, 0, 0, 0.72)"
bubble-backdrop-background-color: "rgba(0, 0, 0, 0.72)"
```
Poznámka: `bubble-pop-up-background-color` ignoruje HA téma — Bubble Card nastavuje inline přes JS!
Skutečný fix popup background: `bg_color` + `bg_opacity` přímo v popup kartě.

---

## ✓ Hotovo (2026-06-25): Grafy historie teplot + úprava kamery

### Graf venkovní teploty — Domov view
- Přidána nová sekce `column_span: 2` (celá šířka) na konci Domov view (před popupy)
- `type: history-graph`, entity `sensor.teplota_venku`, `hours_to_show: 24`

### Historie teplot v popupech místností
Každý popup s teplotním senzorem má dole novou sekci "Historie teplot":
- `type: custom:bubble-card` separator + `type: history-graph` se dvěma entitami:
  - teplota místnosti (sensor.teplota_ROOM)
  - venkovní teplota (sensor.teplota_venku)
- Popupy s historií: Obývák, Dět. pokoj 1, Dět. pokoj 2, Ložnice, Pracovna, Koupelna 2NP

### Kamera — výška
- `rows` kamerakarty zůstává na **4** (pokusy s rows: 5 přidalo ~56px místo požadovaných 17px, vráceno na původní)
- Graf teploty odstraněn ze sekce s kamerou (přesunut dolů)

### Styl — sjednocení (proběhlo v předchozí session)
- Všechny hardcoded rgba/rgb hodnoty přesunuty do `themes/glass_dark.yaml` jako `mik-` proměnné
- Nový template `ventilace_btn` (nahrazuje 3× inline duplicity)
- `rezim_btn`, `svetlo_btn`, `mistnost_karta` převedeny na `var(--mik-*)`
- Deploy script: `python scripts/deploy.py [theme|lovelace]` — nahraje a reloaduje

## Co ještě chybí / TODO
- [ ] Nainstalovat KNX integraci v HA (přes UI)
- [ ] Zkopírovat knx.yaml config a odkomentovat v configuration.yaml
- [ ] Doladit entity_id po importu KNX (ověřit v Vývojářské nástroje → Stavy)
- [ ] Nastavit kamery (ONVIF integrace pro Partizán)
- [ ] Přidat venkovní teplotu (OpenWeatherMap nebo KNX senzor)
- [ ] Ovládání vrat garáže a brány vjezd (button entity — dočasně chybí)
- [ ] Přidat místnosti bez pop-upu: Komora, Šatna, Balkon, WC, Chodba patro, Schodiště
- [ ] Popup pro okna (globální) — zatím Okna tlačítko naviguje na Nastavení view

## ✓ Hotovo (2026-06-25): Rozvrhy a plány topení + ventilace

Nový balíček `packages/heating_schedule.yaml`:
- YAML sekce `schedule:` ODSTRANĚNA (YAML schedule není editovatelný z UI)
- 6 `input_select.topeni_plan_*`: options [Ruční, Vlastní, Společný], initial Ruční
- 14 automations: rozvrh ON/OFF → změna režimu (s podmínkou plánu), okamžitá aplikace při změně plánu, ventilace rozvrh → switch
- Nový button-card template `plan_btn` v lovelace.yaml
- Topení view: pro každou místnost přidána sekce "Plán" (3 tlačítka + entity rozvrhu)
- Fan animace (wrapper div line-height:0) na ALL ventilačních tlačítkách (popup-ventilace, popup-sklep, Nastavení)
- Rozvrh entity pod každým ventilačním tlačítkem

### Schedule helpers — storage mode (UI-editovatelné)
Vytvořeny přes `scripts/create_schedules.py` — přímý zápis do `.storage/core.config_entries`:
- 9 schedule entries injektovány (19 celkem v souboru)
- **ČEKÁ NA RESTART HA** pro načtení nových entit
- Po restartu ověřit: Nastavení → Pomocníci → filtr Rozvrh → musí jít editovat

Entry IDs (pro případ ruční opravy):
- Topení společný:      01KVXVX2RD8DT9YH4VENFX4982  (výchozí Po-Pá 06-22, So-Ne 07-22)
- Topení obývák:        01KVXVX2RD2YXRCMM1MJME4SKD
- Topení dp1:           01KVXVX2RD33TYGB5E7QVH3HVM
- Topení dp2:           01KVXVX2RD84RB6D4DP5PGG0FW
- Topení ložnice:       01KVXVX2RD11DB0C19FWVGZ44Q
- Topení pracovna:      01KVXVX2RD2V51ZE99S6S70EV4
- Topení koupelna 2NP:  01KVXVX2RDJVY9JA1F6E4KYJKG
- Ventilace sklep:      01KVXVX2RDH3MH6P3CGN83WSAT
- Ventilace koupelna 1NP: 01KVXVX2RD066JECXR25SD92QS

### Logika plánování
- `Ruční` → schedule automations blokované (podmínka nesplněna), uživatel nastavuje manuálně
- `Vlastní` → lokální `schedule.topeni_ROOM` řídí režim
- `Společný` → `schedule.topeni_spolecny` řídí režim
- Při přepnutí z Ruční → Vlastní/Společný: okamžitě aplikuje aktuální stav rozvrhu

### Entity IDs v HA (po restartu)
Schedule entity_id se generuje z názvu:
- "Topení společný"      → `schedule.topeni_spolecny`
- "Topení obývák"        → `schedule.topeni_obyvak`
- "Topení dp1"           → `schedule.topeni_dp1`
- "Topení dp2"           → `schedule.topeni_dp2`
- "Topení ložnice"       → `schedule.topeni_loznice`
- "Topení pracovna"      → `schedule.topeni_pracovna`
- "Topení koupelna 2NP"  → `schedule.topeni_koupelna_2np`
- "Ventilace sklep"      → `schedule.ventilace_sklep`
- "Ventilace koupelna 1NP" → `schedule.ventilace_koupelna_1np`

## ✓ Hotovo (2026-06-25): Chlazení + redesign karet místností + okna

### Chlazení — Režim klima
- KNX entity `4/5/x` (switch.rezim_topeni_dp1/dp2/loznice/pracovna):
  - **ON = chlazení**, OFF = topení (opravená logika, předchozí bylo obráceně)
- Separátory "Topení" → **"Režim klima"** v popupech dp1, dp2, loznice, pracovna
- View tab přejmenován na **"Režim klima"**, navigační chip na "Klima"
- Globální popup: "Topení / Klima"
- Na kartičkách místností: ikona vločky `mdi:snowflake` (modrá) se zobrazí před ikonou režimu když `switch.rezim_topeni_XXX == on`
- Nová proměnná `var_klima` v `mistnost_karta` (dp1, dp2, loznice, pracovna mají vyplněno)

### Okna — kontakty
- **Logika**: `off` = otevřeno (červená), `on` = zavřeno (zelená) — normálně-zavřený kontakt KNX
- Nový template `okno_btn` — readonly (tap/hold/double_tap: none), cursor: default, ripple potlačen, výška 50px jako světla
- Popupy (7 místností): nahrazena `type: entities` sekce za `horizontal-stack` + `okno_btn`
- Kartičky místností: ikona okna (`mdi:window-open` červeně) se zobrazí **pouze když je otevřeno**; sloučena do pravého clusteru s vločkou a režimem
- 9 místností má `var_sensor_okna` (dp1 kontroluje oba kontakty: "binary_sensor.okno_dp1_a,binary_sensor.okno_dp1_b")
- **4. rychlý přepínač "Okna"** na Domov view (za Světla): kontroluje všech 10 kontaktů, naviguje na Nastavení

### Redesign `mistnost_karta` template
- **Žárovka** přesunuta inline před název (HTML v `name` poli), `margin-top:-5px`
- **Teplota**: font 22px bold, zarovnaná vlevo, `padding-left:3px`
- **Pravý cluster** (60px): okno (jen pokud open) + vločka (jen při chlazení) + ikona režimu
- Grid zjednodušen: `1fr 60px` (dříve `30px 1fr 28px 50px`)
- Žárovka nesvítí → bílá/šedá (`var(--mik-btn-icon)`), svítí → zlatá

### Technické opravy
- WebSocket save script (`scripts/ws_lovelace_save.py`) opraven: buffer leftover po HTTP upgrade
- Background `lovelace-background` ztmaven (~30%): `#080a1c / #230860 / #081858`

## KNX adresování — schéma dekódování z CSV
Format v mistnosti.csv: X*100000 + Y*1000 + Z = KNX adresa X/Y/Z
Příklad: 301029 = 3/1/29 = "SV obyv.1.3" (světlo obývák)

## Hardware
- HA Green na: http://192.168.40.144:8123/
- KNX připojení: KNX/IP Router (autodiscovery v HA)
- Kamery: Partizán (ONVIF integrace)

## Prerekvizity HACS
- custom:button-card
- custom:bubble-card
- card-mod (volitelný)

## Klíčové technické detaily

### dashboard/lovelace.yaml struktura
- `button_card_templates`: `mistnost_karta`, `svetlo_btn`, `okno_btn`, `rezim_btn`, `topeni_mode_btn`, `plan_btn`, `ventilace_btn`
- `mistnost_karta` proměnné: `var_name`, `var_navigate`, `var_sensor_svetla`, `var_sensor_teplota`, `var_sensor_komfort/standby/noc`, `var_klima`, `var_sensor_okna`
- `mistnost_karta` grid: `1fr 60px` — teplota vlevo, pravý cluster (okno+vločka+režim) vpravo
- Žárovka icon inline v `name` poli (HTML), zobrazuje se vždy
- SEKCE 3: bloky místností, `grid_options: columns: 12` (2 místnosti na řadu)
- SEKCE 4: všechny pop-upy v jedné `type: grid column_span: 2` sekci

### Bubble Card popup config (důležité!)
Každý popup musí mít:
```yaml
bg_color: "rgb(15, 17, 23)"
bg_opacity: 93
```
Bez tohoto Bubble Card ignoruje téma a použije světlou barvu!

### WebSocket save script
`/tmp/ws_lovelace_save.py` — persistentní na HA, volá `lovelace/config/save`
Použití po každém uploadu lovelace.yaml:
```
plink ... "echo 'PASS' | sudo -S python3 /tmp/ws_lovelace_save.py"
```

### bubble-modules.yaml
`/config/www/bubble/bubble-modules.yaml` — nutný pro Bubble Card v3.2+, obsah: `{}`
