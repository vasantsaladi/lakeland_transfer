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

def test_supabase_connection():
    """Test Supabase connection and basic operations."""
    try:
        # Try to select from a table (replace 'person' with an existing table)
        response = supabase.table('person').select('*').limit(1).execute()
        print("Supabase connection successful!")
        print("Table 'person' exists.")
        print("Sample data:", response.data)
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")

if __name__ == "__main__":
    test_supabase_connection()
