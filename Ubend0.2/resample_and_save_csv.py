import os
import csv
from paraview.simple import *

GridNumX = 100
GridNumY = 100
GridNumZ = 110

# Automatically get the path to the .foam file
current_directory = os.getcwd()
foam_file_path = 'C:/Users/RDCHLDDB/Documents/Ubend0.2/withoutWallRefinement/Ubend0.2/case.foam'
print(f"Loading OpenFOAM case from: {foam_file_path}")

# Load the OpenFOAM case
foam_case = OpenFOAMReader(FileName=foam_file_path)
# Set options to only load point arrays
foam_case.CellArrays = []
foam_case.PointArrays = []

# Resample To Image with user-defined parameters
resampleToImage1 = ResampleToImage(registrationName='ResampleToImage1', Input=foam_case)
resampleToImage1.SamplingDimensions = [GridNumX, GridNumY, GridNumZ]  # User-defined dimensions

# Update the pipeline to read the data
foam_case.UpdatePipeline()

# Set up the Spreadsheet View
spreadsheet_view = CreateView('SpreadSheetView')
spreadsheet_view.FieldAssociation = 'Point Data'  # Ensure we are exporting point data

# Show the data arrays in the Spreadsheet View
spreadsheet_rep = Show(resampleToImage1, spreadsheet_view)

# Update the Spreadsheet View to ensure it has the latest data
spreadsheet_view.Update()

# Export the data to a CSV file
output_csv_path = 'C:/Users/RDCHLDDB/Documents/Ubend0.2/withoutWallRefinement/Ubend0.2/output.csv'
print(f"Exporting data to: {output_csv_path}")
ExportView(output_csv_path, view=spreadsheet_view)

# Clean up
Delete(spreadsheet_view)
del spreadsheet_view
Delete(spreadsheet_rep)
del spreadsheet_rep

# Modify the CSV file to retain only the 2nd, 3rd, and 4th columns after removing the first row
def modify_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row
        modified_lines = []
        for line in reader:
            # Retain only the 2nd, 3rd, and 4th columns
            modified_line = line[1:4]  # Assuming the columns to retain are 2nd, 3rd, and 4th
            modified_lines.append(modified_line)

    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(modified_lines)

modify_csv(output_csv_path)