from src.data.strategy import strategy
from src.data.indicators_tmp import *
from loguru import logger


class Ichimoku(strategy.Strategy):
	def __init__(self):
		self.name = "Ichimoku"
		self.tenkan = 9
		self.kijun = 26
		self.senkou_a = 26
		self.senkou_b = 52
		self.displacement = 26

	def should_entry(self, price_data) -> bool:
		i = ichimoku(price_data)
		price = price_data["close"]

		if price[-1] > i["Kijun"][-1]:  #  and price[-2] < i["Kijun"][-2]
			logger.info("Price > Kijun")
			if i["Chikou"][-27] > price[-27]:
				logger.info("Chikou > Price")
				if i["SPANS"][-1] > i["SPBNS"][-1]:
					logger.info("Bullish cloud")
					if i["Tenkan"][-1] > i["Kijun"][-1]:
						logger.info("T/K Cross")
						if price[-1] > i["Senkou Span A"][-1] and price[-1] > i["Senkou Span B"][-1]:
							return True

		return False
