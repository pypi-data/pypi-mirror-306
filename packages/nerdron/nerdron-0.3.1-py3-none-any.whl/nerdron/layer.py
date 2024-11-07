import numpy as np
from typing import Callable

class Layer:
    """
    Represents a single layer in a neural network.
    """
    def __init__(self, input_size: int, output_size: int, activation: Callable[[np.ndarray], np.ndarray]):
        self.weights = np.random.randn(input_size, output_size) * np.sqrt(2 / input_size)
        self.biases = np.zeros(output_size)
        self.activation = activation
        self.input = None
        self.output = None

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        self.input = inputs
        self.output = self.activation(np.dot(inputs, self.weights) + self.biases)
        return self.output