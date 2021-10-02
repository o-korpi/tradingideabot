from src.data.strategy import ema_cross, ichimoku


strategies = [
	ema_cross.EMA(),
	ichimoku.Ichimoku()
]
