"""MatWeb web scraping integration for Virtual Lab data pipeline.

Scrapes mechanical and thermal material properties from MatWeb
using BeautifulSoup.
"""
# src/data_integration/matweb_integration.py

import requests
from bs4 import BeautifulSoup
import time
import random

def search_matweb_material(query):
    """
    Searches MatWeb for materials matching the query.
    
    Args:
        query (str): The search term (e.g., "Aluminum 6061").
        
    Returns:
        list[dict]: A list of dictionaries containing material names and links.
    """
    base_url = "http://www.matweb.com"
    search_url = f"{base_url}/search/QuickText.aspx"
    
    # MatWeb expects the query in the query string
    params = {'SearchText': query}
    
    # Use a realistic User-Agent to avoid immediate blocking
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Searching MatWeb for: {query}...")
    
    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = []
        
        # MatWeb results are typically in a table with specific structure.
        # This is a generalized parser that looks for links in the main content area.
        # Note: Selectors are fragile and may break if MatWeb updates their site.
        
        # Look for the results table or list. 
        # Often MatWeb puts results in a table with id="tblResults" or similar, 
        # or simply specific a tags.
        
        # Strategy: Find all links that contain "MaterialDetail" in the href
        material_links = soup.find_all('a', href=True)
        
        for link in material_links:
            href = link['href']
            if "MaterialDetail.aspx" in href:
                name = link.text.strip()
                if name:
                    full_link = base_url + href if href.startswith('/') else base_url + '/' + href
                    results.append({
                        "name": name,
                        "url": full_link,
                        "source": "MatWeb"
                    })
                    
        # Deduping results based on URL
        unique_results = {v['url']: v for v in results}.values()
        return list(unique_results)

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to MatWeb: {e}")
        return []
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        return []

def get_matweb_details_mock(url):
    """
    Fetches details for a specific material. 
    NOTE: Parsing the specific property table is complex and highly variable.
    This function currently returns a placeholder to demonstrate the architecture.
    """
    print(f"Fetching details from: {url}")
    # In a full implementation, this would:
    # 1. requests.get(url)
    # 2. Parse the property table (often huge and nested)
    # 3. Return a standardized dictionary
    
    # Simulating a delay to respect rate limits
    time.sleep(random.uniform(1, 2))
    
    return {
        "status": "Detail parsing not fully implemented (requires complex table parsing)",
        "url": url
    }

if __name__ == "__main__":
    print("--- Testing MatWeb Integration Module (Scraping) ---")
    print("Disclaimer: This module uses web scraping. MatWeb structure may change.")
    
    query = "Titanium Grade 5"
    results = search_matweb_material(query)
    
    if results:
        print(f"\nFound {len(results)} materials matching '{query}':")
        for i, res in enumerate(results[:5]): # Show top 5
            print(f"  {i+1}. {res['name']}")
            print(f"     Link: {res['url']}")
            
        if len(results) > 0:
            print("\n[Simulating Detail Fetch for first result]")
            details = get_matweb_details_mock(results[0]['url'])
            print(details)
    else:
        print("No results found or connection failed.")

