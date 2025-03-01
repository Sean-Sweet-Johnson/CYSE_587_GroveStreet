import random
import time


class SweepingJammer:
    """
    This class simulates a frequency hopping jammer (sweeping jammer) that disrupts drone communication.
    It hops between different frequencies over time.
    """
    def __init__(self, 
                 jamming_probability=0.4, 
                 noise_intensity=0.8, 
                 jamming_power_dbm=-65, 
                 frequency_range=(900, 920), 
                 hop_interval=2):
        """
        Initialize the jammer.
        
        :param jamming_probability: Probability of jamming occurring at a given frequency.
        :param noise_intensity: Intensity of interference (0 to 1).
        :param jamming_power_dbm: Power of the jamming signal in dBm.
        :param frequency_range: Tuple defining the start and end of the frequency range in MHz.
        :param hop_interval: Time interval (in seconds) before switching to a new frequency.
        """
        self.jamming_probability = jamming_probability
        self.noise_intensity = noise_intensity
        self.jamming_power_dbm = jamming_power_dbm
        self.frequency_range = frequency_range
        self.hop_interval = hop_interval
        self.current_frequency = random.uniform(*self.frequency_range)  

    def hop_frequency(self):
        """Hops to a new random frequency within the defined range."""
        self.current_frequency = random.uniform(*self.frequency_range)
        print(f"[Jammer] Hopping to frequency {self.current_frequency:.2f} MHz")

    def jam_signal(self, message):
        """Introduce signal degradation or block messages based on frequency hopping."""
        self.hop_frequency()  

        if random.random() < self.jamming_probability:
            print(f"[Jammer] Jamming message at {self.current_frequency:.2f} MHz: {message}")
            
            if random.random() < self.noise_intensity:
                print("[Jammer] Message completely lost due to strong interference!")
                return None, True  
            
            # Modify message data with noise
            message['latitude'] += random.uniform(-0.1, 0.1)
            message['longitude'] += random.uniform(-0.1, 0.1)
            message['altitude'] += random.uniform(-50, 50)
            return message, True  

        return message, False  

    def jamming_signal_power(self):
        """Returns the power of the jamming signal in dBm."""
        return self.jamming_power_dbm


drone_message = {
    "latitude": 27.7172,
    "longitude": 85.3240,
    "altitude": 500
}


jammer = SweepingJammer(jamming_probability=0.5, noise_intensity=0.8, frequency_range=(900, 920), hop_interval=2)

for _ in range(5):
    jammed_message, is_jammed = jammer.jam_signal(drone_message)
    
    if is_jammed:
        print("Jammed Message:", jammed_message)
    else:
        print("Message Sent Successfully:", jammed_message)
    
    time.sleep(jammer.hop_interval)  
