import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class GCS:
    def __init__(self, lat, lon, alt=0):
        """Initialize GCS position."""
        self.position = (lat, lon, alt)
        self.drone_positions = {}

    def receive_update(self, drone_id, position):
        """Receive updated position from the drone."""
        self.drone_positions[drone_id] = position

    def plot_status(self, routes):
        """Plots the waypoints, drones, and GCS position."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot waypoints
        for i, route in enumerate(routes):
            latitudes = [p[0] for p in route]
            longitudes = [p[1] for p in route]
            altitudes = [p[2] for p in route]
            ax.plot(latitudes, longitudes, altitudes, 'o-', label=f"Route {i+1}")

        # Plot GCS position
        ax.scatter(*self.position, color='black', marker='s', s=150, label="GCS")

        # Plot drone positions
        for drone_id, pos in self.drone_positions.items():
            ax.scatter(*pos, marker='^', s=100, label=f"Drone {drone_id}")

        ax.set_xlabel("Latitude")
        ax.set_ylabel("Longitude")
        ax.set_zlabel("Altitude (m)")
        ax.legend()
        plt.show()
