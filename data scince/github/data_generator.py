import pandas as pd
import numpy as np
import os

# Set seed for reproducibility
np.random.seed(42)

def generate_housing_data(num_records=1200):
    cities = ['New York', 'London', 'Tokyo', 'Paris', 'Mumbai', 'Sydney']
    property_types = ['Apartment', 'House', 'Penthouse']
    furnishing_statuses = ['Fully', 'Partially', 'Unfurnished']
    
    # Base price per square meter in USD
    city_base_prices = {
        'New York': 12000,
        'London': 11000,
        'Tokyo': 9000,
        'Paris': 10000,
        'Mumbai': 4000,
        'Sydney': 8500
    }
    
    # Currency details: (Currency Code, 1 USD = X local units)
    currencies = {
        'New York': ('USD', 1.0),
        'London': ('GBP', 0.8),
        'Tokyo': ('JPY', 150.0),
        'Paris': ('EUR', 0.92),
        'Mumbai': ('INR', 83.5),
        'Sydney': ('AUD', 1.5)
    }

    data = []
    
    for i in range(num_records):
        city = np.random.choice(cities)
        prop_type = np.random.choice(property_types, p=[0.5, 0.4, 0.1])
        
        # Area in square meters (houses are larger on average)
        if prop_type == 'House':
            area = np.random.normal(200, 70)
            area = max(50, min(area, 600))
        elif prop_type == 'Penthouse':
            area = np.random.normal(180, 50)
            area = max(80, min(area, 400))
        else: # Apartment
            area = np.random.normal(85, 30)
            area = max(25, min(area, 250))
            
        # Round area to 1 decimal place
        area = round(area, 1)
        
        # Bedrooms and Bathrooms based on area and type
        bedrooms = int(max(1, min(5, np.round(area / 45 + np.random.uniform(-0.5, 1)))))
        bathrooms = int(max(1, min(4, np.round(bedrooms * 0.7 + np.random.uniform(-0.3, 0.7)))))
        
        # Age of the property (new properties have 0 age)
        age = int(max(0, np.random.exponential(15)))
        age = min(100, age) # Cap age at 100
        
        # Distance to city center in km
        if prop_type == 'Apartment':
            dist = np.random.exponential(5)
        elif prop_type == 'Penthouse':
            dist = np.random.exponential(3)
        else: # House
            dist = np.random.exponential(12)
        dist = round(max(0.1, min(40, dist)), 2)
        
        # Binary features
        has_garden = (prop_type == 'House') or (np.random.rand() > 0.85)
        has_parking = np.random.rand() > 0.4
        furnished = np.random.choice(furnishing_statuses, p=[0.3, 0.4, 0.3])
        
        # Price Calculation logic
        base_price_sqm = city_base_prices[city]
        
        # Start with area-based cost
        price_usd = area * base_price_sqm
        
        # Modifiers
        # 1. Property Type
        type_mult = {'Apartment': 1.0, 'House': 1.15, 'Penthouse': 1.5}
        price_usd *= type_mult[prop_type]
        
        # 2. Distance to City Center (Exponential Decay)
        dist_factor = np.exp(-0.03 * dist) # price drops 3% per km from center
        price_usd *= dist_factor
        
        # 3. Rooms
        price_usd *= (1.0 + 0.05 * (bedrooms - 1)) # 5% per additional bedroom
        price_usd *= (1.0 + 0.07 * (bathrooms - 1)) # 7% per additional bathroom
        
        # 4. Age of building (0.5% depreciation per year, max 40% drop)
        age_depr = max(0.6, 1.0 - (0.005 * age))
        price_usd *= age_depr
        
        # 5. Features
        if has_garden:
            price_usd *= 1.08 # +8% for garden
        if has_parking:
            price_usd *= 1.05 # +5% for parking
            
        furn_mult = {'Fully': 1.07, 'Partially': 1.03, 'Unfurnished': 1.0}
        price_usd *= furn_mult[furnished]
        
        # 6. Market Noise (random fluctuation)
        noise = np.random.normal(1.0, 0.08) # 8% standard deviation noise
        price_usd *= noise
        
        price_usd = round(price_usd, 2)
        
        # Currency conversion
        curr_code, ex_rate = currencies[city]
        price_local = round(price_usd * ex_rate, 2)
        
        data.append({
            'PropertyID': f'PROP_{i+1:05d}',
            'City': city,
            'PropertyType': prop_type,
            'Area_sqm': area,
            'Bedrooms': bedrooms,
            'Bathrooms': bathrooms,
            'Age_years': age,
            'Distance_to_Center_km': dist,
            'Has_Garden': int(has_garden),
            'Has_Parking': int(has_parking),
            'Furnished': furnished,
            'Price_USD': price_usd,
            'LocalCurrency': curr_code,
            'ExchangeRate_to_USD': ex_rate,
            'Price_Local': price_local
        })
        
    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    print("Generating synthetic international housing dataset...")
    df = generate_housing_data()
    output_path = 'international_housing_data.csv'
    df.to_csv(output_path, index=False)
    print(f"Dataset generated and saved to: {os.path.abspath(output_path)}")
    print(f"Total records generated: {len(df)}")
    print("\nDataset Sample:")
    print(df.head())
