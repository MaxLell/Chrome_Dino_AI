import numpy as np

class Dino_Brain():

    def __init__(self):

        # One Input Layer, one Hidden Layer, One Outputl Layer
        self.n_x = 4
        self.n_h = 7
        self.n_y = 3

        # Random Initialize Weights and Biases
        self.W1 = np.random.randn(self.n_h, self.n_x) * 0.1
        self.b1 = np.random.randn(self.n_h, 1) * 0.1
        self.W2 = np.random.randn(self.n_y, self.n_h) * 0.1
        self.b2 = np.random.randn(self.n_y, 1) * 0.1

    def think_about_action(self, x):

        # ReLu Activation function
        def relu(z):
            return z * (z > 0)

        # Feed current observations into Feed Forward Neural Network
        def feed_forward_nn(x):
            z1 = np.dot(self.W1, x) + self.b1
            a1 = relu(z1)
            z2 = np.dot(self.W2, a1) + self.b2
            a2 = relu(z2)
            return a2.argmax()

        # make sure input array comes in the right shape
        x = x.reshape(self.n_x, 1)

        action = feed_forward_nn(x)
        return action
