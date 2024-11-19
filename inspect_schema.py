import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Please set SUPABASE_URL and SUPABASE_KEY in .env file")

supabase = create_client(supabase_url, supabase_key)

def inspect_table_schema(table_name):
    """Inspect the schema of a given table."""
    try:
        # Fetch table schema
        response = supabase.table(table_name).select('*').limit(0).execute()
        
        # Get column names from the response
        columns = response.data[0].keys() if response.data else []
        
        print(f"Columns in table '{table_name}':")
        for column in columns:
            print(f"- {column}")
        
        return list(columns)
    
    except Exception as e:
        print(f"Error inspecting table {table_name}: {e}")
        return []

def main():
    tables_to_inspect = ['person']
    
    for table in tables_to_inspect:
        print(f"\nInspecting table: {table}")
        inspect_table_schema(table)

if __name__ == "__main__":
    main()
