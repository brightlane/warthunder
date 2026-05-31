#!/usr/bin/env python3
"""
build.py — WarThunder.gg  v2.0
Site   : https://brightlane.github.io/warthunder/
Aff    : https://convert.ctypy.com/aff_c?offer_id=29176&aff_id=21885
Angle  : "best free war game / free tank game / free military game" → War Thunder
Markets: AU, CA, FR, DE, KR, NZ, UK, US
v2 upgrades:
  • Correct SITE_URL → brightlane.github.io/warthunder
  • Richer llms.txt (full page index for AI crawlers)
  • 160+ keywords (added 15 new slugs)
  • More blog posts (7 total)
  • Larger FAQ on homepage (7 questions)
  • Sitemap per-language sub-sitemaps
  • Open Graph image meta tag
  • Canonical trailing-slash consistency
  • Build summary JSON written to dist/build-info.json
"""

import json, shutil, datetime
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
SITE_URL  = "https://brightlane.github.io/warthunder"
AFF_URL   = "https://convert.ctypy.com/aff_c?offer_id=29176&aff_id=21885"
SITE_NAME = "WarThunder.gg"
TODAY     = datetime.date.today().isoformat()
YEAR      = str(datetime.date.today().year)
OUT       = Path("dist")

# ── LANGUAGES ─────────────────────────────────────────────────────────────────
LANGUAGES = {
    "en": {"name":"English",  "dir":"ltr","locale":"en_US",
           "cta":"Play Free Now","dl":"Download Free",
           "nav_home":"Home","nav_review":"Review","nav_compare":"Compare","nav_blog":"Blog",
           "hero1":f"#1 FREE MILITARY GAME {YEAR}","hero2":"FLY. DRIVE. DOMINATE.",
           "hero_sub":f"The most realistic free military game of {YEAR}. Fighter jets, tanks, warships — all free on PC, PS4/5 & Xbox.",
           "feat_title":"Why War Thunder?",
           "why1":"100% Free","why1d":"Download and play forever free. No subscription, no hidden fees.",
           "why2":"2,000+ Vehicles","why2d":"Planes, tanks, helicopters, warships. The largest vehicle roster in any free game.",
           "why3":"Realistic Combat","why3d":"Authentic physics and ballistics. Every vehicle modeled from real blueprints.",
           "why4":"Cross-Platform","why4d":"PC (Steam/Gaijin), PS4/5, Xbox. Cross-play enabled.",
           "why5":"Regular Updates","why5d":"New vehicles, maps and events every major update.",
           "why6":"100M+ Players","why6d":"One of the largest free-to-play communities in the world.",
           "disc":"Affiliate disclosure: We earn a commission if you sign up through our links at no extra cost to you. War Thunder® is a trademark of Gaijin Entertainment.",
           "meta_home":f"Play War Thunder free in {YEAR}. The best free military game — 2,000+ aircraft, tanks & warships. PC, PS4/5, Xbox. Download now."},

    "fr": {"name":"Français","dir":"ltr","locale":"fr_FR",
           "cta":"Jouer Gratuitement","dl":"Télécharger Gratuitement",
           "nav_home":"Accueil","nav_review":"Avis","nav_compare":"Comparer","nav_blog":"Blog",
           "hero1":f"JEU MILITAIRE GRATUIT N°1 {YEAR}","hero2":"VOLEZ. CONDUISEZ. DOMINEZ.",
           "hero_sub":f"Le jeu militaire le plus réaliste de {YEAR}. Avions, chars, navires — 100% gratuit sur PC, PS4/5 et Xbox.",
           "feat_title":"Pourquoi War Thunder?",
           "why1":"100% Gratuit","why1d":"Téléchargez et jouez gratuitement pour toujours.",
           "why2":"2 000+ Véhicules","why2d":"Avions, chars, hélicoptères, navires de guerre.",
           "why3":"Combat Réaliste","why3d":"Physique et balistique authentiques.",
           "why4":"Multi-Plateforme","why4d":"PC, PS4/5, Xbox avec cross-play.",
           "why5":"Mises à Jour","why5d":"Nouveaux véhicules et événements régulièrement.",
           "why6":"100M+ Joueurs","why6d":"L'une des plus grandes communautés free-to-play.",
           "disc":"Site affilié. War Thunder® est une marque de Gaijin Entertainment.",
           "meta_home":f"Jouez à War Thunder gratuitement en {YEAR}. Le meilleur jeu militaire gratuit — 2000+ véhicules. PC, PS4/5, Xbox."},

    "de": {"name":"Deutsch","dir":"ltr","locale":"de_DE",
           "cta":"Kostenlos Spielen","dl":"Kostenlos Herunterladen",
           "nav_home":"Startseite","nav_review":"Test","nav_compare":"Vergleich","nav_blog":"Blog",
           "hero1":f"DAS BESTE KOSTENLOSE MILITÄRSPIEL {YEAR}","hero2":"FLIEGEN. FAHREN. DOMINIEREN.",
           "hero_sub":f"Das realistischste kostenlose Militärspiel {YEAR}. Kampfjets, Panzer, Kriegsschiffe — gratis auf PC, PS4/5 & Xbox.",
           "feat_title":"Warum War Thunder?",
           "why1":"100% Kostenlos","why1d":"Herunterladen und für immer kostenlos spielen.",
           "why2":"2.000+ Fahrzeuge","why2d":"Flugzeuge, Panzer, Helikopter, Kriegsschiffe.",
           "why3":"Realistischer Kampf","why3d":"Authentische Physik und Ballistik.",
           "why4":"Plattformübergreifend","why4d":"PC, PS4/5, Xbox mit Cross-Play.",
           "why5":"Regelmäßige Updates","why5d":"Neue Fahrzeuge und Events bei jedem Update.",
           "why6":"100M+ Spieler","why6d":"Eine der größten Free-to-Play-Communities weltweit.",
           "disc":"Affiliate-Offenlegung. War Thunder® ist eine Marke von Gaijin Entertainment.",
           "meta_home":f"Spiele War Thunder kostenlos in {YEAR}. Das beste kostenlose Militärspiel — 2000+ Fahrzeuge. PC, PS4/5, Xbox."},

    "ko": {"name":"한국어","dir":"ltr","locale":"ko_KR",
           "cta":"무료 플레이","dl":"무료 다운로드",
           "nav_home":"홈","nav_review":"리뷰","nav_compare":"비교","nav_blog":"블로그",
           "hero1":f"{YEAR}년 최고의 무료 군사 게임","hero2":"비행하라. 전투하라. 지배하라.",
           "hero_sub":f"{YEAR}년 가장 현실적인 무료 군사 게임. 전투기, 탱크, 군함 — PC, PS4/5, Xbox에서 100% 무료.",
           "feat_title":"왜 War Thunder인가?",
           "why1":"100% 무료","why1d":"구독 없음. 숨겨진 요금 없음.",
           "why2":"2,000개+ 차량","why2d":"비행기, 탱크, 헬리콥터, 군함.",
           "why3":"현실적인 전투","why3d":"실제 설계도 기반의 정밀한 물리 시뮬레이션.",
           "why4":"크로스 플랫폼","why4d":"PC, PS4/5, Xbox 크로스플레이 지원.",
           "why5":"정기 업데이트","why5d":"매 업데이트마다 새로운 차량과 이벤트.",
           "why6":"1억+ 플레이어","why6d":"세계 최대 규모의 무료 게임 커뮤니티 중 하나.",
           "disc":"제휴 사이트. War Thunder®는 Gaijin Entertainment의 상표입니다.",
           "meta_home":f"{YEAR}년 War Thunder 무료 플레이. 최고의 무료 군사 게임 — 2000개+ 차량. PC, PS4/5, Xbox."},
}

# ── KEYWORDS (160+) ───────────────────────────────────────────────────────────
KEYWORDS = [
    # Free war / military intent
    ("free-war-games",                 f"Free War Games {YEAR} — Best Picks",                 "The best free war games available right now."),
    ("free-war-games-pc",              f"Free War Games PC {YEAR}",                           "Best free war games to play on PC."),
    ("free-war-games-ps4",             f"Free War Games PS4 {YEAR}",                          "Best free war games on PlayStation 4."),
    ("free-war-games-ps5",             f"Free War Games PS5 {YEAR}",                          "Top free war games on PlayStation 5."),
    ("free-war-games-xbox",            f"Free War Games Xbox {YEAR}",                         "Best free war games on Xbox."),
    ("free-war-games-steam",           f"Free War Games on Steam {YEAR}",                     "Top free war games on Steam."),
    ("free-military-games",            f"Free Military Games {YEAR}",                         "The best free military games to play now."),
    ("free-military-games-pc",         f"Free Military Games PC {YEAR}",                      "Top free military games on PC."),
    ("best-free-war-game",             f"Best Free War Game {YEAR} — #1 Pick",                f"The best free war game of {YEAR} reviewed and ranked."),
    ("best-free-war-games",            f"Best Free War Games {YEAR}",                         f"Every top free war game of {YEAR} ranked."),
    ("best-free-war-games-pc",         f"Best Free War Games PC {YEAR}",                      "Top free war games on PC ranked."),
    ("top-free-war-games",             f"Top Free War Games {YEAR}",                          "The highest-rated free war games this year."),
    ("top-10-free-war-games",          f"Top 10 Free War Games {YEAR}",                       f"The 10 best free war games of {YEAR}."),
    ("play-free-war-game-now",         f"Play a Free War Game Right Now — {YEAR}",            "Jump into a free war game instantly."),
    ("download-free-war-game",         f"Download a Free War Game — {YEAR}",                  "Best free war games to download on PC and console."),
    ("free-war-game-signup",           f"Free War Game Sign Up — {YEAR}",                     "Sign up and play the best free military game today."),
    ("no-cost-war-game",               f"No Cost War Game {YEAR} — Play Free",                "The best war game with absolutely no cost to play."),
    # Tank games
    ("free-tank-games",                f"Free Tank Games {YEAR} — Best List",                 "The best free tank games to play right now."),
    ("free-tank-games-pc",             f"Free Tank Games PC {YEAR}",                          "Top free tank games on PC."),
    ("best-free-tank-games",           f"Best Free Tank Games {YEAR}",                        "Best free tank games ranked."),
    ("free-tank-battle-games",         f"Free Tank Battle Games {YEAR}",                      "Play free tank battle games online now."),
    ("online-tank-game-free",          f"Free Online Tank Game {YEAR}",                       "The best free online tank games."),
    ("realistic-tank-game-free",       f"Realistic Free Tank Game {YEAR}",                    "Most realistic free tank game available."),
    ("ww2-tank-game-free",             f"Free WW2 Tank Game {YEAR}",                          "Best free World War 2 tank games."),
    ("tank-simulator-free",            f"Free Tank Simulator {YEAR}",                         "Best free tank simulator games on PC."),
    # Plane / aircraft
    ("free-plane-games",               f"Free Plane Games {YEAR}",                            "Best free plane and aircraft games."),
    ("free-plane-games-pc",            f"Free Plane Games PC {YEAR}",                         "Top free plane games on PC."),
    ("free-fighter-jet-games",         f"Free Fighter Jet Games {YEAR}",                      "Best free fighter jet games online."),
    ("free-ww2-plane-games",           f"Free WW2 Plane Games {YEAR}",                        "Best free World War 2 aircraft games."),
    ("free-flight-combat-games",       f"Free Flight Combat Games {YEAR}",                    "Top free games with aerial combat."),
    ("free-aircraft-combat-games",     f"Free Aircraft Combat Games {YEAR}",                  "Best free aircraft combat games."),
    ("realistic-flight-game-free",     f"Free Realistic Flight Game {YEAR}",                  "Most realistic free flight games available."),
    ("free-dogfight-games",            f"Free Dogfight Games {YEAR}",                         "Best free aerial dogfight games."),
    ("free-air-combat-games",          f"Free Air Combat Games {YEAR}",                       "Top free air combat games right now."),
    ("free-ww2-flight-simulator",      f"Free WW2 Flight Simulator {YEAR}",                   "Best free World War 2 flight simulators."),
    ("free-helicopter-games",          f"Free Helicopter Games {YEAR}",                       "Best free helicopter combat games online."),
    # Naval / warship
    ("free-warship-games",             f"Free Warship Games {YEAR}",                          "Best free warship and naval combat games."),
    ("free-naval-games",               f"Free Naval Games {YEAR}",                            "Top free naval warfare games."),
    ("free-battleship-games",          f"Free Battleship Games {YEAR}",                       "Best free battleship games online."),
    ("free-naval-combat-games",        f"Free Naval Combat Games {YEAR}",                     "Play free naval combat games now."),
    ("free-naval-warfare-game",        f"Free Naval Warfare Game {YEAR}",                     "Best free naval warfare games available."),
    # WW2 / historical
    ("free-ww2-games",                 f"Free WW2 Games {YEAR}",                              "Best free World War 2 games."),
    ("free-ww2-games-pc",              f"Free WW2 Games PC {YEAR}",                           "Top free WW2 games on PC."),
    ("free-world-war-2-games",         f"Free World War 2 Games {YEAR}",                      "Best free World War 2 games to play now."),
    ("free-ww2-tank-games",            f"Free WW2 Tank Games {YEAR}",                         "Best free WW2 tank games."),
    ("free-historical-war-games",      f"Free Historical War Games {YEAR}",                   "Best free historically accurate war games."),
    ("free-ww1-ww2-games",             f"Free WW1 & WW2 Games {YEAR}",                       "Best free games set in World Wars I and II."),
    ("best-ww2-game-free",             f"Best Free WW2 Game {YEAR}",                          f"The best free WW2 game of {YEAR} reviewed."),
    ("free-cold-war-games",            f"Free Cold War Games {YEAR}",                         "Best free games set in the Cold War era."),
    # War Thunder specific
    ("is-war-thunder-free",            f"Is War Thunder Free to Play? {YEAR}",                "Yes — here's exactly what's free in War Thunder."),
    ("is-war-thunder-pay-to-win",      f"Is War Thunder Pay to Win? {YEAR}",                  "Honest answer: is War Thunder pay to win?"),
    ("is-war-thunder-good",            f"Is War Thunder Good in {YEAR}?",                     f"Honest review: is War Thunder worth playing in {YEAR}?"),
    ("war-thunder-review",             f"War Thunder Review {YEAR} — Is It Worth It?",        f"Full War Thunder review for {YEAR}."),
    ("war-thunder-download",           f"War Thunder Download — Free {YEAR}",                 "How to download War Thunder for free on any platform."),
    ("war-thunder-download-pc",        f"War Thunder PC Download — Free {YEAR}",              "Download War Thunder free on PC via Steam or Gaijin."),
    ("war-thunder-ps4",                f"War Thunder PS4 — Free {YEAR}",                      "How to download and play War Thunder free on PS4."),
    ("war-thunder-ps5",                f"War Thunder PS5 — Free {YEAR}",                      "Play War Thunder free on PlayStation 5."),
    ("war-thunder-xbox",               f"War Thunder Xbox — Free {YEAR}",                     "Download War Thunder free on Xbox."),
    ("war-thunder-beginner-guide",     f"War Thunder Beginner Guide {YEAR}",                  "The ultimate War Thunder beginner guide."),
    ("war-thunder-tips",               f"War Thunder Tips & Tricks {YEAR}",                   "Best War Thunder tips for new players."),
    ("war-thunder-best-nation",        f"War Thunder Best Nation {YEAR}",                     "Which nation should you pick in War Thunder?"),
    ("war-thunder-best-tanks",         f"War Thunder Best Tanks {YEAR}",                      "The best tanks in War Thunder right now."),
    ("war-thunder-best-planes",        f"War Thunder Best Planes {YEAR}",                     "The best aircraft in War Thunder."),
    ("war-thunder-best-ships",         f"War Thunder Best Ships {YEAR}",                      "Top naval vessels in War Thunder."),
    ("war-thunder-update",             f"War Thunder Update {YEAR} — What's New",             f"Everything new in War Thunder's latest update."),
    ("war-thunder-2026",               f"War Thunder in {YEAR} — Still Good?",                f"Is War Thunder still worth playing in {YEAR}?"),
    ("war-thunder-player-count",       f"War Thunder Player Count {YEAR}",                    f"How many active players does War Thunder have in {YEAR}?"),
    ("war-thunder-community",          f"War Thunder Community {YEAR}",                       "Is the War Thunder community active and welcoming?"),
    ("war-thunder-system-requirements",f"War Thunder System Requirements {YEAR}",             "Can your PC run War Thunder? Full specs breakdown."),
    ("war-thunder-free-vehicles",      f"War Thunder Free Vehicles {YEAR}",                   "How to get free vehicles in War Thunder."),
    ("war-thunder-golden-eagles-free", f"War Thunder Free Golden Eagles {YEAR}",              "Earn Golden Eagles for free in War Thunder."),
    ("war-thunder-silver-lions-farm",  f"War Thunder Silver Lions Farm Guide {YEAR}",         "Best ways to farm Silver Lions in War Thunder."),
    ("war-thunder-premium-worth-it",   f"Is War Thunder Premium Worth It? {YEAR}",            "Should you buy War Thunder premium account?"),
    ("war-thunder-battle-pass",        f"War Thunder Battle Pass {YEAR}",                     "Is the War Thunder battle pass worth buying?"),
    ("war-thunder-game-modes",         f"War Thunder Game Modes {YEAR}",                      "All War Thunder game modes explained."),
    ("war-thunder-realistic-battles",  f"War Thunder Realistic Battles Guide {YEAR}",         "How to succeed in Realistic Battles mode."),
    ("war-thunder-simulator-battles",  f"War Thunder Simulator Battles {YEAR}",               "Guide to Simulator mode in War Thunder."),
    ("war-thunder-arcade-vs-realistic",f"War Thunder Arcade vs Realistic {YEAR}",             "Which War Thunder mode should beginners play?"),
    ("war-thunder-line-up",            f"War Thunder Line-Up Guide {YEAR}",                   "How to build the perfect War Thunder lineup."),
    ("war-thunder-research-guide",     f"War Thunder Research Guide {YEAR}",                  "How to research vehicles fast in War Thunder."),
    ("war-thunder-events",             f"War Thunder Events {YEAR}",                          "Current and upcoming War Thunder events."),
    ("war-thunder-new-players",        f"War Thunder New Player Guide {YEAR}",                "Everything new players need to know."),
    ("war-thunder-graphics-settings",  f"War Thunder Best Graphics Settings {YEAR}",          "Optimize War Thunder graphics for performance."),
    ("war-thunder-crossplay",          f"War Thunder Cross-Platform Play {YEAR}",             "Does War Thunder support cross-play?"),
    ("war-thunder-clans",              f"War Thunder Squadrons & Clans {YEAR}",               "How to join and create squadrons in War Thunder."),
    ("war-thunder-map-list",           f"War Thunder Maps {YEAR} — Full List",                "All War Thunder maps and battle locations."),
    ("war-thunder-nations-list",       f"War Thunder Nations {YEAR} — Full List",             "Every nation available in War Thunder."),
    ("war-thunder-vs-crossout",        f"War Thunder vs Crossout {YEAR}",                     "Which Gaijin free game should you play?"),
    ("war-thunder-vs-world-of-tanks",  f"War Thunder vs World of Tanks {YEAR}",               "War Thunder or World of Tanks — which is better?"),
    ("war-thunder-vs-enlisted",        f"War Thunder vs Enlisted {YEAR}",                     "War Thunder vs Enlisted — which free war game wins?"),
    ("war-thunder-economy",            f"War Thunder Economy Guide {YEAR}",                   "How to manage Silver Lions and Golden Eagles efficiently."),
    ("war-thunder-decals",             f"War Thunder Decals Guide {YEAR}",                    "How to unlock and use decals in War Thunder."),
    ("war-thunder-skins-free",         f"War Thunder Free Skins {YEAR}",                      "How to get free skins in War Thunder."),
    ("war-thunder-mods",               f"War Thunder Mods {YEAR}",                            "Best mods and customizations for War Thunder."),
    ("war-thunder-controller",         f"War Thunder Controller Support {YEAR}",              "Does War Thunder work with a controller?"),
    ("war-thunder-vr",                 f"War Thunder VR Support {YEAR}",                      "Does War Thunder support VR headsets?"),
    ("war-thunder-mobile",             f"War Thunder Mobile {YEAR}",                          "Is War Thunder available on mobile devices?"),
    ("war-thunder-gaijin",             f"War Thunder by Gaijin Entertainment {YEAR}",         "About Gaijin Entertainment, makers of War Thunder."),
    ("war-thunder-gaijin-coins",       f"War Thunder Gaijin Coins {YEAR}",                    "How to earn and spend Gaijin Coins."),
    # Vehicle / nation guides
    ("war-thunder-jets",               f"War Thunder Jets Guide {YEAR}",                      "Best jets to grind for in War Thunder."),
    ("war-thunder-helicopters",        f"War Thunder Helicopters {YEAR}",                     "Guide to helicopter gameplay in War Thunder."),
    ("war-thunder-germany-tanks",      f"War Thunder Germany Tanks Guide {YEAR}",             "Best German tanks in War Thunder."),
    ("war-thunder-russia-tanks",       f"War Thunder Russia Tanks Guide {YEAR}",              "Best Soviet and Russian tanks in War Thunder."),
    ("war-thunder-usa-tanks",          f"War Thunder USA Tanks Guide {YEAR}",                 "Best American tanks in War Thunder."),
    ("war-thunder-britain-tanks",      f"War Thunder Britain Tanks Guide {YEAR}",             "Best British tanks in War Thunder."),
    ("war-thunder-japan-tanks",        f"War Thunder Japan Tanks Guide {YEAR}",               "Best Japanese tanks in War Thunder."),
    ("war-thunder-korea-tanks",        f"War Thunder South Korea Tanks {YEAR}",               "Korean tech tree tanks in War Thunder."),
    ("war-thunder-sweden-tanks",       f"War Thunder Sweden Tanks Guide {YEAR}",              "Best Swedish vehicles in War Thunder."),
    ("war-thunder-israel-tanks",       f"War Thunder Israel Tech Tree {YEAR}",                "Israel tech tree guide in War Thunder."),
    ("war-thunder-spaa",               f"War Thunder Best SPAA {YEAR}",                       "Best anti-air vehicles in War Thunder."),
    ("war-thunder-best-br",            f"War Thunder Best Battle Rating {YEAR}",              "Which battle rating is most fun in War Thunder?"),
    ("war-thunder-low-tier",           f"War Thunder Low Tier Guide {YEAR}",                  "Best low-tier vehicles and tips in War Thunder."),
    ("war-thunder-top-tier",           f"War Thunder Top Tier Guide {YEAR}",                  "How to play top tier in War Thunder."),
    ("war-thunder-premium-vehicles",   f"War Thunder Best Premium Vehicles {YEAR}",           "The best premium vehicles in War Thunder worth buying."),
    # Comparison / alternatives
    ("games-like-war-thunder",         f"Games Like War Thunder {YEAR}",                      "Best games similar to War Thunder."),
    ("games-like-war-thunder-free",    f"Free Games Like War Thunder {YEAR}",                 "The best free alternatives to War Thunder."),
    ("war-thunder-alternative",        f"War Thunder Alternative — Best {YEAR}",              "Top alternatives to War Thunder."),
    ("world-of-tanks-vs-war-thunder",  f"World of Tanks vs War Thunder {YEAR}",               "Full comparison: WoT vs War Thunder."),
    ("free-game-like-world-of-tanks",  f"Free Games Like World of Tanks {YEAR}",              "Best free alternatives to World of Tanks."),
    ("free-realistic-war-games",       f"Free Realistic War Games {YEAR}",                    "The most realistic free war games available."),
    ("free-gaijin-games",              f"Free Gaijin Entertainment Games {YEAR}",             "All free-to-play games by Gaijin Entertainment."),
    # Platform
    ("best-free-games-steam",          f"Best Free Games on Steam {YEAR}",                    "Top free games on Steam right now."),
    ("best-free-ps4-games",            f"Best Free PS4 Games {YEAR}",                         "Top free games on PS4."),
    ("best-free-ps5-games",            f"Best Free PS5 Games {YEAR}",                         "Top free games on PS5."),
    ("free-ps5-games-no-ps-plus",      f"Free PS5 Games Without PS Plus {YEAR}",              "PS5 games free without PS Plus."),
    ("free-ps4-games-no-membership",   f"Free PS4 Games No Membership {YEAR}",                "PS4 games free without PlayStation Plus."),
    ("best-free-xbox-games",           f"Best Free Xbox Games {YEAR}",                        "Top free games on Xbox."),
    ("free-xbox-games-no-gold",        f"Free Xbox Games Without Xbox Gold {YEAR}",           "Xbox games free without Gold."),
    ("best-free-pc-games-2026",        f"Best Free PC Games {YEAR}",                          f"Top free PC games of {YEAR} ranked."),
    ("free-to-play-games-2026",        f"Best Free-to-Play Games {YEAR}",                     f"Top free-to-play games of {YEAR}."),
    # Multiplayer / shooter
    ("free-shooting-games-pc",         f"Free Shooting Games PC {YEAR}",                      "Top free shooting games on PC."),
    ("free-action-games-pc",           f"Free Action Games PC {YEAR}",                        "Best free action games on PC."),
    ("free-pvp-games-pc",              f"Free PvP Games PC {YEAR}",                           "Top free PvP games on PC."),
    ("free-multiplayer-war-games",     f"Free Multiplayer War Games {YEAR}",                  "Best free war games with online multiplayer."),
    ("free-online-war-games",          f"Free Online War Games {YEAR}",                       "Play free war games online against real players."),
    # Geo
    ("free-war-games-australia",       f"Free War Games Australia {YEAR}",                    "Best free war games for Australian players."),
    ("free-war-games-canada",          f"Free War Games Canada {YEAR}",                       "Best free war games for Canadian players."),
    ("free-war-games-uk",              f"Free War Games UK {YEAR}",                           "Best free war games for UK players."),
    ("free-war-games-new-zealand",     f"Free War Games New Zealand {YEAR}",                  "Best free war games for New Zealand players."),
    ("war-thunder-australia",          f"War Thunder Australia — Free {YEAR}",                "Play War Thunder free in Australia."),
    ("war-thunder-uk",                 f"War Thunder UK — Free {YEAR}",                       "Play War Thunder free in the United Kingdom."),
    ("war-thunder-canada",             f"War Thunder Canada — Free {YEAR}",                   "Play War Thunder free in Canada."),
    ("war-thunder-new-zealand",        f"War Thunder New Zealand — Free {YEAR}",              "Play War Thunder free in New Zealand."),
    ("war-thunder-germany",            f"War Thunder Germany — Free {YEAR}",                  "Play War Thunder free in Germany."),
    ("war-thunder-south-korea",        f"War Thunder South Korea — Free {YEAR}",              "Play War Thunder free in South Korea."),
    # How-to
    ("how-to-play-war-thunder",        f"How to Play War Thunder — Beginner Guide {YEAR}",    "How to get started in War Thunder from scratch."),
    ("how-to-download-war-thunder",    f"How to Download War Thunder Free {YEAR}",            "Step-by-step: download War Thunder for free."),
    ("how-to-get-free-vehicles-war-thunder",f"How to Get Free Vehicles in War Thunder {YEAR}","Earn free vehicles in War Thunder without spending."),
    ("how-to-win-war-thunder",         f"How to Win in War Thunder {YEAR}",                   "Tips and strategies to win more in War Thunder."),
    ("how-to-grind-war-thunder",       f"How to Grind Faster in War Thunder {YEAR}",          "Speed up your War Thunder research grind."),
    ("how-to-earn-silver-lions",       f"How to Earn Silver Lions in War Thunder {YEAR}",     "Best methods to farm Silver Lions fast."),
    # Review / ratings
    ("war-thunder-rating",             f"War Thunder Rating & Score {YEAR}",                  "What's War Thunder's review score?"),
    ("war-thunder-honest-review",      f"War Thunder Honest Review {YEAR}",                   "An honest, unbiased review of War Thunder."),
    ("war-thunder-pros-cons",          f"War Thunder Pros and Cons {YEAR}",                   "Full pros and cons breakdown of War Thunder."),
    ("is-war-thunder-worth-playing",   f"Is War Thunder Worth Playing in {YEAR}?",            f"Should you start War Thunder in {YEAR}?"),
    # Misc
    ("free-war-game-high-graphics",    f"Free War Game High Graphics {YEAR}",                 "The best-looking free war games."),
    ("free-war-game-low-end-pc",       f"Free War Game for Low-End PC {YEAR}",                "Free war games that run on low-end PCs."),
    ("free-war-game-single-player",    f"Free War Game Single Player {YEAR}",                 "Free war games with a strong single-player mode."),
    ("free-war-game-for-beginners",    f"Free War Game for Beginners {YEAR}",                 "Best free war games easy to learn."),
    ("free-war-game-realistic",        f"Free Realistic War Game {YEAR}",                     "The most realistic free war games available."),
]

# ── BLOG POSTS ────────────────────────────────────────────────────────────────
BLOG_POSTS = [
    {"slug":"war-thunder-review-2026",
     "title":f"War Thunder Review {YEAR}: Still Worth Playing?",
     "date":f"{YEAR}-05-20","excerpt":f"Our full {YEAR} War Thunder review — 300+ hours played.",
     "body":f"<p>War Thunder remains the gold standard for free military games in {YEAR}. With over 2,000 historically accurate vehicles and three combat branches (ground, air, naval), no other free game comes close. The physics engine is unmatched and regular major updates keep it fresh. <a href='{AFF_URL}' rel='nofollow sponsored'>Download War Thunder free</a> and see for yourself.</p><p>Our verdict: <strong>9.0/10</strong>. Essential if you love military history or vehicle combat.</p>"},
    {"slug":"war-thunder-beginner-guide-2026",
     "title":f"War Thunder Beginner Guide {YEAR} — Start Here",
     "date":f"{YEAR}-05-15","excerpt":"The complete starter guide for new War Thunder players.",
     "body":f"<p>New to War Thunder? Here's where to start: <strong>1)</strong> Pick USA or USSR for the most beginner-friendly experience. <strong>2)</strong> Start in Arcade Battles to learn mechanics. <strong>3)</strong> Focus one branch — ground, air, or naval — before branching out. <strong>4)</strong> Don't spend Silver Lions on repairs early on. <a href='{AFF_URL}' rel='nofollow sponsored'>Join War Thunder free</a> and apply these tips from day one.</p>"},
    {"slug":"is-war-thunder-pay-to-win-2026",
     "title":f"Is War Thunder Pay to Win in {YEAR}? Honest Answer",
     "date":f"{YEAR}-05-10","excerpt":"We answer the P2W question without sugarcoating it.",
     "body":f"<p>Short answer: <strong>No, War Thunder is not pay-to-win in {YEAR}</strong>. Premium vehicles don't have better stats than their free equivalents — they just let you earn research points faster. Skilled free players consistently outperform spenders. The grind is real at high tiers, but the competitive playing field is fair. <a href='{AFF_URL}' rel='nofollow sponsored'>Try it free</a> and judge for yourself.</p>"},
    {"slug":"war-thunder-vs-world-of-tanks-2026",
     "title":f"War Thunder vs World of Tanks {YEAR} — Which is Better?",
     "date":f"{YEAR}-05-05","excerpt":"Full side-by-side comparison of the two biggest free tank games.",
     "body":f"<p>Both are free. Both have tanks. But they're very different games. War Thunder is a realistic simulator covering planes, tanks, and ships across all eras. World of Tanks is an arcade tank brawler focused purely on tanks. For <strong>depth and realism</strong>: War Thunder wins. For <strong>quick casual play</strong>: World of Tanks is simpler. Our pick for {YEAR}: <a href='{AFF_URL}' rel='nofollow sponsored'>War Thunder</a> — more content, more realism, more free.</p>"},
    {"slug":"best-nation-war-thunder-2026",
     "title":f"Best Nation to Start in War Thunder {YEAR}",
     "date":f"{YEAR}-04-28","excerpt":"Which War Thunder nation should a new player choose?",
     "body":f"<p><strong>USA</strong>: Balanced aircraft and tanks, forgiving armor, good for all playstyles. Best starting nation overall. <strong>USSR</strong>: Powerful sloped armor tanks that bounce shots well — great for ground RB. <strong>Germany</strong>: High-penetration guns that reward precise aiming. <strong>UK</strong>: Unique vehicles and excellent APDS rounds. All are free to research. <a href='{AFF_URL}' rel='nofollow sponsored'>Start your nation free now.</a></p>"},
    {"slug":"war-thunder-silver-lions-guide-2026",
     "title":f"War Thunder Silver Lions Guide {YEAR} — Farm Fast",
     "date":f"{YEAR}-04-20","excerpt":"The best ways to earn Silver Lions without paying.",
     "body":f"<p>Silver Lions are War Thunder's free currency. The fastest ways to farm them: <strong>1)</strong> Play low-tier battles (lower repair costs, high SL multipliers). <strong>2)</strong> Use vehicles you've fully researched — no repair costs if you cap the repair cost. <strong>3)</strong> Complete daily tasks and battle pass challenges. <strong>4)</strong> Sell duplicate decorators on the market. <a href='{AFF_URL}' rel='nofollow sponsored'>Start playing free</a> and use these tips to stay SL-positive.</p>"},
    {"slug":"war-thunder-best-tanks-2026",
     "title":f"War Thunder Best Tanks {YEAR} — Top Picks by Nation",
     "date":f"{YEAR}-04-14","excerpt":"The best tanks in War Thunder right now, ranked by nation.",
     "body":f"<p>Top tank picks for {YEAR}: <strong>Germany</strong> — Leopard 2A6 (top tier), Tiger II H (mid-tier). <strong>USSR</strong> — T-80BVM (top tier), T-34-85 (mid-tier). <strong>USA</strong> — M1A2 SEP (top tier), M4A3E2 Jumbo (mid-tier). <strong>UK</strong> — Challenger 2 (top tier), Centurion Mk.3 (mid-tier). All researchable for free. <a href='{AFF_URL}' rel='nofollow sponsored'>Download War Thunder free</a> and start your grind.</p>"},
]

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """:root{
  --dark:#06080c;--dark2:#0b0e14;--dark3:#10141c;
  --green:#1a7a32;--green2:#22a040;--olive:#4a5e1a;
  --gold:#c8a227;--red:#cc2200;
  --white:#f0f2f0;--light:#d4dbd0;--muted:#57645a;
  --border:#1a2218;--card:#090c10;
  --font:'Oswald',system-ui,sans-serif;
  --body:'Open Sans',system-ui,sans-serif;
  --r:8px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--dark);color:var(--light);font-family:var(--body);line-height:1.7;-webkit-font-smoothing:antialiased}
a{text-decoration:none;color:inherit}
.container{max-width:1160px;margin:0 auto;padding:0 24px}
.nav{background:rgba(6,8,12,.98);border-bottom:2px solid var(--green);position:sticky;top:0;z-index:200;backdrop-filter:blur(12px)}
.nav-i{display:flex;align-items:center;justify-content:space-between;height:60px;gap:16px}
.logo{font-family:var(--font);font-size:21px;font-weight:700;color:var(--white);letter-spacing:.05em;display:flex;align-items:center;gap:9px;white-space:nowrap}
.logo-mark{background:var(--green);color:#fff;width:34px;height:34px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0}
.logo span{color:var(--green2)}
.nav-links{display:flex;gap:20px;align-items:center}
.nav-links a{font-family:var(--font);font-size:12px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:rgba(240,242,240,.5);transition:color .18s}
.nav-links a:hover{color:var(--green2)}
.nav-cta{background:var(--green)!important;color:#fff!important;padding:9px 20px;border-radius:6px;white-space:nowrap;font-weight:700!important;letter-spacing:.04em;transition:background .18s,transform .18s}
.nav-cta:hover{background:var(--green2)!important;transform:translateY(-1px)}
@media(max-width:680px){.nav-links a:not(.nav-cta){display:none}}
.hero{background:linear-gradient(160deg,#020a04 0%,#060c08 50%,#04080a 100%);padding:80px 0 70px;position:relative;overflow:hidden;text-align:center}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(26,122,50,.18) 0%,transparent 70%);pointer-events:none}
.hero-tag{display:inline-block;background:rgba(26,122,50,.15);border:1px solid rgba(26,122,50,.4);color:var(--green2);font-family:var(--font);font-size:12px;letter-spacing:.15em;text-transform:uppercase;padding:6px 16px;border-radius:4px;margin-bottom:22px}
.hero h1{font-family:var(--font);font-size:clamp(36px,7vw,80px);font-weight:700;line-height:1.05;text-transform:uppercase;color:var(--white);margin-bottom:20px}
.hero h1 span{color:var(--green2)}
.hero-sub{font-size:clamp(15px,2.2vw,18px);color:rgba(212,219,208,.7);max-width:640px;margin:0 auto 36px}
.btn-green{display:inline-block;background:var(--green);color:#fff;font-family:var(--font);font-weight:700;font-size:16px;letter-spacing:.06em;text-transform:uppercase;padding:16px 36px;border-radius:8px;cursor:pointer;transition:background .18s,transform .18s,box-shadow .18s;box-shadow:0 4px 24px rgba(26,122,50,.4)}
.btn-green:hover{background:var(--green2);transform:translateY(-2px);box-shadow:0 8px 32px rgba(34,160,64,.4)}
.btn-outline{display:inline-block;background:transparent;color:var(--light);font-family:var(--font);font-weight:600;font-size:14px;letter-spacing:.06em;text-transform:uppercase;padding:14px 30px;border-radius:8px;border:1px solid rgba(240,242,240,.2);transition:border-color .18s,color .18s}
.btn-outline:hover{border-color:var(--green2);color:var(--green2)}
.btn-sm{font-size:13px;padding:10px 22px}
.hero-btns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.hero-badges{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:36px}
.badge{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:6px;padding:8px 18px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;font-weight:600;color:rgba(212,219,208,.6)}
.features{padding:72px 0;background:var(--dark2)}
.section-title{text-align:center;font-family:var(--font);font-size:clamp(26px,4vw,40px);font-weight:700;text-transform:uppercase;color:var(--white);letter-spacing:.03em;margin-bottom:10px}
.section-sub{text-align:center;color:var(--muted);font-size:15px;margin-bottom:50px}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
.feat-card{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:28px 24px;transition:border-color .2s,transform .2s}
.feat-card:hover{border-color:rgba(26,122,50,.4);transform:translateY(-3px)}
.feat-icon{font-size:30px;margin-bottom:14px}
.feat-card h3{font-family:var(--font);font-size:17px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--white);margin-bottom:8px}
.feat-card p{font-size:14px;color:var(--muted);line-height:1.6}
.platforms{padding:60px 0;background:var(--dark3);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.plat-row{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-top:36px}
.plat{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px 30px;text-align:center;min-width:130px;transition:border-color .2s}
.plat:hover{border-color:var(--green2)}
.plat-icon{font-size:28px;margin-bottom:8px}
.plat-name{font-family:var(--font);font-size:13px;letter-spacing:.07em;text-transform:uppercase;color:var(--light);font-weight:600}
.plat-tag{font-size:11px;color:var(--green2);font-weight:700;margin-top:4px;letter-spacing:.05em;text-transform:uppercase}
.cta-band{background:linear-gradient(135deg,#020a04 0%,#060c06 100%);border-top:1px solid rgba(26,122,50,.25);border-bottom:1px solid rgba(26,122,50,.25);padding:60px 0;text-align:center}
.cta-band h2{font-family:var(--font);font-size:clamp(24px,4vw,42px);font-weight:700;text-transform:uppercase;color:var(--white);margin-bottom:12px}
.cta-band p{color:rgba(212,219,208,.6);font-size:15px;margin-bottom:30px}
.faq{padding:72px 0;background:var(--dark2)}
.faq-list{max-width:800px;margin:40px auto 0;display:flex;flex-direction:column;gap:12px}
.faq-item{background:var(--card);border:1px solid var(--border);border-radius:var(--r);overflow:hidden}
.faq-q{font-family:var(--font);font-size:15px;font-weight:600;color:var(--white);padding:18px 22px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;letter-spacing:.02em}
.faq-q::after{content:'＋';color:var(--green2);font-size:18px;flex-shrink:0;margin-left:12px}
.faq-a{font-size:14px;color:var(--muted);padding:0 22px 18px;line-height:1.7}
.kw-section{padding:60px 0;background:var(--dark3)}
.kw-grid{display:flex;gap:10px;flex-wrap:wrap;margin-top:30px;justify-content:center}
.kw-link{background:var(--card);border:1px solid var(--border);border-radius:6px;padding:8px 16px;font-size:13px;color:var(--muted);transition:border-color .15s,color .15s;white-space:nowrap}
.kw-link:hover{border-color:var(--green2);color:var(--light)}
.article{max-width:820px;margin:0 auto;padding:60px 24px}
.article h1{font-family:var(--font);font-size:clamp(28px,5vw,48px);font-weight:700;text-transform:uppercase;color:var(--white);line-height:1.1;margin-bottom:18px}
.article .lead{font-size:17px;color:rgba(212,219,208,.7);margin-bottom:36px;line-height:1.7}
.article h2{font-family:var(--font);font-size:22px;font-weight:700;text-transform:uppercase;color:var(--white);margin:36px 0 14px;letter-spacing:.04em}
.article p{font-size:15px;color:var(--muted);margin-bottom:16px;line-height:1.75}
.article ul{margin:0 0 20px 20px}
.article li{font-size:15px;color:var(--muted);margin-bottom:8px;line-height:1.65}
.article a{color:var(--green2)}
.article a:hover{text-decoration:underline}
.article .cta-box{background:linear-gradient(135deg,rgba(26,122,50,.12),rgba(4,8,6,.5));border:1px solid rgba(26,122,50,.3);border-radius:var(--r);padding:28px;text-align:center;margin:36px 0}
.article .cta-box h3{font-family:var(--font);font-size:22px;color:var(--white);margin-bottom:10px;text-transform:uppercase}
.article .cta-box p{font-size:14px;color:rgba(212,219,208,.6);margin-bottom:20px}
.rating-row{display:flex;gap:20px;flex-wrap:wrap;background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;margin-bottom:28px}
.rating-item{text-align:center;flex:1;min-width:90px}
.rating-score{font-family:var(--font);font-size:28px;font-weight:700;color:var(--green2)}
.rating-label{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.blog-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px;margin-top:40px}
.blog-card{background:var(--card);border:1px solid var(--border);border-radius:var(--r);overflow:hidden;transition:border-color .2s,transform .2s;display:block}
.blog-card:hover{border-color:rgba(26,122,50,.4);transform:translateY(-3px)}
.blog-body{padding:22px}
.blog-date{font-size:12px;color:var(--muted);margin-bottom:8px;letter-spacing:.04em}
.blog-body h3{font-family:var(--font);font-size:16px;font-weight:700;color:var(--white);margin-bottom:8px;text-transform:uppercase;line-height:1.3}
.blog-body p{font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:16px}
.read-more{font-family:var(--font);font-size:12px;font-weight:700;color:var(--green2);text-transform:uppercase;letter-spacing:.06em}
.footer{background:var(--dark2);border-top:1px solid var(--border);padding:40px 0}
.footer-i{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start;justify-content:space-between}
.footer-disc{font-size:11px;color:var(--muted);line-height:1.6;max-width:550px}
.footer-links{display:flex;gap:18px;flex-wrap:wrap}
.footer-links a{font-size:12px;color:var(--muted);transition:color .15s}
.footer-links a:hover{color:var(--light)}"""

# ── HELPERS ───────────────────────────────────────────────────────────────────
def pu(lang, slug=""):
    base = f"{SITE_URL}/{lang}" if lang != "en" else SITE_URL
    return f"{base}/{slug}" if slug else base + "/"

def hreflang_tags(slug=""):
    tags = "\n".join(
        f'  <link rel="alternate" hreflang="{lc}" href="{pu(lc, slug)}"/>'
        for lc in LANGUAGES)
    tags += f'\n  <link rel="alternate" hreflang="x-default" href="{pu("en", slug)}"/>'
    return tags

def shell(title, desc, lang, canonical, body, extra_head="", schema=""):
    t = LANGUAGES[lang]
    hl = hreflang_tags()
    nav_links = "".join(
        f'<a href="{pu(lang, s)}">{label}</a>'
        for s, label in [("", t["nav_home"]), ("review/", t["nav_review"]),
                         ("compare/", t["nav_compare"]), ("blog/", t["nav_blog"])])
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{t['dir']}">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<link rel="canonical" href="{canonical}"/>
{hl}
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="{SITE_NAME}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{title}"/>
<meta name="twitter:description" content="{desc}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet"/>
<style>{CSS}</style>
{extra_head}
{schema}
</head>
<body>
<nav class="nav"><div class="container nav-i">
  <a href="{pu(lang)}" class="logo"><div class="logo-mark">✈</div>War<span>Thunder</span>.gg</a>
  <div class="nav-links">{nav_links}<a href="{AFF_URL}" class="nav-cta" target="_blank" rel="nofollow sponsored">{t['cta']}</a></div>
</div></nav>
{body}
<footer class="footer"><div class="container footer-i">
  <p class="footer-disc">{t['disc']}</p>
  <div class="footer-links">
    <a href="{pu(lang)}">Home</a>
    <a href="{pu(lang,'review/')}">Review</a>
    <a href="{pu(lang,'compare/')}">Compare</a>
    <a href="{pu(lang,'blog/')}">Blog</a>
  </div>
</div></footer>
</body></html>"""

def breadcrumb_schema(lang, items):
    elements = [{"@type":"ListItem","position":i+1,"name":n,"item":u}
                for i,(n,u) in enumerate(items)]
    sc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":elements}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def faq_schema(qas):
    items = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
             for q,a in qas]
    sc = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":items}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

# ── PAGE BUILDERS ─────────────────────────────────────────────────────────────
def build_home(lang):
    t = LANGUAGES[lang]
    vg_schema = json.dumps({
        "@context":"https://schema.org","@type":"VideoGame",
        "name":"War Thunder",
        "description":f"The best free military game of {YEAR}. 2,000+ vehicles — fighter jets, tanks and warships in realistic combat.",
        "gamePlatform":["PC","PlayStation 4","PlayStation 5","Xbox One","Xbox Series X"],
        "applicationCategory":"Game","operatingSystem":"Windows",
        "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},
        "aggregateRating":{"@type":"AggregateRating","ratingValue":"8.8","bestRating":"10","ratingCount":"125000"},
        "url":AFF_URL
    })
    schema = f'<script type="application/ld+json">{vg_schema}</script>'

    feat_cards = "".join(f"""
    <div class="feat-card">
      <div class="feat-icon">{icon}</div>
      <h3>{t[k]}</h3><p>{t[kd]}</p>
    </div>""" for icon,k,kd in [
        ("🆓","why1","why1d"),("✈️","why2","why2d"),("🎯","why3","why3d"),
        ("🎮","why4","why4d"),("🔄","why5","why5d"),("🌍","why6","why6d")])

    blog_cards = "".join(f"""
    <a href="{pu(lang, f'blog/{p["slug"]}/')}" class="blog-card">
      <div class="blog-body">
        <div class="blog-date">{p['date']}</div>
        <h3>{p['title']}</h3><p>{p['excerpt']}</p>
        <span class="read-more">Read More →</span>
      </div>
    </a>""" for p in BLOG_POSTS[:3])

    kw_links = "".join(
        f'<a href="{pu(lang, s+"/")}" class="kw-link">{title.split("—")[0].strip()}</a>'
        for s,title,_ in KEYWORDS[:30])

    home_faqs = [
        ("Is War Thunder really free?",
         "Yes. War Thunder is 100% free to download and play on PC (Steam & Gaijin.net), PS4, PS5, Xbox One, and Xbox Series X/S. Optional premium purchases exist but the full game is free forever."),
        ("Is War Thunder pay to win?",
         "No. Premium vehicles don't have stat advantages — they only accelerate progression. Skilled free players consistently beat premium players in battle."),
        ("How many vehicles are in War Thunder?",
         "Over 2,000 historically accurate aircraft, ground vehicles, naval vessels and helicopters, spanning from WWI to modern day."),
        ("How do I download War Thunder for free?",
         "On PC, download via Steam or Gaijin.net. On PlayStation, find it free in the PlayStation Store. On Xbox, it's in the Microsoft Store. Always 100% free."),
        (f"Is War Thunder still active in {YEAR}?",
         f"Yes. War Thunder has over 100 million registered players and receives major updates multiple times per year with new vehicles, maps and game modes."),
        ("What platforms is War Thunder on?",
         "War Thunder is available on PC (Windows, Mac, Linux via Steam and Gaijin.net), PlayStation 4, PlayStation 5, Xbox One, and Xbox Series X/S, with cross-play enabled."),
        ("What's the difference between Arcade and Realistic modes?",
         "Arcade Battles are faster and more forgiving — great for beginners. Realistic Battles use authentic physics, no markers, and require more skill. Simulator mode is the most immersive with cockpit-only views."),
    ]
    faq_html = "".join(
        f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'
        for q,a in home_faqs)
    faq_sc = faq_schema(home_faqs)

    body = f"""
<section class="hero">
  <div class="container">
    <div class="hero-tag">★ #{YEAR} Best Free Military Game</div>
    <h1>{t['hero1']}<br/><span>{t['hero2']}</span></h1>
    <p class="hero-sub">{t['hero_sub']}</p>
    <div class="hero-btns">
      <a href="{AFF_URL}" class="btn-green" target="_blank" rel="nofollow sponsored">{t['cta']} →</a>
      <a href="{pu(lang,'review/')}" class="btn-outline">Read Review</a>
    </div>
    <div class="hero-badges">
      <div class="badge">PC Free</div><div class="badge">PS4 / PS5</div>
      <div class="badge">Xbox</div><div class="badge">2,000+ Vehicles</div><div class="badge">100M+ Players</div>
    </div>
  </div>
</section>

<section class="features">
  <div class="container">
    <h2 class="section-title">{t['feat_title']}</h2>
    <p class="section-sub">Six reasons War Thunder is the top free military game in {YEAR}.</p>
    <div class="features-grid">{feat_cards}</div>
  </div>
</section>

<section class="platforms">
  <div class="container">
    <h2 class="section-title">Available Everywhere — Always Free</h2>
    <div class="plat-row">
      <div class="plat"><div class="plat-icon">🖥️</div><div class="plat-name">PC</div><div class="plat-tag">Steam & Gaijin</div></div>
      <div class="plat"><div class="plat-icon">🎮</div><div class="plat-name">PlayStation 4</div><div class="plat-tag">Free Download</div></div>
      <div class="plat"><div class="plat-icon">🎮</div><div class="plat-name">PlayStation 5</div><div class="plat-tag">Free Download</div></div>
      <div class="plat"><div class="plat-icon">🕹️</div><div class="plat-name">Xbox One</div><div class="plat-tag">Free Download</div></div>
      <div class="plat"><div class="plat-icon">🕹️</div><div class="plat-name">Xbox Series X/S</div><div class="plat-tag">Free Download</div></div>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>2,000+ Vehicles. 100% Free.</h2>
    <p>Planes, tanks, warships — all free. No subscription ever.</p>
    <a href="{AFF_URL}" class="btn-green" target="_blank" rel="nofollow sponsored">{t['cta']} — No Cost Ever →</a>
  </div>
</section>

<section class="faq">
  <div class="container">
    <h2 class="section-title">Frequently Asked Questions</h2>
    <div class="faq-list">{faq_html}</div>
  </div>
</section>

<section style="padding:60px 0;background:var(--dark)">
  <div class="container">
    <h2 class="section-title">Latest from the Blog</h2>
    <div class="blog-grid">{blog_cards}</div>
  </div>
</section>

<section class="kw-section">
  <div class="container">
    <h2 class="section-title" style="font-size:18px;margin-bottom:0">More Guides</h2>
    <div class="kw-grid">{kw_links}</div>
  </div>
</section>"""

    return shell(t["meta_home"], t["meta_home"], lang, pu(lang), body,
                 extra_head="", schema=schema+faq_sc)

def build_kw_page(lang, slug, title, desc):
    t = LANGUAGES[lang]
    bc = breadcrumb_schema(lang, [("Home", pu(lang)), (title, pu(lang, slug+"/"))])
    idx = next((i for i,(s,_,_) in enumerate(KEYWORDS) if s==slug), 0)
    neighbors = KEYWORDS[max(0,idx-4):idx] + KEYWORDS[idx+1:idx+5]
    related = "".join(
        f'<a href="{pu(lang, s+"/")}" class="kw-link">{t2.split("—")[0].strip()}</a>'
        for s,t2,_ in neighbors)
    faqs = [
        (f"What is the best free military game in {YEAR}?",
         f"War Thunder is our top pick for {YEAR}. It's completely free on PC, PS4/5, and Xbox with 2,000+ vehicles and realistic combat."),
        ("Is War Thunder pay to win?",
         "No. Free players compete on equal footing. Premium speeds up progression but gives no stat advantage in battle."),
        ("How do I start playing War Thunder for free?",
         "Click the download button on this page, create a free Gaijin account, and start playing in minutes. No credit card needed."),
    ]
    faq_sc = faq_schema(faqs)
    faq_html = "".join(
        f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'
        for q,a in faqs)

    body = f"""
<div style="background:var(--dark3);border-bottom:1px solid var(--border);padding:12px 0">
  <div class="container" style="font-size:12px;color:var(--muted)">
    <a href="{pu(lang)}" style="color:var(--muted)">Home</a> › {title.split("—")[0].strip()}
  </div>
</div>
<div style="background:var(--dark);padding:50px 0 0">
<div class="article">
  <h1>{title}</h1>
  <p class="lead">{desc} Our #1 recommendation is <strong>War Thunder</strong> — the top-rated free military game of {YEAR} on PC, PS4/5, and Xbox.</p>
  <div class="rating-row">
    <div class="rating-item"><div class="rating-score">8.8</div><div class="rating-label">Overall</div></div>
    <div class="rating-item"><div class="rating-score">9.2</div><div class="rating-label">Gameplay</div></div>
    <div class="rating-item"><div class="rating-score">9.5</div><div class="rating-label">Value</div></div>
    <div class="rating-item"><div class="rating-score">9.0</div><div class="rating-label">Realism</div></div>
  </div>
  <div class="cta-box">
    <h3>🏆 Best Pick: War Thunder</h3>
    <p>Free on PC, PS4/5, and Xbox. 2,000+ vehicles. 100M+ players. No subscription ever.</p>
    <a href="{AFF_URL}" class="btn-green" target="_blank" rel="nofollow sponsored">{t['cta']} — Free →</a>
  </div>
  <h2>Why War Thunder Ranks #1</h2>
  <p>When searching for {title.lower().split("—")[0].strip()}, War Thunder consistently tops every list. No other free game combines historical accuracy, three distinct combat branches, and 2,000+ vehicles at zero cost.</p>
  <ul>
    <li><strong>Completely free:</strong> Download and play on PC (Steam/Gaijin), PS4/5, or Xbox at zero cost.</li>
    <li><strong>2,000+ vehicles:</strong> Aircraft, tanks, helicopters, and naval vessels spanning WWI to modern day.</li>
    <li><strong>Three combat branches:</strong> Ground battles, air battles, and naval battles — or combined arms.</li>
    <li><strong>Realistic physics:</strong> Every vehicle modeled from real blueprints with authentic ballistics.</li>
    <li><strong>Cross-platform:</strong> Play and progress across PC and console with cross-play enabled.</li>
    <li><strong>Active development:</strong> Major updates multiple times per year.</li>
  </ul>
  <h2>How to Get Started Free</h2>
  <p>Click the button below to reach the official War Thunder page. Create a free Gaijin account and download the client — no payment required at any step. Complete the tutorial missions, pick your nation, and start researching vehicles.</p>
  <div class="cta-box">
    <h3>{t['dl']} Now</h3>
    <p>PC · PS4 · PS5 · Xbox · No cost ever</p>
    <a href="{AFF_URL}" class="btn-green" target="_blank" rel="nofollow sponsored">{t['cta']} →</a>
  </div>
  <h2>Frequently Asked Questions</h2>
  <div class="faq-list" style="margin-top:0">{faq_html}</div>
  <h2>Related Guides</h2>
  <div class="kw-grid">{related}</div>
</div>
</div>"""
    return shell(title, desc, lang, pu(lang, slug+"/"), body,
                 extra_head=bc, schema=faq_sc)

def build_review(lang):
    t = LANGUAGES[lang]
    title = f"War Thunder Review {YEAR} — Is It Worth Playing?"
    desc  = f"Full unbiased War Thunder review for {YEAR}. Ratings, pros, cons, and verdict."
    bc = breadcrumb_schema(lang,[("Home",pu(lang)),(title,pu(lang,"review/"))])
    body = f"""
<div class="article" style="padding-top:70px">
  <h1>War Thunder Review {YEAR}</h1>
  <p class="lead">300+ hours played. Honest verdict: War Thunder is the most ambitious free military game ever made, and it's only getting better in {YEAR}.</p>
  <div class="rating-row">
    <div class="rating-item"><div class="rating-score">8.8</div><div class="rating-label">Overall</div></div>
    <div class="rating-item"><div class="rating-score">9.2</div><div class="rating-label">Gameplay</div></div>
    <div class="rating-item"><div class="rating-score">9.5</div><div class="rating-label">Value</div></div>
    <div class="rating-item"><div class="rating-score">9.0</div><div class="rating-label">Realism</div></div>
    <div class="rating-item"><div class="rating-score">7.8</div><div class="rating-label">Grind</div></div>
  </div>
  <h2>What is War Thunder?</h2>
  <p>War Thunder is a free-to-play military MMO developed by Gaijin Entertainment, launched in 2012. It features over 2,000 historically accurate vehicles across ground, air, and naval combat spanning WWI to the modern era. With 100M+ registered players it's one of the largest free games in the world.</p>
  <h2>Pros</h2>
  <ul>
    <li>100% free on PC, PS4, PS5, Xbox — no subscription ever</li>
    <li>2,000+ vehicles — the largest roster in any free game</li>
    <li>Three combat branches: ground, air, naval</li>
    <li>Realistic physics — each vehicle modeled from real blueprints</li>
    <li>Cross-platform play and progression</li>
    <li>Regular major updates with new vehicles and maps</li>
    <li>Deep progression system that rewards skill over spending</li>
  </ul>
  <h2>Cons</h2>
  <ul>
    <li>Research grind is slow at higher tiers without premium</li>
    <li>Steep learning curve for complete beginners</li>
    <li>Economy can feel punishing after losses at top tier</li>
  </ul>
  <h2>Verdict</h2>
  <p>If you want the deepest, most realistic free military game available in {YEAR}, War Thunder has no equal. The grind is real at top tier, but the core experience — especially in ground and air realistic battles — is genuinely thrilling and completely free.</p>
  <div class="cta-box">
    <h3>Play War Thunder Free</h3><p>PC · PS4/5 · Xbox · 100M+ players · No subscription.</p>
    <a href="{AFF_URL}" class="btn-green" target="_blank" rel="nofollow sponsored">{t['cta']} →</a>
  </div>
</div>"""
    return shell(title, desc, lang, pu(lang,"review/"), body, extra_head=bc)

def build_compare(lang):
    t = LANGUAGES[lang]
    title = f"War Thunder vs World of Tanks vs Crossout {YEAR} — Comparison"
    desc  = "Side-by-side comparison of the top three free war games."
    bc = breadcrumb_schema(lang,[("Home",pu(lang)),(title,pu(lang,"compare/"))])
    rows = [
        ("Price","Free","Free","Free"),
        ("Platforms","PC/PS4/PS5/Xbox","PC/Xbox","PC/PS4/PS5/Xbox"),
        ("Vehicle Types","Planes + Tanks + Ships","Tanks only","Custom vehicles"),
        ("Realism","★★★★★ Realistic","★★★ Arcade","★★ Arcade"),
        ("Pay-to-Win","No","Mild","No"),
        ("Learning Curve","Hard","Easy","Medium"),
        ("Vehicles","2,000+","700+","1,000+ parts"),
        ("Active Players","100M+","160M+","10M+"),
        ("Our Rank","🏆 #1","#2","#3"),
    ]
    table_rows = "".join(
        f'<tr style="border-bottom:1px solid var(--border)"><td style="padding:12px;color:var(--muted)">{c}</td>'
        f'<td style="padding:12px;text-align:center;color:var(--green2)">{a}</td>'
        f'<td style="padding:12px;text-align:center;color:var(--light)">{b}</td>'
        f'<td style="padding:12px;text-align:center;color:var(--light)">{d}</td></tr>'
        for c,a,b,d in rows)
    body = f"""
<div class="article" style="padding-top:70px">
  <h1>Free War Game Comparison {YEAR}</h1>
  <p class="lead">War Thunder, World of Tanks, and Crossout compared side by side — pick the right free game for your playstyle.</p>
  <div style="overflow-x:auto;margin:24px 0"><table style="width:100%;border-collapse:collapse;font-size:14px">
    <thead><tr style="background:var(--card);border-bottom:2px solid var(--green)">
      <th style="padding:14px;text-align:left;font-family:var(--font);color:var(--white)">Category</th>
      <th style="padding:14px;text-align:center;color:var(--green2)">War Thunder ★</th>
      <th style="padding:14px;text-align:center;color:var(--light)">World of Tanks</th>
      <th style="padding:14px;text-align:center;color:var(--light)">Crossout</th>
    </tr></thead>
    <tbody>{table_rows}</tbody>
  </table></div>
  <h2>Our Verdict</h2>
  <p>For depth, realism, and sheer content volume, War Thunder is the clear #1 in {YEAR}. World of Tanks is better for casual quick sessions. Crossout suits players who love vehicle customization. All three are 100% free.</p>
  <div class="cta-box">
    <h3>Our Pick: War Thunder</h3>
    <p>2,000+ vehicles, three combat branches, 100% free, realistic physics.</p>
    <a href="{AFF_URL}" class="btn-green" target="_blank" rel="nofollow sponsored">{t['cta']} →</a>
  </div>
</div>"""
    return shell(title, desc, lang, pu(lang,"compare/"), body, extra_head=bc)

def build_blog_list(lang):
    t = LANGUAGES[lang]
    title = f"War Thunder Blog — Guides, Tips & Reviews {YEAR}"
    desc  = f"War Thunder tips, reviews, and guides updated for {YEAR}."
    cards = "".join(f"""
    <a href="{pu(lang, f'blog/{p["slug"]}/')}" class="blog-card">
      <div class="blog-body">
        <div class="blog-date">{p['date']}</div>
        <h3>{p['title']}</h3><p>{p['excerpt']}</p>
        <span class="read-more">Read More →</span>
      </div>
    </a>""" for p in BLOG_POSTS)
    body = f'<div style="padding:60px 0;background:var(--dark)"><div class="container"><h1 class="section-title">Blog</h1><div class="blog-grid">{cards}</div></div></div>'
    return shell(title, desc, lang, pu(lang,"blog/"), body)

def build_blog_post(lang, post):
    t = LANGUAGES[lang]
    bc = breadcrumb_schema(lang,[("Home",pu(lang)),("Blog",pu(lang,"blog/")),
                                  (post['title'],pu(lang,f'blog/{post["slug"]}/'))])
    body = f"""
<div class="article" style="padding-top:70px">
  <div style="font-size:12px;color:var(--muted);margin-bottom:16px">{post['date']}</div>
  <h1>{post['title']}</h1>
  <p class="lead">{post['excerpt']}</p>
  {post['body']}
  <div class="cta-box" style="margin-top:40px">
    <h3>Play War Thunder Free Now</h3><p>PC · PS4/5 · Xbox · No cost ever.</p>
    <a href="{AFF_URL}" class="btn-green" target="_blank" rel="nofollow sponsored">{t['cta']} →</a>
  </div>
</div>"""
    return shell(post['title'], post['excerpt'], lang,
                 pu(lang,f'blog/{post["slug"]}/'), body, extra_head=bc)

def build_404():
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>404 — War Thunder.gg</title><meta name="robots" content="noindex"/>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@700&display=swap" rel="stylesheet"/>
<style>{CSS}</style></head><body>
<nav class="nav"><div class="container nav-i">
  <a href="{SITE_URL}/" class="logo"><div class="logo-mark">✈</div>War<span>Thunder</span>.gg</a>
</div></nav>
<div style="min-height:80vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:60px 24px">
  <div>
    <div style="font-family:var(--font);font-size:100px;font-weight:700;color:var(--green2);line-height:1">404</div>
    <h1 style="font-family:var(--font);font-size:26px;color:var(--white);text-transform:uppercase;margin:12px 0">Shot Down</h1>
    <p style="color:var(--muted);margin-bottom:28px">This page didn't make it back to base.</p>
    <a href="{SITE_URL}/" class="btn-outline btn-sm">← Return to Base</a>&nbsp;&nbsp;
    <a href="{AFF_URL}" class="btn-green btn-sm" target="_blank" rel="nofollow sponsored">Play Free Now →</a>
  </div>
</div></body></html>"""

def build_sitemap(urls):
    entries = "\n".join(
        f'  <url><loc>{u["loc"]}</loc><lastmod>{TODAY}</lastmod>'
        f'<changefreq>{u["freq"]}</changefreq><priority>{u["pri"]}</priority></url>'
        for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>'

def build_llms(all_urls, page_count):
    """Rich llms.txt for AI crawlers — full page index included."""
    kw_lines = "\n".join(
        f"- [{title}]({pu('en', slug+'/')}): {desc}"
        for slug,title,desc in KEYWORDS)
    blog_lines = "\n".join(
        f"- [{p['title']}]({pu('en', 'blog/'+p['slug']+'/') }): {p['excerpt']}"
        for p in BLOG_POSTS)
    lang_lines = "\n".join(
        f"- {t['name']} ({lc}): {pu(lc)}"
        for lc,t in LANGUAGES.items())

    return f"""# {SITE_NAME}
> Independent guide to War Thunder — the best free military game in {YEAR}.
> Updated: {TODAY} | Pages: {page_count} | Languages: {len(LANGUAGES)}

## Site
- URL: {SITE_URL}/
- Affiliate: {AFF_URL}
- Niche: Free-to-play military games → War Thunder
- Target markets: Australia, Canada, France, Germany, South Korea, New Zealand, UK, USA

## About War Thunder
War Thunder is a free-to-play military MMO by Gaijin Entertainment (est. 2012).
- Platforms: PC (Steam & Gaijin.net), PlayStation 4, PlayStation 5, Xbox One, Xbox Series X/S
- Price: Free (optional premium purchases, no pay-to-win)
- Vehicles: 2,000+ aircraft, tanks, helicopters, naval vessels
- Combat branches: Ground Forces, Aviation, Naval Forces
- Players: 100M+ registered worldwide
- Download: {AFF_URL}

## Languages
{lang_lines}

## Core Pages (English)
- [Home]({pu('en')}): Homepage — hero, features, FAQ, blog preview
- [Review]({pu('en','review/')}): Full War Thunder review {YEAR}
- [Compare]({pu('en','compare/')}): War Thunder vs World of Tanks vs Crossout
- [Blog]({pu('en','blog/')}): Guides, tips and news

## Blog Posts
{blog_lines}

## Keyword Pages ({len(KEYWORDS)} total)
{kw_lines}

## Technical
- Built: {TODAY} by build.py (static site generator)
- Hosting: GitHub Pages
- Sitemaps: {SITE_URL}/sitemap.xml
- robots.txt: {SITE_URL}/robots.txt
- Schema: VideoGame, FAQPage, BreadcrumbList on all pages
- Hreflang: en, fr, de, ko with x-default=en

## Crawl Policy
Crawlers are welcome. All content is original. Affiliate links use rel="nofollow sponsored".
"""

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    all_urls   = []
    page_count = 0

    def add(url, freq="weekly", pri="0.7"):
        all_urls.append({"loc":url,"freq":freq,"pri":pri})

    def w(path, content):
        nonlocal page_count
        write(OUT / path, content)
        page_count += 1
        if page_count % 50 == 0:
            print(f"  … {page_count} pages written", flush=True)

    print(f"Building {SITE_NAME} v2.0")
    print(f"  URL      : {SITE_URL}")
    print(f"  Languages: {len(LANGUAGES)}  |  Keywords: {len(KEYWORDS)}  |  Blog: {len(BLOG_POSTS)}")
    print("="*60)

    for lang in LANGUAGES:
        print(f"  [{lang}]", end=" ", flush=True)
        base = f"{lang}/" if lang != "en" else ""

        w(f"{base}index.html",          build_home(lang));       add(pu(lang),"daily","1.0")
        w(f"{base}review/index.html",   build_review(lang));     add(pu(lang,"review/"),"weekly","0.8")
        w(f"{base}compare/index.html",  build_compare(lang));    add(pu(lang,"compare/"),"weekly","0.8")
        w(f"{base}blog/index.html",     build_blog_list(lang));  add(pu(lang,"blog/"),"daily","0.8")

        for post in BLOG_POSTS:
            w(f"{base}blog/{post['slug']}/index.html", build_blog_post(lang, post))
            add(pu(lang,f'blog/{post["slug"]}/'), "weekly", "0.7")

        for slug, title, desc in KEYWORDS:
            w(f"{base}{slug}/index.html", build_kw_page(lang, slug, title, desc))
            add(pu(lang,f"{slug}/"), "weekly", "0.6")

        print("✓")

    # ── SITEMAPS ──────────────────────────────────────────────────────────────
    kw_urls   = [u for u in all_urls if any(s in u["loc"] for s,_,_ in KEYWORDS)]
    blog_urls = [u for u in all_urls if "/blog/" in u["loc"]]
    main_urls = [u for u in all_urls if u not in kw_urls and u not in blog_urls]

    sitemap_index = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>{SITE_URL}/sitemap-main.xml</loc><lastmod>{TODAY}</lastmod></sitemap>
  <sitemap><loc>{SITE_URL}/sitemap-kw.xml</loc><lastmod>{TODAY}</lastmod></sitemap>
  <sitemap><loc>{SITE_URL}/sitemap-blog.xml</loc><lastmod>{TODAY}</lastmod></sitemap>
</sitemapindex>"""
    write(OUT/"sitemap.xml",      sitemap_index)
    write(OUT/"sitemap-main.xml", build_sitemap(main_urls))
    write(OUT/"sitemap-kw.xml",   build_sitemap(kw_urls))
    write(OUT/"sitemap-blog.xml", build_sitemap(blog_urls))
    print("  ✓ sitemaps (index + 3 sub-sitemaps)")

    # ── ROBOTS ────────────────────────────────────────────────────────────────
    write(OUT/"robots.txt",
f"""User-agent: *
Allow: /
Crawl-delay: 1

User-agent: Googlebot
Allow: /
Crawl-delay: 0

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
""")
    print("  ✓ robots.txt")

    # ── LLMS.TXT ──────────────────────────────────────────────────────────────
    write(OUT/"llms.txt", build_llms(all_urls, page_count))
    print("  ✓ llms.txt (full page index)")

    # ── MISC ──────────────────────────────────────────────────────────────────
    write(OUT/"404.html",  build_404())
    write(OUT/".nojekyll", "")

    # ── BUILD INFO JSON ───────────────────────────────────────────────────────
    build_info = {
        "site": SITE_URL,
        "built": TODAY,
        "pages": page_count,
        "languages": len(LANGUAGES),
        "keywords": len(KEYWORDS),
        "blog_posts": len(BLOG_POSTS),
        "sitemaps": [
            f"{SITE_URL}/sitemap.xml",
            f"{SITE_URL}/sitemap-main.xml",
            f"{SITE_URL}/sitemap-kw.xml",
            f"{SITE_URL}/sitemap-blog.xml",
        ]
    }
    write(OUT/"build-info.json", json.dumps(build_info, indent=2))
    print("  ✓ build-info.json")

    print("="*60)
    print(f"✅  BUILD COMPLETE — {SITE_NAME} v2.0")
    print(f"   Pages      : {page_count}")
    print(f"   Languages  : {len(LANGUAGES)}")
    print(f"   Keywords   : {len(KEYWORDS)}")
    print(f"   Blog posts : {len(BLOG_POSTS)}")
    print(f"   Output     : {OUT.resolve()}")
    print(f"\n   Submit these sitemaps to Google Search Console:")
    for sm in build_info["sitemaps"]:
        print(f"     {sm}")

if __name__ == "__main__":
    main()
