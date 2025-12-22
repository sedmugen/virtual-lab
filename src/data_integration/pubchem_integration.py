# src/data_integration/pubchem_integration.py

import pubchempy as pcp

def get_chemical_info(identifier, identifier_type='name'):
    """
    Retrieves canonical chemical information from PubChem.

    Args:
        identifier (str or int): The chemical name (str) or PubChem CID (int).
        identifier_type (str): 'name' for chemical name, 'cid' for PubChem CID.

    Returns:
        dict: A dictionary containing key chemical properties (cid, name, formula, smiles, inchikey)
              or None if the compound is not found or an error occurs.
    """
    try:
        if identifier_type == 'name':
            compounds = pcp.get_compounds(identifier, 'name')
        elif identifier_type == 'cid':
            compounds = pcp.Compound.from_cid(identifier)
            if compounds:
                compounds = [compounds] # Wrap single compound in a list for consistent processing
        else:
            print(f"Error: Invalid identifier_type '{identifier_type}'. Must be 'name' or 'cid'.")
            return None

        if compounds:
            c = compounds[0] # Take the first result
            return {
                "source": "PubChem",
                "cid": c.cid,
                "name": c.iupac_name,
                "molecular_formula": c.molecular_formula,
                "connectivity_smiles": c.connectivity_smiles,
                "inchikey": c.inchikey
            }
        else:
            print(f"No compound found for {identifier_type}: {identifier}")
            return None
    except pcp.PubChemPyError as e:
        print(f"PubChemPy Error for {identifier_type} '{identifier}': {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred for {identifier_type} '{identifier}': {e}")
        return None

if __name__ == "__main__":
    print("--- Testing PubChem Integration Module ---")

    # Test by chemical name
    aspirin_info = get_chemical_info("Aspirin", 'name')
    if aspirin_info:
        print("\nInformation for Aspirin:")
        for key, value in aspirin_info.items():
            print(f"  {key}: {value}")

    # Test by PubChem CID
    glucose_cid_info = get_chemical_info(5793, 'cid') # CID for Glucose
    if glucose_cid_info:
        print("\nInformation for Glucose (by CID):")
        for key, value in glucose_cid_info.items():
            print(f"  {key}: {value}")
            
    # Test for a non-existent compound
    non_existent_info = get_chemical_info("NonExistentChemical123", 'name')
    if not non_existent_info:
        print("\nNon-existent chemical test passed (returned None).")

    # Test for an invalid CID
    invalid_cid_info = get_chemical_info(99999999999, 'cid') # Very large, unlikely CID
    if not invalid_cid_info:
        print("\nInvalid CID test passed (returned None).")
