import yahooquery as yq
from src.data.strategy import ema_cross
from src import defines
from loguru import logger as lgr
from src.data import stocks
from src.data.strategy import strategies
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as Soup
import json
import pathlib
import re


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
	prev_nh_nl = None

	try:
		with open(pathlib.Path("res/previous_call.json")) as prev_call:
			prev_call = json.load(prev_call)

		previous_call = prev_call["Stocks"].copy()
		prev_nh_nl = prev_call["NHNL"]

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
					data.append(f"Entry for {stock}, using {strategy.name}")
					previous_call.append(stock)

			else:
				if stock in previous_call and strategy.name == "Ichimoku":
					previous_call.remove(stock)

	this_call = {"Stocks": previous_call.copy(), "NHNL": prev_nh_nl}

	with open(pathlib.Path("res/previous_call.json"), "w") as prev_call:
		json.dump(this_call, prev_call, indent=4)

	return data


def get_snp500_nh_nl_data() -> int:
	URL = "https://www.barchart.com/stocks/indices/sp/sp500"
	req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})

	webpage = urlopen(req).read()
	soup = Soup(webpage, "html.parser")

	containers = soup.findAll("div", "block-content bc-table-wrapper")
	for container in containers:
		a = container.findAll("td", "text-center")

		result = int("".join(re.findall(r"\d", str(a[-2]))))

		try:
			with open(pathlib.Path("res/previous_call.json")) as prev_call:
				prev_call = json.load(prev_call)
				previous_call = prev_call["Stocks"].copy()

			this_call = {"Stocks": previous_call.copy(), "NHNL": result}

			with open(pathlib.Path("res/previous_call.json"), "w") as prev_call:
				json.dump(this_call, prev_call, indent=4)
		except FileNotFoundError:
			lgr.error("previous_call.json not found")

			# todo: this is pure spaghetti. refactor it later.

		# Find the 52 Week NH-NL Difference
		return result


def get_yesterdays_nhnl() -> int:
	try:
		with open(pathlib.Path("res/previous_call.json")) as prev_call:
			prev_call = json.load(prev_call)
			return prev_call["NHNL"]

	except FileNotFoundError:
		lgr.error("previous_call.json not found")


if __name__ == '__main__':
	get_snp500_nh_nl_data()
