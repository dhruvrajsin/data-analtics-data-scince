# Global Real Estate Prediction & Analytics Dashboard 🌍

An interactive Data Science & Analytics dashboard built using **Python, Scikit-Learn, Plotly, and Streamlit**. It predicts and analyzes residential property values across six major global cities (New York, London, Tokyo, Paris, Mumbai, Sydney).

---

## 🛠️ Project Structure
* `data_generator.py`: Generates realistic multi-city synthetic transaction data.
* `data_profiling.py`: Generates detailed statistical data profiling reports saved in `data_profile_report.json`.
* `model_training.py`: Trains a Random Forest Regressor on numerical and categorical features.
* `app.py`: Streamlit dashboard with Overview, Data Profiler, Price Predictor, and Portfolio tabs.
* `international_housing_data.csv`: The generated housing dataset.
* `house_price_model.pkl`: Serialized machine learning pipeline.
* `data_profile_report.json`: JSON report containing summary statistics.

---

## 🚀 How to Run Locally

### 1. Set Up Virtual Environment
Ensure you are in the project folder and run:
```bash
python -m venv .venv
```

### 2. Activate the Virtual Environment
* **On Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* **On Windows (CMD)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```
* **On macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Required Dependencies
```bash
pip install pandas numpy plotly scikit-learn streamlit seaborn
```

### 4. Run the Pipeline & App
The dashboard `app.py` has automatic fallbacks to generate data, run profiles, and train models if they are missing. However, you can run them manually:
```bash
python data_generator.py
python data_profiling.py
python model_training.py
```

To run the Streamlit dashboard:
```bash
streamlit run app.py
```

---

## 📤 How to Upload this Code to GitHub

Follow these steps to upload your completed code to your repository:

1. **Configure Git details (if not already set)**:
   ```bash
   git config --global user.name "dhruvrajsin"
   git config --global user.email "your-email@example.com"
   ```
2. **Initialize git repository**:
   ```bash
   git init
   ```
3. **Stage and commit files**:
   ```bash
   git add .
   git commit -m "Initialize Global Real Estate Prediction & Analytics Dashboard"
   ```
4. **Link remote repository and push**:
   ```bash
   git remote add origin https://github.com/dhruvrajsin/data-analtics-data-scince.git
   git branch -M main
   git push -u origin main
   ```
