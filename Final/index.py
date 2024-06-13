# index.py
from flask import Blueprint, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

index_bp = Blueprint('index', __name__, template_folder='templates')

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

class Index:
    def home(self):
        return render_template('index.html')

    def get_stock_metrics(self):
        stock_symbol = request.args.get('symbol')
        if not stock_symbol:
            return jsonify({'error': 'Stock symbol is required'}), 400

        try:
            # Fetch company profile from Finnhub
            profile_url = f'https://finnhub.io/api/v1/stock/profile2?symbol={stock_symbol}&token={FINNHUB_API_KEY}'
            print(f"Fetching company profile from: {profile_url}")
            profile_response = requests.get(profile_url)
            profile_response.raise_for_status()  # Raise HTTPError for bad responses
            profile_data = profile_response.json()
            print(f"Company profile response: {profile_data}")

            # Fetch stock quote from Finnhub
            quote_url = f'https://finnhub.io/api/v1/quote?symbol={stock_symbol}&token={FINNHUB_API_KEY}'
            print(f"Fetching stock quote from: {quote_url}")
            quote_response = requests.get(quote_url)
            quote_response.raise_for_status()  # Raise HTTPError for bad responses
            quote_data = quote_response.json()
            print(f"Stock quote response: {quote_data}")

            # Combine the data into a single response
            data = {
                'symbol': profile_data.get('ticker', 'N/A'),
                'name': profile_data.get('name', 'N/A'),
                'market_cap': profile_data.get('marketCapitalization', 'N/A'),
                'share_outstanding': profile_data.get('shareOutstanding', 'N/A'),
                'country': profile_data.get('country', 'N/A'),
                'currency': profile_data.get('currency', 'N/A'),
                'exchange': profile_data.get('exchange', 'N/A'),
                'industry': profile_data.get('finnhubIndustry', 'N/A'),
                'ipo': profile_data.get('ipo', 'N/A'),
                'logo': profile_data.get('logo', 'N/A'),
                'phone': profile_data.get('phone', 'N/A'),
                'weburl': profile_data.get('weburl', 'N/A'),
                'current_price': quote_data.get('c', 'N/A'),
                'high_price': quote_data.get('h', 'N/A'),
                'low_price': quote_data.get('l', 'N/A'),
                'open_price': quote_data.get('o', 'N/A'),
                'previous_close_price': quote_data.get('pc', 'N/A')
            }

            return jsonify(data)

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return jsonify({'error': 'Failed to fetch stock data', 'details': str(e)}), 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

index_view = Index()

index_bp.add_url_rule('/', view_func=index_view.home, methods=['GET'])
index_bp.add_url_rule('/api/stock/metrics', view_func=index_view.get_stock_metrics, methods=['GET'])
