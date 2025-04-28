import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import simpledialog

def get_user_input():
    # Hardcoded default values
    config = {
        'altitude': 1000,        # Default starting altitude (meters)
        'speed': 250,            # Default starting speed (m/s)
        'max_altitude': 12000,   # Default max altitude (meters)
        'max_speed': 700         # Default max speed (m/s)
    }

    use_gui = False  # Default to CLI, set to True if you want to switch to GUI input

    if use_gui:
        root = tk.Tk()
        root.withdraw()

        # GUI-based input dialog
        altitude = simpledialog.askfloat("Input", "Enter starting altitude (meters):", initialvalue=config['altitude'])
        speed = simpledialog.askfloat("Input", "Enter starting speed (m/s):", initialvalue=config['speed'])
        max_altitude = simpledialog.askfloat("Input", "Enter maximum altitude (meters):", initialvalue=config['max_altitude'])
        max_speed = simpledialog.askfloat("Input", "Enter maximum speed (m/s):", initialvalue=config['max_speed'])

        root.destroy()
    else:
        print("Using CLI input...")

        # CLI-based input dialog with default fallback
        try:
            altitude = float(input(f"Starting altitude (default {config['altitude']}m): ") or config['altitude'])
            speed = float(input(f"Starting speed (default {config['speed']}m/s): ") or config['speed'])
            max_altitude = float(input(f"Max altitude (default {config['max_altitude']}m): ") or config['max_altitude'])
            max_speed = float(input(f"Max speed (default {config['max_speed']}m/s): ") or config['max_speed'])
        except ValueError:
            print("Invalid input, using default configuration.")
            altitude = config['altitude']
            speed = config['speed']
            max_altitude = config['max_altitude']
            max_speed = config['max_speed']

    return {
        "altitude": altitude,
        "speed": speed,
        "max_altitude": max_altitude,
        "max_speed": max_speed
    }

def calculate_thrust_vs_drag(altitude, speed):
    # Simplified thrust vs drag calculation (this can be expanded with actual flight physics)
    drag_coefficient = 0.02  # Example drag coefficient (could be dynamic)
    air_density = 1.225 * (1 - 0.0000225577 * altitude)  # Approximation of air density with altitude
    thrust = 10000  # Example thrust value in Newtons (could be dynamic based on engine specs)
    drag = 0.5 * drag_coefficient * air_density * speed**2
    return thrust, drag

def calculate_power_required(speed, altitude):
    # Power required for level flight (simplified model)
    power = 0.5 * speed**3 / (1 + 0.1 * (altitude / 1000))  # Simplified power calculation
    return power

def update_plot(frame, line1, line2, altitudes, speeds):
    # This function updates the plot during the animation
    altitude = altitudes[frame]
    speed = speeds[frame]

    # Calculate thrust vs drag
    thrust, drag = calculate_thrust_vs_drag(altitude, speed)
    line1.set_data(altitudes[:frame], [calculate_thrust_vs_drag(a, s)[0] for a, s in zip(altitudes[:frame], speeds[:frame])])
    line2.set_data(altitudes[:frame], [calculate_thrust_vs_drag(a, s)[1] for a, s in zip(altitudes[:frame], speeds[:frame])])

    return line1, line2

def main():
    # Get user input (altitude, speed, etc.)
    inputs = get_user_input()

    altitude = inputs['altitude']
    speed = inputs['speed']
    max_altitude = inputs['max_altitude']
    max_speed = inputs['max_speed']

    # Simulation parameters
    altitudes = np.linspace(altitude, max_altitude, num=100)
    speeds = np.linspace(speed, max_speed, num=100)

    # Set up the figure and axis for plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(min(altitudes), max(altitudes))
    ax.set_ylim(0, max(max_altitude, max_speed) * 2)  # Adjust the max y-limits

    # Create empty lines for thrust and drag
    line1, = ax.plot([], [], label='Thrust', color='blue')
    line2, = ax.plot([], [], label='Drag', color='red')

    # Add labels and legend
    ax.set_xlabel("Altitude (meters)")
    ax.set_ylabel("Force (Newtons)")
    ax.legend()

    # Create an animation of the flight performance
    ani = FuncAnimation(fig, update_plot, frames=range(len(altitudes)), fargs=(line1, line2, altitudes, speeds),
                        interval=100, repeat=False)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
