import csv
import os

def get_csv_data(csv_file_path):
    """
    Read data from a CSV file and return it as a list of dictionaries.
    
    Args:
        csv_file_path (str): Path to the CSV file
        
    Returns:
        list: List of dictionaries where keys are column names and values are cell values
    """
    # Check if file exists
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
    
    # Read data from CSV file
    data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    
    return data

def get_test_data_as_parameters(csv_file_path):
    """
    Read data from a CSV file and return it as a list of parameter tuples for pytest.mark.parametrize.
    
    Args:
        csv_file_path (str): Path to the CSV file
        
    Returns:
        list: List of tuples where each tuple contains values for one test case
    """
    data = get_csv_data(csv_file_path)
    parameters = []
    
    for row in data:
        # Convert row dictionary to tuple of values
        parameters.append(tuple(row.values()))
    
    return parameters
