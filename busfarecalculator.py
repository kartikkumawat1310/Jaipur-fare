#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║         JaipurFare — Bus & Auto Calculator           ║
║         By: Kartik Kumawat | Jaipur, RJ              ║
╚══════════════════════════════════════════════════════╝
"""

import os
import json
import datetime

# ─────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────
HISTORY_FILE = "fare_history.json"

ORANGE = "\033[38;5;208m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# ─────────────────────────────────────────
#  JAIPUR AREAS / STOPS
# ─────────────────────────────────────────
AREAS = [
    "Sindhi Camp",       "Ajmeri Gate",       "Badi Chaupar",
    "Choti Chaupar",     "MI Road",            "Sanganeri Gate",
    "New Gate",          "Amber Fort",         "Jal Mahal",
    "Govind Dev Ji",     "Albert Hall",        "Jantar Mantar",
    "Hawa Mahal",        "City Palace",        "Nahargarh Fort",
    "Birla Mandir",      "Jaipur Railway Stn", "Jaipur Airport",
    "Mansarovar",        "Vaishali Nagar",     "Malviya Nagar",
    "Jagatpura",         "Sanganer",           "Chitrakoot",
    "Tonk Road",         "Ajmer Road",         "Delhi Road",
    "Sikar Road",        "Agra Road",          "C-Scheme",
    "Bani Park",         "Raja Park",          "Adarsh Nagar",
    "Shyam Nagar",       "Pratap Nagar",
]

# ─────────────────────────────────────────
#  FARE LOGIC
# ─────────────────────────────────────────
def bus_fare(km: float) -> int:
    """JCTSL slab-based fare."""
    slabs = [(2, 10), (5, 15), (10, 20), (15, 25), (20, 30)]
    for limit, fare in slabs:
        if km <= limit:
            return fare
    extra_slabs = int((km - 20) // 5) + 1
    return 30 + extra_slabs * 5

def auto_fare(km: float) -> int:
    """Auto rickshaw negotiated fare (standard Jaipur rates)."""
    if km <= 2:
        return 30
    elif km <= 5:
        return round(30 + (km - 2) * 12)
    elif km <= 10:
        return round(30 + 3 * 12 + (km - 5) * 11)
    else:
        return round(30 + 3 * 12 + 5 * 11 + (km - 10) * 10)

def ola_fare(km: float) -> int:
    return round(50 + km * 9)

def rapido_fare(km: float) -> int:
    return round(25 + km * 7)

def night_fare(fare: int) -> int:
    """1.5x after 10 PM for auto."""
    return round(fare * 1.5)

def travel_time(km: float, mode: str) -> int:
    """Estimated travel time in minutes."""
    speed = 15 if mode == "bus" else 20
    return round((km / speed) * 60)

# ─────────────────────────────────────────
#  HISTORY
# ─────────────────────────────────────────
def load_history() -> list:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(record: dict):
    history = load_history()
    history.insert(0, record)
    history = history[:10]  # keep last 10
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# ─────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header():
    print(f"""
{ORANGE}{BOLD}╔══════════════════════════════════════════════════════╗
║         JaipurFare — Bus & Auto Calculator           ║
║         Jaipur, Rajasthan  |  Python CLI             ║
╚══════════════════════════════════════════════════════╝{RESET}
""")

def divider(char="─", width=54):
    print(f"{GRAY}{char * width}{RESET}")

def print_areas():
    print(f"\n{WHITE}{BOLD}Available Areas / Stops:{RESET}")
    divider()
    for i, area in enumerate(AREAS, 1):
        num  = f"{ORANGE}{i:>2}.{RESET}"
        name = f"{WHITE}{area:<22}{RESET}"
        print(f"  {num} {name}", end="\n" if i % 2 == 0 else "   ")
    if len(AREAS) % 2 != 0:
        print()
    divider()

def pick_area(prompt: str) -> str:
    print_areas()
    while True:
        try:
            raw = input(f"\n{ORANGE}  {prompt} (1-{len(AREAS)} or type name): {RESET}").strip()
            if raw.isdigit():
                idx = int(raw)
                if 1 <= idx <= len(AREAS):
                    return AREAS[idx - 1]
                print(f"{RED}  Invalid number. Try again.{RESET}")
            else:
                matches = [a for a in AREAS if raw.lower() in a.lower()]
                if len(matches) == 1:
                    return matches[0]
                elif len(matches) > 1:
                    print(f"{YELLOW}  Multiple matches:{RESET}")
                    for i, m in enumerate(matches, 1):
                        print(f"    {i}. {m}")
                    sub = input(f"{ORANGE}  Pick number: {RESET}").strip()
                    if sub.isdigit() and 1 <= int(sub) <= len(matches):
                        return matches[int(sub) - 1]
                else:
                    print(f"{RED}  No match found. Try again.{RESET}")
        except (ValueError, KeyboardInterrupt):
            print(f"{RED}  Invalid input.{RESET}")

def pick_distance() -> float:
    while True:
        try:
            km = float(input(f"\n{ORANGE}  Enter distance in km (1–40): {RESET}").strip())
            if 1 <= km <= 40:
                return round(km, 1)
            print(f"{RED}  Please enter a value between 1 and 40.{RESET}")
        except ValueError:
            print(f"{RED}  Enter a valid number.{RESET}")

def pick_mode() -> str:
    print(f"\n{WHITE}{BOLD}  Select Vehicle:{RESET}")
    print(f"  {ORANGE}1.{RESET} {WHITE}City Bus  {GRAY}(JCTSL){RESET}")
    print(f"  {ORANGE}2.{RESET} {WHITE}Auto Rickshaw{RESET}")
    while True:
        choice = input(f"\n{ORANGE}  Enter 1 or 2: {RESET}").strip()
        if choice == "1":
            return "bus"
        elif choice == "2":
            return "auto"
        print(f"{RED}  Invalid choice. Enter 1 or 2.{RESET}")

def is_night() -> bool:
    hour = datetime.datetime.now().hour
    return hour >= 22 or hour < 6

def show_result(from_area, to_area, km, mode):
    clear()
    header()

    fare     = bus_fare(km) if mode == "bus" else auto_fare(km)
    time_min = travel_time(km, mode)
    rate     = round(fare / km, 1)
    night    = is_night() and mode == "auto"
    night_f  = night_fare(fare) if night else None
    mode_lbl = "City Bus (JCTSL)" if mode == "bus" else "Auto Rickshaw"

    print(f"\n{WHITE}{BOLD}  FARE RESULT{RESET}")
    divider("═")
    print(f"\n  {GRAY}Route  :{RESET}  {WHITE}{from_area}{RESET}  {ORANGE}→{RESET}  {WHITE}{to_area}{RESET}")
    print(f"  {GRAY}Mode   :{RESET}  {WHITE}{mode_lbl}{RESET}")
    print(f"  {GRAY}Distance:{RESET} {WHITE}{km} km{RESET}")
    divider()

    print(f"\n  {ORANGE}{BOLD}  ₹ {fare}{RESET}   {GRAY}estimated fare{RESET}")

    if night:
        print(f"\n  {YELLOW}⚠  Night fare (after 10 PM): ₹{night_f}{RESET}  {GRAY}(1.5x applied){RESET}")

    print(f"\n  {GRAY}Travel time :{RESET}  {WHITE}~{time_min} min{RESET}")
    print(f"  {GRAY}Rate per km :{RESET}  {WHITE}₹{rate}/km{RESET}")

    # ── Alternatives ──
    divider()
    print(f"\n  {WHITE}{BOLD}Compare Alternatives:{RESET}\n")
    if mode == "bus":
        print(f"  {ORANGE}Auto Rickshaw  :{RESET}  ₹{auto_fare(km)}")
        print(f"  {ORANGE}Rapido Bike    :{RESET}  ₹{rapido_fare(km)}")
        print(f"  {ORANGE}Ola/Uber Auto  :{RESET}  ₹{ola_fare(km)}")
    else:
        print(f"  {ORANGE}City Bus       :{RESET}  ₹{bus_fare(km)}  {GRAY}(cheapest){RESET}")
        print(f"  {ORANGE}Rapido Bike    :{RESET}  ₹{rapido_fare(km)}")
        print(f"  {ORANGE}Ola/Uber Auto  :{RESET}  ₹{ola_fare(km)}")

    # ── Tips ──
    divider()
    print(f"\n  {WHITE}{BOLD}Local Tips:{RESET}\n")
    tips = get_tips(mode, km, night)
    for tip in tips:
        print(f"  {ORANGE}✦{RESET} {GRAY}{tip}{RESET}")

    # ── Save history ──
    record = {
        "from": from_area, "to": to_area,
        "km": km, "mode": mode,
        "fare": fare,
        "time": str(datetime.datetime.now().strftime("%d %b %Y, %H:%M"))
    }
    save_history(record)

    print()
    divider()
    input(f"\n  {GRAY}Press Enter to go back to menu...{RESET}")

def get_tips(mode, km, night):
    bus_tips = [
        "JCTSL buses run 6 AM – 10 PM. Last bus from Sindhi Camp at 9:45 PM.",
        "Keep exact change — drivers rarely have change for ₹100+ notes.",
        "Route 2 & 5 cover most tourist spots. Ask conductor for stop names.",
        "Avoid peak hours 8–10 AM and 5–7 PM — buses get very crowded.",
    ]
    auto_tips = [
        "Always agree on fare BEFORE boarding. Meters are rarely used in Jaipur.",
        "Shared autos on fixed routes cost ₹10–15 per person — very cheap.",
        "Rapido & Ola Auto apps often give cheaper rates than street autos.",
        "For airport trips, negotiate fixed fare — ₹200–350 from city center.",
    ]
    tips = bus_tips if mode == "bus" else auto_tips
    if night and mode == "auto":
        tips = ["Night fare is 1.5x standard. Confirm with driver before boarding."] + tips[:2]
    if km > 15:
        tips = tips[:2] + ["For long routes, cab apps (Ola/Uber) may be more comfortable."]
    return tips[:3]

def show_history():
    clear()
    header()
    history = load_history()
    print(f"\n{WHITE}{BOLD}  Recent Searches (Last 10):{RESET}")
    divider("═")

    if not history:
        print(f"\n  {GRAY}No history yet. Make your first search!{RESET}\n")
    else:
        for i, h in enumerate(history, 1):
            mode_icon = "🚌" if h["mode"] == "bus" else "🛺"
            print(f"\n  {ORANGE}{i:>2}.{RESET} {mode_icon}  {WHITE}{h['from']}{RESET} → {WHITE}{h['to']}{RESET}")
            print(f"      {GRAY}{h['km']} km  |  ₹{h['fare']}  |  {h.get('time','')}{RESET}")

    print()
    divider()
    input(f"\n  {GRAY}Press Enter to go back...{RESET}")

def show_fare_chart():
    clear()
    header()
    print(f"\n{WHITE}{BOLD}  Jaipur Fare Chart{RESET}")
    divider("═")
    print(f"\n  {GRAY}{'Distance':<12} {'Bus Fare':>10} {'Auto Fare':>12} {'Rapido':>10}{RESET}")
    divider()
    distances = [1, 2, 3, 5, 8, 10, 12, 15, 20, 25, 30, 40]
    for km in distances:
        b = bus_fare(km)
        a = auto_fare(km)
        r = rapido_fare(km)
        print(f"  {WHITE}{km:>4} km{RESET}       {ORANGE}₹{b:>5}{RESET}      {WHITE}₹{a:>5}{RESET}    {GRAY}₹{r:>5}{RESET}")
    print()
    divider()
    input(f"\n  {GRAY}Press Enter to go back...{RESET}")

# ─────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────
def main_menu():
    while True:
        clear()
        header()
        print(f"  {WHITE}{BOLD}Main Menu{RESET}\n")
        print(f"  {ORANGE}1.{RESET}  {WHITE}Calculate Fare{RESET}")
        print(f"  {ORANGE}2.{RESET}  {WHITE}View Fare Chart{RESET}")
        print(f"  {ORANGE}3.{RESET}  {WHITE}Search History{RESET}")
        print(f"  {ORANGE}4.{RESET}  {WHITE}About{RESET}")
        print(f"  {ORANGE}5.{RESET}  {RED}Exit{RESET}")
        divider()

        choice = input(f"\n{ORANGE}  Enter choice (1-5): {RESET}").strip()

        if choice == "1":
            clear()
            header()
            from_area = pick_area("From (area/stop)")
            clear()
            header()
            to_area = pick_area("To (area/stop)")
            if from_area == to_area:
                print(f"{RED}  From and To cannot be the same!{RESET}")
                input(f"  {GRAY}Press Enter...{RESET}")
                continue
            clear()
            header()
            km   = pick_distance()
            mode = pick_mode()
            show_result(from_area, to_area, km, mode)

        elif choice == "2":
            show_fare_chart()

        elif choice == "3":
            show_history()

        elif choice == "4":
            clear()
            header()
            print(f"""
  {WHITE}{BOLD}About JaipurFare{RESET}

  {GRAY}A command-line fare calculator for Jaipur's public
  transport — buses and auto rickshaws.

  Fare data based on JCTSL (Jaipur City Transport
  Services Limited) slab rates and standard auto
  negotiation rates as of 2024.

  {ORANGE}Features:{RESET}
  {GRAY}✦  Bus & Auto fare with real slab logic
  ✦  Night fare detection (auto 1.5x after 10 PM)
  ✦  Alternative transport comparison
  ✦  Local tips for Jaipur commuters
  ✦  Search history saved locally (JSON)
  ✦  Full fare chart for quick reference

  {ORANGE}Built with:{RESET} {GRAY}Python 3  |  No external libraries

  {ORANGE}Author:{RESET}    {WHITE}Kartik Kumawat{RESET}
  {ORANGE}City:{RESET}      {WHITE}Jaipur, Rajasthan{RESET}{RESET}
""")
            divider()
            input(f"\n  {GRAY}Press Enter to go back...{RESET}")

        elif choice == "5":
            clear()
            print(f"\n  {ORANGE}{BOLD}JaipurFare — Safe travels! 🚌{RESET}\n")
            break

        else:
            print(f"{RED}  Invalid choice. Enter 1–5.{RESET}")
            input(f"  {GRAY}Press Enter...{RESET}")


# ─────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {ORANGE}Exiting JaipurFare. Alvida! 👋{RESET}\n")