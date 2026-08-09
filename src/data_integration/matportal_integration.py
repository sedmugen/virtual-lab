"""MatPortal API integration for Virtual Lab data pipeline.

Retrieves ontology-aligned materials science concepts and property
definitions from the MatPortal REST API.
"""
# src/data_integration/matportal_integration.py

import requests
import os
import json # Added for JSONDecodeError in try-except blocks
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URL for MatPortal API
MATPORTAL_API_BASE_URL = "https://www.matportal.org/api/v1/ontologies"

def get_matportal_ontology_metadata(ontology_acronym, api_key=None):
    """
    Retrieves metadata for a specific ontology from MatPortal.

    Args:
        ontology_acronym (str): The acronym of the ontology (e.g., "EMMO", "OMO").
        api_key (str): Your MatPortal API Key. If None, checks 'MATPORTAL_API_KEY' environment variable.

    Returns:
        dict: A dictionary containing the ontology metadata, or None if not found or error.
    """
    if not api_key:
        api_key = os.environ.get("MATPORTAL_API_KEY")
    
    if not api_key:
        print("Error: No MatPortal API Key provided. Set 'MATPORTAL_API_KEY' environment variable or pass explicitly.")
        return None

    url = f"{MATPORTAL_API_BASE_URL}/{ontology_acronym}"
    headers = {
        "Authorization": f"apikey token={api_key}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} for {url} - Response: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err} for {url}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decoding error: {json_err} - Response text: {response.text}")
    return None

def search_matportal_classes(ontology_acronym, query, api_key=None, page=1, page_size=20):
    """
    Searches for classes within a specific ontology in MatPortal.

    Args:
        ontology_acronym (str): The acronym of the ontology (e.g., "EMMO").
        query (str): The search term.
        api_key (str): Your MatPortal API Key. If None, checks 'MATPORTAL_API_KEY' environment variable.
        page (int): The page number for results.
        page_size (int): The number of results per page.

    Returns:
        dict: A dictionary containing search results, or None if not found or error.
    """
    if not api_key:
        api_key = os.environ.get("MATPORTAL_API_KEY")
    
    if not api_key:
        print("Error: No MatPortal API Key provided. Set 'MATPORTAL_API_KEY' environment variable or pass explicitly.")
        return None

    url = f"{MATPORTAL_API_BASE_URL}/{ontology_acronym}/classes"
    params = {
        "q": query,
        "page": page,
        "pagesize": page_size
    }
    headers = {
        "Authorization": f"apikey token={api_key}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} for {url} - Response: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err} for {url}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decoding error: {json_err} - Response text: {response.text}")
    return None

if __name__ == "__main__":
    print("--- Testing MatPortal Integration Module ---")
    
    # Get API Key from environment variable
    # You need to obtain a MatPortal API Key from matportal.org/accounts/apikey
    # and set it as an environment variable: MATPORTAL_API_KEY="YOUR_KEY_HERE"
    matportal_key = os.environ.get("MATPORTAL_API_KEY")

    if matportal_key:
        print("MatPortal API Key found. Proceeding with live test...")

        # Test 1: Get metadata for an ontology (e.g., EMMO)
        print("\nGetting metadata for 'EMMO' ontology...")
        emmo_metadata = get_matportal_ontology_metadata("EMMO", matportal_key)
        if emmo_metadata:
            print(f"  Ontology Name: {emmo_metadata.get('name')}")
            print(f"  Description: {emmo_metadata.get('description', 'N/A')[:100]}...")
            print(f"  Version: {emmo_metadata.get('version', 'N/A')}")
        else:
            print("  Could not retrieve EMMO metadata.")

        # Test 2: Search for a class within an ontology (e.g., 'polymer' in EMMO)
        print("\nSearching for 'polymer' class in 'EMMO' ontology...")
        polymer_classes = search_matportal_classes("EMMO", "polymer", matportal_key)
        if polymer_classes and polymer_classes.get('collection'):
            print(f"  Found {len(polymer_classes['collection'])} classes matching 'polymer':")
            for cls in polymer_classes['collection'][:3]: # Print first 3 results
                print(f"    - {cls.get('prefLabel') or cls.get('name')} (IRI: {cls.get('accession')})")
        else:
            print("  No 'polymer' classes found in EMMO or error.")
            
        # Test 3: Search with an invalid ontology acronym
        print("\nGetting metadata for invalid ontology 'INVALID_ONTO'...")
        invalid_onto_metadata = get_matportal_ontology_metadata("INVALID_ONTO", matportal_key)
        if invalid_onto_metadata is None:
            print("  Correctly handled invalid ontology acronym (returned None).")

    else:
        print("\n[!] SKIPPING LIVE TEST: No 'MATPORTAL_API_KEY' environment variable found.")
        print("To test this module:")
        print("  1. Obtain an API key from https://www.matportal.org/accounts/apikey")
        print("  2. Set it as an environment variable: set MATPORTAL_API_KEY=your_key_here")
        print("  3. Run: python src/data_integration/matportal_integration.py")

