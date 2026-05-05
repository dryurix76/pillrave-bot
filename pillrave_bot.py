#!/usr/bin/env python3
import os, time, json, sys, urllib.request, urllib.error
from datetime import datetime, timedelta
import re

BOT_TOKEN = os.environ.get("BOT_TOKEN") or "8701250025:AAGQQTzKvLmnuEt_VPPHD3BWurUnWSEldkA"
WEB_URL   = "https://cyberavers.online"
PUMP_URL  = "https://pump.fun/coin/6uCaWNvRTUExSMM6qnFF2uujcRVWXbRwL9eFSUdJpump"
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

# ─── WEB SECTIONS ROTATION ────────────────────────────────────
WEB_SECTIONS = [
    {
        "title": "THE PILLRAVE MISSION",
        "content": (
            "La nostalgia del 99, defrosted to heal the economy of 2026.\n\n"
            "Real infrastructure. Direct value to the artist.\n\n"
            "PILLRAVE is not a promise. We are the cure so value returns to its origin.\n\n"
            "In the 90s, police were shutting clubs at 2 AM.\n"
            "The Berkshire Mountains offered freedom to dance under the stars\n"
            "without anyone knocking on the door.\n\n"
            "That energy never died. It was frozen.\n"
            "Today we defrost it — with code, with community, with $PILL.\n\n"
            "Welcome to the resistance. The signal is back.\n\n"
            "🌐 cyberavers.online"
        ),
        "url": "https://cyberavers.online"
    },
    {
        "title": "THE $PILL TOKEN",
        "content": (
            "909M SUPPLY // SOLANA // THE UNDERGROUND TOKEN\n\n"
            "Public Sale: 80% — 727.2M tokens\n"
            "Team & Dev: 15% — 136.35M (12-month vesting)\n"
            "Airdrops & Rewards: 10% — 90.9M tokens\n\n"
            "100% fair distribution.\n"
            "No locked team wallets. No manipulation.\n"
            "The PILL is the cure to the chaos of the scene.\n\n"
            "Live now on Pump.fun:\n"
            "https://pump.fun/coin/6uCaWNvRTUExSMM6qnFF2uujcRVWXbRwL9eFSUdJpump"
        ),
        "url": "https://pump.fun/coin/6uCaWNvRTUExSMM6qnFF2uujcRVWXbRwL9eFSUdJpump"
    },
    {
        "title": "PILLRAVE DAO — GOVERNANCE BY THE GRID",
        "content": (
            "Tired of labels deciding what you hear and what artists earn?\n\n"
            "The DAO is your all-access pass to run the club.\n\n"
            "TIER 1 — VIBE CHECKER\n"
            "Hold any $PILL → Vote on polls, Discord access, early drops\n\n"
            "TIER 2 — RESIDENT\n"
            "Stake 30+ days → Propose app changes, nominate artists\n\n"
            "TIER 3 — FOUNDING OG\n"
            "Stake 90+ days → Full treasury access, DAO Council seat\n\n"
            "The longer you stay in the after, the more say you get in the set.\n\n"
            "🌐 cyberavers.online/dao"
        ),
        "url": "https://cyberavers.online"
    },
    {
        "title": "HOW TO SECURE THE PILL",
        "content": (
            "[ TRANSMISSION RECOVERED - LATE NIGHT SOCIETY ]\n\n"
            "In 1992, electronic music was not a business — it was a code of freedom.\n"
            "We were called CyberRavers because we understood that technology\n"
            "should serve the dancefloor, not the other way around.\n\n"
            "PILLRAVE has evolved from NFTs to real infrastructure:\n"
            "an ecosystem where music in motion rewards directly those who create it.\n\n"
            "STEP 1 — Connect your Phantom or Solflare wallet\n"
            "STEP 2 — Go to Pump.fun via the official link\n"
            "STEP 3 — Choose your $PILL amount\n"
            "STEP 4 — HOLD & GOVERN: once the token graduates to Raydium,\n"
            "your PILL becomes the governance key for the DAO\n\n"
            "🔗 https://pump.fun/coin/6uCaWNvRTUExSMM6qnFF2uujcRVWXbRwL9eFSUdJpump"
        ),
        "url": "https://pump.fun/coin/6uCaWNvRTUExSMM6qnFF2uujcRVWXbRwL9eFSUdJpump"
    },
    {
        "title": "THE PILLRAVE APP — SHAZAM FOR UNDERGROUND MUSIC",
        "content": (
            "You're on the dancefloor. A track drops.\n"
            "You don't know what it is — but you need it.\n\n"
            "The PILLRAVE app identifies it in real time.\n"
            "The producer gets paid. You earn $PILL.\n\n"
            "HOW IT WORKS:\n"
            "🎵 You hear a track → App identifies it\n"
            "💰 Producer receives royalties automatically on-chain\n"
            "💊 You earn $PILL for the identification\n"
            "🗳️ Accumulate $PILL → Govern the protocol\n\n"
            "This is not streaming. This is the underground rewired.\n\n"
            "App launching Q3 2026.\n"
            "🌐 cyberavers.online"
        ),
        "url": "https://cyberavers.online"
    },
    {
        "title": "PILLRAVE ROADMAP",
        "content": (
            "PHASE 0 — NOW\n"
            "✅ Token live on Solana via Pump.fun\n"
            "✅ Website and branding active\n"
            "✅ Telegram community live\n\n"
            "PHASE 1 — Q3 2026\n"
            "📱 iOS/Android app demo\n"
            "🎁 First airdrops to holders\n"
            "🎪 First pilot festival\n\n"
            "PHASE 2 — Q1 2027\n"
            "📈 Active staking (The After)\n"
            "🎛️ Producers dashboard live\n"
            "🗳️ DAO fully launched\n\n"
            "PHASE 3 — 2027+\n"
            "🌍 Major international festivals\n"
            "📱 Global public app launch\n"
            "🎵 Global royalties standard\n\n"
            "The curve is filling. Get in before the After opens.\n"
            "🔗 https://pump.fun/coin/6uCaWNvRTUExSMM6qnFF2uujcRVWXbRwL9eFSUdJpump"
        ),
        "url": "https://pump.fun/coin/6uCaWNvRTUExSMM6qnFF2uujcRVWXbRwL9eFSUdJpump"
    },
    {
        "title": "PILLRAVE — A CULTURAL AND TECHNICAL EXPERIMENT",
        "content": (
            "The true law is the rhythm,\n"
            "but we respect the code of the network.\n\n"
            "PILLRAVE is not a hype train. It is a mission.\n\n"
            "treasury.supply = 15%\n"
            "treasury.control = DAO_ONLY\n"
            "intervention.manual = false\n"
            "cyberavers.override = false\n\n"
            "Every vote is public on the Explorer.\n"
            "Zero backroom deals.\n"
            "Zero manipulation.\n\n"
            "The code is the DJ.\n"
            "The dancefloor is the blockchain.\n"
            "And you are the Promoter.\n\n"
            "Step up and take control of the culture.\n\n"
            "🌐 cyberavers.online\n"
            "📱 @CYBERRAVERS"
        ),
        "url": "https://cyberavers.online"
    },
]

last_web_section_day = None
web_section_index = 0

def auto_post_web_section():
    global last_web_section_day, web_section_index
    now = datetime.now()
    today = now.date()
    hour = now.hour
    minute = now.minute
    # Post at 3 PM daily
    if hour == 15 and minute == 0 and last_web_section_day != today:
        cid = load()
        if not cid:
            return
        last_web_section_day = today
        section = WEB_SECTIONS[web_section_index % len(WEB_SECTIONS)]
        web_section_index += 1
        msg = "📡 " + section["title"] + "\n\n" + section["content"]
        send_all(msg)
        print("[WEB] Posted section: " + section["title"])

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
"Commands: /token /roadmap /buy /info /web /track /mix /news /price /dao /launch /safety\n\n""💊 Buy now: https://pump.fun/coin/6uCaWNvRTUExSMM6qnFF2uujcRVWXbRwL9eFSUdJpump")

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


"daily_pump": (
"💊 $PILL IS LIVE ON PUMP.FUN\n\n"
"The PILLRAVE protocol is officially deployed on Solana.\n"
"This is a 100% fair launch — no insiders, no private rounds,\n"
"no locked team wallets.\n\n"
"WHY $PILL?\n"
"- Real utility: powers the audio ID protocol and DAO\n"
"- 909M total supply — no inflation\n"
"- Fair distribution: 80% public, 15% team vesting, 10% airdrops\n"
"- Once the bond curve is met: staking and DAO governance go live\n\n"
"HOW TO BUY:\n"
"1. Get a Solana wallet (Phantom or Solflare)\n"
"2. Add SOL for gas\n"
"3. Hit the link below and buy $PILL\n\n"
"The signal is live. The floor is open.\n"
"Secure your position before the curve is met.\n\n"
"🔗 https://pump.fun/coin/6uCaWNvRTUExSMM6qnFF2uujcRVWXbRwL9eFSUdJpump\n"
"🌐 cyberavers.online\n\n"
"#PILLRAVE #Solana #PumpFun #FairLaunch #Web3Music"
),
"launch": (
"[ SYSTEM DEPLOYED // THE ANTIDOTE IS HERE ] 💊\n\n"
"The wait is over. The PILLRAVE protocol is now officially live on the Grid.\n"
"We are no longer just a concept; we are infrastructure.\n\n"
"WHAT HAPPENS NOW?\n\n"
"1. Fair Launch: The market is now open. No insiders, no private rounds.\n\n"
"2. Utility First: $PILL powers real-time audio identification and the DAO.\n\n"
"3. The After: Once the bond curve is met, Staking and DAO Proposals\n"
"   will be initialized next week.\n\n"
"VERIFY BEFORE YOU ACT:\n"
"Always check the URL. Ensure you are on the official cyberavers.online\n"
"and following links from this pinned message.\n\n"
"THE NIGHT HAS JUST BEGUN.\n"
"[ STATUS: OPERATIONAL ]"
),
"safety": (
"[ SECURITY PROTOCOL ACTIVATED ] 📶\n\n"
"🛡️ SAFEGUARDING THE GRID: INVESTOR SAFETY GUIDE\n\n"
"In the Late Night Society, we build for the long term.\n"
"Knowledge is your best encryption.\n\n"
"1. THE OFFICIAL CONTRACT 📜\n"
"- We will NEVER DM you a contract address.\n"
"- The only valid Pump.fun link is posted in this channel and on our X profile.\n"
"- Always cross-reference the Mint Address across our official platforms.\n\n"
"2. NO PRIVATE SALES 🚫\n"
"- PILLRAVE is a 100% Fair Launch.\n"
"- No seed rounds, no private presales, no special allocations.\n"
"- Anyone claiming to sell $PILL before official launch is a bad actor.\n\n"
"3. WALLET HYGIENE 🦾\n"
"- No Cyberavers team member will ever ask for your seed phrase or private keys.\n"
"- Use a burner wallet for new mints. Keep main assets in cold storage.\n\n"
"4. UNDERSTAND THE UTILITY ⚖️\n"
"- $PILL is a Utility Token powering the PILLRAVE audio-identification protocol and DAO.\n"
"- Read our Legal Framework and AML Policy at cyberavers.online before participating.\n\n"
"5. THE AFTER PROTOCOL (STAKING) 🧪\n"
"- Locking periods: 7, 30 and 90 days.\n"
"- Governance is a responsibility, not just a reward.\n\n"
"Stay alert. Stay decentralized.\n"
"🌐 cyberavers.online\n"
"[ SIGNAL: PROTECTED ]"
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

# Mixcloud: acid-ted
MC_RSS = "https://www.mixcloud.com/acid-ted/feed/"
MC_POSTED = set()
last_mc_day = None
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
    if hour == 9 and now.minute == 0 and last_price_day != today:
        cid = load()
        if not cid:
            return
        last_price_day = today  # Set first to prevent double-posting
        p = fetch_prices()
        if p:
            send_all(format_prices(p))
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
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; PillRaveBot/1.0)",
            "Accept": "application/rss+xml, application/xml, text/xml, */*"
        })
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print("[RSS ERR] " + url.split("/")[2] + " -> " + str(e)[:60])
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
    if last_news_time and (now - last_news_time) < timedelta(hours=6, minutes=-5):
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
    send_all(format_news(item) + "\n\n" + item["link"])
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
                [{"text": "💊 BUY PILLRAVE", "url": PUMP_URL},
                 {"text": "🌐 WEBSITE",      "url": WEB_URL}],
                [{"text": "📱 Instagram", "url": "https://instagram.com/cybarravers"},
                 {"text": "🐦 Twitter/X", "url": "https://x.com/CyberRaversNFT"}],
                [{"text": "🎧 SoundCloud", "url": "https://soundcloud.com/cyberavers-pillrave"},
                 {"text": "🎵 Mixcloud",   "url": "https://www.mixcloud.com/acid-ted"}]
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

all_chats = set()

def save(cid):
    global saved
    saved = str(cid)
    all_chats.add(str(cid))
    try:
        with open("/tmp/pillcid.txt", "w") as f:
            f.write(str(cid))
        # Save all chats
        with open("/tmp/allchats.txt", "w") as f:
            f.write("\n".join(all_chats))
    except:
        pass
    print("[INFO] Chat ID saved: " + str(cid))

def load():
    global saved
    if saved:
        return saved
    try:
        with open("/tmp/pillcid.txt") as f:
            saved = f.read().strip()
        # Load all chats
        try:
            with open("/tmp/allchats.txt") as f:
                for line in f.read().strip().split("\n"):
                    if line.strip():
                        all_chats.add(line.strip())
        except:
            if saved:
                all_chats.add(saved)
        return saved
    except:
        return None

def get_all_chats():
    load()
    return list(all_chats) if all_chats else ([saved] if saved else [])

def send_all(txt):
    chats = get_all_chats()
    for cid in chats:
        try:
            call("sendMessage", {"chat_id": int(cid), "text": txt})
        except Exception as e:
            print("[ERR] send_all " + str(cid) + ": " + str(e))

def send_all(text, use_menu=False):
    """Send a message to ALL registered groups."""
    targets = list(all_chats) if all_chats else ([saved] if saved else [])
    for cid in targets:
        try:
            if use_menu:
                send_menu(int(cid), text)
            else:
                send(int(cid), text)
        except Exception as e:
            print("[BROADCAST ERR] " + str(cid) + ": " + str(e))

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

    # ─── Auto-reply keywords ──────────────────────────────────
    txt_lower = txt.lower()
    keyword_replies = {
        "when launch": "The PILLRAVE protocol is LIVE now on Pump.fun! Use /launch for details.",
        "when moon": "The moon is the floor, Operator. Focus on utility. Use /token to understand the protocol.",
        "wen": "It's already live. Use /launch to check the status.",
        "rug": "100% fair launch. No locked team wallets. No private rounds. Use /safety for the full security guide.",
        "scam": "PILLRAVE is a verified fair launch on Solana. Use /safety for full security info.",
        "contract": f"Official contract: https://pump.fun/coin/6uCaWNvRTUExSMM6qnFF2uujcRVWXbRwL9eFSUdJpump — Always verify on official channels.",
        "ca ": f"Official CA: https://pump.fun/coin/6uCaWNvRTUExSMM6qnFF2uujcRVWXbRwL9eFSUdJpump",
        "buy": "Use /buy for step-by-step instructions. Direct link: https://pump.fun/coin/6uCaWNvRTUExSMM6qnFF2uujcRVWXbRwL9eFSUdJpump",
        "how to": "Use /buy for purchase guide, /dao for governance, /token for tokenomics.",
        "price": "Use /price for live SOL and BTC prices. $PILL is currently on the bonding curve at pump.fun.",
        "staking": "Staking (The After) launches once the bond curve is met. Use /tiers for tier details.",
        "airdrop": "Airdrops & rewards = 10% of total supply (90.9M $PILL). Use /token for full distribution.",
        "whitepaper": "Read our full documentation at cyberavers.online",
        "website": "Official site: cyberavers.online",
        "twitter": "Follow us: https://x.com/CyberRaversNFT",
        "instagram": "Follow us: https://instagram.com/cybarravers",
        "gm": "GM Operator. The grid is live. 💊",
        "gn": "GN Operator. The signal never sleeps. 💊",
        "wagmi": "WAGMI. The protocol is live. Stay decentralized. 💊",
        "ngmi": "Don't say that. Read /info and understand the mission. 💊",
        "lfg": "LFG! Protocol is live. Use /launch for the full status. 🚀",
    }

    for keyword, reply in keyword_replies.items():
        if keyword in txt_lower and not txt_lower.startswith("/"):
            send(cid, reply)
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
            send(cid, format_news(item) + "\n\n" + item["link"])
        else:
            send(cid, "No relevant news found at this time. Try again later.")
    elif txt in ("/price", "/sol", "/btc"):
        p = fetch_prices()
        if p:
            send(cid, format_prices(p))
        else:
            send(cid, "Could not fetch prices. Try again later.")
    elif txt in ("/mixcloud", "/acidted", "/mc"):
        item = fetch_mc_mix()
        if item:
            MC_POSTED.add(item["link"])
            send(cid, format_mc_mix(item) + "\n\n" + item["link"])
        else:
            send(cid, "Could not fetch Mixcloud mix. Try again later.")
    elif txt in ("/mix", "/dailymix"):
        item = fetch_sc_mix()
        if item:
            SC_POSTED.add(item["link"])
            send(cid, format_sc_mix(item) + "\n\n" + item["link"])
        else:
            send(cid, "Could not fetch the mix. Try again later.")
    elif txt in ("/track", "/dailytrack"):
        t = get_daily_track()
        send(cid, format_track(t) + "\n\n" + t["url"])
    elif txt in ("/blast", "/announce_all"):
        # Post full launch sequence to group
        c = load()
        if c:
            send_menu(int(c), MSGS["launch"])
            send(int(c), "https://www.youtube.com/watch?v=BDj73pGQ6pE")
            import time as _t; _t.sleep(2)
            send_menu(int(c), MSGS["safety"])
            send(cid, "Blast sent to group.")
    elif txt in ("/acidted", "/mixcloud", "/mc"):
        item = fetch_mc_mix()
        if item:
            MC_POSTED.add(item["link"])
            send(cid, format_mc_mix(item) + "\n\n" + item["link"])
        else:
            send(cid, "Could not fetch Mixcloud mix. Try again later.")
    elif txt in ("/section", "/web_post", "/featured"):
        section = WEB_SECTIONS[web_section_index % len(WEB_SECTIONS)]
        msg = "📡 " + section["title"] + "\n\n" + section["content"]
        send(cid, msg)
    elif txt in ("/pill", "/buypill", "/token_link"):
        send(cid, MSGS["daily_pump"])
    elif txt in ("/launch", "/live", "/protocol"):
        send_menu(cid, MSGS["launch"])
        send(cid, "https://www.youtube.com/watch?v=BDj73pGQ6pE")
    elif txt in ("/safety", "/security", "/safe"):
        send_menu(cid, MSGS["safety"])
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

def fetch_mc_mix():
    try:
        xml = fetch_rss(MC_RSS)
        if not xml:
            print("[MC] Empty RSS response")
            return None
        items = parse_rss(xml)
        print("[MC] Items parsed: " + str(len(items)))
        if items:
            return items[0]
        return None
    except Exception as e:
        print("[MC ERR] " + str(e))
        return None

def format_mc_mix(item):
    return "🎚️ ACID TED MIX — Mixcloud\n\n" + item["title"]

def auto_post_mc_mix():
    global last_mc_day
    now = datetime.now()
    today = now.date()
    if now.hour == 22 and now.minute == 0 and last_mc_day != today:
        cid = load()
        if not cid:
            return
        last_mc_day = today
        item = fetch_mc_mix()
        if item and item["link"] not in MC_POSTED:
            MC_POSTED.add(item["link"])
            send_all(format_mc_mix(item) + "\n\n" + item["link"])
            print("[MC MIX] Posted: " + item["title"][:60])

def fetch_sc_mix():
    try:
        xml = fetch_rss(SC_RSS)
        if not xml:
            print("[SC] Empty response from RSS")
            return None
        print("[SC] RSS fetched, length: " + str(len(xml)))
        items = parse_rss(xml)
        print("[SC] Items parsed: " + str(len(items)))
        if items:
            print("[SC] First item: " + items[0].get("title","?")[:50])
            return items[0]
        # Try alternate parsing for SoundCloud format
        import re as _re
        links = _re.findall(r'<enclosure url="([^"]+)"', xml)
        titles = _re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', xml)
        if links and len(titles) > 1:
            return {"title": titles[1], "link": links[0], "desc": ""}
        return None
    except Exception as e:
        print("[SC ERR] " + str(e))
        return None

def format_sc_mix(item):
    # Return only a short header — the URL generates the rich preview
    return "🎧 MIX OF THE DAY — The Classic Mix CD Series"

def auto_post_sc_mix():
    global last_sc_day
    now = datetime.now()
    today = now.date()
    hour = now.hour
    # Post SC mix at 8 PM every day
    if hour == 20 and now.minute == 0 and last_sc_day != today:
        cid = load()
        if not cid:
            return
        last_sc_day = today  # Set first to prevent double-posting
        item = fetch_sc_mix()
        if item and item["link"] not in SC_POSTED:
            SC_POSTED.add(item["link"])
            send_all(format_sc_mix(item) + "\n\n" + item["link"])
            print("[SC MIX] Posted: " + item["title"][:60])

def auto_post_daily_pump():
    global last_price_day
    # Reuse last_price_day logic but for a different hour (6 PM)
    # Use a separate tracker
    pass  # handled below

last_pump_day = None

def fetch_mc_mix():
    try:
        xml = fetch_rss(MC_RSS)
        if not xml:
            print("[MC] Empty response")
            return None
        items = parse_rss(xml)
        if items:
            print("[MC] Got: " + items[0].get("title","?")[:50])
            return items[0]
        return None
    except Exception as e:
        print("[MC ERR] " + str(e))
        return None

def format_mc_mix(item):
    return "🎧 ACID TED MIX — Mixcloud\n\n" + item["title"]

def auto_post_mc_mix():
    global last_mc_day
    now = datetime.now()
    today = now.date()
    hour = now.hour
    minute = now.minute
    # Post Mixcloud mix at 10 PM daily
    if hour == 22 and minute == 0 and last_mc_day != today:
        cid = load()
        if not cid:
            return
        last_mc_day = today
        item = fetch_mc_mix()
        if item and item["link"] not in MC_POSTED:
            MC_POSTED.add(item["link"])
            send_all(format_mc_mix(item) + "\n\n" + item["link"])
            print("[MC] Posted: " + item["title"][:60])

last_pump_day = None

def auto_post_pump():
    global last_pump_day
    now = datetime.now()
    today = now.date()
    hour = now.hour
    minute = now.minute
    # Post daily pump message at 6 PM
    if hour == 18 and minute == 0 and last_pump_day != today:
        cid = load()
        if not cid:
            return
        last_pump_day = today
        send_all(MSGS["daily_pump"])
        print("[PUMP] Daily pump message posted")

def auto_post_track():
    global last_track_day
    now = datetime.now()
    today = now.date()
    hour = now.hour
    # Publica a las 12:00 PM cada dia
    if hour == 12 and now.minute == 0 and last_track_day != today:
        cid = load()
        if cid:
            last_track_day = today  # Set first to prevent double-posting
            t = get_daily_track()
            send_all(format_track(t) + "\n\n" + t["url"])
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
            auto_post_pump()
            auto_post_web_section()
            auto_post_mc_mix()
            auto_post_mc_mix()
            r = get_upd(off)
            if r and r.get("ok"):
                for u in r["result"]:
                    off = u["update_id"] + 1
                    if "message" in u:
                        handle(u["message"])
            time.sleep(60)  # Check auto-posts every 60 seconds
        except KeyboardInterrupt:
            print("Detenido.")
            break
        except Exception as e:
            print("[ERR] " + str(e))
            time.sleep(30)

if __name__ == "__main__":
    main()
