from flask import Blueprint, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from google.cloud import datastore

load_dotenv()

analytics_bp = Blueprint('analytics', __name__, template_folder='templates')

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
PROJECT_ID = os.getenv('cloud-nataraja-raghuram')  # Ensure this is set in your .env file

# Datastore client
datastore_client = datastore.Client(project=PROJECT_ID)

@analytics_bp.route('/analytics')
def analytics_dashboard():
    stock_symbol = request.args.get('symbol', 'AAPL')  # Default to Apple if no symbol provided
    return render_template('analytics.html', stock_symbol=stock_symbol)

@analytics_bp.route('/api/stock/key-metrics')
def get_key_metrics():
    stock_symbol = request.args.get('symbol')
    if not stock_symbol:
        return jsonify({'error': 'Stock symbol is required'}), 400

    try:
        # Fetch key metrics from Finnhub
        metrics_url = f'https://finnhub.io/api/v1/stock/metric?symbol={stock_symbol}&metric=all&token={FINNHUB_API_KEY}'
        print(f"Fetching key metrics from: {metrics_url}")
        metrics_response = requests.get(metrics_url)
        
        # Check if the response was successful
        metrics_response.raise_for_status()
        
        metrics_data = metrics_response.json()
        print(f"Key metrics response: {metrics_data}")

        if 'metric' not in metrics_data:
            return jsonify({'error': 'No metrics data found'}), 404

        # Store the metrics in Datastore
        store_metrics_in_datastore(stock_symbol, metrics_data['metric'])

        return jsonify(metrics_data['metric'])

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return jsonify({'error': 'Failed to fetch key metrics', 'details': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

def store_metrics_in_datastore(symbol, metrics):
    """Stores the metrics data in Google Cloud Datastore."""
    try:
        key = datastore_client.key('StockMetrics', symbol)
        entity = datastore.Entity(key=key)
        entity.update(metrics)
        datastore_client.put(entity)
        print(f"Stored metrics for {symbol} in Datastore")
    except Exception as e:
        print(f"Failed to store metrics in Datastore: {e}")
