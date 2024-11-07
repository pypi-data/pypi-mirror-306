import numpy as np
from typing import Callable

class Activation:
    """
    Activation function types.
    """
    SIGMOID = lambda x: 1 / (1 + np.exp(-x))
    TANH = lambda x: np.tanh(x)
    RELU = lambda x: np.maximum(0, x)
    SOFTMAX = lambda x: np.exp(x) / np.sum(np.exp(x), axis=-1, keepdims=True)