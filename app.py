import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# API endpoint to fetch exchange rates from Open Exchange Rates
OPEN_EXCHANGE_RATES_API = "https://openexchangerates.org/api/latest.json"
APP_ID = "YOUR_APP_ID"  # Replace with your Open Exchange Rates app ID


# Helper function to fetch exchange rates from Open Exchange Rates API
def fetch_exchange_rates():
    params = {
        "app_id": APP_ID,
        "base": "USD",  # We use USD as the base currency
    }
    response = requests.get(OPEN_EXCHANGE_RATES_API, params=params)
    data = response.json()
    return data.get("rates", {})

# GET /currencies - Retrieve currency names with their respective currency codes
@app.route('/currencies', methods=['GET'])
def get_currencies():
    currencies = fetch_exchange_rates()
    return jsonify(currencies)

# GET /convert/<from_currency>/<to_currency> - Convert between currencies using USD conversion rates
@app.route('/convert/<from_currency>/<to_currency>', methods=['GET'])
def convert_currency(from_currency, to_currency):
    amount = float(request.args.get('amount', 1.0))

    rates = fetch_exchange_rates()

    # Calculate the cross-exchange rate using USD as the base
    from_currency_to_usd = rates.get(from_currency.upper(), 1.0)
    to_currency_to_usd = rates.get(to_currency.upper(), 1.0)
    from_currency_to_to_currency = to_currency_to_usd / from_currency_to_usd

    converted_amount = amount * from_currency_to_to_currency

    result = {
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "amount": amount,
        "converted_amount": converted_amount
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run()
