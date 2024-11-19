import os
from supabase import create_client
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Please set SUPABASE_URL and SUPABASE_KEY in .env file")

supabase = create_client(supabase_url, supabase_key)

def get_table_schema(table_name):
    """Fetch and print detailed schema information for a table."""
    try:
        # Fetch a sample row to get column names
        response = supabase.table(table_name).select('*').limit(1).execute()
        
        if response.data:
            # Get column names from the first row
            columns = list(response.data[0].keys())
            
            print(f"Columns in table '{table_name}':")
            for col in columns:
                print(f"- {col}")
            
            return columns
        else:
            print(f"No data found in table {table_name}")
            return []
    
    except Exception as e:
        print(f"Error fetching table schema: {e}")
        return []

def main():
    tables_to_inspect = ['person']
    
    for table in tables_to_inspect:
        print(f"\nInspecting table: {table}")
        get_table_schema(table)

if __name__ == "__main__":
    main()
