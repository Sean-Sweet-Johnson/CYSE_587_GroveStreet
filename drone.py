import math
import matplotlib.pyplot as plt
import time

class Drone:
    def __init__(self, id, drone_type, acceleration_rate, climb_rate, speed, position_error,
                 altitude_error, battery_consume_rate, battery_capacity, route):
        self.id = id
        self.drone_type = drone_type
        self.acceleration_rate = acceleration_rate
        self.climb_rate = climb_rate  # Meters per second
        self.speed = speed  # Meters per second
        self.position_error = position_error  # Meters
        self.altitude_error = altitude_error  # Meters
        self.battery_consume_rate = battery_consume_rate  # Ah per second
        self.battery_capacity = battery_capacity  # Ah
        self.battery_remaining = battery_capacity
        self.route = route  # List of waypoints (lat, lon, alt)
        
        if not route or len(route) < 2:
            self.current_position = route[0] if route else None
            self.target_position = None
            self.route_index = 0
        else:
            self.current_position = route[0]
            self.target_position = route[1]
            self.route_index = 1

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate the great-circle distance between two points on Earth (meters)."""
        R = 6371000  # Earth radius in meters
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (math.sin(delta_phi / 2) ** 2 +
             math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c  # Distance in meters

    def calculate_battery_usage(self, move_distance, move_altitude):
        """Compute battery consumption based on movement and altitude change."""
        base_usage = self.battery_consume_rate * (move_distance / self.speed)
        climb_factor = abs(move_altitude) * 0.05  # Additional consumption for climbing
        return base_usage + climb_factor

    def calculate_navigation(self, delta_time):
        """
        Simulates drone movement for a given time interval.
        Returns:
        -1 : No valid route
        -2 : Battery depleted
         0 : No more waypoints (completed)
         1 : Continue to next waypoint
        """
        if self.battery_remaining <= 0:
            return -2  # Battery depleted

        if self.current_position is None or self.target_position is None:
            return -1  # No valid route

        lat1, lon1, alt1 = self.current_position
        lat2, lon2, alt2 = self.target_position

        distance = self.haversine_distance(lat1, lon1, lat2, lon2)
        alt_difference = alt2 - alt1
        move_distance = min(self.speed * delta_time, distance)
        move_altitude = min(self.climb_rate * delta_time, abs(alt_difference)) * (1 if alt_difference > 0 else -1)

        # Interpolate new position
        if distance > 0:
            ratio = move_distance / distance
            new_lat = lat1 + ratio * (lat2 - lat1)
            new_lon = lon1 + ratio * (lon2 - lon1)
        else:
            new_lat, new_lon = lat1, lon1

        new_alt = alt1 + move_altitude

        # Battery usage
        energy_used = self.calculate_battery_usage(move_distance, move_altitude)
        self.battery_remaining = max(0, self.battery_remaining - energy_used)  # Prevent negative battery

        if self.battery_remaining == 0:
            return -2  # Battery depleted

        # Check if the drone reached the target
        if self.haversine_distance(new_lat, new_lon, lat2, lon2) <= self.position_error and abs(new_alt - alt2) <= self.altitude_error:
            self.current_position = self.target_position
            self.route_index += 1
            if self.route_index < len(self.route):
                self.target_position = self.route[self.route_index]
                return 1
            else:
                self.target_position = None
                return 0  # No more waypoints
        else:
            self.current_position = (new_lat, new_lon, new_alt)
            return 1  # Continue moving

# ----------- Visualization Code ----------- #

def plot_drone_path(route, drone):
    """
    Simulates the drone's movement and plots its trajectory.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract route points
    latitudes = [p[0] for p in route]
    longitudes = [p[1] for p in route]
    altitudes = [p[2] for p in route]

    # Plot the route
    ax.plot(latitudes, longitudes, altitudes, 'bo-', label="Waypoints")
    
    # Drone movement simulation
    drone_positions = []
    timestamps = []
    time_step = 1  # seconds per step

    print("\nDrone Simulation Start:")
    while True:
        status = drone.calculate_navigation(time_step)
        print(f"Position: {drone.current_position}, Battery: {drone.battery_remaining:.2f} Ah, Status: {status}")
        drone_positions.append(drone.current_position)

        if status in [-1, -2, 0]:  # Stop simulation
            break
        time.sleep(0.1)

    # Plot drone's actual movement
    drone_lat = [p[0] for p in drone_positions]
    drone_lon = [p[1] for p in drone_positions]
    drone_alt = [p[2] for p in drone_positions]

    ax.plot(drone_lat, drone_lon, drone_alt, 'r-', label="Drone Path")

    # Labels
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Longitude")
    ax.set_zlabel("Altitude (m)")
    ax.legend()
    plt.show()

