import random
import time

class PulsedNoiseJammer:
    """
    Simulates pulsed noise jamming by periodically introducing errors, increasing delay, or blocking messages.
    """
    def __init__(self, jamming_probability=0.3, noise_intensity=0.7, jamming_power_dbm=-70, pulse_duration=2, pulse_interval=5):
        """
        :param jamming_probability: Probability of jamming occurring in a pulse
        :param noise_intensity: Intensity of noise when jamming occurs
        :param jamming_power_dbm: Jamming signal power in dBm
        :param pulse_duration: Duration (in seconds) when the jammer is active
        :param pulse_interval: Time interval (in seconds) between jamming pulses
        """
        self.jamming_probability = jamming_probability
        self.noise_intensity = noise_intensity
        self.jamming_power_dbm = jamming_power_dbm
        self.pulse_duration = pulse_duration
        self.pulse_interval = pulse_interval
        self.last_pulse_time = time.time()
        self.is_jamming = False
    
    def update_jamming_state(self):
        """Updates whether the jammer is currently active based on pulse timing."""
        current_time = time.time()
        elapsed_time = current_time - self.last_pulse_time
        
        if self.is_jamming and elapsed_time >= self.pulse_duration:
            self.is_jamming = False  # End of jamming pulse
            self.last_pulse_time = current_time
            print("[Jammer] Pulse ended.")
        elif not self.is_jamming and elapsed_time >= self.pulse_interval:
            self.is_jamming = True  # Start new jamming pulse
            self.last_pulse_time = current_time
            print("[Jammer] New jamming pulse started!")
    
    def jam_signal(self, message):
        """Introduce signal degradation or block messages during active jamming pulses."""
        self.update_jamming_state()
        
        if self.is_jamming and random.random() < self.jamming_probability:
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

# Example usage
if __name__ == "__main__":
    jammer = PulsedNoiseJammer(jamming_probability=0.5, noise_intensity=0.8, pulse_duration=3, pulse_interval=7)
    
    for i in range(20):  # Simulating multiple messages being sent
        message = {'latitude': 37.7749, 'longitude': -122.4194, 'altitude': 500}  # Sample GPS data
        jammed_message, jammed = jammer.jam_signal(message)
        
        if jammed:
            print("[Main] Message was jammed!", jammed_message)
        else:
            print("[Main] Message transmitted successfully:", jammed_message)
        
        time.sleep(1)  # Simulating real-time message transmission
