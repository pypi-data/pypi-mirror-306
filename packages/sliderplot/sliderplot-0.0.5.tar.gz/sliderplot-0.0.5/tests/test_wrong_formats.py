import numpy as np
import pytest

from sliderplot import sliderplot


def test_wrong_depth_1():
    def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        return (x, y, "Hey"), x, 2 * y

    with pytest.raises(ValueError):
        sliderplot(f, show=False)


def test_wrong_depth_2():
    def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        return ((x, y, "Hey"),), (x, 2 * y)

    with pytest.raises(ValueError):
        sliderplot(f, show=False)
