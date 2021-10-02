from src.data.strategy import strategy
from src.data.indicators_tmp import *


class EMA(strategy.Strategy):
	def __init__(self):
		self.name = "EMA10/21 Cross"
		self.short_ema = 10
		self.long_ema = 21
		self.ma = 50

	def should_entry(self, price_data) -> bool:
		price = price_data["close"]
		short = ema(price, self.short_ema)
		long = ema(price, self.long_ema)
		vlong = ma(price, self.ma)

		if price[-1] > vlong[-1] and price[-2] < vlong[-2]:
			if short[-1] > long[-1]:
					return True

		elif short[-1] > long[-1] and short[-2] < long[-2]:
			if price[-1] > ma(price, self.ma)[-1]:
					return True

		return False
