import requests

CRYPTO_IDS = {
    "bitcoin": "Bitcoin",
    "ethereum": "Ethereum",
    "solana": "Solana",
}


def fetch_crypto_data():
    """Fetch 24h price change for the top 3 cryptos from CoinGecko (no API key needed).
    Returns a dict keyed by coin id, or None on failure."""
    try:
        ids = ",".join(CRYPTO_IDS.keys())
        res = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price"
            f"?ids={ids}&vs_currencies=usd&include_24hr_change=true",
            timeout=4,
        )
        res.raise_for_status()
        data = res.json()
        return {
            coin_id: {
                "name": CRYPTO_IDS[coin_id],
                "price": data[coin_id]["usd"],
                "change_24h": data[coin_id]["usd_24h_change"],
            }
            for coin_id in CRYPTO_IDS
            if coin_id in data
        }
    except Exception:
        return None


def get_revenue_multiplier(crypto_data):
    """Pick the best-performing crypto and return a revenue multiplier + event text.
    Falls back to a neutral multiplier if data is unavailable."""
    if not crypto_data:
        return 1.0, "Market data unavailable. Revenue at baseline."

    # Pick the coin with the highest 24h change
    best = max(crypto_data.values(), key=lambda c: c["change_24h"])
    change = best["change_24h"]
    name = best["name"]

    if change > 10:
        return 1.5, f" {name} surged {change:.1f}%! Investors are throwing money at you."
    elif change > 3:
        return 1.2, f" {name} is up {change:.1f}%. Solid investor confidence this cycle."
    elif change > -3:
        return 1.0, f" {name} is flat ({change:.1f}%). Revenue at baseline."
    elif change > -10:
        return 0.8, f" {name} dropped {change:.1f}%. Funding is shaky."
    else:
        return 0.5, f" {name} crashed {change:.1f}%! Investors are pulling out."
