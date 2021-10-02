import yahooquery as yq
from src.data.strategy import ema_cross
from src import defines
from loguru import logger as lgr
from src.data import stocks
from src.data.strategy import strategies
import json
import pathlib


def get_stock_data(ticker):
	"""Returns OHCL-data for a stock

	:param ticker: Ticker for the stock, also requires market as a suffix
	:return: OHCL-Data
	"""
	data = yq.ticker.Ticker(ticker).history(interval="1d", period="6mo", adj_ohlc=True)
	return data


def should_entry(ticker, strategy):
	"""

	:param ticker: Ticker, don't forget suffix (.ST)
	:param strategy: Strategy used to analyze the ticker
	:return: True/False
	"""

	data = get_stock_data(ticker)
	result = strategy.should_entry(data)
	return result


def run_analysis():
	lgr.info("Running analysis")

	data = []
	previous_call = []

	try:
		with open(pathlib.Path("res/previous_call.json")) as prev_call:
			prev_call = json.load(prev_call)

		previous_call = prev_call["Stocks"].copy()

	except FileNotFoundError:
		lgr.error("previous_call.json not found")

	lgr.info(f"Stocks to analyze: {stocks.stocks}")
	for stock in stocks.stocks:
		lgr.info(f"Analysing stock {stock}")

		for strategy in strategies.strategies:
			lgr.info(f"Using strategy {strategy.name}")

			if should_entry(stock, strategy):

				if stock not in previous_call or strategy.name != "Ichimoku":

					lgr.info(f"Found entry for stock {stock} using strategy {strategy.name}")
					data.append(f"Found possible entry for {stock}, using {strategy.name}")
					previous_call.append(stock)

			else:
				if stock in previous_call and strategy.name == "Ichimoku":
					previous_call.remove(stock)

	this_call = {"Stocks": previous_call.copy()}

	with open(pathlib.Path("res/previous_call.json"), "w") as prev_call:
		json.dump(this_call, prev_call, indent=4)

	return data


if __name__ == '__main__':
	get_stock_data("BOL.ST")
