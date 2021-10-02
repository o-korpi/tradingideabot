import numpy as np
import pandas as pd


def ma(price_data, period) -> np.float64:
	data = pd.Series(price_data).rolling(window=period).mean().iloc[period - 1:].values
	return data


def ema(values, period):
	return values.ewm(span=period, adjust=False).mean()


def rsi(df, periods=14):
	"""
	Returns a pd.Series with the relative strength index.
	"""
	close_delta = df['close'].diff()

	# Make two series: one for lower closes and one for higher closes
	up = close_delta.clip(lower=0)
	down = -1 * close_delta.clip(upper=0)

	# Use exponential moving average
	ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
	ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()

	rsi_ = ma_up / ma_down
	rsi_ = 100 - (100 / (1 + rsi_))
	return rsi_


def ichimoku(data, tenkan_period=9, kijun_period=26, displacement=26, span_b_period=52):

	def get_period_avg(period, lag=0, data_=data):
		period_low = data_['low'].rolling(window=period).min()
		period_high = data_['high'].rolling(window=period).max()
		return (period_high + period_low) / 2

	tenkan = get_period_avg(tenkan_period)
	kijun = get_period_avg(kijun_period)

	senkou_b_noshift = get_period_avg(span_b_period, 26, data)
	senkou_b = senkou_b_noshift.shift(26)

	senkou_a_noshift = ((tenkan + kijun) / 2)
	senkou_a = senkou_a_noshift.shift(26)

	chikou = data["close"].shift(-26)

	return {"Tenkan": tenkan, "Kijun": kijun, "Senkou Span A": senkou_a, "Senkou Span B": senkou_b, "Chikou": chikou, "SPANS": senkou_a_noshift, "SPBNS": senkou_b_noshift}
