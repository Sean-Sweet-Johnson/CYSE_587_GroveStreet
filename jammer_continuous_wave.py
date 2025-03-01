import random
import time

class ContinuousJammer:
    """
    This class simulates jamming by introducing errors, increasing delay, or blocking messages.
    It also includes continuous wave jamming.
    """
    def __init__(self, jamming_probability=0.3, noise_intensity=0.7, jamming_power_dbm=-70, continuous_noise_level=0.2, cw_jamming_power=-60):
        self.jamming_probability = jamming_probability
        self.noise_intensity = noise_intensity  # Higher value increases interference
        self.jamming_power_dbm = jamming_power_dbm  # Default jamming signal power in dBm
        self.continuous_noise_level = continuous_noise_level  # Background noise level
        self.cw_jamming_power = cw_jamming_power  # Power level for continuous wave jamming

    def apply_continuous_wave_jamming(self, message):
        """Apply continuous wave jamming effect to the message."""
        message['latitude'] += random.uniform(-self.continuous_noise_level, self.continuous_noise_level)
        message['longitude'] += random.uniform(-self.continuous_noise_level, self.continuous_noise_level)
        message['altitude'] += random.uniform(-self.continuous_noise_level * 100, self.continuous_noise_level * 100)
        return message

    def jam_signal(self, message):
        """Introduce signal degradation or block messages entirely."""
        # Apply continuous wave jamming
        message = self.apply_continuous_wave_jamming(message)
        
        # Apply probabilistic jamming
        if random.random() < self.jamming_probability:
            print("[Jammer] Jamming message:", message)
            if random.random() < self.noise_intensity:
                print("[Jammer] Message completely lost!")
                return None, True  # Message is lost
            else:
                message['latitude'] += random.uniform(-0.1, 0.1)
                message['longitude'] += random.uniform(-0.1, 0.1)
                message['altitude'] += random.uniform(-100, 100)
                return message, True
        
        return message, False

    def jamming_signal_power(self):
        """Returns the power of the jamming signal in dBm."""
        return self.jamming_power_dbm

    def continuous_wave_jamming_power(self):
        """Returns the power of the continuous wave jamming signal in dBm."""
        return self.cw_jamming_power
