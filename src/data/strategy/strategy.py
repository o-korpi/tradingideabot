from typing import Protocol


class Strategy(Protocol):

	def should_entry(self, price_data) -> bool:
		"""Conditions for whether or not a trade should be entered"""
