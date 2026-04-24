#!/usr/bin/env python3
import os, time, json, sys, urllib.request, urllib.error

BOT_TOKEN = os.environ.get("BOT_TOKEN") or "8701250025:AAGQQTzKvLmnuEt_VPPHD3BWurUnWSEldkA"
WEB_URL   = "https://cyberavers.online.com"
PUMP_URL  = "https://pump.fun"
API       = "https://api.telegram.org/bot" + BOT_TOKEN

MSGS = {
"start": (
"Bienvenido al grupo oficial de PILLRAVE\n\n"
"El token de la musica electronica en Solana\n\n"
"Comandos:\n"
"/info - Historia del proyecto\n"
"/token - Tokenomics\n"
"/roadmap - Las 4 fases\n"
"/comprar - Como comprar $PILL\n"
"/web - Web oficial\n\n"
"pillrave.com\n"
"Instagram: @CYBERRAVERS\n"
"Twitter: @CyberRaversNFT"
),
"info": (
"THE FROZEN ARE BACK\n\n"
"En 1992 la musica electronica era un codigo de libertad.\n\n"
"En los 90, la policia cerraba los clubes a las 2 AM.\n"
"Las Berkshire Mountains ofrecian bailar bajo las estrellas\n"
"sin que nadie tocara a la puerta.\n\n"
"Hoy PILLRAVE es el descongelamiento de esa vision.\n"
"La senal ha vuelto.\n\n"
"Berkshire Mountain, MA - 12.31.1999 - 06:13 AM"
),
"token": (
"TOKENOMICS $PILL\n\n"
"Venta publica: 80% - 727.2M tokens\n"
"Equipo y Dev: 15% - 136.35M (vesting 12 meses)\n"
"Airdrops y Rewards: 10% - 90.9M tokens\n\n"
"Supply total: 909,000,000 $PILL\n"
"Blockchain: Solana\n"
"Plataforma: Pump.fun\n\n"
"Distribucion 100% justa. Sin wallets bloqueadas."
),
"roadmap": (
"ROADMAP PILLRAVE\n\n"
"FASE 0 - AHORA\n"
"- Token en Solana via Pump.fun\n"
"- Landing y branding activo\n\n"
"FASE 1 - Q3 2026\n"
"- App demo iOS/Android\n"
"- Primeros airdrops\n"
"- Primer festival piloto\n\n"
"FASE 2 - Q1 2027\n"
"- Staking activo\n"
"- Dashboard productores\n"
"- DAO lanzada\n\n"
"FASE 3 - 2027+\n"
"- Festivales grandes\n"
"- App publica global\n"
"- Estandar global de royalties"
),
"comprar": (
"COMO COMPRAR $PILL\n\n"
"1. Instala Phantom o Solflare (wallet Solana)\n"
"2. Compra algo de SOL para el gas\n"
"3. Ve a pump.fun y busca $PILL\n"
"4. Compra y HOLD\n\n"
"pump.fun\n"
"pillrave.com\n\n"
"Sin KYC. Sin intermediarios. 100% on-chain."
),
}

def call(m, d=None):
    url = API + "/" + m
    p = json.dumps(d).encode() if d else None
    h = {"Content-Type": "application/json", "User-Agent": "PillBot"}
    try:
        req = urllib.request.Request(url, p, h)
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print("[ERR] HTTP " + str(e.code) + ": " + e.read().decode()[:100])
        return None
    except Exception as e:
        print("[ERR] " + str(e))
        return None

def send(cid, txt):
    return call("sendMessage", {"chat_id": cid, "text": txt})

def send_menu(cid, txt):
    return call("sendMessage", {
        "chat_id": cid,
        "text": txt,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "Comprar $PILL", "url": PUMP_URL}, {"text": "Web oficial", "url": WEB_URL}],
                [{"text": "Instagram", "url": "https://instagram.com/cybarravers"}, {"text": "Twitter/X", "url": "https://x.com/CyberRaversNFT"}]
            ]
        }
    })

def get_upd(off=None):
    d = {"timeout": 30, "allowed_updates": ["message"]}
    if off:
        d["offset"] = off
    p = json.dumps(d).encode()
    h = {"Content-Type": "application/json", "User-Agent": "PillBot"}
    try:
        req = urllib.request.Request(API + "/getUpdates", p, h)
        with urllib.request.urlopen(req, timeout=35) as r:
            return json.loads(r.read())
    except Exception as e:
        print("[ERR] getUpdates: " + str(e))
        return None

saved = None

def save(cid):
    global saved
    saved = str(cid)
    try:
        with open("/tmp/pillcid.txt", "w") as f:
            f.write(str(cid))
    except:
        pass
    print("[INFO] Chat ID guardado: " + str(cid))

def load():
    global saved
    if saved:
        return saved
    try:
        with open("/tmp/pillcid.txt") as f:
            saved = f.read().strip()
            return saved
    except:
        return None

def handle(msg):
    cid  = msg["chat"]["id"]
    txt  = msg.get("text", "").strip().split("@")[0].lower()
    user = msg.get("from", {}).get("first_name", "Raver")
    print("[MSG] " + user + ": " + txt)
    if not load():
        save(cid)
    if txt in ("/start", "/help"):
        send_menu(cid, MSGS["start"])
    elif txt in ("/info", "/about"):
        send(cid, MSGS["info"])
    elif txt in ("/token", "/tokenomics"):
        send(cid, MSGS["token"])
    elif txt == "/roadmap":
        send(cid, MSGS["roadmap"])
    elif txt in ("/comprar", "/buy"):
        send(cid, MSGS["comprar"])
    elif txt == "/web":
        send(cid, WEB_URL)
    elif txt == "/chatid":
        send(cid, "Chat ID: " + str(cid))
    elif txt.startswith("/anuncio "):
        c = load()
        if c:
            send(int(c), "ANUNCIO PILLRAVE\n\n" + msg.get("text", "")[9:])

def main():
    print("==================================================")
    print("  PILLRAVE BOT - Railway Edition")
    print("  Token activo: " + BOT_TOKEN[:20] + "...")
    print("==================================================")
    me = call("getMe")
    if not me or not me.get("ok"):
        print("[ERR] Token invalido: " + str(me))
        return
    print("[OK] Bot activo: @" + me["result"]["username"])
    c = load()
    print("[OK] Chat ID previo: " + str(c or "ninguno"))
    print("[INFO] Escuchando mensajes...\n")
    off = None
    while True:
        try:
            r = get_upd(off)
            if r and r.get("ok"):
                for u in r["result"]:
                    off = u["update_id"] + 1
                    if "message" in u:
                        handle(u["message"])
        except KeyboardInterrupt:
            print("Detenido.")
            break
        except Exception as e:
            print("[ERR] " + str(e))
            time.sleep(5)

if __name__ == "__main__":
    main()
