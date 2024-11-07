import numpy as np
from typing import Callable

class Layer:
    def __init__(self, input_size: int, output_size: int, activation: Callable[[np.ndarray], np.ndarray]):
        self.input_size = input_size
        self.output_size = output_size
        self.activation = activation
        self.weights = np.random.randn(input_size, output_size)
        self.biases = np.zeros((1, output_size))
    
    def forward(self, inputs: np.ndarray) -> np.ndarray:
        self.input = inputs  # Store input for backpropagation
        self.output = self.activation(np.dot(inputs, self.weights) + self.biases)
        return self.output
