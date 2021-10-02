import numpy as np
import pandas as pd


class MovingAverage:
	def __init__(self):
		self.name = "Moving Average"

	@staticmethod
	def calculate(price_data, period) -> np.float64:
		data = pd.Series(price_data["close"]).rolling(window=period).mean().iloc[period - 1:].values
		return data


indicator = MovingAverage()
