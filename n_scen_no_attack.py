import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from drone import Drone
from route import RouteGenerator
from gcs import GCS
from channel import Channel

# Define central location (e.g., Washington, D.C.)
center_lat, center_lon = 38.8977, -77.0365  # White House location

# Initialize GCS
gcs = GCS(center_lat, center_lon)

# Create a RouteGenerator instance
route_gen = RouteGenerator(center_lat, center_lon, num_routes=3, waypoints_per_route=5, max_offset=0.02)
routes = route_gen.generate_routes()

# Initialize multiple drones with generated routes
drones = [
    Drone(id=f"{i+1}", drone_type=f"type{i+1}", acceleration_rate=2.0, climb_rate=3.0, speed=10.0 + i*5,
          position_error=2.0, altitude_error=1.0, battery_consume_rate=0.05, battery_capacity=10.0 + i*5, route=routes[i])
    for i in range(len(routes))
]

# Initialize the communication channel
channel = Channel(delay_mean=0.1, delay_std=0.05, error_rate=0.01)

# Create a figure for 3D plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot waypoints
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # Extend as needed for more drones
for i, route in enumerate(routes):
    latitudes = [p[0] for p in route]
    longitudes = [p[1] for p in route]
    altitudes = [p[2] for p in route]
    ax.scatter(latitudes, longitudes, altitudes, color=colors[i % len(colors)], label=f"Route {i+1} Waypoints")

# Plot GCS position
gcs_marker, = ax.plot([gcs.position[0]], [gcs.position[1]], [gcs.position[2]], 'ks', markersize=8, label="GCS")

# Initialize drone markers
drone_markers = {}
for i, drone in enumerate(drones):
    marker, = ax.plot([], [], [], 'o', color=colors[i % len(colors)], markersize=6, label=f"Drone {drone.id}")
    drone_markers[drone.id] = marker

# Set labels
ax.set_xlabel("Latitude")
ax.set_ylabel("Longitude")
ax.set_zlabel("Altitude (m)")
ax.legend()

def update(frame):
    active_drones = False
    for drone in drones:
        status = drone.calculate_navigation(1)

        if status == -2:
            print(f"Drone {drone.id} battery depleted.")
        elif status == 0:
            print(f"Drone {drone.id} completed its route.")
        else:
            active_drones = True
            # Original (ideal) message
            original_message = {
                'drone_id': drone.id,
                'latitude': drone.current_position[0],
                'longitude': drone.current_position[1],
                'altitude': drone.current_position[2],
                'timestamp': time.time()
            }

            # Transmit message through the channel
            received_message, delay, corrupted = channel.transmit(original_message)

            # Print original and received messages
            print(f"Original Message from Drone {drone.id}: {original_message}")
            if corrupted:
                print(f"Received Corrupted Message at GCS after {delay:.2f}s delay: {received_message}")
            else:
                print(f"Received Message at GCS after {delay:.2f}s delay: {received_message}")

            # Update GCS with the received (possibly corrupted) message
            gcs.receive_update(drone.id, (received_message['latitude'], received_message['longitude'], received_message['altitude']))

            # Update drone marker position
            marker = drone_markers[drone.id]
            marker.set_data([received_message['latitude']], [received_message['longitude']])
            marker.set_3d_properties([received_message['altitude']])

    if not active_drones:
        print("All drones have completed their routes or are inactive.")
        plt.close(fig)  # Close the plot window to end the simulation

    return list(drone_markers.values())

# Set up animation
ani = FuncAnimation(fig, update, frames=range(100), interval=1000, blit=False)

plt.show()
