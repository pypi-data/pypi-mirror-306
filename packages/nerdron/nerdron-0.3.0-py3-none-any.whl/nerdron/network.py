import numpy as np
from typing import Callable, Tuple
from nerdron.activation import Activation
from .layer import Layer

class NeuralNetwork:
    """
    Represents a multi-layer neural network.
    """
    def __init__(self, layers: Tuple[int, ...], activation: Callable[[np.ndarray], np.ndarray] = Activation.SIGMOID, learning_rate: float = 0.01, epochs: int = 1000):
        self.layers = []
        for i in range(len(layers) - 1):
            self.layers.append(Layer(layers[i], layers[i+1], activation))
        self.learning_rate = learning_rate
        self.epochs = epochs

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        x = inputs
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Train the neural network using backpropagation.
        """
        for epoch in range(self.epochs):
            # Forward pass
            outputs = self.forward(X)

            # Backpropagation
            deltas = [None] * len(self.layers)
            deltas[-1] = outputs - y
            for i in reversed(range(len(self.layers) - 1)):
                deltas[i] = np.dot(deltas[i + 1], self.layers[i + 1].weights.T) * self.layers[i].activation(self.layers[i].input, derivative=True)

            # Update weights and biases
            for i, layer in enumerate(self.layers):
                layer.weights -= self.learning_rate * np.dot(layer.input.T, deltas[i])
                layer.biases -= self.learning_rate * np.sum(deltas[i], axis=0)
