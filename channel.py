import random
import time



class Channel:
    def __init__(self, delay_mean=0.1, delay_std=0.05, error_rate=0.01):
        """
        Initialize the channel with specified parameters.
        :param delay_mean: Mean of the transmission delay in seconds.
        :param delay_std: Standard deviation of the transmission delay.
        :param error_rate: Probability of a message being corrupted.
        """
        self.delay_mean = delay_mean
        self.delay_std = delay_std
        self.error_rate = error_rate

    def transmit(self, message):
        """
        Simulate the transmission of a message through the channel.
        :param message: The original message to be transmitted.
        :return: The received message after channel effects.
        """
        # Simulate transmission delay
        delay = random.gauss(self.delay_mean, self.delay_std)
        time.sleep(max(0, delay))

        # Simulate message corruption
        if random.random() < self.error_rate:
            corrupted_message = self.corrupt_message(message)
            return corrupted_message, delay, True
        else:
            return message, delay, False

    def corrupt_message(self, message):
        """
        Simulate corruption of the message.
        :param message: The original message.
        :return: A corrupted version of the message.
        """
        corrupted_message = message.copy()
        # Introduce random errors into the position data
        corrupted_message['latitude'] += random.uniform(-0.01, 0.01)
        corrupted_message['longitude'] += random.uniform(-0.01, 0.01)
        corrupted_message['altitude'] += random.uniform(-10, 10)
        return corrupted_message
