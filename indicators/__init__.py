from os.path import dirname, basename, isfile, join
from typing import Protocol, Dict
import glob
import importlib

from loguru import logger
import numpy as np
import pandas as pd


class Indicator(Protocol):
	@staticmethod
	def calculate(price_data: pd.DataFrame, *args) -> np.float64:
		"""Calculate the value(s) of the indicator, given OHCL price data
		"""


def study(indicator: str) -> Indicator.calculate:
	"""Get the values from an indicator"""
	return __indicators[indicator].calculate


def register(indicator_name: str, indicator: Indicator) -> None:
	__indicators[indicator_name] = indicator


def load_indicators() -> None:
	"""Load the indicators in /indicators/"""
	# Get all the indicators in the folder
	logger.info("Loading indicators")
	modules = glob.glob(join(dirname(__file__), "*.py"))
	__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

	logger.info(f"Found {len(__all__)} indicators")

	# Import them
	modules = map(importlib.import_module, __all__)

	i = 1
	for module in modules:
		# Register them to __indicators
		register(module.indicator.name, module.indicator.calculate)
		logger.info(f"Loaded indicator {module.indicator.name} ({i}/{len(__all__)})")
		i += 1


__indicators: Dict[str, Indicator] = {}


if __name__ == "__main__":
	load_indicators()
