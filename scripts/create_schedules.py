#!/usr/bin/env python3
"""
Injektuje schedule config entries přímo do .storage/core.config_entries.
Spustit na HA serveru, pak restartovat HA.

Použití: python3 /tmp/create_schedules.py && reboot_ha
"""

import json, os, time, uuid, shutil
from datetime import datetime, timezone

STORAGE = "/root/config/.storage/core.config_entries"
BACKUP  = STORAGE + ".bak"

DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

SCHEDULES = [
    {
        "name": "Topení společný", "icon": "mdi:calendar-multiple",
        "monday":    [{"from": "06:00:00", "to": "22:00:00"}],
        "tuesday":   [{"from": "06:00:00", "to": "22:00:00"}],
        "wednesday": [{"from": "06:00:00", "to": "22:00:00"}],
        "thursday":  [{"from": "06:00:00", "to": "22:00:00"}],
        "friday":    [{"from": "06:00:00", "to": "22:00:00"}],
        "saturday":  [{"from": "07:00:00", "to": "22:00:00"}],
        "sunday":    [{"from": "07:00:00", "to": "22:00:00"}],
    },
    {"name": "Topení obývák",          "icon": "mdi:sofa"},
    {"name": "Topení dp1",             "icon": "mdi:bed"},
    {"name": "Topení dp2",             "icon": "mdi:bed"},
    {"name": "Topení ložnice",         "icon": "mdi:bed-king"},
    {"name": "Topení pracovna",        "icon": "mdi:desk-lamp"},
    {"name": "Topení koupelna 2NP",    "icon": "mdi:shower"},
    {"name": "Ventilace sklep",        "icon": "mdi:fan"},
    {"name": "Ventilace koupelna 1NP", "icon": "mdi:fan"},
]

CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

def gen_ulid():
    """Generate a ULID-compatible entry_id."""
    t = int(time.time() * 1000)
    r = int.from_bytes(os.urandom(10), 'big')
    result = []
    for _ in range(10):   # 10 timestamp chars
        result.insert(0, CROCKFORD[t % 32])
        t //= 32
    for _ in range(16):   # 16 random chars
        result.append(CROCKFORD[r % 32])
        r //= 32
    return ''.join(result)

def now_iso():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', '+00:00')

def make_entry(s):
    ts = now_iso()
    options = {"name": s["name"], "icon": s.get("icon", "")}
    for day in DAYS:
        if day in s:
            options[day] = s[day]
    return {
        "created_at": ts,
        "data": {},
        "disabled_by": None,
        "discovery_keys": {},
        "domain": "schedule",
        "entry_id": gen_ulid(),
        "minor_version": 1,
        "modified_at": ts,
        "options": options,
        "pref_disable_new_entities": False,
        "pref_disable_polling": False,
        "source": "user",
        "subentries": [],
        "title": s["name"],
        "unique_id": None,
        "version": 1,
    }

def main():
    if not os.path.exists(STORAGE):
        print(f"CHYBA: Storage soubor nenalezen: {STORAGE}")
        return

    # Backup
    shutil.copy2(STORAGE, BACKUP)
    print(f"Záloha: {BACKUP}")

    with open(STORAGE, encoding="utf-8") as f:
        data = json.load(f)

    entries = data["data"]["entries"]

    # Smaž existující schedule config entries (pokud jsou)
    orig_count = len(entries)
    entries = [e for e in entries if e.get("domain") != "schedule"]
    removed = orig_count - len(entries)
    if removed:
        print(f"Odstraněno {removed} starých schedule entries")

    # Přidej nové
    for s in SCHEDULES:
        entry = make_entry(s)
        entries.append(entry)
        print(f"[+] {s['name']}  (entry_id: {entry['entry_id']})")

    data["data"]["entries"] = entries
    # Inkrementuj verzi storage souboru
    data["version"] = data.get("version", 1)

    with open(STORAGE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nStorage aktualizován ({len(entries)} entries celkem).")
    print("→ Restart HA pro načtení nových entit.")

if __name__ == "__main__":
    main()
