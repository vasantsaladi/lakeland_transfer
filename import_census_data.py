import pandas as pd
import os

def load_census_data():
    """Load census data from 1900 to 1940 into separate DataFrames."""
    
    # Dictionary to store DataFrames
    census_data = {}
    
    # Base directory for data files
    data_dir = 'data'
    
    try:
        # Load 1900 census
        file_1900 = os.path.join(data_dir, 'lakeland_1900_census.csv')
        if os.path.exists(file_1900):
            df_1900 = pd.read_csv(file_1900)
            census_data['1900'] = df_1900
            print(f"Loaded 1900 census data: {len(df_1900)} records")
            print("Columns:", df_1900.columns.tolist())
            print("\n")

        # Load 1910 census
        file_1910 = os.path.join(data_dir, 'lakeland_1910_census.csv')
        if os.path.exists(file_1910):
            df_1910 = pd.read_csv(file_1910)
            census_data['1910'] = df_1910
            print(f"Loaded 1910 census data: {len(df_1910)} records")
            print("Columns:", df_1910.columns.tolist())
            print("\n")

        # Load 1920 census
        file_1920 = os.path.join(data_dir, 'lakeland_1920_census.csv')
        if os.path.exists(file_1920):
            df_1920 = pd.read_csv(file_1920)
            census_data['1920'] = df_1920
            print(f"Loaded 1920 census data: {len(df_1920)} records")
            print("Columns:", df_1920.columns.tolist())
            print("\n")

        # Load 1930 census
        file_1930 = os.path.join(data_dir, 'lakeland_1930_census.csv')
        if os.path.exists(file_1930):
            df_1930 = pd.read_csv(file_1930)
            census_data['1930'] = df_1930
            print(f"Loaded 1930 census data: {len(df_1930)} records")
            print("Columns:", df_1930.columns.tolist())
            print("\n")

        # Load 1940 census
        file_1940 = os.path.join(data_dir, 'lakeland_1940_census.csv')
        if os.path.exists(file_1940):
            df_1940 = pd.read_csv(file_1940)
            census_data['1940'] = df_1940
            print(f"Loaded 1940 census data: {len(df_1940)} records")
            print("Columns:", df_1940.columns.tolist())
            print("\n")

        # Print summary of loaded data
        print("Summary of loaded census data:")
        for year, df in census_data.items():
            print(f"{year}: {len(df)} records")
        
        return census_data

    except Exception as e:
        print(f"Error loading census data: {str(e)}")
        return None

if __name__ == "__main__":
    census_data = load_census_data()
    
    # Example of accessing individual census years
    if census_data:
        for year, df in census_data.items():
            print(f"\nSample of {year} census data:")
            print(df.head(2))  # Show first 2 records of each year
            print("\nData Info:")
            print(df.info())
            print("-" * 80)
