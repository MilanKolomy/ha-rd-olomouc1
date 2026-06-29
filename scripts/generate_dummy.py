"""Generátor knx_dummy.yaml package pro HA testování dashboardu."""

lights = [
    "svetlo_obyvak_1", "svetlo_obyvak_2", "svetlo_obyvak_3",
    "svetlo_obyvak_dim_1", "svetlo_obyvak_dim_2",
    "svetlo_kuchyn_central", "svetlo_kuchyn_linka_p", "svetlo_kuchyn_linka_l", "svetlo_kuchyn_bar",
    "svetlo_detsky_pokoj_1", "svetlo_detsky_pokoj_2",
    "svetlo_loznice", "svetlo_satna", "svetlo_pracovna",
    "svetlo_koupelna_2np_strop", "svetlo_koupelna_2np_zrcadlo",
    "svetlo_koupelna_1np_strop", "svetlo_koupelna_1np_zrcadlo",
    "svetlo_wc", "svetlo_garaz",
    "svetlo_vchod", "svetlo_vchod_bok",
    "svetlo_terasa", "svetlo_sklep", "svetlo_schodiste_sklep",
    "svetlo_kotelna", "svetlo_komora",
    "svetlo_chodba", "svetlo_chodba_patro",
    "svetlo_balkon", "zasuvka_venku", "svetlo_hala",
]

switches = [
    "topeni_komfort_obyvak", "topeni_standby_obyvak", "topeni_noc_obyvak",
    "topeni_komfort_dp1",    "topeni_standby_dp1",    "topeni_noc_dp1",
    "topeni_komfort_dp2",    "topeni_standby_dp2",    "topeni_noc_dp2",
    "topeni_komfort_loznice","topeni_standby_loznice","topeni_noc_loznice",
    "topeni_komfort_pracovna","topeni_standby_pracovna","topeni_noc_pracovna",
    "topeni_komfort_koupelna_2np","topeni_standby_koupelna_2np","topeni_noc_koupelna_2np",
    "rezim_topeni_dp1", "rezim_topeni_dp2", "rezim_topeni_pracovna", "rezim_topeni_loznice",
    "ventilace_sklep", "ventilace_koupelna_1np",
]

temperatures = {
    "teplota_obyvak": 21.5,
    "teplota_detsky_pokoj_1": 20.8,
    "teplota_detsky_pokoj_2": 21.2,
    "teplota_loznice": 19.5,
    "teplota_pracovna": 22.0,
    "teplota_koupelna_2np": 23.5,
    "teplota_venku": 12.3,
    "teplota_sklep": 16.8,
}

binary_sensors = [
    ("okno_obyvak",          "window"),
    ("okno_kuchyn",          "window"),
    ("okno_dp1_a",           "window"),
    ("okno_dp1_b",           "window"),
    ("okno_dp2",             "window"),
    ("okno_loznice",         "window"),
    ("okno_pracovna",        "window"),
    ("okno_terasa",          "window"),
    ("okno_garaz",           "window"),
    ("okno_kotelna",         "window"),
    ("dvere_terasa",         "door"),
    ("dvere_vstup",          "door"),
    ("vrata_garaz_kontakt",  "garage_door"),
]

lines = ["# KNX Dummy entities — pro testování dashboardu bez KNX integrace", ""]

# ── input_boolean ─────────────────────────────────────────────────────────────
lines += ["input_boolean:"]
for name in lights:
    lines += [f"  {name}:", f"    name: \"{name}\"", f"    initial: false"]
for name in switches:
    lines += [f"  {name}:", f"    name: \"{name}\"", f"    initial: false"]
for name, _ in binary_sensors:
    lines += [f"  {name}:", f"    name: \"{name}\"", f"    initial: false"]
lines.append("")

# ── template ──────────────────────────────────────────────────────────────────
lines += ["template:"]

# --- lights ---
lines.append("  - light:")
for name in lights:
    lines += [
        f"      - name: \"{name}\"",
        f"        unique_id: dummy_{name}",
        f"        state: \"{{{{ is_state('input_boolean.{name}', 'on') }}}}\"",
        f"        turn_on:",
        f"          service: input_boolean.turn_on",
        f"          target:",
        f"            entity_id: input_boolean.{name}",
        f"        turn_off:",
        f"          service: input_boolean.turn_off",
        f"          target:",
        f"            entity_id: input_boolean.{name}",
    ]

# --- switches ---
lines.append("  - switch:")
for name in switches:
    lines += [
        f"      - name: \"{name}\"",
        f"        unique_id: dummy_{name}",
        f"        state: \"{{{{ is_state('input_boolean.{name}', 'on') }}}}\"",
        f"        turn_on:",
        f"          service: input_boolean.turn_on",
        f"          target:",
        f"            entity_id: input_boolean.{name}",
        f"        turn_off:",
        f"          service: input_boolean.turn_off",
        f"          target:",
        f"            entity_id: input_boolean.{name}",
    ]

# --- sensors ---
lines.append("  - sensor:")
for name, value in temperatures.items():
    lines += [
        f"      - name: \"{name}\"",
        f"        unique_id: dummy_{name}",
        f"        state: \"{value}\"",
        f"        unit_of_measurement: \"°C\"",
        f"        device_class: temperature",
        f"        state_class: measurement",
    ]

# --- binary sensors ---
lines.append("  - binary_sensor:")
for name, device_class in binary_sensors:
    lines += [
        f"      - name: \"{name}\"",
        f"        unique_id: dummy_{name}",
        f"        state: \"{{{{ is_state('input_boolean.{name}', 'on') }}}}\"",
        f"        device_class: {device_class}",
    ]

yaml_content = "\n".join(lines) + "\n"

out_path = "C:/project/HA-michal/knx-dummy/knx_dummy.yaml"
import os
os.makedirs("C:/project/HA-michal/knx-dummy", exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(yaml_content)

# Ověření YAML validity
import yaml
yaml.safe_load(yaml_content)

entity_count = len(lights) + len(switches) + len(temperatures) + len(binary_sensors)
print(f"OK - {entity_count} entit vygenerovano: {out_path}")
print(f"  lights: {len(lights)}, switches: {len(switches)}, sensors: {len(temperatures)}, binary_sensors: {len(binary_sensors)}")
