import pandas as pd
import numpy as np
import json
import os

def profile_dataset(data_path='international_housing_data.csv', report_path='data_profile_report.json'):
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Please run data_generator.py first.")
        
    print(f"Profiling dataset: {data_path}...")
    df = pd.read_csv(data_path)
    
    # 1. Dataset Overview
    overview = {
        'total_rows': int(df.shape[0]),
        'total_columns': int(df.shape[1]),
        'memory_usage_kb': round(df.memory_usage(deep=True).sum() / 1024, 2),
        'missing_values': df.isnull().sum().to_dict(),
        'column_types': {col: str(dtype) for col, dtype in df.dtypes.items()}
    }
    
    # 2. Numerical Features Profiling
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    num_profile = {}
    for col in num_cols:
        num_profile[col] = {
            'count': int(df[col].count()),
            'mean': float(df[col].mean()),
            'std': float(df[col].std()),
            'min': float(df[col].min()),
            'q25': float(df[col].quantile(0.25)),
            'median': float(df[col].median()),
            'q75': float(df[col].quantile(0.75)),
            'max': float(df[col].max()),
            'skew': float(df[col].skew())
        }
        
    # 3. Categorical Features Profiling
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    cat_profile = {}
    for col in cat_cols:
        value_counts = df[col].value_counts()
        total = len(df[col])
        cat_profile[col] = {
            'unique_count': int(df[col].nunique()),
            'top_value': str(value_counts.index[0]),
            'top_frequency': int(value_counts.iloc[0]),
            'distribution': {str(k): {'count': int(v), 'percentage': round(int(v)/total * 100, 2)} 
                             for k, v in value_counts.items()}
        }
        
    # 4. Correlation Analysis
    # Get numeric columns excluding ID codes if any
    corr_cols = [c for c in num_cols if 'ID' not in c and 'ExchangeRate' not in c]
    corr_matrix = df[corr_cols].corr().round(4).to_dict()
    
    # 5. Business/Insight Profiles
    # Average Price by City
    avg_price_by_city = df.groupby('City')['Price_USD'].mean().round(2).to_dict()
    
    # Average Price by Property Type
    avg_price_by_type = df.groupby('PropertyType')['Price_USD'].mean().round(2).to_dict()
    
    # Price distribution statistics by City
    city_price_stats = {}
    for city, group in df.groupby('City'):
        city_price_stats[city] = {
            'avg_price_usd': float(group['Price_USD'].mean()),
            'avg_area_sqm': float(group['Area_sqm'].mean()),
            'avg_price_per_sqm': float((group['Price_USD'] / group['Area_sqm']).mean()),
            'total_properties': int(group.shape[0])
        }

    report = {
        'overview': overview,
        'numerical_profile': num_profile,
        'categorical_profile': cat_profile,
        'correlation_matrix': corr_matrix,
        'business_insights': {
            'avg_price_by_city': avg_price_by_city,
            'avg_price_by_type': avg_price_by_type,
            'city_price_stats': city_price_stats
        }
    }
    
    # Save report to JSON file
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
        
    print(f"Data profile report saved to: {os.path.abspath(report_path)}")
    return report

if __name__ == '__main__':
    profile_dataset()
