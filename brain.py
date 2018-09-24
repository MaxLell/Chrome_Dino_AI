import numpy as np

class Dino_Brain():

    def __init__(self):

        # One Input Layer, one Hidden Layer, One Outputl Layer
        self.n_x = 5
        self.n_h = 7
        self.n_y = 3

        # Random Initialize Weights and Biases
        self.W1 = np.random.randn(self.n_h, self.n_x)
        self.b1 = np.random.randn(self.n_h, 1)
        self.W2 = np.random.randn(self.n_y, self.n_h)
        self.b2 = np.random.randn(self.n_y, 1)

    def think_about_action(self, x):

        # Sigmoid Activation function
        def sigmoid(z):
            s = 1 / (1 + np.exp(-z))
            return s

        # Feed current observations into Feed Forward Neural Network
        def feed_forward_nn(x):
            z1 = np.dot(self.W1, x) + self.b1
            a1 = sigmoid(z1)
            z2 = np.dot(self.W2, a1) + self.b2
            a2 = sigmoid(z2)
            return a2.argmax()

        # make sure input array comes in the right shape
        x = x.reshape(self.n_x, 1)

        action = feed_forward_nn(x)
        return action
