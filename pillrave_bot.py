#!/usr/bin/env python3
"""
PILLRAVE Telegram Bot — Railway Edition
========================================
Variables de entorno en Railway:
  BOT_TOKEN  — token de BotFather
  CHAT_ID    — ID del grupo (opcional)
"""
import os, time, json, sys
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN", "PEGA_TU_NUEVO_TOKEN_AQUI")
CHAT_ID   = os.environ.get("CHAT_ID", None)
WEB_URL   = "https://cyberavers.online.com"
PUMP_URL  = "https://pump.fun"
API       = f"https://api.telegram.org/bot{BOT_TOKEN}"

SECTIONS = {
"bienvenida": (
"👋 *Bienvenido al grupo oficial de PILLRAVE*\n\n"
"💊 El token de la música electrónica en Solana\n\n"
"Comandos:\n"
"/info — Historia\n"
"/token — Tokenomics\n"
"/roadmap — Roadmap\n"
"/comprar — Cómo comprar\n"
"/web — Web oficial\n\n"
f"🌐 {WEB_URL}\n"
"📱 @CYBERRAVERS en Instagram\n"
"🐦 @CyberRaversNFT en X"
),
"hero": (
"💊 *PILLRAVE \\($PILL\\)*\n\n"
"_La nostalgia del 99, descongelada para sanar la economía del 2026\\._\n"
"*Infraestructura real, valor directo al artista\\.*\n\n"
"🌐 Solana Blockchain\n"
"📦 909M Supply Total\n"
"✅ Distribución 100% justa\n"
"🔓 Sin wallets de equipo bloqueadas\n"
"🎵 Royalties on\\-chain para productores\n\n"
f"🔗 [Comprar en Pump\\.fun]({PUMP_URL})"
),
"about": (
"❄️ *THE FROZEN ARE BACK*\n\n"
"En 1992, la música electrónica no era un negocio, era un código de libertad\\.\n\n"
"En los 90, la policía cerraba los clubes a las 2 AM\\. Las Berkshire Mountains "
"ofrecían la libertad de bailar bajo las estrellas sin que nadie tocara a la puerta\\.\n\n"
"Hoy, *PILLRAVE* es el descongelamiento de esa visión\\.\n"
"La PILL es el antídoto\\. La señal ha vuelto\\.\n\n"
"🎵 Berkshire Mountain, MA — 12\\.31\\.1999 — 06:13 AM"
),
"token": (
"📊 *TOKENOMICS $PILL*\n\n"
"🟢 Venta pública: *80%* — 727\\.2M tokens\n"
"🔵 Equipo & Dev: *15%* — 136\\.35M \\(vesting 12 meses\\)\n"
"🔴 Airdrops & Rewards: *10%* — 90\\.9M tokens\n\n"
"📦 Supply total: *909,000,000 $PILL*\n"
"⛓️ Blockchain: *Solana*\n"
"🚀 Plataforma: *Pump\\.fun*\n\n"
"Distribución 100% justa\\. Sin wallets bloqueadas\\."
),
"roadmap": (
"🗺️ *ROADMAP PILLRAVE*\n\n"
"✅ *FASE 0 — AHORA*\n"
"• Token en Solana vía Pump\\.fun\n"
"• Landing & branding activo\n\n"
"🔜 *FASE 1 — Q3 2026*\n"
"• App demo iOS/Android\n"
"• Primeros airdrops\n"
"• Primer festival piloto\n\n"
"🔮 *FASE 2 — Q1 2027*\n"
"• Staking activo\n"
"• Dashboard productores\n"
"• DAO lanzada\n\n"
"🚀 *FASE 3 — 2027\\+*\n"
"• Festivales grandes\n"
"• App pública global\n"
"• Estándar global de royalties"
),
"comprar": (
"🛒 *CÓMO COMPRAR $PILL*\n\n"
"*1\\.* Instala *Phantom* o *Solflare* \\(wallet Solana\\)\n"
"*2\\.* Compra algo de *SOL* para el gas\n"
"*3\\.* Ve a Pump\\.fun y busca *$PILL*\n"
"*4\\.* Compra y HOLD 💊\n\n"
f"🔗 [Pump\\.fun]({PUMP_URL})\n"
f"🌐 [pillrave\\.com]({WEB_URL})\n\n"
"_Sin intermediarios\\. Sin KYC\\. 100% on\\-chain\\._"
),
}

def menu():
    return {"inline_keyboard":[
        [{"text":"💊 Comprar $PILL","url":PUMP_URL},{"text":"🌐 Web","url":WEB_URL}],
        [{"text":"📊 Tokenomics","callback_data":"token"},{"text":"🗺️ Roadmap","callback_data":"roadmap"}],
        [{"text":"📱 Instagram","url":"https://instagram.com/cybarravers"},{"text":"🐦 X","url":"https://x.com/CyberRaversNFT"}],
    ]}

def send_md(cid, txt, rm=None):
    d={"chat_id":cid,"text":txt,"parse_mode":"MarkdownV2","disable_web_page_preview":False}
    if rm: d["reply_markup"]=json.dumps(rm)
    try: return requests.post(f"{API}/sendMessage",json=d,timeout=15).json()
    except Exception as e: print(f"[ERR] {e}")

def send(cid,txt):
    try: return requests.post(f"{API}/sendMessage",json={"chat_id":cid,"text":txt},timeout=15).json()
    except Exception as e: print(f"[ERR] {e}")

def get_upd(offset=None):
    p={"timeout":30,"allowed_updates":["message","callback_query"]}
    if offset: p["offset"]=offset
    try: return requests.get(f"{API}/getUpdates",params=p,timeout=35).json()
    except: return None

saved_cid = CHAT_ID

def save(cid):
    global saved_cid; saved_cid=str(cid)
    try:
        with open("/tmp/cid.txt","w") as f: f.write(str(cid))
    except: pass
    print(f"[INFO] Chat ID: {cid}")

def load():
    global saved_cid
    if saved_cid: return saved_cid
    try:
        with open("/tmp/cid.txt") as f: saved_cid=f.read().strip(); return saved_cid
    except: return None

def handle(msg):
    cid  = msg["chat"]["id"]
    txt  = msg.get("text","").strip().split("@")[0].lower()
    user = msg.get("from",{}).get("first_name","Raver")
    print(f"[MSG] {user}: {txt}")
    if not load(): save(cid)
    if txt in ("/start","/help"):        send_md(cid,SECTIONS["bienvenida"],menu())
    elif txt in ("/info","/about"):      send_md(cid,SECTIONS["about"])
    elif txt in ("/token","/tokenomics"):send_md(cid,SECTIONS["token"])
    elif txt=="/roadmap":                send_md(cid,SECTIONS["roadmap"])
    elif txt in ("/comprar","/buy"):     send_md(cid,SECTIONS["comprar"])
    elif txt in ("/pillrave","/pill"):   send_md(cid,SECTIONS["hero"],menu())
    elif txt=="/web":                    send(cid,f"🌐 {WEB_URL}")
    elif txt=="/chatid":                 send(cid,f"Chat ID: {cid}")
    elif txt.startswith("/anuncio "):
        msg_txt=msg.get("text","")[9:]
        c=load()
        if c: send_md(c,f"📢 *ANUNCIO*\n\n{msg_txt}")

def handle_cb(cb):
    cid=cb["message"]["chat"]["id"]; d=cb.get("data","")
    try: requests.post(f"{API}/answerCallbackQuery",json={"callback_query_id":cb["id"]},timeout=10)
    except: pass
    if d=="token":   send_md(cid,SECTIONS["token"])
    elif d=="roadmap": send_md(cid,SECTIONS["roadmap"])

def broadcast(cid):
    print(f"[BROADCAST] → {cid}")
    for i,k in enumerate(["bienvenida","about","token","roadmap","comprar"]):
        time.sleep(2)
        if k=="bienvenida": send_md(cid,SECTIONS[k],menu())
        else: send_md(cid,SECTIONS[k])
        print(f"  [{i+1}/5] {k} ✓")
    print("[BROADCAST] Listo.")

def main():
    print("="*50)
    print("  💊 PILLRAVE BOT — Railway Edition")
    print(f"  Token: {BOT_TOKEN[:20]}...")
    print("="*50)
    try:
        me=requests.get(f"{API}/getMe",timeout=10).json()
        if me.get("ok"): print(f"[OK] @{me['result']['username']} activo")
        else: print("[ERR] Token inválido"); return
    except Exception as e: print(f"[ERR] {e}"); return
    print("[INFO] Escuchando... (Ctrl+C para detener)\n")
    offset=None
    while True:
        try:
            upds=get_upd(offset)
            if upds and upds.get("ok"):
                for u in upds["result"]:
                    offset=u["update_id"]+1
                    if "message" in u: handle(u["message"])
                    elif "callback_query" in u: handle_cb(u["callback_query"])
        except KeyboardInterrupt: print("\n[INFO] Detenido."); break
        except Exception as e: print(f"[ERR] {e}"); time.sleep(5)

if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=="broadcast":
        c=load()
        if c: broadcast(c)
        else: print("[ERR] Escribe /start en el grupo primero.")
    else: main()
