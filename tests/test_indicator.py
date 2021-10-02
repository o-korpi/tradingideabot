import numpy as np
import pandas as pd
import indicators


class MockIndicator:
	name = "Test Indicator"

	@staticmethod
	def calculate(price_data) -> np.float64:
		return np.float64(1)


def test_register_and_run():
	indicators.register(MockIndicator.name, MockIndicator)
	test_data = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'])
	assert indicators.study("Test Indicator")(test_data) == 1
