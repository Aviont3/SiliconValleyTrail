import json
import os
import ssl
import urllib.parse
import urllib.request
from dotenv import load_dotenv
import certifi

load_dotenv()

# Get API key from environment variables
api_key = os.getenv("COINMARKETCAP_API_KEY")
if not api_key:
    raise ValueError("COINMARKETCAP_API_KEY not found in environment variables")


params = urllib.parse.urlencode(
    {
        "start": "1",
        "limit": "10",
        "convert": "USD",
    }
)

request = urllib.request.Request(
    f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?{params}",
    headers={
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    },
)

context = ssl.create_default_context(cafile=certifi.where())

with urllib.request.urlopen(request, context=context) as response:
    data = json.load(response)

# Organize and display cryptocurrency data
print("\n" + "="*120)
print("TOP 10 CRYPTOCURRENCIES - LIVE MARKET DATA".center(120))
print("="*120 + "\n")

print(f"{'Rank':<6} {'Name':<20} {'Symbol':<8} {'Price (USD)':<15} {'24h Change':<12} {'Market Cap':<20} {'Dominance':<12}")
print("-"*120)

for crypto in data['data']:
    rank = crypto['cmc_rank']
    name = crypto['name'][:19]
    symbol = crypto['symbol']
    price = crypto['quote']['USD']['price']
    change_24h = crypto['quote']['USD']['percent_change_24h']
    market_cap = crypto['quote']['USD']['market_cap']
    dominance = crypto['quote']['USD']['market_cap_dominance']
    
    # Format output
    change_str = f"{change_24h:+.2f}%"
    price_str = f"${price:,.2f}"
    cap_str = f"${market_cap:,.0f}"
    dom_str = f"{dominance:.2f}%"
    
    print(f"{rank:<6} {name:<20} {symbol:<8} {price_str:<15} {change_str:<12} {cap_str:<20} {dom_str:<12}")

print("\n" + "="*120)
print(f"Last Updated: {data['status'].get('timestamp', 'N/A')}")
print("="*120 + "\n")