from flask import Blueprint, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

analytics_bp = Blueprint('analytics', __name__, template_folder='templates')

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

@analytics_bp.route('/analytics')
def analytics_dashboard():
    stock_symbol = request.args.get('symbol', 'AAPL')  # Default to Apple if no symbol provided
    return render_template('analytics.html', stock_symbol=stock_symbol)

@analytics_bp.route('/api/stock/history')
def get_stock_history():
    stock_symbol = request.args.get('symbol')
    if not stock_symbol:
        return jsonify({'error': 'Stock symbol is required'}), 400

    try:
        # Fetch historical data for the past 6 months from Finnhub
        history_url = f'https://finnhub.io/api/v1/stock/candle?symbol={stock_symbol}&resolution=D&count=180&token={FINNHUB_API_KEY}'
        history_response = requests.get(history_url)
        history_response.raise_for_status()
        history_data = history_response.json()

        return jsonify(history_data)

    except requests.RequestException as e:
        return jsonify({'error': 'Failed to fetch historical stock data', 'details': str(e)}), 500

@analytics_bp.route('/api/stock/key-metrics')
def get_key_metrics():
    stock_symbol = request.args.get('symbol')
    if not stock_symbol:
        return jsonify({'error': 'Stock symbol is required'}), 400

    try:
        # Fetch key metrics from Finnhub
        metrics_url = f'https://finnhub.io/api/v1/stock/metric?symbol={stock_symbol}&metric=all&token={FINNHUB_API_KEY}'
        metrics_response = requests.get(metrics_url)
        metrics_response.raise_for_status()
        metrics_data = metrics_response.json()

        return jsonify(metrics_data['metric'])

    except requests.RequestException as e:
        return jsonify({'error': 'Failed to fetch key metrics', 'details': str(e)}), 500
