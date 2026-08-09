"""ChEBI REST API integration for Virtual Lab data pipeline.

Fetches chemical entity metadata (names, formulae, roles, ontology IDs)
from the ChEBI (Chemical Entities of Biological Interest) database.
"""
# src/data_integration/chebi_integration.py

import requests
import json

CHEBI_API_BASE_URL = "https://www.ebi.ac.uk/webservices/chebi"

def search_chebi_compounds(query, search_category="ALL", maximum_results=10):
    """
    Searches ChEBI for compounds based on a query.

    Args:
        query (str): The search term (e.g., "glucose", "CHEMBL123").
        search_category (str): The category to search within (e.g., "ALL", "CHEBI_NAME", "CHEBI_ID", "FORMULA").
                               See ChEBI documentation for full list.
        maximum_results (int): Maximum number of results to return.

    Returns:
        list[dict]: A list of dictionaries, each representing a ChEBI search hit.
                    Returns an empty list if no results or an error occurs.
    """
    endpoint = f"{CHEBI_API_BASE_URL}/search"
    params = {
        "query": query,
        "searchCategory": search_category,
        "maximumResults": maximum_results,
        "stars": "ALL" # Include all star levels
    }
    
    try:
        response = requests.get(endpoint, params=params, headers={"Accept": "application/json"})
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Response: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decoding error: {json_err} - Response text: {response.text}")
    return []

def get_chebi_entry(chebi_id):
    """
    Retrieves detailed information for a specific ChEBI ID.

    Args:
        chebi_id (str): The ChEBI ID (e.g., "CHEBI:17234").

    Returns:
        dict: A dictionary containing detailed ChEBI entry information.
              Returns None if the entry is not found or an error occurs.
    """
    endpoint = f"{CHEBI_API_BASE_URL}/getCompleteEntity"
    params = {
        "chebiId": chebi_id
    }

    try:
        response = requests.get(endpoint, params=params, headers={"Accept": "application/json"})
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"ChEBI entry '{chebi_id}' not found.")
        else:
            print(f"HTTP error occurred: {http_err} - Response: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decoding error: {json_err} - Response text: {response.text}")
    return None


if __name__ == "__main__":
    print("--- Testing ChEBI Integration Module ---")

    # Test 1: Search for 'glucose'
    print("\nSearching for 'glucose' in ChEBI...")
    glucose_search_results = search_chebi_compounds("glucose", maximum_results=2)
    if glucose_search_results:
        print(f"Found {len(glucose_search_results)} results:")
        for res in glucose_search_results:
            print(f"  - ChEBI ID: {res.get('chebiId')}, Name: {res.get('chebiName')}, Star: {res.get('star')}")
        
        # Take the first ChEBI ID and get its full entry
        if glucose_search_results[0].get('chebiId'):
            first_chebi_id = glucose_search_results[0]['chebiId']
            print(f"\nGetting full entry for {first_chebi_id}...")
            full_entry = get_chebi_entry(first_chebi_id)
            if full_entry:
                print(f"  ChEBI ID: {full_entry.get('chebiId')}")
                print(f"  Name: {full_entry.get('chebiAsciiName')}")
                print(f"  Definition: {full_entry.get('definition', 'N/A')[:100]}...") # Truncate for display
                # print("  Parents:", [p['chebiId'] for p in full_entry.get('relationship', {}).get('is_a', []) if p.get('chebiId')])
            else:
                print(f"Could not retrieve full entry for {first_chebi_id}.")
    else:
        print("No results found for 'glucose'.")

    # Test 2: Search for a specific chemical (e.g., Aspirin by name)
    print("\nSearching for 'aspirin'...")
    aspirin_results = search_chebi_compounds("aspirin", search_category="CHEBI_NAME", maximum_results=1)
    if aspirin_results:
        print(f"Found {len(aspirin_results)} result for aspirin:")
        print(f"  - ChEBI ID: {aspirin_results[0].get('chebiId')}, Name: {aspirin_results[0].get('chebiName')}")
    else:
        print("No results found for 'aspirin'.")

    # Test 3: Get an entry for a non-existent ChEBI ID
    print("\nGetting entry for non-existent ChEBI ID 'CHEBI:9999999'...")
    non_existent_entry = get_chebi_entry("CHEBI:9999999")
    if non_existent_entry is None:
        print("Test for non-existent ChEBI ID passed (returned None).")

