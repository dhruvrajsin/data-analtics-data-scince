import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import pickle
import os

# Set page configuration with a premium title and layout
st.set_page_config(
    page_title="Global Real Estate Analytics & Predictor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design (Gradients, Glassmorphism, Google Fonts)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Premium background and card styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.25);
    }
    
    .metric-label {
        font-size: 14px;
        color: #A0AEC0;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(90deg, #6366F1 0%, #A855F7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-sub {
        font-size: 12px;
        color: #48BB78;
        margin-top: 4px;
        font-weight: 500;
    }
    
    /* Section Headers */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #FFFFFF;
        border-left: 5px solid #6366F1;
        padding-left: 12px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    /* Profile styling */
    .profile-card {
        background: linear-gradient(135deg, #1e1e38 0%, #0f0f23 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .profile-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin: 0 auto 15px auto;
        background: linear-gradient(45deg, #6366F1, #A855F7);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        color: white;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
    }
    
    .profile-name {
        font-size: 24px;
        font-weight: 700;
        color: #fff;
        margin-bottom: 5px;
    }
    
    .profile-role {
        font-size: 16px;
        color: #A855F7;
        font-weight: 600;
        margin-bottom: 15px;
    }
    
    /* Git commands block */
    .git-command {
        background-color: #111;
        border-left: 4px solid #A855F7;
        color: #58a6ff;
        padding: 10px;
        border-radius: 4px;
        font-family: monospace;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA / MODEL LOADING FALLBACKS -----------------
DATA_FILE = 'international_housing_data.csv'
MODEL_FILE = 'house_price_model.pkl'
PROFILE_FILE = 'data_profile_report.json'

@st.cache_data
def check_and_generate_data():
    if not os.path.exists(DATA_FILE):
        st.info("Creating fresh synthetic global housing data...")
        from data_generator import generate_housing_data
        df = generate_housing_data()
        df.to_csv(DATA_FILE, index=False)
    else:
        df = pd.read_csv(DATA_FILE)
    return df

@st.cache_data
def check_and_profile_data():
    if not os.path.exists(PROFILE_FILE):
        st.info("Generating data profile reports...")
        from data_profiling import profile_dataset
        report = profile_dataset()
    else:
        with open(PROFILE_FILE, 'r') as f:
            report = json.load(f)
    return report

def check_and_train_model():
    if not os.path.exists(MODEL_FILE):
        st.info("Training the predictive machine learning model...")
        from model_training import train_model
        train_model()
    
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)
    return model

# Initialize components
try:
    df = check_and_generate_data()
    report = check_and_profile_data()
    model = check_and_train_model()
except Exception as e:
    st.error(f"Error initializing workspace components: {e}")
    st.stop()

# ----------------- SIDEBAR -----------------
st.sidebar.markdown(
    "<div style='text-align: center; padding: 10px;'>"
    "<h2 style='color: #6366F1; margin-bottom: 0;'>Global Estate</h2>"
    "<p style='color: #A0AEC0; font-size: 12px;'>Data Analytics & Prediction Suite</p>"
    "</div>", 
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# Navigation Menu
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Overview & Trends", "📊 Data Profiler & Properties", "🔍 Interactive Analytics Table", "🔮 Price Predictor", "🔬 ML Diagnostics & Science", "👤 Developer Profile & GitHub"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size: 11px; color: #718096;'>"
    "<b>Project Status</b>: Active<br>"
    "<b>Dataset Size</b>: 1,200 records<br>"
    "<b>Target Cities</b>: 6 Global hubs<br>"
    "<b>Algorithms</b>: Random Forest Regressor"
    "</div>", 
    unsafe_allow_html=True
)

# ----------------- MENU TAB 1: OVERVIEW & TRENDS -----------------
if menu == "🏠 Overview & Trends":
    st.markdown("<h1 style='color: white; font-weight: 700;'>🌍 International Real Estate Market Overview</h1>", unsafe_allow_html=True)
    st.write("An interactive analysis of residential properties across six major international hubs.")
    
    st.markdown("<div class='section-title'>Key Market Indicators</div>", unsafe_allow_html=True)
    
    # Custom high-aesthetic metrics row
    total_properties = len(df)
    avg_price_usd = df['Price_USD'].mean()
    avg_price_sqm = (df['Price_USD'] / df['Area_sqm']).mean()
    avg_distance = df['Distance_to_Center_km'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Properties</div>
            <div class="metric-value">{total_properties:,}</div>
            <div class="metric-sub">Across 6 Global Cities</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Property Value</div>
            <div class="metric-value">${avg_price_usd:,.0f}</div>
            <div class="metric-sub">USD valuation</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Price / Sq Meter</div>
            <div class="metric-value">${avg_price_sqm:,.2f}</div>
            <div class="metric-sub">USD per sqm</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Proximity to Center</div>
            <div class="metric-value">{avg_distance:.2f} km</div>
            <div class="metric-sub">Distance from center</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div class='section-title'>Visualizing Price Distributions & Property Types</div>", unsafe_allow_html=True)
    
    plot_col1, plot_col2 = st.columns(2)
    
    with plot_col1:
        # Chart 1: Average Price per Sqm by City
        city_avg = df.groupby('City')['Price_USD'].mean().reset_index().sort_values(by='Price_USD', ascending=False)
        fig_city = px.bar(
            city_avg, 
            x='City', 
            y='Price_USD',
            title='Average Property Price by City (USD)',
            labels={'Price_USD': 'Average Price (USD)', 'City': 'City'},
            color='Price_USD',
            color_continuous_scale=px.colors.sequential.Plasma
        )
        fig_city.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E2E8F0',
            title_font_size=18,
            title_x=0.0
        )
        st.plotly_chart(fig_city, use_container_width=True)
        
    with plot_col2:
        # Chart 2: Property Type Breakdown
        type_counts = df['PropertyType'].value_counts().reset_index()
        type_counts.columns = ['PropertyType', 'Count']
        fig_type = px.pie(
            type_counts, 
            values='Count', 
            names='PropertyType',
            title='Distribution of Property Types',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_type.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E2E8F0',
            title_font_size=18,
            title_x=0.0
        )
        st.plotly_chart(fig_type, use_container_width=True)

    st.markdown("<div class='section-title'>Price vs. Size & Distance from City Center</div>", unsafe_allow_html=True)
    
    # Scatter plot: Price vs Area with City coloring
    fig_scatter = px.scatter(
        df, 
        x='Area_sqm', 
        y='Price_USD', 
        color='City',
        size='Bedrooms',
        hover_data=['PropertyType', 'Distance_to_Center_km'],
        title='Price vs. Area (Sqm) styled by City (Size represents bedrooms)',
        opacity=0.7,
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#E2E8F0',
        title_font_size=18,
        title_x=0.0
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------- MENU TAB 2: DATA PROFILER & PROPERTIES -----------------
elif menu == "📊 Data Profiler & Properties":
    st.markdown("<h1 style='color: white; font-weight: 700;'>📊 Dataset Properties & Profiling</h1>", unsafe_allow_html=True)
    st.write("Detailed metadata, data qualities, correlations, and characteristics of the underlying real estate dataset.")
    
    # Tabs inside profiler
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
        "📋 Dataset Overview", 
        "🔢 Numerical Properties", 
        "🔤 Categorical Distributions", 
        "🔗 Feature Correlations"
    ])
    
    # 1. Overview
    with sub_tab1:
        st.subheader("Global Schema Details")
        col_ov1, col_ov2 = st.columns(2)
        
        with col_ov1:
            st.write("**General Stats:**")
            st.table(pd.DataFrame({
                "Property": [
                    "Total Rows", 
                    "Total Columns", 
                    "Total Memory (KB)", 
                    "File Path"
                ],
                "Value": [
                    report['overview']['total_rows'],
                    report['overview']['total_columns'],
                    f"{report['overview']['memory_usage_kb']} KB",
                    f"d:\\data analytics\\data scince\\github\\{DATA_FILE}"
                ]
            }))
            
        with col_ov2:
            st.write("**Data Types and Missing Values:**")
            types_df = pd.DataFrame({
                "Column Name": list(report['overview']['column_types'].keys()),
                "Data Type": list(report['overview']['column_types'].values()),
                "Null Values": [report['overview']['missing_values'].get(col, 0) for col in report['overview']['column_types'].keys()]
            })
            st.dataframe(types_df, use_container_width=True, hide_index=True)
            
    # 2. Numerical
    with sub_tab2:
        st.subheader("Summary Statistics for Numerical Columns")
        num_df = pd.DataFrame(report['numerical_profile']).T
        st.dataframe(num_df.style.format("{:.2f}"), use_container_width=True)
        
        st.markdown("---")
        # Visual distribution plot
        st.subheader("Interactive Feature Distributions")
        selected_col = st.selectbox("Select column to visualize:", ['Area_sqm', 'Age_years', 'Distance_to_Center_km', 'Price_USD'])
        fig_hist = px.histogram(
            df, 
            x=selected_col, 
            color='City', 
            marginal='box', 
            nbins=35,
            title=f'Distribution of {selected_col}',
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E2E8F0'
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # 3. Categorical
    with sub_tab3:
        st.subheader("Categorical Value Distributions")
        cat_choices = list(report['categorical_profile'].keys())
        selected_cat = st.selectbox("Select categorical feature:", cat_choices)
        
        cat_data = report['categorical_profile'][selected_cat]
        st.write(f"**Total unique categories:** {cat_data['unique_count']}")
        st.write(f"**Top category:** {cat_data['top_value']} (occurs {cat_data['top_frequency']} times)")
        
        # Display distribution table
        dist_df = pd.DataFrame(cat_data['distribution']).T.reset_index()
        dist_df.columns = [selected_cat, 'Record Count', 'Percentage (%)']
        
        col_c1, col_c2 = st.columns([1, 2])
        with col_c1:
            st.dataframe(dist_df, hide_index=True, use_container_width=True)
        with col_c2:
            fig_cat = px.bar(
                dist_df, 
                x=selected_cat, 
                y='Record Count', 
                color='Percentage (%)',
                title=f'Distribution breakdown of {selected_cat}',
                color_continuous_scale='Sunset'
            )
            fig_cat.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#E2E8F0'
            )
            st.plotly_chart(fig_cat, use_container_width=True)
            
    # 4. Correlations
    with sub_tab4:
        st.subheader("Correlation Heatmap")
        st.write("Identifies the linear relationships between numeric properties. A score close to +1 represents strong positive correlation, while -1 represents strong negative correlation.")
        
        corr_matrix_df = pd.DataFrame(report['correlation_matrix'])
        
        # Convert to arrays for Plotly Heatmap
        x_vals = list(corr_matrix_df.columns)
        y_vals = list(corr_matrix_df.index)
        z_vals = corr_matrix_df.values
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=z_vals,
            x=x_vals,
            y=y_vals,
            colorscale='RdBu',
            zmin=-1,
            zmax=1,
            text=np.round(z_vals, 2),
            texttemplate="%{text}",
            hoverongaps = False
        ))
        fig_heat.update_layout(
            title='Feature Correlation Matrix',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E2E8F0',
            width=700,
            height=500
        )
        st.plotly_chart(fig_heat, use_container_width=True)

# ----------------- MENU TAB 3: INTERACTIVE ANALYTICS TABLE -----------------
elif menu == "🔍 Interactive Analytics Table":
    st.markdown("<h1 style='color: white; font-weight: 700;'>🔍 Interactive Data Analytics Table</h1>", unsafe_allow_html=True)
    st.write("Explore, filter, search, and export the real estate dataset using advanced features.")
    
    # Collapsible filter expander
    with st.expander("🛠️ Advanced Search & Filter Options", expanded=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            search_query = st.text_input("🔍 Search by Property ID", placeholder="e.g. PROP_00042").strip()
            
            cities_list = sorted(df['City'].unique())
            selected_cities = st.multiselect("Filter by City", cities_list, default=cities_list)
            
            types_list = sorted(df['PropertyType'].unique())
            selected_types = st.multiselect("Filter by Property Type", types_list, default=types_list)
            
        with col_f2:
            min_price = float(df['Price_USD'].min())
            max_price = float(df['Price_USD'].max())
            selected_price_range = st.slider(
                "Price Range (USD)", 
                min_value=min_price, 
                max_value=max_price, 
                value=(min_price, max_price),
                format="$%,.0f"
            )
            
            min_area = float(df['Area_sqm'].min())
            max_area = float(df['Area_sqm'].max())
            selected_area_range = st.slider(
                "Area Range (m²)", 
                min_value=min_area, 
                max_value=max_area, 
                value=(min_area, max_area),
                format="%.0f m²"
            )
            
        with col_f3:
            furnishing_list = sorted(df['Furnished'].unique())
            selected_furnishing = st.multiselect("Filter by Furnishing", furnishing_list, default=furnishing_list)
            
            min_dist = float(df['Distance_to_Center_km'].min())
            max_dist = float(df['Distance_to_Center_km'].max())
            selected_dist_range = st.slider(
                "Distance to Center (km)", 
                min_value=min_dist, 
                max_value=max_dist, 
                value=(min_dist, max_dist),
                format="%.1f km"
            )
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                garden_filter = st.selectbox("Garden Option", ["All", "Has Garden", "No Garden"])
            with col_b2:
                parking_filter = st.selectbox("Parking Option", ["All", "Has Parking", "No Parking"])

    # Filtering logic
    filtered_df = df.copy()
    
    if search_query:
        filtered_df = filtered_df[filtered_df['PropertyID'].str.contains(search_query, case=False, na=False)]
        
    if selected_cities:
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]
    else:
        filtered_df = filtered_df.iloc[0:0] # empty dataframe if no city selected
        
    if selected_types:
        filtered_df = filtered_df[filtered_df['PropertyType'].isin(selected_types)]
    else:
        filtered_df = filtered_df.iloc[0:0]
        
    if selected_furnishing:
        filtered_df = filtered_df[filtered_df['Furnished'].isin(selected_furnishing)]
    else:
        filtered_df = filtered_df.iloc[0:0]
        
    filtered_df = filtered_df[
        (filtered_df['Price_USD'] >= selected_price_range[0]) & 
        (filtered_df['Price_USD'] <= selected_price_range[1])
    ]
    
    filtered_df = filtered_df[
        (filtered_df['Area_sqm'] >= selected_area_range[0]) & 
        (filtered_df['Area_sqm'] <= selected_area_range[1])
    ]
    
    filtered_df = filtered_df[
        (filtered_df['Distance_to_Center_km'] >= selected_dist_range[0]) & 
        (filtered_df['Distance_to_Center_km'] <= selected_dist_range[1])
    ]
    
    if garden_filter == "Has Garden":
        filtered_df = filtered_df[filtered_df['Has_Garden'] == 1]
    elif garden_filter == "No Garden":
        filtered_df = filtered_df[filtered_df['Has_Garden'] == 0]
        
    if parking_filter == "Has Parking":
        filtered_df = filtered_df[filtered_df['Has_Parking'] == 1]
    elif parking_filter == "No Parking":
        filtered_df = filtered_df[filtered_df['Has_Parking'] == 0]

    # Metrics Section
    st.markdown("<div class='section-title'>Filtered Insights Summary</div>", unsafe_allow_html=True)
    
    match_count = len(filtered_df)
    pct_match = (match_count / len(df)) * 100
    
    if match_count > 0:
        avg_price = filtered_df['Price_USD'].mean()
        avg_price_sqm = (filtered_df['Price_USD'] / filtered_df['Area_sqm']).mean()
        avg_age = filtered_df['Age_years'].mean()
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Matching Properties</div>
                <div class="metric-value">{match_count:,}</div>
                <div class="metric-sub">{pct_match:.1f}% of total dataset</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Filtered Price</div>
                <div class="metric-value">${avg_price:,.0f}</div>
                <div class="metric-sub">USD Valuation</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Price / Sqm</div>
                <div class="metric-value">${avg_price_sqm:,.2f}</div>
                <div class="metric-sub">USD per sqm</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Property Age</div>
                <div class="metric-value">{avg_age:.1f} Yrs</div>
                <div class="metric-sub">Average age in years</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No properties match your current filter selections. Please expand your filters.")

    # Table section
    st.markdown("<div class='section-title'>Data Analytics Explorer Table</div>", unsafe_allow_html=True)
    
    if match_count > 0:
        # Download button
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Filtered Data as CSV",
            data=csv_data,
            file_name="filtered_housing_analytics.csv",
            mime="text/csv",
            key="download-csv"
        )
        
        # Display table
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "PropertyID": st.column_config.TextColumn("Property ID", help="Unique property ID code"),
                "City": st.column_config.TextColumn("City"),
                "PropertyType": st.column_config.TextColumn("Property Type"),
                "Area_sqm": st.column_config.NumberColumn("Area (m²)", format="%.1f m²"),
                "Bedrooms": st.column_config.NumberColumn("Bedrooms"),
                "Bathrooms": st.column_config.NumberColumn("Bathrooms"),
                "Age_years": st.column_config.NumberColumn("Age", format="%d yrs"),
                "Distance_to_Center_km": st.column_config.NumberColumn("Distance (km)", format="%.2f km"),
                "Has_Garden": st.column_config.CheckboxColumn("Garden"),
                "Has_Parking": st.column_config.CheckboxColumn("Parking"),
                "Furnished": st.column_config.TextColumn("Furnishing"),
                "Price_USD": st.column_config.NumberColumn("Price (USD)", format="$%,.2f"),
                "LocalCurrency": st.column_config.TextColumn("Local Currency"),
                "ExchangeRate_to_USD": st.column_config.NumberColumn("Exch. Rate"),
                "Price_Local": st.column_config.NumberColumn("Price (Local)", format="%,.2f")
            }
        )
        
        # Filtered Analytics Visualizations
        st.markdown("<div class='section-title'>Filtered Insights Visualizations</div>", unsafe_allow_html=True)
        plot_fcol1, plot_fcol2 = st.columns(2)
        
        with plot_fcol1:
            fig_fprice = px.histogram(
                filtered_df,
                x='Price_USD',
                title='Price Distribution of Filtered Results',
                labels={'Price_USD': 'Price (USD)'},
                color_discrete_sequence=['#A855F7']
            )
            fig_fprice.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#E2E8F0',
                title_font_size=16,
                title_x=0.0
            )
            st.plotly_chart(fig_fprice, use_container_width=True)
            
        with plot_fcol2:
            fig_fdist = px.scatter(
                filtered_df,
                x='Distance_to_Center_km',
                y='Price_USD',
                color='City',
                size='Area_sqm',
                title='Price vs. Center Distance (Size indicates Area)',
                labels={'Distance_to_Center_km': 'Distance from Center (km)', 'Price_USD': 'Price (USD)'},
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_fdist.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#E2E8F0',
                title_font_size=16,
                title_x=0.0
            )
            st.plotly_chart(fig_fdist, use_container_width=True)
    else:
        st.info("Visualizations and export options will appear when there is data matching the filter criteria.")

# ----------------- MENU TAB 4: PRICE PREDICTOR -----------------
elif menu == "🔮 Price Predictor":
    st.markdown("<h1 style='color: white; font-weight: 700;'>🔮 Global Property Price Predictor</h1>", unsafe_allow_html=True)
    st.write("Input property parameters to calculate the estimated price based on our trained Random Forest Regression model.")
    
    st.markdown("---")
    
    # Define form and inputs
    col_in1, col_in2 = st.columns([2, 1.5])
    
    # Currency conversions definition
    currencies = {
        'New York': ('USD', 1.0, '$'),
        'London': ('GBP', 0.8, '£'),
        'Tokyo': ('JPY', 150.0, '¥'),
        'Paris': ('EUR', 0.92, '€'),
        'Mumbai': ('INR', 83.5, '₹'),
        'Sydney': ('AUD', 1.5, 'A$')
    }
    
    with col_in1:
        st.markdown("<div class='section-title'>Property Details</div>", unsafe_allow_html=True)
        
        # Input widgets
        city_val = st.selectbox("City Location", list(currencies.keys()))
        prop_type_val = st.radio("Property Type", ['Apartment', 'House', 'Penthouse'], horizontal=True)
        
        area_val = st.slider("Total Area (Square Meters)", min_value=25, max_value=600, value=120, step=5)
        
        c_bed, c_bath = st.columns(2)
        with c_bed:
            bedrooms_val = st.number_input("Bedrooms", min_value=1, max_value=5, value=2, step=1)
        with c_bath:
            bathrooms_val = st.number_input("Bathrooms", min_value=1, max_value=4, value=2, step=1)
            
        c_age, c_dist = st.columns(2)
        with c_age:
            age_val = st.number_input("Property Age (Years)", min_value=0, max_value=100, value=5, step=1)
        with c_dist:
            dist_val = st.slider("Distance to City Center (km)", min_value=0.1, max_value=40.0, value=5.0, step=0.5)
            
        furnished_val = st.selectbox("Furnishing Level", ['Fully', 'Partially', 'Unfurnished'])
        
        c_gard, c_park = st.columns(2)
        with c_gard:
            has_garden_val = st.checkbox("Includes Private Garden", value=False)
        with c_park:
            has_parking_val = st.checkbox("Includes Private Parking Space", value=True)
            
    with col_in2:
        st.markdown("<div class='section-title'>Valuation Prediction</div>", unsafe_allow_html=True)
        st.write("Click below to compute the estimated market value of the described property using the trained Machine Learning pipeline.")
        
        if st.button("Predict Property Price", type="primary", use_container_width=True):
            # Formulate the input DataFrame matching trained pipeline
            input_df = pd.DataFrame([{
                'City': city_val,
                'PropertyType': prop_type_val,
                'Area_sqm': float(area_val),
                'Bedrooms': int(bedrooms_val),
                'Bathrooms': int(bathrooms_val),
                'Age_years': int(age_val),
                'Distance_to_Center_km': float(dist_val),
                'Has_Garden': int(has_garden_val),
                'Has_Parking': int(has_parking_val),
                'Furnished': furnished_val
            }])
            
            # Run prediction
            predicted_usd = model.predict(input_df)[0]
            
            # Conversion
            curr_code, rate, symbol = currencies[city_val]
            predicted_local = predicted_usd * rate
            
            # Display results in beautiful gradient card
            st.markdown(f"""
            <div class="profile-card" style="margin-top: 20px;">
                <div style="font-size: 16px; color: #A0AEC0; font-weight: 600; text-transform: uppercase;">Estimated Value (USD)</div>
                <div style="font-size: 40px; font-weight: 800; background: linear-gradient(90deg, #6366F1 0%, #A855F7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 15px;">
                    ${predicted_usd:,.2f}
                </div>
                <hr style="border-top: 1px solid rgba(255,255,255,0.1); margin: 15px 0;">
                <div style="font-size: 14px; color: #A0AEC0; font-weight: 600; text-transform: uppercase;">Estimated Value (Local Currency)</div>
                <div style="font-size: 32px; font-weight: 700; color: #48BB78; margin-top: 5px;">
                    {symbol} {predicted_local:,.2f} {curr_code}
                </div>
                <div style="font-size: 11px; color: #718096; margin-top: 10px;">
                    Exchange rate model basis: 1 USD = {rate:.2f} {curr_code}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("Prediction complete! Features processed successfully through scaling and one-hot encoding pipelines.")
        else:
            # Welcome message before click
            st.info("Adjust the property details on the left, then click 'Predict Property Price' to fetch ML valuation details.")

# ----------------- MENU TAB 5: ML DIAGNOSTICS & SCIENCE -----------------
elif menu == "🔬 ML Diagnostics & Science":
    st.markdown("<h1 style='color: white; font-weight: 700;'>🔬 Machine Learning Diagnostics & Model Science</h1>", unsafe_allow_html=True)
    st.write("Analyze the backend model training metrics, performance logs, feature importance, and diagnostic predictions.")
    
    st.markdown("---")
    
    col_d1, col_d2 = st.columns([1.5, 1])
    
    with col_d1:
        st.markdown("<div class='section-title'>Model Comparison (5-Fold Cross Validation)</div>", unsafe_allow_html=True)
        st.write("Both ensemble models were trained on 80% of the dataset (960 records) and evaluated on a 20% holdout set (240 records). Prices were log-transformed during training to handle skewness.")
        
        # Comparative DataFrame
        comparison_data = {
            "Metric Name": [
                "Cross-Validation R² Mean",
                "Cross-Validation R² Std Dev",
                "Holdout Test R² Score",
                "Mean Absolute Error (MAE)",
                "Root Mean Squared Error (RMSE)",
                "Mean Absolute Percentage Error"
            ],
            "Random Forest Regressor": [
                "0.9353", "±0.0097", "0.9447", "$191,619.71 USD", "$324,501.09 USD", "11.86%"
            ],
            "Gradient Boosting Regressor": [
                "0.9590", "±0.0149", "0.9620", "$151,550.20 USD", "$268,805.51 USD", "9.81%"
            ]
        }
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
    with col_d2:
        st.markdown("<div class='section-title'>Optimized Winner Model</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="profile-card" style="text-align: left; padding: 20px;">
            <div style="font-size: 14px; color: #A0AEC0; font-weight: 600; text-transform: uppercase;">Winning Model</div>
            <div style="font-size: 24px; font-weight: 700; color: #48BB78; margin-top: 5px; margin-bottom: 10px;">
                Gradient Boosting Regressor
            </div>
            <b style="color: #6366F1;">Tuned Hyperparameters (GridSearch):</b><br>
            • <code>learning_rate</code>: 0.15<br>
            • <code>max_depth</code>: 3<br>
            • <code>n_estimators</code>: 200<br>
            <hr style="border-top: 1px solid rgba(255,255,255,0.1); margin: 12px 0;">
            <b style="color: #A855F7;">Optimized Performance:</b><br>
            • <b>Holdout Test R²</b>: <span style="color:#FFF;">0.9706</span><br>
            • <b>MAE (Tuned)</b>: <span style="color:#FFF;">$140,300.84 USD</span><br>
            • <b>RMSE (Tuned)</b>: <span style="color:#FFF;">$236,713.31 USD</span>
        </div>
        """, unsafe_allow_html=True)

    # Visualizations section
    st.markdown("<div class='section-title'>Model Diagnostic Charts</div>", unsafe_allow_html=True)
    
    plot_col1, plot_col2 = st.columns(2)
    
    with plot_col1:
        if os.path.exists("plots/feature_importance.png"):
            st.image("plots/feature_importance.png", caption="Feature Importance Analysis (Top 10 predictors)", use_container_width=True)
        else:
            st.warning("⚠️ Feature importance chart not found. Please run the training pipeline.")
            
    with plot_col2:
        if os.path.exists("plots/actual_vs_predicted.png"):
            st.image("plots/actual_vs_predicted.png", caption="Actual Prices vs Predicted Prices fit", use_container_width=True)
        else:
            st.warning("⚠️ Actual vs. Predicted chart not found. Please run the training pipeline.")
            
    st.markdown("---")
    
    # Residuals distribution (Errors)
    col_res1, col_res2 = st.columns([1, 1.5])
    with col_res1:
        st.subheader("Residuals Diagnostics")
        st.write(r"""
        The residuals represent the difference between the actual selling price and the price predicted by the Gradient Boosting model (\(y - \hat{y}\)).
        
        * **Zero Center**: A residual model centered at $0 indicates unbiased predictions.
        * **Normal Distribution**: Errors display a bell-shaped normal curve, indicating that the prediction noise is random.
        * **Variance Stability**: Homoscedasticity of errors supports the model's reliability across low and high valuation bands.
        """)
    with col_res2:
        if os.path.exists("plots/residuals_distribution.png"):
            st.image("plots/residuals_distribution.png", caption="Distribution of Prediction Residuals (Errors)", use_container_width=True)
        else:
            st.warning("⚠️ Residuals distribution chart not found. Please run the training pipeline.")

    # Retrain pipeline section
    st.markdown("<div class='section-title'>Model Retraining Pipeline Control</div>", unsafe_allow_html=True)
    
    st.info("💡 **Retraining Info**: Clicking below runs the full backend training script `ds_pipeline.py` inside the virtual environment. It performs 5-fold cross-validation, checks model R² scores, performs hyperparameter grid search, rewrites `house_price_model.pkl`, and regenerates all three diagnostic charts.")
    
    if st.button("🔄 Retrain ML Pipeline", type="primary", use_container_width=True):
        with st.spinner("Executing model retraining and grid search optimization (approx. 10 seconds)..."):
            import subprocess
            try:
                # Run the backend training script using virtual env python
                run_res = subprocess.run(
                    [".venv/Scripts/python.exe", "ds_pipeline.py"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                st.success("ML Pipeline retrained successfully! Model and plots updated.")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Error executing retraining script: {e}")
                if 'run_res' in locals():
                    st.code(run_res.stderr)

# ----------------- MENU TAB 4: DEVELOPER PROFILE & GITHUB -----------------
elif menu == "👤 Developer Profile & GitHub":
    st.markdown("<h1 style='color: white; font-weight: 700;'>👤 Professional Profile & GitHub Repository</h1>", unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns([1, 2])
    
    with col_p1:
        # Developer profile card
        st.markdown("""
        <div class="profile-card">
            <div class="profile-avatar">👨‍💻</div>
            <div class="profile-name">dhruvrajsin</div>
            <div class="profile-role">Data Analyst & Data Scientist</div>
            <p style="color: #A0AEC0; font-size: 14px; line-height: 1.6;">
                Specializing in building end-to-end data pipelines, predictive machine learning models, and interactive visual dashboards.
            </p>
            <hr style="border-top: 1px solid rgba(255,255,255,0.1); margin: 15px 0;">
            <div style="text-align: left; font-size: 13px;">
                <b style="color: #A855F7;">Core Toolkit:</b><br>
                • Python (Pandas, Numpy, Scikit-Learn)<br>
                • Data Visualization (Plotly, Seaborn, Matplotlib)<br>
                • Interactive Apps (Streamlit, Web App integrations)<br>
                • Version Control (Git, GitHub)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_p2:
        st.markdown("<div class='section-title'>How to Upload Data & Code on GitHub</div>", unsafe_allow_html=True)
        st.write("Below is a step-by-step developer guide on linking your local workspace to your GitHub repository and uploading your project files.")
        
        st.markdown("**1. Configure Git Credentials (One-time Setup)**")
        st.write("Ensure your local system knows who you are so commits are attributed properly:")
        st.markdown('<div class="git-command">git config --global user.name "dhruvrajsin"<br>git config --global user.email "your-email@example.com"</div>', unsafe_allow_html=True)
        
        st.markdown("**2. Initialize Local Git Repository**")
        st.write("Run this command inside your project folder (`d:\\data analytics\\data scince\\github`) to make it a Git repo:")
        st.markdown('<div class="git-command">git init</div>', unsafe_allow_html=True)
        
        st.markdown("**3. Add Files and Commit Changes**")
        st.write("Stage all files and save a checkpoint of your project:")
        st.markdown('<div class="git-command">git add .<br>git commit -m "Initialize Global Real Estate Prediction & Analytics Dashboard"</div>', unsafe_allow_html=True)
        
        st.markdown("**4. Link to Remote GitHub Repository**")
        st.write("Associate your local repository with the GitHub repository you created:")
        st.markdown('<div class="git-command">git remote add origin https://github.com/dhruvrajsin/data-analtics-data-scince.git<br>git branch -M main</div>', unsafe_allow_html=True)
        
        st.markdown("**5. Push Files to GitHub**")
        st.write("Upload the files online to your remote repository:")
        st.markdown('<div class="git-command">git push -u origin main</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.info("💡 **Tip**: If you receive a credential prompt, sign in with your web browser or use a personal access token (PAT) generated in your GitHub Developer Settings.")
