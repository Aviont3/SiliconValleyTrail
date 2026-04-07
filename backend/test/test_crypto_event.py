"""
Tests for services/crypto_event.py.
fetch_crypto_data() is tested with mocks so no real network calls are made.
get_revenue_multiplier() is tested with hand-crafted data covering every branch.
"""
from unittest.mock import patch, MagicMock
from services.crypto_event import fetch_crypto_data, get_revenue_multiplier


# --- get_revenue_multiplier (no network needed) ---

def make_data(btc_change, eth_change, sol_change):
    return {
        "bitcoin":  {"name": "Bitcoin",  "price": 60000, "change_24h": btc_change},
        "ethereum": {"name": "Ethereum", "price": 2000,  "change_24h": eth_change},
        "solana":   {"name": "Solana",   "price": 80,    "change_24h": sol_change},
    }

def test_fallback_when_no_data():
    multiplier, message = get_revenue_multiplier(None)
    assert multiplier == 1.0
    assert "baseline" in message.lower()

def test_bull_run_above_10_percent():
    data = make_data(btc_change=15.0, eth_change=2.0, sol_change=1.0)
    multiplier, message = get_revenue_multiplier(data)
    assert multiplier == 1.5
    assert "Bitcoin" in message

def test_healthy_market_between_3_and_10():
    data = make_data(btc_change=5.0, eth_change=1.0, sol_change=0.5)
    multiplier, message = get_revenue_multiplier(data)
    assert multiplier == 1.2

def test_flat_market_between_negative3_and_3():
    data = make_data(btc_change=0.5, eth_change=-0.5, sol_change=1.0)
    multiplier, message = get_revenue_multiplier(data)
    assert multiplier == 1.0

def test_shaky_market_between_negative10_and_negative3():
    # Best coin is -4.0, which is between -10 and -3 → shaky
    data = make_data(btc_change=-9.0, eth_change=-4.0, sol_change=-7.0)
    multiplier, message = get_revenue_multiplier(data)
    assert multiplier == 0.8

def test_crash_below_negative10():
    # All coins below -10 → best is -11.0 → crash
    data = make_data(btc_change=-15.0, eth_change=-12.0, sol_change=-11.0)
    multiplier, message = get_revenue_multiplier(data)
    assert multiplier == 0.5

def test_picks_best_performing_coin():
    # ETH is best here — should drive the multiplier
    data = make_data(btc_change=-5.0, eth_change=12.0, sol_change=2.0)
    multiplier, message = get_revenue_multiplier(data)
    assert multiplier == 1.5
    assert "Ethereum" in message


# --- fetch_crypto_data (mocked network) ---

def test_fetch_returns_all_three_coins():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "bitcoin":  {"usd": 69000, "usd_24h_change": 3.5},
        "ethereum": {"usd": 2100,  "usd_24h_change": 4.0},
        "solana":   {"usd": 82,    "usd_24h_change": 2.5},
    }
    mock_response.raise_for_status = MagicMock()

    with patch("services.crypto_event.requests.get", return_value=mock_response):
        data = fetch_crypto_data()

    assert data is not None
    assert "bitcoin" in data
    assert "ethereum" in data
    assert "solana" in data
    assert data["bitcoin"]["price"] == 69000
    assert data["bitcoin"]["change_24h"] == 3.5

def test_fetch_returns_none_on_network_error():
    with patch("services.crypto_event.requests.get", side_effect=Exception("timeout")):
        data = fetch_crypto_data()
    assert data is None

def test_fetch_returns_none_on_bad_status():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("404")

    with patch("services.crypto_event.requests.get", return_value=mock_response):
        data = fetch_crypto_data()
    assert data is None
