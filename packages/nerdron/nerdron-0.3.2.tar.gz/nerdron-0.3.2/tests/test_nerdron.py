import unittest
from nerdron import NeuralNetwork, Activation
import numpy as np

class TestNerdron(unittest.TestCase):
    
    def setUp(self):
        self.nn = NeuralNetwork(layers=(2, 2, 1), activation=Activation.SIGMOID, learning_rate=0.1, epochs=1000)
        
    def test_forward(self):
        # Example data
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 1, 1, 1])
        
        # Train the neural network
        self.nn.train(X, y)
        
        # Test predictions
        prediction_01 = self.nn.forward(np.array([0, 1]))
        self.assertAlmostEqual(prediction_01, 0.9, delta=0.1)

if __name__ == '__main__':
    unittest.main()
