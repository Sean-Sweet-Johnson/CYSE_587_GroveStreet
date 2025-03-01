import numpy as np
import random
import time

class ADSBChannel:
    def __init__(self, error_rate=0.01, frequency=1090e6, noise_figure_db=5.0):
        self.error_rate = np.float64(error_rate)
        self.frequency = np.float64(frequency)
        self.noise_figure_db = np.float64(noise_figure_db)
        self.light_speed = np.float64(3e8)  # Speed of light in m/s

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        R = np.float64(6371000)  # Earth radius in meters
        phi1, phi2 = np.radians(lat1), np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)

        a = (np.sin(delta_phi / 2) ** 2) + np.cos(phi1) * np.cos(phi2) * (np.sin(delta_lambda / 2) ** 2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        return R * c  # Distance in meters

    def free_space_path_loss(self, distance):
        if distance <= 0:
            return 0  # Avoid infinite loss
        wavelength = self.light_speed / self.frequency
        path_loss_db = 20 * np.log10(4 * np.pi * distance / wavelength)
        return path_loss_db

    def thermal_noise_power(self, bandwidth_hz):
        k = np.float64(1.38e-23)  # Boltzmann constant in J/K
        T = np.float64(290)  # Standard temperature in Kelvin
        noise_power_watts = k * T * bandwidth_hz
        noise_power_dbm = 10 * np.log10(noise_power_watts) + 30
        return noise_power_dbm

    def transmit(self, message, gcs_position, tx_power_dbm=50, bandwidth_hz=1e6, jammer=None, spoofer=None):
        drone_lat, drone_lon = message["latitude"], message["longitude"]
        gcs_lat, gcs_lon = gcs_position

        distance = self.haversine_distance(drone_lat, drone_lon, gcs_lat, gcs_lon)

        delay_seconds = distance / self.light_speed
        delay_ns = np.round(delay_seconds * 1e9, decimals=2)

        time.sleep(delay_seconds)

        path_loss_db = self.free_space_path_loss(distance)
        noise_power_dbm = self.thermal_noise_power(bandwidth_hz)

        rx_power_dbm = tx_power_dbm - path_loss_db

        # Initialize SNR with the basic calculation
        snr_db = rx_power_dbm - (noise_power_dbm + self.noise_figure_db)

        # Apply jamming effects if a jammer is present
        if jammer:
            jamming_signal_power_dbm = jammer.jamming_signal_power()
            # Combine the noise power with the jamming signal power
            effective_noise_power_dbm = 10 * np.log10(
                10**(noise_power_dbm / 10) + 10**(jamming_signal_power_dbm / 10)
            )
            snr_db = rx_power_dbm - (effective_noise_power_dbm + self.noise_figure_db)

        # Apply spoofing effects if a spoofer is present
        if spoofer:
            spoofed_message, spoofed = spoofer.spoof_message(message)
            if spoofed:
                # Assuming the spoofed message interferes with the legitimate signal
                spoofing_signal_power_dbm = tx_power_dbm  # Assuming same power for simplicity
                effective_noise_power_dbm = 10 * np.log10(
                    10**(noise_power_dbm / 10) + 10**(spoofing_signal_power_dbm / 10)
                )
                snr_db = rx_power_dbm - (effective_noise_power_dbm + self.noise_figure_db)

        corrupted = False
        if snr_db < 0 or random.random() < self.error_rate:
            message = self.corrupt_message(message)
            corrupted = True

        return message, delay_ns, corrupted, snr_db

    def corrupt_message(self, message):
        corrupted_message = message.copy()
        corrupted_message['latitude'] += random.uniform(-0.01, 0.01)
        corrupted_message['longitude'] += random.uniform(-0.01, 0.01)
        corrupted_message['altitude'] += random.uniform(-10, 10)
        return corrupted_message
