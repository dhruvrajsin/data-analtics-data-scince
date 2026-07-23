import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error

# Set design styles for plots
sns.set_theme(style="darkgrid")
plt.rcParams.update({
    'figure.facecolor': '#111125',
    'axes.facecolor': '#181832',
    'text.color': '#FFFFFF',
    'axes.labelcolor': '#E2E8F0',
    'xtick.color': '#A0AEC0',
    'ytick.color': '#A0AEC0',
    'grid.color': '#2D3748',
    'font.family': 'sans-serif'
})

DATA_FILE = 'international_housing_data.csv'
MODEL_FILE = 'house_price_model.pkl'
PLOTS_DIR = 'plots'

# Ensure dataset exists
if not os.path.exists(DATA_FILE):
    print("Dataset not found. Running data generator...")
    from data_generator import generate_housing_data
    df = generate_housing_data()
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)

print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# 1. Feature Engineering
print("Performing feature engineering...")
df['Area_Per_Bedroom'] = df['Area_sqm'] / df['Bedrooms']
df['Distance_Age_Interaction'] = df['Distance_to_Center_km'] * df['Age_years']

# Define target and feature columns
features = [
    'City', 'PropertyType', 'Area_sqm', 'Bedrooms', 'Bathrooms', 
    'Age_years', 'Distance_to_Center_km', 'Has_Garden', 'Has_Parking', 
    'Furnished', 'Area_Per_Bedroom', 'Distance_Age_Interaction'
]
target = 'Price_USD'

X = df[features]
y = df[target]

# Train-Test Split (80% Train, 20% Holdout Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples\n")

# 2. Preprocessing Pipeline
numeric_features = ['Area_sqm', 'Bedrooms', 'Bathrooms', 'Age_years', 'Distance_to_Center_km', 'Area_Per_Bedroom', 'Distance_Age_Interaction']
categorical_features = ['City', 'PropertyType', 'Has_Garden', 'Has_Parking', 'Furnished']

numerical_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# 3. Model Definition (Comparing 2 Ensemble Models)
# We wrap them in TransformedTargetRegressor to apply log(y+1) target transformation automatically.
model_rf = TransformedTargetRegressor(
    regressor=RandomForestRegressor(random_state=42),
    func=np.log1p,
    inverse_func=np.expm1
)

model_gbr = TransformedTargetRegressor(
    regressor=GradientBoostingRegressor(random_state=42),
    func=np.log1p,
    inverse_func=np.expm1
)

models = {
    'Random Forest Regressor': model_rf,
    'Gradient Boosting Regressor': model_gbr
}

# 4. Model Evaluation & Comparison
results = {}
kf = KFold(n_splits=5, shuffle=True, random_state=42)

print("="*60)
print("Evaluating Models via 5-Fold Cross Validation & Test Set Holdout:")
print("="*60)

best_model_name = None
best_model_r2 = -float('inf')
best_pipeline = None

for name, model_pipeline_wrapper in models.items():
    # Build complete pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model_pipeline_wrapper)
    ])
    
    # 5-Fold Cross Validation (using R2 score)
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=kf, scoring='r2')
    
    # Fit model on training set
    pipeline.fit(X_train, y_train)
    
    # Predict on holdout test set
    y_pred = pipeline.predict(X_test)
    
    # Test set evaluation metrics
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    
    results[name] = {
        'CV Mean R2': cv_scores.mean(),
        'CV Std R2': cv_scores.std(),
        'Test R2': r2,
        'Test MAE': mae,
        'Test RMSE': rmse,
        'Test MAPE (%)': mape,
        'pipeline': pipeline
    }
    
    print(f"\n--- {name} ---")
    print(f"Cross-Validation R2 Score : {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
    print(f"Test Holdout R2 Score     : {r2:.4f}")
    print(f"Mean Absolute Error (MAE) : ${mae:,.2f} USD")
    print(f"Root Mean Squared Error   : ${rmse:,.2f} USD")
    print(f"Mean Abs Pct Error (MAPE) : {mape:.2f}%")
    
    # Identify best pipeline based on Test R2
    if r2 > best_model_r2:
        best_model_r2 = r2
        best_model_name = name
        best_pipeline = pipeline

print("\n" + "="*60)
print(f"WINNER MODEL: {best_model_name} (Test R2: {best_model_r2:.4f})")
print("="*60 + "\n")

# 5. Hyperparameter Tuning of the Winner Model
print(f"Tuning hyperparameters for {best_model_name} using GridSearchCV...")

if 'Random Forest' in best_model_name:
    param_grid = {
        'model__regressor__n_estimators': [100, 150, 200],
        'model__regressor__max_depth': [8, 12, 16],
        'model__regressor__min_samples_split': [2, 5]
    }
else: # Gradient Boosting
    param_grid = {
        'model__regressor__n_estimators': [100, 150, 200],
        'model__regressor__max_depth': [3, 5, 7],
        'model__regressor__learning_rate': [0.05, 0.1, 0.15]
    }

grid_search = GridSearchCV(best_pipeline, param_grid, cv=3, scoring='r2', n_jobs=-1)
grid_search.fit(X_train, y_train)

best_tuned_pipeline = grid_search.best_estimator_
tuned_y_pred = best_tuned_pipeline.predict(X_test)

tuned_r2 = r2_score(y_test, tuned_y_pred)
tuned_mae = mean_absolute_error(y_test, tuned_y_pred)
tuned_rmse = root_mean_squared_error(y_test, tuned_y_pred)
tuned_mape = np.mean(np.abs((y_test - tuned_y_pred) / y_test)) * 100

print(f"\nBest Parameters Found: {grid_search.best_params_}")
print(f"Tuned Test R2 Score: {tuned_r2:.4f} (Improved from {best_model_r2:.4f})")
print(f"Tuned Test MAE: ${tuned_mae:,.2f} USD")
print(f"Tuned Test RMSE: ${tuned_rmse:,.2f} USD")

# 6. Save the Tuned Winning Model Pipeline
with open(MODEL_FILE, 'wb') as f:
    pickle.dump(best_tuned_pipeline, f)
print(f"\nSaved tuned model pipeline to: {os.path.abspath(MODEL_FILE)}")

# 7. Generate Diagnostic Visualizations
os.makedirs(PLOTS_DIR, exist_ok=True)
print(f"Saving diagnostic visualizations to folder: '{PLOTS_DIR}'...")

# Chart 1: Actual vs Predicted
plt.figure(figsize=(8, 6))
plt.scatter(y_test, tuned_y_pred, alpha=0.5, color='#A855F7', edgecolors='k')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.title(f'{best_model_name} - Actual vs Predicted Prices', fontsize=14, pad=15)
plt.xlabel('Actual Price (USD)', fontsize=12)
plt.ylabel('Predicted Price (USD)', fontsize=12)
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'actual_vs_predicted.png'), dpi=150, facecolor='#111125')
plt.close()

# Chart 2: Residuals Distribution
plt.figure(figsize=(8, 6))
residuals = y_test - tuned_y_pred
sns.histplot(residuals, kde=True, color='#6366F1', bins=30, edgecolor='w')
plt.axvline(x=0, color='red', linestyle='--', lw=2)
plt.title('Distribution of Model Prediction Residuals (Errors)', fontsize=14, pad=15)
plt.xlabel('Residual (Actual - Predicted Price in USD)', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'residuals_distribution.png'), dpi=150, facecolor='#111125')
plt.close()

# Chart 3: Feature Importances
plt.figure(figsize=(10, 6))
# Get feature names after one-hot encoding
cat_encoder = best_tuned_pipeline.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot']
cat_feature_names = cat_encoder.get_feature_names_out(categorical_features).tolist()
all_features_names = numeric_features + cat_feature_names

# Get model importances from TransformedTargetRegressor
raw_regressor = best_tuned_pipeline.named_steps['model'].regressor_
importances = raw_regressor.feature_importances_

feat_imp_df = pd.DataFrame({
    'Feature': all_features_names,
    'Importance': importances
}).sort_values(by='Importance', ascending=False).head(10)

sns.barplot(data=feat_imp_df, x='Importance', y='Feature', hue='Feature', palette='plasma', legend=False)
plt.title('Top 10 Most Influential Features (Feature Importance)', fontsize=14, pad=15)
plt.xlabel('Relative Importance Value', fontsize=12)
plt.ylabel('Feature Name', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'feature_importance.png'), dpi=150, facecolor='#111125')
plt.close()

print("Visualizations created and saved successfully.")
print("\nData Science pipeline run completed successfully!")
