import os
from matplotlib.backends.backend_pdf import PdfPages
# Function to find files in directory and its subdirectories
def find_files(directory, filename):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

# Function to find files in a directory and its subdirectories with a specific prefix
def find_files(directory, prefix):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith(prefix):
                files.append(os.path.join(root, filename))
    return files

# Search for the "U" file
U_filenames = find_files("postProcessing", "multU")
P_filenames = find_files("postProcessing", "multP")

# For naming the pdfs later
U_filenames_with_underscores = [filename.replace(os.path.sep, "_") for filename in U_filenames]
P_filenames_with_underscores = [filename.replace(os.path.sep, "_") for filename in P_filenames]
print(U_filenames_with_underscores)
print(P_filenames_with_underscores)
print("hi")

if U_filenames is None:
    print("Error: 'U' file not found in postProcessing directory.")
else:
    print("Location of 'U' file:", U_filenames)
    

import re
import matplotlib.pyplot as plt

for numFiles in range(len(U_filenames_with_underscores)):
    # Step 1: Open the file
    filename = U_filenames[numFiles]  # Assuming the file is named "U" and is in the current directory

    # Open the file for reading
    with open(filename, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()

    # Find the index of the line containing 'Time'
    time_index = next((i for i, line in enumerate(lines) if 'Time' in line), None)

    if time_index is None:
        print("Error: 'Time' not found in the file.")
        exit()

    # Extract the data and store it in arrays
    time_ids = []
    U_data = {}
    time_values = set()

    for line in lines[time_index + 1:]:
        # Split each line into time and velocity vectors
        time, *vectors = re.findall(r'[\w.-]+|\(.*?\)', line)

        # Convert time to float
        time = float(time)

        # Store time value
        time_values.add(time)

        # Store velocity vectors as tuples
        for i, vector_str in enumerate(vectors):
            # Convert string representation of the vector to a tuple of floats
            vector = tuple(map(float, vector_str.strip('()').split()))

            # Append vector to U_data dict under the corresponding probe ID
            probe_id = i + 1  # Adjust probe ID to start from 1
            if probe_id not in U_data:
                U_data[probe_id] = []
            U_data[probe_id].append(vector)

    # Determine the number of probes from the length of data
    num_probes = len(U_data)

    # Group probes in groups of 10
    probe_groups = [list(range(i, min(i + 10, num_probes + 1))) for i in range(1, num_probes + 1, 10)]
    print(U_filenames_with_underscores[numFiles]+'_velocity_plots.pdf')
    pdf_pages = PdfPages(U_filenames_with_underscores[numFiles]+'_velocity_plots.pdf')

    # Initialize lists to store time values and x velocity values for each probe group
    time_values = sorted(time_values)
    x_velocities = {tuple(probe_group): [] for probe_group in probe_groups}

    # Extract x velocity values for each probe group
    for probe_group in probe_groups:
        for probe_id in probe_group:
            x_vels = [vector[0] for vector in U_data.get(probe_id, [])]
            if x_vels:
                x_velocities[tuple(probe_group)].append(x_vels)

    # Plot x velocity values for each probe group and save as PNG
    for probe_group, x_vels_group in x_velocities.items():
        plt.figure()
        for i, probe_id in enumerate(probe_group):
            if i < len(x_vels_group):  # Check if x_vels_group has elements for this probe
                plt.plot(time_values, x_vels_group[i], label=f"Probe {probe_id}")
        plt.xlabel('Time')
        plt.ylabel('X Velocity')
        plt.title(f'X Velocity vs. Time for Probes {probe_group[0]}-{probe_group[-1]}')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.grid(True)
        pdf_pages.savefig(bbox_inches='tight')  # Save the plot in PDF
        plt.close()  # Close the plot to release memory

    print("xvel Plots saved as PNG files.")

    # Initialize lists to store time values and y velocity values for each probe group
    time_values = sorted(time_values)
    y_velocities = {tuple(probe_group): [] for probe_group in probe_groups}

    # Extract y velocity values for each probe group
    for probe_group in probe_groups:
        for probe_id in probe_group:
            y_vels = [vector[1] for vector in U_data.get(probe_id, [])]
            if y_vels:
                y_velocities[tuple(probe_group)].append(y_vels)

    # Plot y velocity values for each probe group and save as PNG
    for probe_group, y_vels_group in y_velocities.items():
        plt.figure()
        for i, probe_id in enumerate(probe_group):
            if i < len(y_vels_group):  # Check if y_vels_group has elements for this probe
                plt.plot(time_values, y_vels_group[i], label=f"Probe {probe_id}")
        plt.xlabel('Time')
        plt.ylabel('Y Velocity')
        plt.title(f'Y Velocity vs. Time for Probes {probe_group[0]}-{probe_group[-1]}')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.grid(True)
        pdf_pages.savefig(bbox_inches='tight')  # Save the plot in PDF
        plt.close()  # Close the plot to release memory

    print("yvel Plots saved as PNG files.")

    # Initialize lists to store time values and z velocity values for each probe group
    time_values = sorted(time_values)
    z_velocities = {tuple(probe_group): [] for probe_group in probe_groups}

    # Extract z velocity values for each probe group
    for probe_group in probe_groups:
        for probe_id in probe_group:
            z_vels = [vector[2] for vector in U_data.get(probe_id, [])]
            if z_vels:
                z_velocities[tuple(probe_group)].append(z_vels)

    # Plot z velocity values for each probe group and save as PNG
    for probe_group, z_vels_group in z_velocities.items():
        plt.figure()
        for i, probe_id in enumerate(probe_group):
            if i < len(z_vels_group):  # Check if z_vels_group has elements for this probe
                plt.plot(time_values, z_vels_group[i], label=f"Probe {probe_id}")
        plt.xlabel('Time')
        plt.ylabel('Z Velocity')
        plt.title(f'Z Velocity vs. Time for Probes {probe_group[0]}-{probe_group[-1]}')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.grid(True)
        pdf_pages.savefig(bbox_inches='tight')  # Save the plot in PDF
        plt.close()  # Close the plot to release memory

    print("zvel Plots saved as PNG files.")

    # Close the PDF file
    pdf_pages.close()

    # Step 1: Open the file
    filename = P_filenames[numFiles]  # Assuming the file is named "p" and is in the current directory

    # Open the file for reading
    with open(filename, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()

    # Find the index of the line containing 'Time'
    time_index = next((i for i, line in enumerate(lines) if 'Time' in line), None)

    if time_index is None:
        print("Error: 'Time' not found in the file.")
        exit()

    # Extract the data and store it in arrays
    time_values = []
    scalar_values = {}

    for line in lines[time_index + 1:]:
        # Split each line into time and scalar values
        data = line.split()
        time = float(data[0])  # Extract time
        time_values.append(time)

        for i, value_str in enumerate(data[1:]):
            value = float(value_str)  # Convert scalar value to float
            probe_id = i + 1  # Adjust probe ID to start from 1

            if probe_id not in scalar_values:
                scalar_values[probe_id] = []

            scalar_values[probe_id].append(value)

    # Group probes in groups of 10
    probe_groups = [list(range(i, min(i + 10, len(scalar_values) + 1))) for i in range(1, len(scalar_values) + 1, 10)]

    # Initialize PDF pages to save plots
    pdf_pages = PdfPages(P_filenames_with_underscores[numFiles]+'_pressure_plots.pdf')

    # Plot scalar values for each probe group and save as PDF
    for probe_group in probe_groups:
        plt.figure()
        for probe_id in probe_group:
            if probe_id in scalar_values:
                plt.plot(time_values, scalar_values[probe_id], label=f"Probe {probe_id}")
        plt.xlabel('Time')
        plt.ylabel('Pressure Value')
        plt.title(f'Pressure Value vs. Time for Probes {probe_group[0]}-{probe_group[-1]}')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.grid(True)
        pdf_pages.savefig(bbox_inches='tight')  # Save the plot in PDF
        plt.close()  # Close the plot to release memory

    # Close the PDF file
    pdf_pages.close()

    print("Scalar Plots saved as PDF file.")