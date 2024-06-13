# conversion.py
from flask import Blueprint, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

conversion_bp = Blueprint('conversion', __name__, template_folder='templates')

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
EXCHANGE_RATE_API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')

class Conversion:
    def convert_price(self):
        stock_symbol = request.args.get('stock-symbol')
        if not stock_symbol:
            return jsonify({'error': 'Stock symbol is required'}), 400

        # Render the conversion.html template
        return render_template('conversion.html', stock_symbol=stock_symbol)

    def get_conversion(self):
        stock_symbol = request.form.get('stock-symbol')
        target_currency = request.form.get('currency')

        if not stock_symbol or not target_currency:
            return jsonify({'error': 'Stock symbol and target currency are required'}), 400

        try:
            # Fetch stock price from Finnhub
            stock_url = f'https://finnhub.io/api/v1/quote?symbol={stock_symbol}&token={FINNHUB_API_KEY}'
            print(f"Fetching stock data from: {stock_url}")
            stock_response = requests.get(stock_url)
            stock_response.raise_for_status()  # Raise HTTPError for bad responses
            stock_data = stock_response.json()
            print(f"Stock data response: {stock_data}")

            if 'c' not in stock_data:
                return jsonify({'error': 'Failed to fetch stock data', 'details': stock_data}), 500

            latest_price_usd = stock_data['c']
            print(f"Latest price (USD): {latest_price_usd}")

            # Fetch conversion rate from Exchange Rate API
            conversion_url = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/pair/USD/{target_currency}'
            print(f"Fetching conversion data from: {conversion_url}")
            conversion_response = requests.get(conversion_url)
            conversion_response.raise_for_status()  # Raise HTTPError for bad responses
            conversion_data = conversion_response.json()
            print(f"Conversion data response: {conversion_data}")

            if conversion_data['result'] != 'success':
                return jsonify({'error': 'Failed to fetch conversion data', 'details': conversion_data}), 500

            conversion_rate = conversion_data['conversion_rate']
            converted_price = float(latest_price_usd) * conversion_rate
            print(f"Conversion rate: {conversion_rate}, Converted price: {converted_price}")

            return jsonify({
                'stock_symbol': stock_symbol,
                'latest_price_usd': latest_price_usd,
                'target_currency': target_currency,
                'conversion_rate': conversion_rate,
                'converted_price': converted_price
            })
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return jsonify({'error': 'Failed to fetch conversion data', 'details': str(e)}), 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

conversion_view = Conversion()

conversion_bp.add_url_rule('/convert_price', view_func=conversion_view.convert_price, methods=['GET'])
conversion_bp.add_url_rule('/get_conversion', view_func=conversion_view.get_conversion, methods=['POST'])
