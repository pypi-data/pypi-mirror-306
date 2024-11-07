# Nerdron

This is a Python package that provides a simple and flexible neural network implementation, with support for customizable layer configurations, activation functions, and training parameters.

## Features
- **Multi-layer Neural Network**: The `NeuralNetwork` class allows you to create neural networks with an arbitrary number of layers.
- **Customizable Activation Functions**: The `Activation` class provides common activation functions like sigmoid, tanh, ReLU, and softmax, which can be used in the neural network layers.
- **Backpropagation-based Training**: The `NeuralNetwork` class implements the backpropagation algorithm for training the neural network on input-output pairs.
- **User-friendly API**: The package provides a simple and intuitive API, making it easy to integrate into your projects.

## Installation
To install the neural network package, you can use pip:

```
pip install nerdron==0.3.1
```

## Usage

### Creating a Neural Network
To create a neural network, you can use the `NeuralNetwork` class. The constructor takes the following arguments:

- `layers`: A tuple of integers representing the number of neurons in each layer, including the input and output layers.
- `activation`: (optional) A callable that represents the activation function to be used in the layers. Defaults to `Activation.SIGMOID`.
- `learning_rate`: (optional) The learning rate to be used during training. Defaults to 0.01.
- `epochs`: (optional) The number of training epochs. Defaults to 1000.

Example:
```python
from nerdron import NeuralNetwork, Activation

# Create a neural network with 2 input neurons, 2 hidden neurons, and 1 output neuron
nn = NeuralNetwork(layers=(2, 2, 1), activation=Activation.SIGMOID, learning_rate=0.1, epochs=1000)
```

### Training the Neural Network
To train the neural network, you can use the `train` method, which takes the input data `X` and the target output `y` as arguments.

Example:
```python
# Example data
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 1, 1, 1])

# Train the neural network
nn.train(X, y)
```

### Making Predictions
After training the neural network, you can use the `forward` method to make predictions on new input data.

Example:
```python
# Make predictions
print(nn.forward(np.array([0, 1])))  # Output: ~0.9
print(nn.forward(np.array([1, 0])))  # Output: ~0.9
print(nn.forward(np.array([0, 0])))  # Output: ~0.1
print(nn.forward(np.array([1, 1])))  # Output: ~0.9
```

## Modules

### `activation.py`
This module defines the `Activation` class, which provides common activation functions like sigmoid, tanh, ReLU, and softmax.

### `layer.py`
This module defines the `Layer` class, which represents a single layer in the neural network. Each layer has an activation function, weights, and biases.

### `network.py`
This module defines the `NeuralNetwork` class, which represents the entire neural network. It handles the forward propagation, backpropagation, and updating of the weights and biases.

## Contribution
If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/MuhammadRamzy/nerdron).

> [!NOTE]  
> Under Development.    