#!/usr/bin/env python3
import os, time, json, sys, urllib.request, urllib.error
from datetime import datetime, timedelta
import re

BOT_TOKEN = os.environ.get("BOT_TOKEN") or "8701250025:AAGQQTzKvLmnuEt_VPPHD3BWurUnWSEldkA"
WEB_URL   = "https://cyberavers.online"
PUMP_URL  = "https://pump.fun"
API       = "https://api.telegram.org/bot" + BOT_TOKEN

# ─── TRACK OF THE DAY — 30 underground classics ─────────────────
TRACKS = [
    {
        "title": "Energy Flash",
        "artist": "Joey Beltram",
        "year": "1990",
        "label": "R&S Records · Belgium",
        "genre": "Techno",
        "note": "Produced at age 19. The 909 kick that defined European techno. A hypnotic bassline that never ages.",
        "url": "https://www.youtube.com/watch?v=BDj73pGQ6pE"
    },
    {
        "title": "Strings of Life",
        "artist": "Rhythim Is Rhythim (Derrick May)",
        "year": "1987",
        "label": "Transmat · Detroit",
        "genre": "Techno / House",
        "note": "No bassline. Just pianos and strings. Frankie Knuckles named it. #4 on the BBC Greatest Ever Dance Record.",
        "url": "https://www.youtube.com/watch?v=3hZA0xarSac"
    },
    {
        "title": "Spastik",
        "artist": "Plastikman (Richie Hawtin)",
        "year": "1993",
        "label": "NovaMute · UK",
        "genre": "Techno Minimalista",
        "note": "Richie Hawtin at his purest. Hypnotic minimalism. A loop that pulls you in for 10 minutes without noticing.",
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
        "note": "The Juno sound that changed hardcore. Recorded with a Casio and a Juno. The most influential Belgian techno collaboration.",
        "url": "https://www.youtube.com/watch?v=JTCcjOuAnKg"
    },
    {
        "title": "Good Life",
        "artist": "Inner City (Kevin Saunderson)",
        "year": "1988",
        "label": "10 Records · Detroit",
        "genre": "Detroit House",
        "note": "Kevin Saunderson and Paris Grey. One of the first major crossovers from Detroit sound to the global pop market.",
        "url": "https://www.youtube.com/watch?v=M-lNPSHfUKE"
    },
    {
        "title": "No UFOs",
        "artist": "Model 500 (Juan Atkins)",
        "year": "1985",
        "label": "Metroplex · Detroit",
        "genre": "Detroit Techno",
        "note": "Juan Atkins. The first techno recorded in Detroit. Metroplex Records. The Big Bang of the genre. Everything starts here.",
        "url": "https://www.youtube.com/watch?v=RCLjXNHkjXc"
    },
    {
        "title": "Jackmaster",
        "artist": "Jeff Mills",
        "year": "1992",
        "label": "Axis Records · Detroit",
        "genre": "Detroit Techno",
        "note": "Jeff Mills — The Wizard. Speed and surgical precision. A legendary DJ who produces like no other.",
        "url": "https://www.youtube.com/watch?v=h9Zao0GJ1mQ"
    },
    {
        "title": "The Bells",
        "artist": "Jeff Mills",
        "year": "1996",
        "label": "Tresor · Berlin",
        "genre": "Techno",
        "note": "Jeff Mills' most emotional track. Synthetic bells over a kick drum storm. An absolute Tresor Berlin classic.",
        "url": "https://www.youtube.com/watch?v=85EBSMiGkBU"
    },
    {
        "title": "Nude Photo",
        "artist": "Rhythim Is Rhythim (Derrick May)",
        "year": "1987",
        "label": "Transmat · Detroit",
        "genre": "Detroit Techno",
        "note": "Derrick May's first single. Before Strings of Life. This is where it all started for one of the Belleville Three.",
        "url": "https://www.youtube.com/watch?v=N8XU_xMnm7U"
    },
    {
        "title": "Pacific State",
        "artist": "808 State",
        "year": "1989",
        "label": "ZTT · Manchester",
        "genre": "Ambient House",
        "note": "Manchester 1989. The sound of the Madchester scene. Flows like water. A moment of peace between devastating sets.",
        "url": "https://www.youtube.com/watch?v=vv1qeGKR10E"
    },
    {
        "title": "Voodoo Ray",
        "artist": "A Guy Called Gerald",
        "year": "1988",
        "label": "Rham! · Manchester",
        "genre": "House / Acid",
        "note": "Gerald Simpson in his Manchester bedroom. The most recognizable acid bassline in the UK. Recorded in one week.",
        "url": "https://www.youtube.com/watch?v=4MCdoFNAGH8"
    },
    {
        "title": "Theme From S-Express",
        "artist": "S'Express",
        "year": "1988",
        "label": "Rhythm King · UK",
        "genre": "House",
        "note": "Mark Moore samples Rose Royce. #1 on UK Charts. The first time house truly broke into the British mainstream.",
        "url": "https://www.youtube.com/watch?v=3ej-oFKUoP8"
    },
    {
        "title": "Acid Trax",
        "artist": "Phuture",
        "year": "1987",
        "label": "Trax Records · Chicago",
        "genre": "Acid House",
        "note": "DJ Pierre, Spanky and Herb J. The first acid house recording in history. The TB-303 as a dance weapon.",
        "url": "https://www.youtube.com/watch?v=mn31N1gkCLY"
    },
    {
        "title": "Move Your Body",
        "artist": "Marshall Jefferson",
        "year": "1986",
        "label": "Trax Records · Chicago",
        "genre": "House",
        "note": "The first house song with a real piano. Marshall Jefferson, Chicago 1986. The genesis of gospel on the dancefloor.",
        "url": "https://www.youtube.com/watch?v=FvABQU5LSUU"
    },
    {
        "title": "Your Love",
        "artist": "Frankie Knuckles",
        "year": "1987",
        "label": "Trax Records · Chicago",
        "genre": "Chicago House",
        "note": "The Godfather of House. Frankie Knuckles at The Warehouse. The song that gave an entire genre its name.",
        "url": "https://www.youtube.com/watch?v=TZpPJcAFaJQ"
    },
    {
        "title": "Windowlicker",
        "artist": "Aphex Twin",
        "year": "1999",
        "label": "Warp Records · UK",
        "genre": "IDM / Electronic",
        "note": "Richard D. James at his wildest. Video by Chris Cunningham. The most accessible and disturbing IDM simultaneously.",
        "url": "https://www.youtube.com/watch?v=UBnVL61RDiE"
    },
    {
        "title": "Come to Daddy",
        "artist": "Aphex Twin",
        "year": "1997",
        "label": "Warp Records · UK",
        "genre": "IDM / Drill'n'Bass",
        "note": "The most terrifying track in electronic history. Iconic video by Chris Cunningham. Not for the faint-hearted.",
        "url": "https://www.youtube.com/watch?v=h-9UvrLyj3k"
    },
    {
        "title": "Children",
        "artist": "Robert Miles",
        "year": "1995",
        "label": "Deconstruction · Italy",
        "genre": "Dream Trance",
        "note": "Robert Miles wanted to reduce post-rave traffic accidents with soft music. It resulted in a worldwide #1.",
        "url": "https://www.youtube.com/watch?v=CC5ca6Hsb2Q"
    },
    {
        "title": "Sandstorm",
        "artist": "Darude",
        "year": "1999",
        "label": "Neo · Finland",
        "genre": "Trance",
        "note": "Finland 1999. The most recognizable trance track worldwide. Vilified and loved in equal measure. A cultural phenomenon.",
        "url": "https://www.youtube.com/watch?v=y6120QOlsfU"
    },
    {
        "title": "Da Funk",
        "artist": "Daft Punk",
        "year": "1995",
        "label": "Soma Quality Recordings",
        "genre": "French House",
        "note": "Thomas Bangalter and Guy-Manuel in Glasgow. The groove that launched Daft Punk to the world. Perfect robotic funk.",
        "url": "https://www.youtube.com/watch?v=XaMFBHAZFbE"
    },
    {
        "title": "Around the World",
        "artist": "Daft Punk",
        "year": "1997",
        "label": "Virgin Records · France",
        "genre": "French House",
        "note": "A phrase repeated 144 times. Iconic choreography by Michel Gondry. Loop philosophy taken to its ultimate glory.",
        "url": "https://www.youtube.com/watch?v=K0HSD_i2DvA"
    },
    {
        "title": "Stakker Humanoid",
        "artist": "Humanoid",
        "year": "1988",
        "label": "Westside · UK",
        "genre": "Acid House",
        "note": "Brian Dougans and Gary Cobain (Future Sound of London). One of the first UK acid crossovers. Premonitory.",
        "url": "https://www.youtube.com/watch?v=eSrKR9OPDkA"
    },
    {
        "title": "LFO",
        "artist": "LFO",
        "year": "1990",
        "label": "Warp Records · Sheffield",
        "genre": "Bleep Techno",
        "note": "Sheffield's first Bleep techno. Mark Bell and Gez Varley. The sound that defined Warp Records and English techno.",
        "url": "https://www.youtube.com/watch?v=jIpBvvvRkNk"
    },
    {
        "title": "Technarchy",
        "artist": "Cybersonik (Richie Hawtin & Dan Bell)",
        "year": "1991",
        "label": "Plus 8 · Canada",
        "genre": "Hardcore Techno",
        "note": "Richie Hawtin and Dan Bell as Cybersonik. Plus 8 Records. Canadian hardcore at its most brutal and perfect.",
        "url": "https://www.youtube.com/watch?v=dMqDpKIo-WE"
    },
    {
        "title": "The Bouncer",
        "artist": "Kicks Like a Mule",
        "year": "1992",
        "label": "Tribal Bass · UK",
        "genre": "Hardcore Rave",
        "note": "The most sampled sample in UK rave. Warrior tone, wild piano and the energy of Ardkore at its absolute peak.",
        "url": "https://www.youtube.com/watch?v=dxKdsoODvMk"
    },
    {
        "title": "Charly",
        "artist": "The Prodigy",
        "year": "1991",
        "label": "XL Recordings · UK",
        "genre": "Hardcore Rave",
        "note": "Liam Howlett at age 19. The Prodigy's first single. Sample from a children's cat PSA. Brilliant and absurd.",
        "url": "https://www.youtube.com/watch?v=EJYNGGgZi2M"
    },
    {
        "title": "Out of Space",
        "artist": "The Prodigy",
        "year": "1992",
        "label": "XL Recordings · UK",
        "genre": "Hardcore / Rave",
        "note": "The Prodigy samples Max Romeo. The most unexpected connection between Jamaican reggae and British hardcore.",
        "url": "https://www.youtube.com/watch?v=NkBmNgNNQI4"
    },
    {
        "title": "Promised Land",
        "artist": "Joe Smooth",
        "year": "1987",
        "label": "DJ International · Chicago",
        "genre": "Gospel House",
        "note": "The dancefloor sermon. Chicago 1987. Gospel, soul and house united in a track that transcends the floor.",
        "url": "https://www.youtube.com/watch?v=K0qWZtH3FME"
    },
    {
        "title": "Plastic Dreams",
        "artist": "Jaydee",
        "year": "1993",
        "label": "R&S Records · Belgium",
        "genre": "Trance / House",
        "note": "Robin Albers in Holland. The crying synthesizer. One of the most emotional tracks in 90s European trance.",
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
"Commands: /token /roadmap /buy /info /web /track /mix /news /price /dao")

MSGS = {
"info": ("THE FROZEN ARE BACK\n\n"
"In 1992, electronic music was not a business — it was a code of freedom.\n\n"
"In the 90s, police were shutting down clubs at 2 AM.\n"
"The Berkshire Mountains offered freedom to dance under the stars "
"without anyone knocking on the door.\n\n"
"Today PILLRAVE is the defrosting of that vision.\n"
"The signal is back.\n\n"
"Berkshire Mountain, MA - 12.31.1999 - 06:13 AM"),
"token": ("TOKENOMICS $PILL\n\n"
"Public sale: 80% - 727.2M tokens\n"
"Team & Dev: 15% - 136.35M (12-month vesting)\n"
"Airdrops & Rewards: 10% - 90.9M tokens\n\n"
"Total supply: 909,000,000 $PILL\n"
"Blockchain: Solana\n"
"Platform: Pump.fun\n\n"
"100% fair distribution. No locked team wallets."),
"roadmap": ("PILLRAVE ROADMAP\n\n"
"PHASE 0 - NOW\n"
"- Token live on Solana via Pump.fun\n"
"- Landing page and branding active\n\n"
"PHASE 1 - Q3 2026\n"
"- iOS/Android app demo\n"
"- First airdrops\n"
"- First pilot festival\n\n"
"PHASE 2 - Q1 2027\n"
"- Active staking\n"
"- Producers dashboard\n"
"- DAO launched\n\n"
"PHASE 3 - 2027+\n"
"- Major festivals\n"
"- Global public app"),

"dao": (
"PILLRAVE DAO — Governance by the Grid\n\n"
"Tired of labels deciding what you hear and what artists are worth?\n"
"The DAO is your all-access pass to run the club.\n\n"
"YOUR VOICE IS THE BEAT.\n\n"
"$PILL holders are not just users — they are decision nodes\n"
"inside a value distribution protocol.\n"
"You don't just attend the party. You throw it.\n\n"
"Architecture: SOLANA SPL\n"
"Transparency: 100% ON-CHAIN\n"
"Treasury: 15% SUPPLY (DAO controlled)\n"
"Voting: SNAPSHOT (gasless proposals)\n\n"
"/tiers — Access Tiers\n"
"/howit — How It Works\n"
"/pillars — What We Decide\n"
"/manifesto — The Manifesto\n\n"
"dao@cyberavers.online"
),
"tiers": (
"ACCESS TIERS — PILLRAVE DAO\n\n"
"TIER 1 — VIBE CHECKER\n"
"Hold any amount of $PILL\n"
"- Vote on community polls\n"
"- Private Discord access\n"
"- Early access to artist drops\n"
"- DAO newsletter\n\n"
"TIER 2 — RESIDENT\n"
"Stake 30+ days\n"
"- Everything in Tier 1\n"
"- Propose app changes\n"
"- Nominate artists for The Studio\n"
"- Protocol analytics access\n\n"
"TIER 3 — FOUNDING OG\n"
"Stake 90+ consecutive days\n"
"- Everything in Tier 1 and 2\n"
"- Full DAO Treasury access\n"
"- Propose protocol-level changes\n"
"- Seat on the DAO Council\n\n"
"The longer you stay in the after, the more say you get in the set."
),
"howit": (
"HOW IT WORKS — PILLRAVE DAO\n\n"
"To get in, you need to Hit the After (Staking).\n"
"Lock up your $PILL and get $sPILL — your immutable voting unit.\n\n"
"STEP 01 — Send your $PILL to the After\n"
"Smart Contract Staking (SPL Protocol)\n\n"
"STEP 02 — Get your Member ID\n"
"Governance token issuance: $sPILL\n\n"
"STEP 03 — Vote on artists and events\n"
"Proposal execution via DAO Snapshot\n\n"
"No wallet? No problem.\n"
"The PILLRAVE app auto-generates a self-custody wallet.\n"
"You earn $PILL automatically every time you ID a track on the floor.\n"
"$sPILL works so you don't have to."
),
"pillars": (
"WHAT WE DECIDE — DAO PILLARS\n\n"
"The DAO doesn't vote on trivial stuff. We vote on CULTURE.\n\n"
"THE ARTIST FUND\n"
"Which independent producers get direct grants from the treasury.\n\n"
"THE GRID EXPANSION\n"
"Which cities and festivals activate Dance-to-Earn rewards.\n\n"
"PROTOCOL UPGRADES\n"
"Adjustments to reward rates for track identification.\n\n"
"EMERGENCY BRAKE\n"
"If the market goes sideways, the DAO can vote to pause\n"
"emissions and protect the community."
),
"manifesto": (
"THE CYBERAVERS MANIFESTO\n\n"
"The DAO isn't a board meeting — it's a 24/7 afterhour.\n\n"
"In PILLRAVE, the code is the DJ, and you are the Promoter.\n\n"
"treasury.supply = 15%\n"
"treasury.control = DAO_ONLY\n"
"intervention.manual = false\n"
"cyberavers.override = false\n\n"
"Every vote is public on the Explorer.\n"
"Zero backroom deals.\n\n"
"The code is the DJ. The dance floor is the blockchain.\n"
"And you are the Promoter. Step up and take control of the culture."
),
"comprar": ("HOW TO BUY $PILL\n\n"
"1. Install Phantom or Solflare (Solana wallet)\n"
"2. Buy some SOL for gas fees\n"
"3. Go to pump.fun and search $PILL\n"
"4. Buy and HOLD\n\n"
"pump.fun\n"
"cyberavers.online\n\n"
"No KYC. No middlemen. 100% on-chain."),
}


import urllib.parse
from datetime import datetime, timedelta
import re

# ─── RSS NEWS SYSTEM ──────────────────────────────────────────
RSS_FEEDS = [
    # News
    "https://ra.co/xml/news.xml",
    "https://www.mixmag.net/feed",
    "https://djmag.com/feed",
    "https://xlr8r.com/feed",
    # Bandcamp new releases by tag
    "https://bandcamp.com/tag/techno?format=rss",
    "https://bandcamp.com/tag/acid-house?format=rss",
    "https://bandcamp.com/tag/rave?format=rss",
    "https://bandcamp.com/tag/detroit-techno?format=rss",
    "https://bandcamp.com/tag/chicago-house?format=rss",
    "https://bandcamp.com/tag/hardcore-techno?format=rss",
    "https://bandcamp.com/tag/underground-house?format=rss",
]

# SoundCloud: The Classic Mix CD Series (user ID: 70548)
SC_RSS = "https://feeds.soundcloud.com/users/soundcloud:users:70548/sounds.rss"
SC_POSTED = set()
last_sc_day = None

# ─── CRYPTO PRICES ────────────────────────────────────────────
last_price_day = None

def fetch_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=solana,bitcoin&vs_currencies=usd&include_24hr_change=true"
        req = urllib.request.Request(url, headers={"User-Agent": "PillRaveBot/1.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        sol_price  = data["solana"]["usd"]
        sol_change = data["solana"]["usd_24h_change"]
        btc_price  = data["bitcoin"]["usd"]
        btc_change = data["bitcoin"]["usd_24h_change"]
        return {
            "sol": sol_price, "sol_change": sol_change,
            "btc": btc_price, "btc_change": btc_change,
        }
    except Exception as e:
        print("[PRICE ERR] " + str(e))
        return None

def format_prices(p):
    def arrow(c): return "📈" if c >= 0 else "📉"
    def sign(c):  return "+" if c >= 0 else ""
    return (
        "💹 CRYPTO PRICES\n\n"
        + arrow(p["sol_change"]) + " SOL/USD: $" + "{:,.2f}".format(p["sol"])
        + "  (" + sign(p["sol_change"]) + "{:.2f}".format(p["sol_change"]) + "% 24h)\n"
        + arrow(p["btc_change"]) + " BTC/USD: $" + "{:,.0f}".format(p["btc"])
        + "  (" + sign(p["btc_change"]) + "{:.2f}".format(p["btc_change"]) + "% 24h)\n\n"
        + "Source: CoinGecko\n"
        + "#solana #bitcoin #crypto #pillrave"
    )

def auto_post_prices():
    global last_price_day
    now = datetime.now()
    today = now.date()
    hour = now.hour
    # Post prices at 9 AM every day
    if hour == 9 and last_price_day != today:
        cid = load()
        if not cid:
            return
        p = fetch_prices()
        if p:
            send(int(cid), format_prices(p))
            last_price_day = today
            print("[PRICE] Prices posted: SOL=$" + str(p["sol"]) + " BTC=$" + str(p["btc"]))

BANDCAMP_FEEDS = [
    "https://bandcamp.com/tag/techno?format=rss",
    "https://bandcamp.com/tag/acid-house?format=rss",
    "https://bandcamp.com/tag/rave?format=rss",
    "https://bandcamp.com/tag/detroit-techno?format=rss",
    "https://bandcamp.com/tag/chicago-house?format=rss",
    "https://bandcamp.com/tag/hardcore-techno?format=rss",
    "https://bandcamp.com/tag/underground-house?format=rss",
]

# Artistas vigentes hasta 1999
ARTISTS = [
    # Detroit Techno — The Belleville Three & scene
    "derrick may", "juan atkins", "kevin saunderson", "model 500",
    "inner city", "rhythim is rhythim", "metroplex",
    # Jeff Mills & Underground Resistance
    "jeff mills", "underground resistance", "mad mike", "robert hood",
    "millsart", "axis records", "ur records",
    # Richie Hawtin & Plus 8
    "richie hawtin", "plastikman", "plus 8", "cybersonik", "f.u.s.e.",
    "dan bell", "john acquaviva",
    # Belgian / R&S Records
    "joey beltram", "human resource", "r&s records", "lenny dee",
    "frank de wulf", "cj bolland", "t99", "outlander", "jam & spoon",
    "marmion", "second phase",
    # Tresor / Berlin
    "tresor", "blake baxter", "tanith", "woosh", "westbam",
    "marusha", "legal shot",
    # UK Hardcore / Rave
    "the prodigy", "liam howlett", "orbital", "the chemical brothers",
    "underworld", "leftfield", "goldie", "4 hero", "a guy called gerald",
    "kicks like a mule", "altern8", "adamski", "baby d",
    "carl cox", "dj hype", "grooverider", "fabio",
    # Chicago House / Acid
    "frankie knuckles", "larry heard", "mr fingers", "marshall jefferson",
    "larry levan", "ron hardy", "dj pierre", "phuture", "trax records",
    "dj international", "joe smooth", "ten city", "jamie principle",
    "fingers inc", "chip e", "farley jackmaster funk", "jesse saunders",
    # New York
    "francois kevorkian", "tony humphries", "jellybean benitez",
    "david morales", "louie vega", "masters at work", "little louie",
    "todd terry", "dj duke",
    # Sheffield / Warp
    "warp records", "lfo", "autechre", "aphex twin", "richard d james",
    "squarepusher", "tom jenkinson", "boards of canada",
    "808 state", "sweet exorcist", "nightmares on wax",
    # French House
    "daft punk", "thomas bangalter", "guy-manuel", "cassius",
    "laurent garnier", "f communications", "yellow productions",
    "bob sinclar", "stardust", "etienne de crecy", "air",
    # Amsterdam / Holland
    "jaydee", "robin albers", "id&t", "thunderdome", "gabber",
    "dj paul elstak", "rotterdam records",
    # Ambient / Electronic
    "brian eno", "harold budd", "the orb", "alex paterson",
    "moby", "fluke", "banco de gaia", "the future sound of london",
    "fsol", "amorphous androgynous",
    # Drum & Bass / Jungle
    "goldie", "metalheadz", "roni size", "reprazent",
    "ltj bukem", "good looking records", "dj krush",
    # Misc Legends
    "juan maclean", "new order", "depeche mode", "kraftwerk",
    "tangerine dream", "jean michel jarre", "giorgio moroder",
    "donna summer", "harold faltermeyer", "vangelis",
    "yello", "nitzer ebb", "front 242", "the klinik",
    "skinny puppy", "ministry", "nine inch nails",
]

# Blacklist — ignorar estas noticias
BLACKLIST = [
    "reggaeton", "kpop", "k-pop", "country", "pop star",
    "taylor swift", "bad bunny", "justin bieber", "ariana grande",
    "drake", "kanye", "hip hop chart", "billboard hot 100",
]

posted_urls = set()
last_news_time = None

def fetch_rss(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PillRaveBot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print("[RSS ERR] " + url + " -> " + str(e))
        return ""

def parse_rss(xml):
    items = []
    entries = re.findall(r"<item>(.*?)</item>", xml, re.DOTALL)
    for entry in entries[:10]:
        title = re.findall(r"<title><![CDATA[(.*?)]]></title>|<title>(.*?)</title>", entry)
        title = (title[0][0] or title[0][1]).strip() if title else ""
        link  = re.findall(r"<link>(.*?)</link>|<guid>(.*?)</guid>", entry)
        link  = (link[0][0] or link[0][1]).strip() if link else ""
        desc  = re.findall(r"<description><![CDATA[(.*?)]]></description>|<description>(.*?)</description>", entry)
        desc  = (desc[0][0] or desc[0][1]).strip() if desc else ""
        desc  = re.sub(r"<[^>]+>", "", desc)[:200]
        if title and link:
            items.append({"title": title, "link": link, "desc": desc})
    return items

def is_relevant(item):
    text = (item["title"] + " " + item["desc"]).lower()
    # Check blacklist first
    for bad in BLACKLIST:
        if bad in text:
            return False
    # Bandcamp releases are already filtered by genre tag - always relevant
    if "bandcamp.com" in item.get("link", ""):
        return True
    # For news sites check artists
    for artist in ARTISTS:
        if artist in text:
            return True
    return False

def get_news():
    all_items = []
    for feed in RSS_FEEDS:
        xml = fetch_rss(feed)
        if xml:
            items = parse_rss(xml)
            all_items.extend(items)
    # Filter relevant + not posted
    relevant = [i for i in all_items
                if is_relevant(i) and i["link"] not in posted_urls]
    return relevant

def is_bandcamp(item):
    return "bandcamp.com" in item.get("link", "")

def format_news(item):
    if is_bandcamp(item):
        return (
            "🎧 NEW RELEASE\n\n"
            + item["title"] + "\n\n"
            + item["desc"][:200] + "\n\n"
            + "#newrelease #underground #techno #rave #pillrave"
        )
    return (
        "📰 UNDERGROUND NEWS\n\n"
        + item["title"] + "\n\n"
        + item["desc"][:200] + "...\n\n"
        + "#underground #techno #rave #pillrave"
    )

def auto_post_news():
    global last_news_time
    now = datetime.now()
    # Post every 6 hours
    if last_news_time and (now - last_news_time) < timedelta(hours=6):
        return
    cid = load()
    if not cid:
        return
    print("[NEWS] Fetching news...")
    items = get_news()
    if not items:
        print("[NEWS] No new relevant news")
        last_news_time = now
        return
    item = items[0]
    posted_urls.add(item["link"])
    send(int(cid), format_news(item))
    send(int(cid), item["link"])
    last_news_time = now
    print("[NEWS] Posted: " + item["title"][:60])

def get_daily_track():
    day = datetime.now().timetuple().tm_yday  # dia del año 1-365
    idx = (day - 1) % len(TRACKS)
    return TRACKS[idx]

def format_track(t):
    return (
        "🎵 TRACK OF THE DAY\n\n"
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
    elif txt in ("/info", "/about", "/history"):
        send(cid, MSGS["info"])
    elif txt in ("/token", "/tokenomics"):
        send(cid, MSGS["token"])
    elif txt == "/roadmap":
        send(cid, MSGS["roadmap"])
    elif txt in ("/buy", "/purchase"):
        send(cid, MSGS["comprar"])
    elif txt == "/web":
        send(cid, WEB_URL)
    elif txt == "/chatid":
        send(cid, "Chat ID: " + str(cid))
    elif txt == "/news":
        items = get_news()
        if items:
            item = items[0]
            posted_urls.add(item["link"])
            send(cid, format_news(item))
            send(cid, item["link"])
        else:
            send(cid, "No relevant news found at this time. Try again later.")
    elif txt in ("/price", "/sol", "/btc"):
        p = fetch_prices()
        if p:
            send(cid, format_prices(p))
        else:
            send(cid, "Could not fetch prices. Try again later.")
    elif txt in ("/mix", "/dailymix"):
        item = fetch_sc_mix()
        if item:
            SC_POSTED.add(item["link"])
            send(cid, format_sc_mix(item))
            send(cid, item["link"])
        else:
            send(cid, "Could not fetch the mix. Try again later.")
    elif txt in ("/track", "/dailytrack"):
        t = get_daily_track()
        send(cid, format_track(t))
        send(cid, t["url"])
    elif txt in ("/dao", "/governance"):
        send_menu(cid, MSGS["dao"])
    elif txt == "/tiers":
        send(cid, MSGS["tiers"])
    elif txt in ("/howit", "/howitworks", "/mechanics"):
        send(cid, MSGS["howit"])
    elif txt in ("/pillars", "/vote", "/voting"):
        send(cid, MSGS["pillars"])
    elif txt in ("/manifesto", "/mission"):
        send(cid, MSGS["manifesto"])
    elif txt.startswith("/announce "):
        c = load()
        if c:
            send(int(c), "ANNOUNCEMENT\n\n" + msg.get("text", "")[10:])

def fetch_sc_mix():
    try:
        xml = fetch_rss(SC_RSS)
        if not xml:
            return None
        items = parse_rss(xml)
        if items:
            return items[0]
        return None
    except Exception as e:
        print("[SC ERR] " + str(e))
        return None

def format_sc_mix(item):
    return (
        "🎧 MIX OF THE DAY — The Classic Mix CD Series\n\n"
        + item["title"] + "\n\n"
        + item["desc"][:200] + "\n\n"
        + "#classicmix #underground #rave #pillrave"
    )

def auto_post_sc_mix():
    global last_sc_day
    now = datetime.now()
    today = now.date()
    hour = now.hour
    # Post SC mix at 8 PM every day
    if hour == 20 and last_sc_day != today:
        cid = load()
        if not cid:
            return
        item = fetch_sc_mix()
        if item and item["link"] not in SC_POSTED:
            SC_POSTED.add(item["link"])
            send(int(cid), format_sc_mix(item))
            send(int(cid), item["link"])
            last_sc_day = today
            print("[SC MIX] Posted: " + item["title"][:60])

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
                print("[TRACK] Track of the day posted: " + t["title"])

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
    print("[INFO] Track of the day at 12:00 PM daily")
    print("[INFO] Listening for messages...\n")
    off = None
    while True:
        try:
            auto_post_track()
            auto_post_news()
            auto_post_sc_mix()
            auto_post_prices()
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
