# src/data_integration/materials_project_integration.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from mp_api.client import MPRester
from emmet.core.summary import SummaryDoc

def get_material_summary(identifier, api_key=None):
    """
    Retrieves material summary data from the Materials Project.

    Args:
        identifier (str): A chemical formula (e.g., "Fe2O3") or Material ID (e.g., "mp-19").
        api_key (str): Your Materials Project API Key. If None, checks 'MP_API_KEY' environment variable.

    Returns:
        list[dict]: A list of dictionaries containing material summary data.
    """
    if not api_key:
        api_key = os.environ.get("MP_API_KEY")
    
    if not api_key:
        print("Error: No API Key provided. Set 'MP_API_KEY' environment variable or pass explicitly.")
        return []

    results = []
    
    try:
        with MPRester(api_key) as mpr:
            # Check if identifier looks like a Material ID (starts with "mp-" or "mvc-")
            if identifier.startswith("mp-") or identifier.startswith("mvc-"):
                # Fetch specific ID
                # Note: search allows mapping IDs directly
                docs = mpr.materials.summary.search(material_ids=[identifier])
            else:
                # Assume it's a formula
                docs = mpr.materials.summary.search(formula=identifier)

            for doc in docs:
                # doc is typically an Emmet SummaryDoc object
                results.append({
                    "material_id": str(doc.material_id),
                    "formula": doc.formula_pretty,
                    "structure_symmetry": doc.symmetry.symbol if doc.symmetry else None,
                    "formation_energy_per_atom": doc.formation_energy_per_atom,
                    "band_gap": doc.band_gap,
                    "is_stable": doc.is_stable,
                    "density": doc.density,
                    "source": "Materials Project"
                })
                
    except Exception as e:
        print(f"Materials Project API Error: {e}")
        return []

    return results

if __name__ == "__main__":
    print("--- Testing Materials Project Integration Module ---")
    
    # 1. Check for API Key
    # You can set this in your terminal: set MP_API_KEY=your_key_here
    key = os.environ.get("MP_API_KEY")
    
    if key:
        print("API Key found. Proceeding with live test...")
        
        # Test 1: Search by Formula (Si)
        print("\nSearching for 'Si' (Silicon)...")
        si_data = get_material_summary("Si", key)
        if si_data:
             # Just show the first result to avoid spam
            print(f"Found {len(si_data)} entries. Top result:")
            print(si_data[0])
        else:
            print("No data found for Si.")

        # Test 2: Search by ID (mp-149)
        print("\nSearching for 'mp-149'...")
        mp_data = get_material_summary("mp-149", key)
        if mp_data:
            print(mp_data[0])
        else:
            print("No data found for mp-149.")
            
    else:
        print("\n[!] SKIPPING LIVE TEST: No 'MP_API_KEY' environment variable found.")
        print("To test this module, run:")
        print("  set MP_API_KEY=your_actual_api_key_here")
        print("  python src/data_integration/materials_project_integration.py")
