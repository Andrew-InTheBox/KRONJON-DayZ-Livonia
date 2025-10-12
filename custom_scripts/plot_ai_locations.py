#!/usr/bin/env python3
"""
Plot AI Location positions from AILocationSettings.json on an X/Y scatter plot.
Labels each point with its location name.
"""

import json
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

def plot_ai_locations(json_file_path, output_dir=None):
    """
    Read AILocationSettings.json and create an X/Y scatter plot of all locations.

    Args:
        json_file_path: Path to the AILocationSettings.json file
        output_dir: Directory to save the output image (defaults to current directory)
    """
    # Read the JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Extract location data
    locations = data.get('RoamingLocations', [])

    if not locations:
        print("No locations found in the JSON file!")
        return

    # Extract X, Y coordinates and names
    x_coords = []
    y_coords = []
    names = []

    for location in locations:
        position = location.get('Position', [])
        name = location.get('Name', 'Unknown')

        if len(position) >= 3:
            x = position[0]  # First coordinate
            y = position[2]  # Third coordinate (middle is always 0)

            x_coords.append(x)
            y_coords.append(y)
            names.append(name)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)  # 1000x1000 pixels (10 inches * 100 dpi)

    # Plot points
    ax.scatter(x_coords, y_coords, c='red', s=50, alpha=0.6, edgecolors='black', linewidth=0.5)

    # Add labels for each point
    for i, name in enumerate(names):
        ax.annotate(name, (x_coords[i], y_coords[i]),
                   fontsize=6,
                   alpha=0.7,
                   xytext=(3, 3),  # Offset text slightly from point
                   textcoords='offset points')

    # Set labels and title
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)
    ax.set_title('AI Location Positions', fontsize=14, fontweight='bold')

    # Add grid for better readability
    ax.grid(True, alpha=0.3, linestyle='--')

    # Make sure the plot is square with equal aspect ratio
    ax.set_aspect('equal', adjustable='box')

    # Generate timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d%H%M')
    output_filename = f'AILocationsPlots-{timestamp}.png'

    # Determine output path
    if output_dir:
        output_path = Path(output_dir) / output_filename
    else:
        output_path = Path(output_filename)

    # Save the figure
    plt.tight_layout()
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    print(f"Plot saved to: {output_path}")
    print(f"Total locations plotted: {len(names)}")

    # Close the plot to free memory
    plt.close()

if __name__ == '__main__':
    # Default path to AILocationSettings.json
    # Adjust this path if running from a different location
    json_path = Path(__file__).parent.parent / 'mpmissions' / 'dayzOffline.enoch' / 'expansion' / 'settings' / 'AILocationSettings.json'

    # Output to the custom_scripts directory
    output_directory = Path(__file__).parent

    print(f"Reading AI locations from: {json_path}")
    plot_ai_locations(json_path, output_directory)
