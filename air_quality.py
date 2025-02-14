import pandas as pd
from sklearn.impute import KNNImputer

pd.set_option('future.no_silent_downcasting', True)

# Load the dataset
file_path = 'air quality day by day.xlsx'  # Replace with your actual file path
data = pd.read_excel(file_path)

# Replace 'blank' with 0 in a specific column
data['AQI_Bucket'] = data['AQI_Bucket'].replace("(blank)", 0)


# Handle Median Imputation for specified columns
median_columns = ['AQI', 'Benzene', 'CO', 'NH3', 'NO', 'NO2', 'Nox', 'O3', 'SO2', 'Toluene']
for col in median_columns:
    if col in data.columns:
        # Replace zeros and blank cells with NaN
        data[col] = data[col].replace([0, ''], None)
        median_value = data[col].median()
        data[col] = data[col].fillna(median_value).infer_objects()  # Convert back to appropriate dtype

# Handle KNN Imputation for specified columns
knn_columns = ['PM10', 'PM2.5']
if set(knn_columns).issubset(data.columns):
    # Replace zeros and blank cells with NaN
    knn_data = data[knn_columns].replace([0, ''], None)
    imputer = KNNImputer(n_neighbors=5)  # KNN with 5 neighbors
    knn_imputed = imputer.fit_transform(knn_data)
    knn_imputed_df = pd.DataFrame(knn_imputed, columns=knn_columns)
    data[knn_columns] = knn_imputed_df

# Map AQI values to AQI_Bucket categories
if 'AQI' in data.columns:
    # Define AQI ranges and corresponding categories
    bins = [0, 50, 100, 200, 300, 400, float('inf')]
    labels = ['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe']
    
    # Map AQI values to AQI_Bucket categories
    data['AQI_Bucket'] = pd.cut(data['AQI'], bins=bins, labels=labels, right=False)

# Create a dictionary mapping cities to states
city_to_state = {
    'Delhi': 'Delhi',
    'Mumbai': 'Maharashtra',
    'Amaravati': 'Maharashtra',
    'Kolkata': 'West Bengal',
    'Chennai': 'Tamil Nadu',
    'Coimbatore': 'Tamil Nadu',
    'Bengaluru': 'Karnataka',
    'Hyderabad': 'Telangana',
    'Ahmedabad': 'Gujarat',
    'Amritsar': 'Punjab',
    'Bhopal': 'Madhya Pradesh',
    'Brajrajnagar': 'Odisha',
    'Ernakulam': 'Kerala',
    'Gurugram': 'Haryana',
    'Guwahati': 'Assam',
    'Jaipur': ' Rajasthan',
    'Kochi': 'Kerala',
    'Lucknow': 'Uttar Pradesh',
    'Patna': 'Bihar',
    'Shillong': 'Meghalaya',
    'Talcher': 'Odisha',
    'Thiruvananthapuram': 'Kerala',
    'Visakhapatnam': 'Andhra Pradesh'
}

# Create a new column for state names
data['State'] = data['City'].map(city_to_state)

# Remove rows with 'City' as 'Chandigarh' or 'Jorapokhar'
data = data[~data['City'].isin(['Chandigarh', 'Jorapokhar'])]


# Save the updated dataset back to an Excel file
output_path = 'updated_air_quality.xlsx'
data.to_excel(output_path, index=False)

print(f"Updated dataset saved to {output_path}")

