import random
import numpy as np
import time

class Spoofer:
    def __init__(self, spoof_probability=0.3, fake_drone_id="FAKE123", drift_rate=0.01):
        self.spoof_probability = spoof_probability
        self.fake_drone_id = fake_drone_id
        self.drift_rate = drift_rate
        self.spoofed_drones = {}

    def spoof_message(self, message):
        drone_id = message['drone_id']
        
        if random.random() < self.spoof_probability:
            if drone_id not in self.spoofed_drones:
                self.spoofed_drones[drone_id] = {
                    'latitude': random.uniform(-0.01, 0.01),
                    'longitude': random.uniform(-0.01, 0.01),
                    'altitude': random.uniform(-5, 5)
                }
            
            drift = self.spoofed_drones[drone_id]
            
            spoofed_message = message.copy()
            spoofed_message['latitude'] += drift['latitude']
            spoofed_message['longitude'] += drift['longitude']
            spoofed_message['altitude'] += drift['altitude']
            
            self.spoofed_drones[drone_id]['latitude'] += random.uniform(-self.drift_rate, self.drift_rate)
            self.spoofed_drones[drone_id]['longitude'] += random.uniform(-self.drift_rate, self.drift_rate)
            self.spoofed_drones[drone_id]['altitude'] += random.uniform(-self.drift_rate * 50, self.drift_rate * 50)
            
            spoofed_message['drone_id'] = self.fake_drone_id if random.random() < 0.2 else message['drone_id']
            return spoofed_message, True
        
        return message, False
