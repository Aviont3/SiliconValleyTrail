# Silicon Valley Trail

A text-based startup journey game inspired by Oregon Trail. Travel from New York to San Francisco through key tech hubs, make strategic decisions, manage your team and resources, and build a successful startup unicorn before time runs out.

---

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd SiliconValleyTrail
```

### 2. Set up the backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Set up API keys (optional)
The core game uses **CoinGecko** (no API key required) for live crypto market data.

The standalone utility scripts require keys. Create a `.env` file inside `backend/` only if you want to use them:
```
COINMARKETCAP_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```
- Get a free CoinMarketCap key at: https://coinmarketcap.com/api/
- Get a free News API key at: https://newsapi.org/

### Running without API keys
The game runs fully without any `.env` file. `api_crypto.py` and `api_services.py` are standalone scripts not used during normal gameplay.

### 4. Start the backend server
```bash
cd backend
source .venv/bin/activate
python app.py
# Runs on http://localhost:5000
```

### 5. Start the frontend
```bash
cd frontend
npm install
npm start
# Opens at http://localhost:3000
```

---

## Architecture Overview

```
SiliconValleyTrail/
├── backend/
│   ├── app.py                  # Flask app, API routes (/api/start, /api/turn, /api/intro)
│   ├── requirements.txt
│   ├── data/
│   │   ├── events.py           # TRAVEL_EVENTS and LOCAL_EVENTS dictionaries
│   │   ├── locations.py        # LOCATIONS list and ROUTES with miles
│   │   ├── locations_choices.py# Per-city choice menus
│   │   └── start.py            # Intro/welcome content
│   ├── engine/
│   │   ├── game_engine.py      # process_turn() — orchestrates each turn
│   │   ├── choice_engine.py    # City action choices and effects
│   │   ├── travel_engine.py    # Travel logic, days/cost calculation
│   │   ├── event_engine.py     # Random event picker
│   │   └── win_engine.py       # is_game_over(), check_game_status()
│   ├── models/
│   │   └── game_state.py       # GameState class, to_dict(), apply_effects()
│   ├── services/
│   │   ├── crypto_event.py     # CoinGecko live BTC/ETH/SOL data → revenue multiplier
│   │   ├── api_crypto.py       # CoinMarketCap live data (standalone utility)
│   │   └── api_services.py     # News API (standalone utility)
│   └── test/
│       ├── test_win_engine.py      # 10 tests — win/lose conditions
│       ├── test_full_turn_flow.py  # 14 integration tests — full turn lifecycle
│       ├── test_crypto_event.py    # 10 tests — CoinGecko service (mocked)
│       └── travel_test.py          # 1 test — travel engine
└── frontend/
    └── src/
        ├── App.js              # React Router setup
        ├── StartScreen.jsx     # Intro screen, fetches /api/intro
        ├── GameScreen.jsx      # Main game UI, travel loading screen
        └── api.js              # Fetch wrappers for backend endpoints
```

### Dependencies
| Layer | Package | Purpose |
|---|---|---|
| Backend | Flask | REST API server |
| Backend | Flask-CORS | Allow React frontend to call API |
| Backend | requests | HTTP client for CoinGecko API |
| Backend | python-dotenv | Load `.env` API keys |
| Backend | certifi | SSL certificates for API calls |
| Backend | pytest | Test runner |
| Frontend | React | UI framework |
| Frontend | React Router | Client-side routing |

---

## How to Run Tests

35 tests across 4 files covering the win engine, full turn integration, crypto service, and travel engine.

```bash
cd backend
source .venv/bin/activate
python -m pytest test/ -v
```

| File | Tests | Coverage |
|---|---|---|
| `test_win_engine.py` | 10 | `is_game_over()`, `check_game_status()` |
| `test_full_turn_flow.py` | 14 | `process_turn()` end-to-end |
| `test_crypto_event.py` | 10 | CoinGecko fetch + revenue multiplier (mocked) |
| `travel_test.py` | 1 | Travel engine day/cost calculation |

To also manually verify the API:

```bash
# Must have backend running (python app.py)
curl http://localhost:5000/api/intro
curl http://localhost:5000/api/start
curl -X POST http://localhost:5000/api/turn \
  -H "Content-Type: application/json" \
  -d '{"choice": "travel"}'
```

---

## Example Commands / Game Inputs

After starting the game at `http://localhost:3000`:

| Action | What it does |
|---|---|
| Click **Start Game** | Navigates to the game screen, initializes state |
| Click a city choice (e.g. "Work on product") | Advances 1 day, applies effects to money/progress |
| Click **Travel** | Travels to next city, triggers a random travel event |
| Run out of money | Game over — "You ran out of money!" |
| Reach San Francisco with product_progress ≥ 100 | Win — "You built a successful startup!" |

---

## AI Utilization

GitHub Copilot was used throughout development to:
- Generate React components
- Debug CORS errors, import path issues 
- Suggest game balance adjustments (travel day calculations, starting money)
- Generate edges cases for unit test 


All generated code was reviewed, tested, and modified by the developer. The game logic, data (locations, events, choices), and design decisions are the developer's own.

---

## Design Notes

### Game Loop & Balance
Each turn either applies a city action (costs money, advances 1 day) or travels to the next city (costs money + days based on mileage). Revenue is earned every 5 days automatically. The player must reach San Francisco with `product_progress >= 100` within 60 days to win. City choices and travel costs are tuned so the player has meaningful tradeoffs between building, marketing, and moving forward.

### Why These APIs
- **CoinGecko** (active, no key required): Fetches live 24h price change data for BTC, ETH, and SOL each time revenue is collected. The best-performing coin determines a revenue multiplier (0.5×–1.5×), directly affecting gameplay. If the API times out, the game falls back to a 1.0× neutral multiplier.
- **CoinMarketCap** (`api_crypto.py`, standalone): Alternative crypto data source requiring an API key. Not used in the main game loop.
- **News API** (`api_services.py`, standalone): Tech headlines that could be used to generate dynamic events based on real-world news. Not yet wired into gameplay.

### Data Modeling
- **GameState** is a plain Python class held in memory server-side (global variable). It stores all mutable state: money, chemistry, followers, location, product progress, days.
- **Effects** are dictionaries (`{"money": -100, "product_progress": 10}`) applied via `apply_effects()`, keeping choice/event data declarative.
- **No persistence** — restarting the server resets the game. A session or database would be needed for multi-user or persistent play.

### Error Handling
- Flask wraps `make_turn` in try/except and returns `{"error": ...}` with a 500 status on failure.
- Frontend logs API errors to the console and shows a loading state during travel.
- API key errors in the utility scripts raise `ValueError` immediately on startup.
- **Rate limits**: CoinMarketCap free tier allows 333 requests/day. The script is run on-demand, not on a loop, so this is not a concern in current usage.

### Tradeoffs & "If I Had More Time"
- **Sessions instead of global state** — currently only one game can run at a time server-side. A proper session store (Flask sessions or Redis) would support multiple simultaneous players.
- **Persistent save state** — store `GameState` in a database so players can resume.
- **More city choices** — each city currently has 3–4 choices; more variety and city-specific flavor would improve replayability.
- **Real city backgrounds** — placeholder background images are used for each city; replacing them with real photography would improve immersion.
- **News API events** — `api_services.py` fetches real tech headlines but is not yet wired into the game loop. Connecting it would allow real-world events to dynamically affect gameplay.
- **Expanded test coverage** — current tests cover win logic, turn flow, travel, and the crypto service. Edge cases (e.g. maximum travel days, simultaneous events) could be tested further.

