import pandas as pd
import io
import requests
import os
from dotenv import load_dotenv

# Load API Keys
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# CSV data
csv_data = """bill_paid_at_local,bill_total_billed,bill_total_discount_item_level,bill_total_gratuity,bill_total_net,bill_total_tax,bill_total_voided,bill_uuid,business_date,order_duration_seconds,order_seated_at_local,order_closed_at_local,order_take_out_type_label,order_uuid,payment_amount,payment_count,payment_total_tip,sales_revenue_with_tax,venue_xref_id,waiter_uuid
2024-07-01 12:30:15,65.50,0.00,8.00,57.50,8.00,0.00,240701123015~A2BCDB70-2B26-41AD-91E0-16B03AE57525,2024-07-01,1800,2024-07-01 12:00:00,2024-07-01 12:30:00,,240701120000~B45831B3-2DB0-485E-B940-C279ADDF0E62,65.50,1,8.00,65.50,33a6fac78331382c568cfa689dfae1b85c09bbc39471cc5dbaec97adcf6f6e62,231029105657~D6736218-9AF0-4513-A02B-762527205CAE
2024-07-01 18:45:22,32.25,0.00,0.00,28.50,3.75,0.00,240701184522~C3DEF481-3A37-42BE-A2F1-27C14BF68636,2024-07-01,600,2024-07-01 18:35:00,2024-07-01 18:45:00,takeout,240701183500~D59042C4-4BB1-49CF-B302-38D25CE79747,32.25,1,0.00,32.25,33a6fac78331382c568cfa689dfae1b85c09bbc39471cc5dbaec97adcf6f6e62,231029105657~E78153D5-5CC2-4AB0-C413-49E36DF8A858
2024-07-02 13:10:30,85.00,5.00,10.00,70.00,10.00,0.00,240702131030~F4567892-4B48-44CF-B503-59F47EE9B969,2024-07-02,2700,2024-07-02 12:25:00,2024-07-02 13:10:00,,240702122500~G6A154E5-6DD3-4BC1-D524-6AF58EEAB07A,85.00,1,10.00,85.00,33a6fac78331382c568cfa689dfae1b85c09bbc39471cc5dbaec97adcf6f6e62,231029105657~H9C265F6-7EE4-4DD2-E635-7BF69FFBC18B
2024-07-02 19:55:45,48.75,0.00,6.00,42.75,6.00,0.00,240702195545~I5789013-5C59-46D0-C746-7CF7B00CD29C,2024-07-02,1200,2024-07-02 19:35:00,2024-07-02 19:55:00,,240702193500~J7E37607-8FF5-4EE3-F757-8DF8AFFD13AC,48.75,1,6.00,48.75,33a6fac78331382c568cfa689dfae1b85c09bbc39471cc5dbaec97adcf6f6e62,231029105657~K0D487G8-9GG6-4FF4-0868-9EF9B11DE4BD
2024-07-03 11:00:00,25.00,0.00,0.00,22.00,3.00,0.00,240703110000~L6890124-6D6A-48EF-D979-0AFAB22EF30E,2024-07-03,450,2024-07-03 10:52:00,2024-07-03 11:00:00,takeout,240703105200~M8F59818-0AA7-4005-0A8A-0BFAC33FE51F,25.00,1,0.00,25.00,33a6fac78331382c568cfa689dfae1b85c09bbc39471cc5dbaec97adcf6f6e62,231029105657~N1E609H9-1BB8-4116-1B9B-1CFBC4401620
2024-07-03 17:20:00,102.50,10.00,15.00,87.50,15.00,0.00,240703172000~O7901235-7E7B-4A0D-2B0C-2DFCD5512731,2024-07-03,3600,2024-07-03 16:20:00,2024-07-03 17:20:00,,240703162000~P2D710I0-2CC9-4227-3C1D-2E0DA6623842,102.50,1,15.00,102.50,33a6fac78331382c568cfa689dfae1b85c09bbc39471cc5dbaec97adcf6f6e62,231029105657~Q3C821J1-3DD0-4338-4D2E-3F1EB7734953
2024-07-04 14:40:00,55.00,0.00,7.00,48.00,7.00,0.00,240704144000~R8012346-8F8C-4C1E-5D3F-402FAC845A64,2024-07-04,2100,2024-07-04 14:05:00,2024-07-04 14:40:00,,240704140500~S4E932K2-4EE1-4449-6E40-4130CB956B75,55.00,1,7.00,55.00,33a6fac78331382c568cfa689dfae1b85c09bbc39471cc5dbaec97adcf6f6e62,231029105657~T5B043L3-5FF2-455A-7F51-5241DCA67C86
2024-07-04 20:15:00,92.75,0.00,12.00,80.75,12.00,0.00,240704201500~U9123457-9G9D-4E3F-9052-5352DDB58D97,2024-07-04,3000,2024-07-04 19:35:00,2024-07-04 20:15:00,,240704193500~V6C154M4-6GG3-466B-A163-6462EEC79EAB,92.75,1,12.00,92.75,33a6fac78331382c568cfa689dfae1b85c09bbc39471cc5dbaec97adcf6f6e62,231029105657~W7A265N5-7HH4-477C-B274-7573FFD8A0BC
2024-07-05 10:45:00,38.50,0.00,0.00,34.00,4.50,0.00,240705104500~X0234568-0A0E-4080-C385-8684EEF9B1CD,2024-07-05,750,2024-07-05 10:32:00,2024-07-05 10:45:00,takeout,240705103200~Y8B376O6-8II5-488D-D496-8794000A12DE,38.50,1,0.00,38.50,33a6fac78331382c568cfa689dfae1b85c09bbc39471cc5dbaec97adcf6f6e62,231029105657~Z9C487P7-9JJ6-499E-E5A7-98A5111B23EF
2024-07-05 16:00:00,72.00,0.00,9.00,63.00,9.00,0.00,240705160000~A1345679-1B1F-4191-F4B8-09A6222C34FE,2024-07-05,2400,2024-07-05 15:20:00,2024-07-05 16:00:00,,240705152000~B0D598Q8-2CC0-42A2-05C9-0AB6333D450F,72.00,1,9.00,72.00,33a6fac78331382c568cfa689dfae1b85c09bbc39471cc5dbaec97adcf6f6e62,231029105657~C2E609R9-3DD1-43B3-16DA-1BC7444E5610"""

# Portfolio Weights
weights = {
    "Consumer Behavior": 0.35,
    "Local Economy": 0.15,
    "Marketability": 0.10,
    "Accessibility": 0.25,
    "Competition": 0.15,
}

# Data Analysis
df = pd.read_csv(io.StringIO(csv_data))

# Function to determine portfolio
def determine_portfolio(df):
    """Analyzes the DataFrame to determine the dominant portfolio."""
    takeout_ratio = df['order_take_out_type_label'].value_counts(normalize=True).get('takeout', 0)
    average_bill = df['bill_total_billed'].mean()
    df['bill_paid_at_local'] = pd.to_datetime(df['bill_paid_at_local'])
    df['hour_of_day'] = df['bill_paid_at_local'].dt.hour
    hourly_distribution = df['hour_of_day'].value_counts(normalize=True)

    # Peak lunch hours (11 AM - 2 PM)
    lunch_hours = hourly_distribution[(hourly_distribution.index >= 11) & (hourly_distribution.index <= 14)].sum()

    # Simple logic - needs adjustment with a proper dataset
    if takeout_ratio > 0.6 and average_bill < 50 and lunch_hours > 0.5:
        return "Busy Lunchtime Professional"
    elif average_bill > 70 and lunch_hours < 0.3:
        return "Relaxed Dinner Guest"
    else:
        return "General Audience"

# Determine portfolio
dominant_portfolio = determine_portfolio(df)
print(f"Dominant Portfolio: {dominant_portfolio}")

# Simplified Scoring - you'll need to replace with real API data/analysis
def get_location_score(location, portfolio):
    """Calculates a theoretical score for a potential location."""
    # Simplified scoring based on portfolio
    if portfolio == "Busy Lunchtime Professional":
        consumer_behavior = 8  # High takeout, quick service
        local_economy = 7  # Proximity to businesses
        marketability = 7  # Demand for quick lunch
        accessibility = 9  # High foot traffic
        competition = 6  # Moderate competition
    elif portfolio == "Relaxed Dinner Guest":
        consumer_behavior = 9  # High satisfaction
        local_economy = 8  # Affluent area
        marketability = 8  # Demand for upscale dining
        accessibility = 5  # Parking, easy to find
        competition = 7  # Higher competition
    else:
        consumer_behavior = 6
        local_economy = 6
        marketability = 6
        accessibility = 6
        competition = 6

    score = (
        consumer_behavior * weights["Consumer Behavior"] +
        local_economy * weights["Local Economy"] +
        marketability * weights["Marketability"] +
        accessibility * weights["Accessibility"] +
        competition * weights["Competition"]
    )
    return score

def search_toronto_locations(query, api_key=GOOGLE_MAPS_API_KEY, location="Toronto, Ontario"):
    """Searches for locations in Toronto that match a query using the Google Maps API."""
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query + " in " + location,
        'key': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        results = response.json()

        if results['status'] == 'OK':
            return results['results']
        else:
            print(f"Error: {results['status']} - {results.get('error_message', 'No error message')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# Set search query dynamically based on the determined portfolio
if dominant_portfolio == "Busy Lunchtime Professional":
    search_query = "Quick Service Restaurant near office buildings"
elif dominant_portfolio == "Relaxed Dinner Guest":
    search_query = "Upscale Restaurant with parking"  #
else:
    search_query = "Restaurant in a busy area"

# Fetch potential locations in Toronto
potential_locations = search_toronto_locations(search_query)

# Rank locations
ranked_locations = []
for location in potential_locations:
    location_name = location['name']
    location_address = location['formatted_address']
    score = get_location_score(location, dominant_portfolio)  # Pass portfolio to scoring
    ranked_locations.append((location_name, location_address, score))

ranked_locations.sort(key=lambda x: x[2], reverse=True)  # Sort by score (highest first)

# Output Top Potential Locations
print("\nTop Potential Expansion Locations in Toronto (Theoretical Ranking):")
for name, address, score in ranked_locations[:5]:  # Show top 5
    print(f"- {name}: {address} (Score: {score:.2f})")

print("\nGeneral Expansion Tips:")
if dominant_portfolio == "Busy Lunchtime Professional":
    print("- Focus on areas with high foot traffic during lunchtime (near office buildings, transit hubs).")
    print("- Optimize for quick service and takeout options.")
    print("- Consider offering affordable lunch specials to attract price-sensitive customers.")
elif dominant_portfolio == "Relaxed Dinner Guest":
    print("- Look for locations in affluent areas with ample parking.")
    print("- Focus on creating a relaxed and upscale dining atmosphere.")
    print("- Develop a menu with high-quality ingredients and creative dishes.")
else:
    print("- This location can be anywhere with good traffic")


