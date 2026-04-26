#!/usr/bin/env python3
import os, time, json, sys, urllib.request, urllib.error
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN") or "8701250025:AAGQQTzKvLmnuEt_VPPHD3BWurUnWSEldkA"
WEB_URL   = "https://cyberavers.online"
PUMP_URL  = "https://pump.fun"
API       = "https://api.telegram.org/bot" + BOT_TOKEN

# ─── TRACK DEL DIA — 30 clasicos del underground ──────────────
TRACKS = [
    {
        "title": "Energy Flash",
        "artist": "Joey Beltram",
        "year": "1990",
        "label": "R&S Records · Belgium",
        "genre": "Techno",
        "note": "Producido a los 19 anos. El kick del 909 que definio el techno europeo. Una linea de bajo hipnotica que nunca envejece.",
        "url": "https://www.youtube.com/watch?v=BDj73pGQ6pE"
    },
    {
        "title": "Strings of Life",
        "artist": "Rhythim Is Rhythim (Derrick May)",
        "year": "1987",
        "label": "Transmat · Detroit",
        "genre": "Techno / House",
        "note": "Sin linea de bajo. Solo pianos y cuerdas. Frankie Knuckles le dio el nombre. #4 en el Greatest Ever Dance Record de la BBC.",
        "url": "https://www.youtube.com/watch?v=3hZA0xarSac"
    },
    {
        "title": "Spastik",
        "artist": "Plastikman (Richie Hawtin)",
        "year": "1993",
        "label": "NovaMute · UK",
        "genre": "Techno Minimalista",
        "note": "Richie Hawtin en estado puro. Minimalismo hipnotico. Un loop que te arrastra durante 10 minutos sin que te des cuenta.",
        "url": "https://www.youtube.com/watch?v=6TYsOMYaz6E"
    },
    {
        "title": "Dominator",
        "artist": "Human Resource",
        "year": "1991",
        "label": "R&S Records · Belgium",
        "genre": "Hardcore / Techno",
        "note": "El grito mas icónico del hardcore europeo. Remixado por Joey Beltram. Sonó en todos los raves del planeta en el 91.",
        "url": "https://www.youtube.com/watch?v=Q--79iGN_t8"
    },
    {
        "title": "Mentasm",
        "artist": "Second Phase (Joey Beltram & Mundo Musik)",
        "year": "1991",
        "label": "R&S Records · Belgium",
        "genre": "Techno",
        "note": "El sonido Juno que cambio el hardcore. Grabado con un Casio y un Juno. La colaboracion mas influyente del techno belga.",
        "url": "https://www.youtube.com/watch?v=JTCcjOuAnKg"
    },
    {
        "title": "Good Life",
        "artist": "Inner City (Kevin Saunderson)",
        "year": "1988",
        "label": "10 Records · Detroit",
        "genre": "Detroit House",
        "note": "Kevin Saunderson y Paris Grey. Uno de los primeros grandes crossovers del sonido Detroit al mercado pop mundial.",
        "url": "https://www.youtube.com/watch?v=M-lNPSHfUKE"
    },
    {
        "title": "No UFOs",
        "artist": "Model 500 (Juan Atkins)",
        "year": "1985",
        "label": "Metroplex · Detroit",
        "genre": "Detroit Techno",
        "note": "Juan Atkins. El primer techno grabado en Detroit. Metroplex Records. El Big Bang del genero. Todo empieza aqui.",
        "url": "https://www.youtube.com/watch?v=RCLjXNHkjXc"
    },
    {
        "title": "Jackmaster",
        "artist": "Jeff Mills",
        "year": "1992",
        "label": "Axis Records · Detroit",
        "genre": "Detroit Techno",
        "note": "Jeff Mills — The Wizard. Velocidad y precision quirurgica. Un DJ legendario que produce como ninguno.",
        "url": "https://www.youtube.com/watch?v=h9Zao0GJ1mQ"
    },
    {
        "title": "The Bells",
        "artist": "Jeff Mills",
        "year": "1996",
        "label": "Tresor · Berlin",
        "genre": "Techno",
        "note": "El track mas emotivo de Jeff Mills. Campanas sinteticas sobre una tormenta de kicks. Un clasico absoluto de Tresor Berlin.",
        "url": "https://www.youtube.com/watch?v=85EBSMiGkBU"
    },
    {
        "title": "Nude Photo",
        "artist": "Rhythim Is Rhythim (Derrick May)",
        "year": "1987",
        "label": "Transmat · Detroit",
        "genre": "Detroit Techno",
        "note": "El primer single de Derrick May. Antes de Strings of Life. Aqui empezo todo para uno de los Belleville Three.",
        "url": "https://www.youtube.com/watch?v=N8XU_xMnm7U"
    },
    {
        "title": "Pacific State",
        "artist": "808 State",
        "year": "1989",
        "label": "ZTT · Manchester",
        "genre": "Ambient House",
        "note": "Manchester 1989. El sonido de la Madchester scene. Fluye como agua. Un momento de paz entre sets devastadores.",
        "url": "https://www.youtube.com/watch?v=vv1qeGKR10E"
    },
    {
        "title": "Voodoo Ray",
        "artist": "A Guy Called Gerald",
        "year": "1988",
        "label": "Rham! · Manchester",
        "genre": "House / Acid",
        "note": "Gerald Simpson en su habitacion de Manchester. La linea de bajo acid mas reconocible del UK. Grabado en una semana.",
        "url": "https://www.youtube.com/watch?v=4MCdoFNAGH8"
    },
    {
        "title": "Theme From S-Express",
        "artist": "S'Express",
        "year": "1988",
        "label": "Rhythm King · UK",
        "genre": "House",
        "note": "Mark Moore samplea Rose Royce. #1 en UK Charts. La primera vez que el house rompio el mainstream britanico de verdad.",
        "url": "https://www.youtube.com/watch?v=3ej-oFKUoP8"
    },
    {
        "title": "Acid Trax",
        "artist": "Phuture",
        "year": "1987",
        "label": "Trax Records · Chicago",
        "genre": "Acid House",
        "note": "DJ Pierre, Spanky y Herb J. La primera grabacion de acid house de la historia. El TB-303 como arma de baile.",
        "url": "https://www.youtube.com/watch?v=mn31N1gkCLY"
    },
    {
        "title": "Move Your Body",
        "artist": "Marshall Jefferson",
        "year": "1986",
        "label": "Trax Records · Chicago",
        "genre": "House",
        "note": "La primera cancion house con un piano real. Marshall Jefferson Chicago 1986. La genesis del gospel en el dancefloor.",
        "url": "https://www.youtube.com/watch?v=FvABQU5LSUU"
    },
    {
        "title": "Your Love",
        "artist": "Frankie Knuckles",
        "year": "1987",
        "label": "Trax Records · Chicago",
        "genre": "Chicago House",
        "note": "El Godfather of House. Frankie Knuckles en The Warehouse. La cancion que le dio nombre a todo un genero.",
        "url": "https://www.youtube.com/watch?v=TZpPJcAFaJQ"
    },
    {
        "title": "Windowlicker",
        "artist": "Aphex Twin",
        "year": "1999",
        "label": "Warp Records · UK",
        "genre": "IDM / Electronic",
        "note": "Richard D. James en estado salvaje. Video de Chris Cunningham. El IDM mas accesible y perturbador al mismo tiempo.",
        "url": "https://www.youtube.com/watch?v=UBnVL61RDiE"
    },
    {
        "title": "Come to Daddy",
        "artist": "Aphex Twin",
        "year": "1997",
        "label": "Warp Records · UK",
        "genre": "IDM / Drill'n'Bass",
        "note": "El track mas aterrador de la historia electronica. Video iconico de Chris Cunningham. No apto para debiles.",
        "url": "https://www.youtube.com/watch?v=h-9UvrLyj3k"
    },
    {
        "title": "Children",
        "artist": "Robert Miles",
        "year": "1995",
        "label": "Deconstruction · Italy",
        "genre": "Dream Trance",
        "note": "Robert Miles queria reducir accidentes de trafico post-rave con musica suave. Resulto en un #1 mundial.",
        "url": "https://www.youtube.com/watch?v=CC5ca6Hsb2Q"
    },
    {
        "title": "Sandstorm",
        "artist": "Darude",
        "year": "1999",
        "label": "Neo · Finland",
        "genre": "Trance",
        "note": "Finlandia 1999. El track mas reconocible del trance mundial. Villanizado y amado a partes iguales. Un fenomeno cultural.",
        "url": "https://www.youtube.com/watch?v=y6120QOlsfU"
    },
    {
        "title": "Da Funk",
        "artist": "Daft Punk",
        "year": "1995",
        "label": "Soma Quality Recordings",
        "genre": "French House",
        "note": "Thomas Bangalter y Guy-Manuel en Glasgow. El groove que lanzo a Daft Punk al mundo. Funk robotico perfecto.",
        "url": "https://www.youtube.com/watch?v=XaMFBHAZFbE"
    },
    {
        "title": "Around the World",
        "artist": "Daft Punk",
        "year": "1997",
        "label": "Virgin Records · France",
        "genre": "French House",
        "note": "Una frase repetida 144 veces. Coreografia iconica de Michel Gondry. La filosofia del loop llevada a su maximo esplendor.",
        "url": "https://www.youtube.com/watch?v=K0HSD_i2DvA"
    },
    {
        "title": "Stakker Humanoid",
        "artist": "Humanoid",
        "year": "1988",
        "label": "Westside · UK",
        "genre": "Acid House",
        "note": "Brian Dougans y Gary Cobain (Future Sound of London). Uno de los primeros acid crossovers del UK. Premonitorio.",
        "url": "https://www.youtube.com/watch?v=eSrKR9OPDkA"
    },
    {
        "title": "LFO",
        "artist": "LFO",
        "year": "1990",
        "label": "Warp Records · Sheffield",
        "genre": "Bleep Techno",
        "note": "El primer Bleep techno de Sheffield. Mark Bell y Gez Varley. El sonido que definio Warp Records y el techno ingles.",
        "url": "https://www.youtube.com/watch?v=jIpBvvvRkNk"
    },
    {
        "title": "Technarchy",
        "artist": "Cybersonik (Richie Hawtin & Dan Bell)",
        "year": "1991",
        "label": "Plus 8 · Canada",
        "genre": "Hardcore Techno",
        "note": "Richie Hawtin y Dan Bell como Cybersonik. Plus 8 Records. El hardcore canadiense en su punto mas brutal y perfecto.",
        "url": "https://www.youtube.com/watch?v=dMqDpKIo-WE"
    },
    {
        "title": "The Bouncer",
        "artist": "Kicks Like a Mule",
        "year": "1992",
        "label": "Tribal Bass · UK",
        "genre": "Hardcore Rave",
        "note": "El sample mas sampleado del UK rave. Warrior tone, piano alocado y la energia del Ardkore en su apogeo total.",
        "url": "https://www.youtube.com/watch?v=dxKdsoODvMk"
    },
    {
        "title": "Charly",
        "artist": "The Prodigy",
        "year": "1991",
        "label": "XL Recordings · UK",
        "genre": "Hardcore Rave",
        "note": "Liam Howlett a los 19 anos. El primer single de The Prodigy. Sample de un PSA infantil sobre gatos. Genial y absurdo.",
        "url": "https://www.youtube.com/watch?v=EJYNGGgZi2M"
    },
    {
        "title": "Out of Space",
        "artist": "The Prodigy",
        "year": "1992",
        "label": "XL Recordings · UK",
        "genre": "Hardcore / Rave",
        "note": "The Prodigy samplea a Max Romeo. La conexion mas inesperada entre el reggae jamaicano y el hardcore britanico.",
        "url": "https://www.youtube.com/watch?v=NkBmNgNNQI4"
    },
    {
        "title": "Promised Land",
        "artist": "Joe Smooth",
        "year": "1987",
        "label": "DJ International · Chicago",
        "genre": "Gospel House",
        "note": "El sermon del dancefloor. Chicago 1987. El gospel, la soul y el house unidos en un track que trasciende la pista.",
        "url": "https://www.youtube.com/watch?v=K0qWZtH3FME"
    },
    {
        "title": "Plastic Dreams",
        "artist": "Jaydee",
        "year": "1993",
        "label": "R&S Records · Belgium",
        "genre": "Trance / House",
        "note": "Robin Albers en Holanda. El sintetizador que llora. Uno de los tracks mas emocionales del trance europeo de los 90.",
        "url": "https://www.youtube.com/watch?v=TIHHlFRSLLU"
    },
]

WELCOME = ("[ CONNECTION ESTABLISHED ] 📶\n\n"
"Welcome to the Late Night Society headquarters, Operator.\n\n"
"You have bypassed the static and entered the core of the "
"Cyberavers // PILLRAVE network. This isn't a hype train; "
"it's a mission to restore the underground.\n\n"
"CURRENT PROTOCOLS:\n"
"* The Mission: Defrosting the rave culture since 1992.\n"
"* The Tech: Real-time audio fingerprinting & producer rewards.\n"
"* The Drop: Wednesday @ Pump.fun.\n\n"
"RULES OF THE GRID:\n"
"1. No FUD. Only Logic.\n"
"2. Respect the OGs. We value the legacy.\n"
"3. Verify the Stack. Check the pinned legal docs before engaging.\n\n"
"The night is long. The signal is pure.\n\n"
"💊 [ TAKE THE PILL ]\n\n"
"Commands: /token /roadmap /comprar /info /web /track")

MSGS = {
"info": ("THE FROZEN ARE BACK\n\n"
"En 1992 la musica electronica era un codigo de libertad.\n\n"
"En los 90, la policia cerraba los clubes a las 2 AM.\n"
"Las Berkshire Mountains ofrecian bailar bajo las estrellas "
"sin que nadie tocara a la puerta.\n\n"
"Hoy PILLRAVE es el descongelamiento de esa vision.\n"
"La senal ha vuelto.\n\n"
"Berkshire Mountain, MA - 12.31.1999 - 06:13 AM"),
"token": ("TOKENOMICS $PILL\n\n"
"Venta publica: 80% - 727.2M tokens\n"
"Equipo y Dev: 15% - 136.35M (vesting 12 meses)\n"
"Airdrops y Rewards: 10% - 90.9M tokens\n\n"
"Supply total: 909,000,000 $PILL\n"
"Blockchain: Solana\n"
"Plataforma: Pump.fun\n\n"
"Distribucion 100% justa. Sin wallets bloqueadas."),
"roadmap": ("ROADMAP PILLRAVE\n\n"
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
"- App publica global"),
"comprar": ("COMO COMPRAR $PILL\n\n"
"1. Instala Phantom o Solflare (wallet Solana)\n"
"2. Compra algo de SOL para el gas\n"
"3. Ve a pump.fun y busca $PILL\n"
"4. Compra y HOLD\n\n"
"pump.fun\n"
"cyberavers.online\n\n"
"Sin KYC. Sin intermediarios. 100% on-chain."),
}

def get_daily_track():
    day = datetime.now().timetuple().tm_yday  # dia del año 1-365
    idx = (day - 1) % len(TRACKS)
    return TRACKS[idx]

def format_track(t):
    return (
        "🎵 TRACK DEL DIA\n\n"
        + t["title"] + "\n"
        + t["artist"] + " · " + t["year"] + "\n"
        + t["label"] + "\n"
        + t["genre"] + "\n\n"
        + t["note"] + "\n\n"
        + "#underground #rave #pillrave #" + t["genre"].lower().replace(" ","").replace("/","")
    )

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
    return call("sendMessage", {"chat_id": cid, "text": txt,
                                "disable_web_page_preview": False})

def send_menu(cid, txt):
    return call("sendMessage", {
        "chat_id": cid, "text": txt,
        "disable_web_page_preview": False,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "BUY $PILL", "url": PUMP_URL},
                 {"text": "WEBSITE",   "url": WEB_URL}],
                [{"text": "Instagram", "url": "https://instagram.com/cybarravers"},
                 {"text": "Twitter/X", "url": "https://x.com/CyberRaversNFT"}]
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
last_track_day = None

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
    cid = msg["chat"]["id"]
    user = msg.get("from", {}).get("first_name", "Raver")
    new_members = msg.get("new_chat_members", [])
    if new_members:
        for member in new_members:
            if not member.get("is_bot", False):
                name = member.get("first_name", "Operator")
                send_menu(cid, "Welcome " + name + "!\n\n" + WELCOME)
        return
    txt = msg.get("text", "")
    if not txt:
        return
    txt = txt.strip().split("@")[0].lower()
    print("[MSG] " + user + ": " + txt)
    if not load():
        save(cid)
    if txt in ("/start", "/help"):
        send_menu(cid, WELCOME)
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
    elif txt in ("/track", "/trackdeldia"):
        t = get_daily_track()
        send(cid, format_track(t))
        send(cid, t["url"])
    elif txt.startswith("/anuncio "):
        c = load()
        if c:
            send(int(c), "ANUNCIO PILLRAVE\n\n" + msg.get("text", "")[9:])

def auto_post_track():
    global last_track_day
    now = datetime.now()
    today = now.date()
    hour = now.hour
    # Publica a las 12:00 PM cada dia
    if hour == 12 and last_track_day != today:
        cid = load()
        if cid:
            t = get_daily_track()
            send(int(cid), format_track(t))
            result = send(int(cid), t["url"])
            if result and result.get("ok"):
                last_track_day = today
                print("[TRACK] Track del dia publicado: " + t["title"])

def main():
    print("==================================================")
    print("  PILLRAVE BOT - Railway Edition")
    print("  Token: " + BOT_TOKEN[:20] + "...")
    print("==================================================")
    me = call("getMe")
    if not me or not me.get("ok"):
        print("[ERR] Token invalido")
        return
    print("[OK] Bot activo: @" + me["result"]["username"])
    c = load()
    print("[OK] Chat ID: " + str(c or "ninguno"))
    print("[INFO] Track del dia a las 12:00 PM cada dia")
    print("[INFO] Escuchando mensajes...\n")
    off = None
    while True:
        try:
            auto_post_track()
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
