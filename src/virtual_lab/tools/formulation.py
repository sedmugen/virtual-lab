"""Agent tool functions for querying the materials science Data Lake.

These functions wrap the processed CSV and JSON files produced by
``src/data_integration/main.py`` and return natural-language summaries
suitable for injection into an agent response.

Functions
---------
search_bioprinting_params(material_name)
    Look up 3D bioprinting parameters for a given material.
suggest_hydrogel(application_type)
    Suggest hydrogels from the harvested HydrogelDB metadata.
"""
# src/virtual_lab/tools/formulation.py

import pandas as pd
import os
import glob

def get_latest_file(pattern):
    """Helper to find the most recent file in the data lake matching a pattern."""
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

def search_bioprinting_params(material_name: str) -> str:
    """
    Searches the Data Lake for 3D bioprinting parameters for a given material.
    
    Args:
        material_name (str): The name of the material (e.g., "Alginate", "GelMA").
        
    Returns:
        str: A natural language summary of the findings.
    """
    # path to processed data. Assumes project root is two levels up from 'tools/'
    project_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
    lake_dir = os.path.join(project_root, 'src', 'data_integration', 'data_lake', 'processed')
    file_pattern = os.path.join(lake_dir, "bioprinting_hub_*.csv")
    
    csv_path = get_latest_file(file_pattern)
    if not csv_path:
        return "Error: Bioprinting data not found in Data Lake. Please run the integration pipeline first."
    
    try:
        df = pd.read_csv(csv_path)
        # Case insensitive search
        matches = df[df['bioink_type'].str.contains(material_name, case=False, na=False)]
        
        if matches.empty:
            return f"No bioprinting parameters found for '{material_name}'."
        
        # Summarize findings
        summary = f"Found {len(matches)} protocols for {material_name}:\n"
        for _, row in matches.iterrows():
            summary += (f"- For {row['cell_type']}: Print at {row['temperature_c']}°C, "
                        f"Speed: {row['print_speed_mm_s']} mm/s, "
                        f"Pressure/Nozzle: {row['nozzle_diameter_um']} um. "
                        f"(Viability: {row['viability_percentage']}% , Strength: {row['mechanical_strength_kpa']} kPa)\n")
        return summary
    except Exception as e:
        return f"Error reading data lake: {str(e)}"

def suggest_hydrogel(application_type: str) -> str:
    """
    Suggests a hydrogel based on typical keywords (mock logic wrapping the OAI harvest).
    In a real scenario, this would search the vector database or JSON dump.
    """
    # For this prototype, we'll scan the raw JSON dump of the harvest
    lake_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data_integration', 'data_lake', 'raw')
    file_pattern = os.path.join(lake_dir, "hydrogeldb_harvest_*.json")
    
    json_path = get_latest_file(file_pattern)
    if not json_path:
        return "Hydrogel database not found."
        
    import json
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        matches = []
        for record in data:
            # simple keyword match in title or description
            text_content = str(record.get('title', '')) + " " + str(record.get('description', ''))
            if application_type.lower() in text_content.lower():
                matches.append(record)
        
        if not matches:
            return f"No hydrogels found specifically mentioning '{application_type}'."
            
        summary = f"Found {len(matches)} hydrogels for '{application_type}':\n"
        for m in matches[:3]: # Limit to 3
            title = m.get('title', ['Unknown Title'])[0]
            desc = m.get('description', ['No description'])[0]
            summary += f"- {title}: {desc}\n"
        return summary
        
    except Exception as e:
        return f"Error reading hydrogel data: {str(e)}"
