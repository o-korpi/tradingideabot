import numpy as np
import pandas as pd
from indicators import moving_average
import pytest


def test_sma():
	test_data = pd.DataFrame(np.array([[1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [2, 2], [2, 2], [2, 2]]), columns=['close', 'b'])
	assert moving_average.MovingAverage.calculate(test_data, 5)[0] == 1
	assert moving_average.MovingAverage.calculate(test_data, 5)[-3] == 1.2
	assert moving_average.MovingAverage.calculate(test_data, 5)[-2] == 1.4
	assert moving_average.MovingAverage.calculate(test_data, 5)[-1] == 1.6
