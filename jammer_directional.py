import random
import math

class DirectionalJammer:
    """
    This class simulates directional jamming by introducing errors, increasing delay,
    or blocking messages within a certain area.
    """
    def __init__(self, jamming_probability=0.3, noise_intensity=0.7, jamming_power_dbm=-70, 
                 center_coordinates=(0.0, 0.0), jamming_radius=0.5):
        """
        :param jamming_probability: Probability of jamming occurring.
        :param noise_intensity: Intensity of noise affecting the signal.
        :param jamming_power_dbm: Power of the jamming signal in dBm.
        :param center_coordinates: The (latitude, longitude) of the jamming zone.
        :param jamming_radius: The radius within which jamming occurs.
        """
        self.jamming_probability = jamming_probability
        self.noise_intensity = noise_intensity
        self.jamming_power_dbm = jamming_power_dbm
        self.center_coordinates = center_coordinates  # (latitude, longitude)
        self.jamming_radius = jamming_radius  # in degrees 

    def is_within_jamming_zone(self, latitude, longitude):
        """Check if a given coordinate is within the jamming radius."""
        distance = math.sqrt((latitude - self.center_coordinates[0])**2 +
                             (longitude - self.center_coordinates[1])**2)
        return distance <= self.jamming_radius

    def jam_signal(self, message):
        """Introduce signal degradation or block messages entirely if within jamming zone."""
        if not isinstance(message, dict):
            print("[Jammer] Error: Invalid message format")
            return None  

        lat, lon = message['latitude'], message['longitude']

        if self.is_within_jamming_zone(lat, lon) and random.random() < self.jamming_probability:
            print("[Jammer] Jamming message:", message)

            if random.random() < self.noise_intensity:
                print("[Jammer] Message completely lost due to jamming!")
                return None  # Message is lost
            
            # Otherwise, introduce errors in message
            message['latitude'] += random.uniform(-0.1, 0.1)
            message['longitude'] += random.uniform(-0.1, 0.1)
            message['altitude'] += random.uniform(-100, 100)

        return message  # Return modified message or original if not jammed

    def jamming_signal_power(self):
        """Returns the power of the jamming signal in dBm."""
        return self.jamming_power_dbm
