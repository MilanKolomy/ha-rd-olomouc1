#!/usr/bin/env python3
"""
Deploy skript pro HA-michal projekt.
Nahraje téma a/nebo lovelace dashboard na HA server.

Použití:
  python scripts/deploy.py theme        # jen téma
  python scripts/deploy.py lovelace     # jen lovelace
  python scripts/deploy.py              # obojí
"""

import subprocess, sys, urllib.request, urllib.error, json, os

# ── Konfigurace ────────────────────────────────────────────────
HA_HOST    = "192.168.40.144"
HA_PORT    = 22
HA_USER    = "uzivatel-ssh-api"
HA_PASS    = "Jidl*dEgleo598"
HA_HOSTKEY = "ssh-ed25519 255 SHA256:ww4XIIQ0SEk3H7YjMwiawiZSN0v8Me5aqcZHKGILOyU"
HA_URL     = f"http://{HA_HOST}:8123"

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_FILE = os.path.join(BASE_DIR, ".token-ha-api")

THEME_LOCAL  = os.path.join(BASE_DIR, "themes", "glass_dark.yaml")
THEME_REMOTE = "/root/config/themes/glass_dark.yaml"

LOVELACE_LOCAL  = os.path.join(BASE_DIR, "dashboard", "lovelace.yaml")
LOVELACE_REMOTE = "/tmp/lovelace_new.yaml"
WS_SAVE_SCRIPT  = "/tmp/ws_lovelace_save.py"

PSCP  = "pscp"
PLINK = "plink"

SSH_OPTS = ["-pw", HA_PASS, "-P", str(HA_PORT), "-hostkey", HA_HOSTKEY]

# ── Pomocné funkce ─────────────────────────────────────────────

def run(cmd, desc=""):
    print(f"  > {desc or ' '.join(cmd[:3])}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"    CHYBA: {r.stderr.strip() or r.stdout.strip()}")
        sys.exit(1)
    return r.stdout.strip()

def scp_upload(local, remote_tmp):
    run([PSCP] + SSH_OPTS + [local, f"{HA_USER}@{HA_HOST}:{remote_tmp}"],
        f"upload {os.path.basename(local)}")

def ssh(command, desc=""):
    run([PLINK] + SSH_OPTS + [f"{HA_USER}@{HA_HOST}", command], desc)

def ha_service(service, payload=None):
    token = open(TOKEN_FILE).read().strip()
    domain, action = service.split("/")
    url = f"{HA_URL}/api/services/{domain}/{action}"
    body = json.dumps(payload or {}).encode()
    req = urllib.request.Request(url, data=body, method="POST",
          headers={"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
        return True
    except urllib.error.URLError as e:
        print(f"    API chyba: {e}")
        return False

# ── Akce ──────────────────────────────────────────────────────

def deploy_theme():
    print("\n[ Téma ]")
    scp_upload(THEME_LOCAL, "/tmp/glass_dark.yaml")
    ssh(f"echo '{HA_PASS}' | sudo -S cp /tmp/glass_dark.yaml {THEME_REMOTE}",
        "kopírovat na cílové místo")
    print("  > reload_themes (API)")
    if ha_service("frontend/reload_themes"):
        print("  OK Tema nahrano a reloadovano")
    else:
        print("  ! Reload selhal - udělej Ctrl+F5 v prohlizeci")

def deploy_lovelace():
    print("\n[ Lovelace ]")
    scp_upload(LOVELACE_LOCAL, LOVELACE_REMOTE)
    ssh(f"echo '{HA_PASS}' | sudo -S python3 {WS_SAVE_SCRIPT}",
        "uložit přes WebSocket API")
    print("  OK Lovelace nahrano")

# ── Main ──────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if not args:
        deploy_theme()
        deploy_lovelace()
    elif "theme" in args:
        deploy_theme()
    elif "lovelace" in args:
        deploy_lovelace()
    else:
        print(f"Neznámý argument: {args}")
        print(__doc__)
        sys.exit(1)
    print()

if __name__ == "__main__":
    main()
