import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error

def train_model(data_path='international_housing_data.csv', model_path='house_price_model.pkl'):
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Please run data_generator.py first.")
        
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    
    # Define features and target
    features = [
        'City', 'PropertyType', 'Area_sqm', 'Bedrooms', 'Bathrooms', 
        'Age_years', 'Distance_to_Center_km', 'Has_Garden', 'Has_Parking', 'Furnished'
    ]
    target = 'Price_USD'
    
    X = df[features]
    y = df[target]
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Define preprocessing for numerical and categorical features
    numerical_features = ['Area_sqm', 'Bedrooms', 'Bathrooms', 'Age_years', 'Distance_to_Center_km']
    categorical_features = ['City', 'PropertyType', 'Has_Garden', 'Has_Parking', 'Furnished']
    
    numerical_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )
    
    # Define the model pipeline
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42))
    ])
    
    # Train the model
    print("Training Random Forest Regressor...")
    model_pipeline.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model_pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    
    print("\nModel Evaluation Metrics (Test Set):")
    print(f"R-squared (R2) Score : {r2:.4f}")
    print(f"Mean Absolute Error (MAE): ${mae:.2f} USD")
    print(f"Root Mean Squared Error (RMSE): ${rmse:.2f} USD")
    
    # Save the pipeline
    with open(model_path, 'wb') as f:
        pickle.dump(model_pipeline, f)
        
    print(f"\nModel pipeline successfully saved to: {os.path.abspath(model_path)}")

if __name__ == '__main__':
    train_model()
