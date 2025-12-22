# src/data_integration/bioprinting_data_hub_integration.py

import pandas as pd
import os

def load_bioprinting_data(file_path):
    """
    Loads bioprinting data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The full path to the CSV file.

    Returns:
        pandas.DataFrame: A DataFrame containing the bioprinting data,
                          or None if the file cannot be loaded.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded {len(df)} rows from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading CSV from {file_path}: {e}")
        return None

def clean_bioprinting_data(df):
    """
    Performs basic cleaning and standardization on the bioprinting DataFrame.
    (Placeholder for more complex cleaning logic)

    Args:
        df (pandas.DataFrame): The DataFrame to clean.

    Returns:
        pandas.DataFrame: The cleaned DataFrame.
    """
    if df is None:
        return None

    # Example cleaning: convert column names to lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Convert numeric columns if they aren't already
    numeric_cols = ['concentration_g_l', 'nozzle_diameter_um', 'print_speed_mm_s',
                    'temperature_c', 'viability_percentage', 'mechanical_strength_kPa']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print("Basic data cleaning applied.")
    return df

if __name__ == "__main__":
    print("--- Testing 3D Bioprinting Data Hub Integration Module ---")

    # Define the path to the sample CSV file (relative to the project root)
    # Adjust this path if the sample CSV is moved
    sample_csv_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 
        '..', 
        'data_integration_analysis', 
        '3d_bioprinting_data_hub_sample.csv'
    )
    
    # Load the data
    bioprinting_df = load_bioprinting_data(sample_csv_path)

    if bioprinting_df is not None:
        print("\n--- Raw Data Head ---")
        print(bioprinting_df.head())

        # Clean the data
        cleaned_df = clean_bioprinting_data(bioprinting_df)

        print("\n--- Cleaned Data Head ---")
        print(cleaned_df.head())

        print("\n--- Cleaned Data Info ---")
        cleaned_df.info()

    # Test with a non-existent file
    print("\n--- Testing with non-existent file ---")
    non_existent_df = load_bioprinting_data("non_existent_file.csv")
    if non_existent_df is None:
        print("Correctly handled non-existent file.")
