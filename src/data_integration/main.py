# src/data_integration/main.py

import os
import json
import pandas as pd
from datetime import datetime

# Import integration modules
from src.data_integration.pubchem_integration import get_chemical_info
from src.data_integration.materials_project_integration import get_material_summary
from src.data_integration.bioprinting_data_hub_integration import load_bioprinting_data, clean_bioprinting_data
from src.data_integration.signaling_pathways_integration import load_signaling_pathways_data, clean_signaling_pathways_data
from src.data_integration.hydrogeldb_integration import harvest_hydrogel_metadata

# Define Data Lake Paths
DATA_LAKE_DIR = os.path.join(os.path.dirname(__file__), 'data_lake')
RAW_DIR = os.path.join(DATA_LAKE_DIR, 'raw')
PROCESSED_DIR = os.path.join(DATA_LAKE_DIR, 'processed')

def setup_directories():
    """Ensures data lake directories exist."""
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

def save_to_lake(data, source, stage='raw', file_format='json'):
    """
    Saves data to the data lake.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{source}_{timestamp}.{file_format}"
    filepath = os.path.join(DATA_LAKE_DIR, stage, filename)
    
    try:
        if file_format == 'json':
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        elif file_format == 'csv' and isinstance(data, pd.DataFrame):
            data.to_csv(filepath, index=False)
        print(f"Saved {stage} data to {filepath}")
        return filepath
    except Exception as e:
        print(f"Error saving to lake: {e}")
        return None

def orchestrate_integrations():
    print("--- Starting Data Integration Orchestration ---")
    setup_directories()
    
    # 1. PubChem Integration
    print("\n[1] PubChem: Fetching data for 'Aspirin'...")
    aspirin_data = get_chemical_info("Aspirin", 'name')
    if aspirin_data:
        save_to_lake(aspirin_data, "pubchem_aspirin")
    
    # 2. Materials Project Integration
    print("\n[2] Materials Project: Fetching data for 'Si'...")
    # Note: Requires MP_API_KEY env var to be set
    mp_data = get_material_summary("Si")
    if mp_data:
        save_to_lake(mp_data, "materials_project_si")
    else:
        print("Skipping Materials Project save (No data/key).")

    # 3. HydrogelDB Integration
    print("\n[3] HydrogelDB: Harvesting metadata...")
    hydrogel_data = harvest_hydrogel_metadata()
    if hydrogel_data:
        save_to_lake(hydrogel_data, "hydrogeldb_harvest")

    # 4. 3D Bioprinting Data Hub (File Based)
    print("\n[4] 3D Bioprinting Hub: Processing CSV...")
    bio_csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data_integration_analysis', '3d_bioprinting_data_hub_sample.csv')
    if os.path.exists(bio_csv_path):
        raw_bio_df = load_bioprinting_data(bio_csv_path)
        if raw_bio_df is not None:
            # Save Raw
            save_to_lake(raw_bio_df, "bioprinting_hub", stage='raw', file_format='csv')
            
            # Process
            clean_bio_df = clean_bioprinting_data(raw_bio_df)
            
            # Save Processed
            save_to_lake(clean_bio_df, "bioprinting_hub", stage='processed', file_format='csv')
    else:
        print(f"Bioprinting sample file not found at {bio_csv_path}")

    # 5. Signaling Pathways Project (File Based)
    print("\n[5] Signaling Pathways: Processing CSV...")
    sig_csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data_integration_analysis', 'signaling_pathways_project_sample.csv')
    if os.path.exists(sig_csv_path):
        raw_sig_df = load_signaling_pathways_data(sig_csv_path)
        if raw_sig_df is not None:
             # Save Raw
            save_to_lake(raw_sig_df, "signaling_pathways", stage='raw', file_format='csv')
            
            # Process
            clean_sig_df = clean_signaling_pathways_data(raw_sig_df)
            
            # Save Processed
            save_to_lake(clean_sig_df, "signaling_pathways", stage='processed', file_format='csv')
    else:
        print(f"Signaling pathways sample file not found at {sig_csv_path}")

    print("\n--- Orchestration Complete ---")
    print(f"Check directory: {DATA_LAKE_DIR}")

if __name__ == "__main__":
    # Ensure MP_API_KEY is loaded if available
    from dotenv import load_dotenv
    load_dotenv()
    
    orchestrate_integrations()
