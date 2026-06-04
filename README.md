# 🚌 JaipurFare — Bus & Auto Fare Calculator

A command-line tool to calculate public transport fares in **Jaipur, Rajasthan** — for City Buses (JCTSL) and Auto Rickshaws. No internet required, no external libraries, pure Python.

---

## 📸 Preview

```
╔══════════════════════════════════════════════════════╗
║         JaipurFare — Bus & Auto Calculator           ║
║         Jaipur, Rajasthan  |  Python CLI             ║
╚══════════════════════════════════════════════════════╝

  Main Menu

  1.  Calculate Fare
  2.  View Fare Chart
  3.  Search History
  4.  About
  5.  Exit
```

---

## 🚀 Getting Started

### Requirements
- Python 3.x
- No external libraries needed

### Installation

```bash
# Clone the repository
git clone https://github.com/kartikkumawat1310/jaipur-fare-calculator.git

# Go into the folder
cd jaipur-fare-calculator
```

### Run

**Windows:**
```powershell
python busfarecalculator.py
```

**Linux / Mac:**
```bash
python3 busfarecalculator.py
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🚌 Bus Fare | JCTSL slab-based official fare rates |
| 🛺 Auto Fare | Standard negotiated rates for Jaipur |
| 🌙 Night Fare | Auto fare automatically 1.5x after 10 PM |
| 🔄 Alternatives | Compare Bus, Auto, Rapido & Ola side by side |
| 📊 Fare Chart | Full table from 1–40 km at a glance |
| 🕓 History | Last 10 searches saved locally in JSON |
| 🔍 Smart Search | Find areas by number or by typing name |
| 💡 Local Tips | Jaipur-specific travel tips per mode |

---

## 🗺️ Supported Areas (35+)

```
Sindhi Camp       Ajmeri Gate       Badi Chaupar
Hawa Mahal        City Palace       Amber Fort
Jaipur Railway    Jaipur Airport    MI Road
Mansarovar        Vaishali Nagar    Malviya Nagar
C-Scheme          Bani Park         Raja Park
Tonk Road         Ajmer Road        Delhi Road
... and more
```

---

## 💰 Fare Logic

### City Bus — JCTSL Slab Rates

| Distance | Fare |
|---|---|
| Up to 2 km | ₹10 |
| Up to 5 km | ₹15 |
| Up to 10 km | ₹20 |
| Up to 15 km | ₹25 |
| Up to 20 km | ₹30 |
| Every 5 km after 20 km | +₹5 |

### Auto Rickshaw — Standard Rates

| Distance | Fare |
|---|---|
| Up to 2 km | ₹30 (base) |
| 2–5 km | ₹12/km |
| 5–10 km | ₹11/km |
| 10 km+ | ₹10/km |
| After 10 PM | 1.5x night charge |

---

## 📁 Project Structure

```
jaipur-fare-calculator/
│
├── busfarecalculator.py   # Main application
├── fare_history.json      # Auto-created on first run
└── README.md
```

---

## 🛠️ Built With

- **Language:** Python 3
- **Libraries:** `os`, `json`, `datetime` (all built-in)
- **Platform:** Windows / Linux / Mac

---

## 🙋 Why I Built This

Jaipur mein public transport fares confusing hote hain — especially for new students and tourists. Auto drivers often overcharge and bus routes aren't clearly documented anywhere in a simple format. This tool gives anyone a quick, offline reference for fair fares.

---

## 👨‍💻 Author

**Kartik Kumawat**
B.Tech CSE (Cybersecurity) — Jaipur, Rajasthan

- GitHub: [@kartikkumawat1310](https://github.com/kartikkumawat1310)
- LinkedIn: [kartik-kumawat-894144381](https://www.linkedin.com/in/kartik-kumawat-894144381/)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
