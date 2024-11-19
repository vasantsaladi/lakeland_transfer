import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
from typing import Dict, List
import logging
import numpy as np
import sys

# Set up more detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('census_import.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Please set SUPABASE_URL and SUPABASE_KEY in .env file")

supabase = create_client(supabase_url, supabase_key)

def create_person_table():
    """Create the person table if it doesn't exist."""
    try:
        # Use PostgreSQL's CREATE TABLE IF NOT EXISTS
        create_table_query = """
        CREATE TABLE IF NOT EXISTS person (
            person_id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            marital_level_marital_level_id INTEGER,
            personal_attributes_attribute_id INTEGER,
            family_family_id TEXT,
            relationship_relationship_id TEXT,
            property_ownership_ownership_id TEXT,
            census_year INTEGER
        )
        """
        
        # Execute raw PostgreSQL query
        response = supabase.table('person').select('*').limit(1).execute()
        
        # If no exception is raised, table exists
        logger.info("Person table already exists.")
    except Exception as e:
        # Table does not exist, so create it
        try:
            # Use Supabase's PostgreSQL extension
            supabase.rpc('execute_sql', {'query': create_table_query}).execute()
            logger.info("Person table created successfully.")
        except Exception as create_error:
            logger.error(f"Error creating person table: {create_error}")
            raise

def create_reference_tables():
    """Create and populate all reference tables before data import."""
    try:
        # Marital Level Table
        marital_levels = [
            {"marital_level_id": 1, "marital_level": "Married"},
            {"marital_level_id": 2, "marital_level": "Never Married"},
            {"marital_level_id": 3, "marital_level": "Divorced"},
            {"marital_level_id": 4, "marital_level": "Widowed"},
            {"marital_level_id": 5, "marital_level": "Separated"}
        ]
        
        # Personal Attributes (Race) Table
        race_attributes = [
            {"attribute_id": 1, "attribute_name": "White"},
            {"attribute_id": 2, "attribute_name": "Black"},
            {"attribute_id": 3, "attribute_name": "Hispanic"},
            {"attribute_id": 4, "attribute_name": "Asian"},
            {"attribute_id": 5, "attribute_name": "Native American"},
            {"attribute_id": 6, "attribute_name": "Other"}
        ]
        
        # Relationship Table
        relationships = [
            {"relationship_id": 1, "relationship_name": "Head of Household"},
            {"relationship_id": 2, "relationship_name": "Spouse"},
            {"relationship_id": 3, "relationship_name": "Child"},
            {"relationship_id": 4, "relationship_name": "Parent"},
            {"relationship_id": 5, "relationship_name": "Sibling"},
            {"relationship_id": 6, "relationship_name": "Other Relative"},
            {"relationship_id": 7, "relationship_name": "Lodger/Boarder"}
        ]
        
        # Populate tables
        tables_to_populate = [
            ('marital_level', marital_levels),
            ('personal_attributes', race_attributes),
            ('relationship', relationships)
        ]
        
        for table_name, data in tables_to_populate:
            # Inspect table schema
            try:
                schema_result = supabase.table(table_name).select('*').limit(1).execute()
                logger.info(f"Schema for {table_name}: {list(schema_result.data[0].keys()) if schema_result.data else 'No data'}")
            except Exception as schema_error:
                logger.error(f"Error inspecting {table_name} schema: {schema_error}")
            
            # Use upsert to handle both insert and update
            for item in data:
                try:
                    supabase.table(table_name).upsert(item).execute()
                except Exception as insert_error:
                    logger.error(f"Error inserting item into {table_name}: {insert_error}")
        
        logger.info("All reference tables populated successfully.")
    except Exception as e:
        logger.error(f"Error creating reference tables: {e}")
        raise

def clean_data(value, column_type=None):
    """
    Clean and transform data for database insertion.
    
    Args:
        value: Input value to clean
        column_type: Optional type hint for specific cleaning
    
    Returns:
        Cleaned value or None if value cannot be processed
    """
    if pd.isna(value) or value is None or value == '':
        return None
    
    # Convert to string first
    str_value = str(value).strip()
    
    # Handle marital status column
    if column_type == 'marital':
        marital_mapping = {
            'mar': 1,  # Married
            'married': 1,
            'nev': 2,  # Never Married
            'never': 2,
            'div': 3,  # Divorced
            'divorced': 3,
            'wd': 4,   # Widowed
            'widowed': 4,
            'sep': 5   # Separated
        }
        str_value = str_value.lower()[:3]
        return marital_mapping.get(str_value)
    
    # Handle race column
    if column_type == 'race':
        race_mapping = {
            'w': 1,    # White
            'white': 1,
            'b': 2,    # Black
            'black': 2,
            'h': 3,    # Hispanic
            'hispanic': 3,
            'a': 4,    # Asian
            'asian': 4,
            'o': 5     # Other
        }
        str_value = str_value.lower()[:1]
        return race_mapping.get(str_value)
    
    # Default handling: try to convert to integer
    try:
        return int(str_value)
    except ValueError:
        # If integer conversion fails, return None
        return None

def insert_person(df: pd.DataFrame, file_offset: int = 0, census_year: int = None) -> Dict[int, int]:
    """Insert person data with robust error handling and foreign key validation."""
    person_ids = {}
    total_rows = len(df)
    processed_rows = 0
    
    # Retrieve existing reference data to validate foreign keys
    try:
        marital_levels = {level['marital_level']: level['marital_level_id'] 
                          for level in supabase.table('marital_level').select('*').execute().data}
        race_attributes = {attr['attribute_name']: attr['attribute_id'] 
                           for attr in supabase.table('personal_attributes').select('*').execute().data}
        relationships = {rel['relationship_name']: rel['relationship_id'] 
                         for rel in supabase.table('relationship').select('*').execute().data}
    except Exception as e:
        logger.error(f"Failed to retrieve reference data: {e}")
        raise
    
    for idx, row in df.iterrows():
        try:
            # Map text values to reference IDs with fallback
            marital_id = marital_levels.get(row.get('marital', 'Unknown'), None)
            race_id = race_attributes.get(row.get('race', 'Other'), 6)  # Default to 'Other'
            relationship_id = relationships.get(row.get('relationship', 'Other Relative'), 6)
            
            # Create person data dictionary with cleaned and validated values
            data = {
                'person_id': str(idx + file_offset),
                'first_name': clean_data(row.get('first_name')),
                'last_name': clean_data(row.get('last_name')),
                'personal_attributes_attribute_id': race_id,
                'family_family_id': clean_data(row.get('family_id')),
                'relationship_relationship_id': relationship_id,
                'marital_level_marital_level_id': marital_id,
                'census_year': census_year
            }
            
            # Remove None values
            data = {k: v for k, v in data.items() if v is not None}
            
            if data:
                # Insert person record
                result = supabase.table('person').insert(data).execute()
                
                if result and result.data:
                    person_ids[idx] = result.data[0]['person_id']
                    processed_rows += 1
                    
                    # Log progress periodically
                    if processed_rows % 100 == 0:
                        logger.info(f"Processed {processed_rows}/{total_rows} persons")
                else:
                    logger.warning(f"No data returned for person at index {idx}")
        
        except Exception as e:
            logger.error(f"Error inserting person at index {idx}: {e}")
            # Optionally, you could add more detailed error logging or error recovery logic
    
    logger.info(f"Completed person insertion. Total processed: {processed_rows}/{total_rows}")
    return person_ids

def process_csv_file(file_path: str, file_offset: int = 0):
    """Process a single CSV file with comprehensive error handling."""
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Standardize column names
        df.columns = [col.lower().strip() for col in df.columns]
        
        # Extract census year from filename
        census_year = int(file_path.split('_')[-2])
        
        logger.info(f"Processing file: {file_path}")
        logger.info(f"Total rows: {len(df)}")
        
        # Insert persons first
        person_ids = insert_person(df, file_offset, census_year)
        
        logger.info(f"Successfully inserted {len(person_ids)} persons")
        
        return len(person_ids)
    
    except Exception as e:
        logger.error(f"Critical error processing {file_path}: {e}")
        raise

def main():
    """Main function to process census files with robust error handling."""
    # First, create the person table
    create_person_table()
    
    # Create and populate reference tables
    create_reference_tables()
    
    data_dir = "data"
    file_offset = 0
    census_years = ['1900', '1920', '1930', '1940', '1950']
    
    # Track overall import status
    total_files_processed = 0
    failed_files = []
    
    logger.info("Starting Census Data Import Process")
    
    for year in census_years:
        file_name = f"lakeland_{year}_census.csv"
        file_path = os.path.join(data_dir, file_name)
        
        if os.path.exists(file_path):
            logger.info(f"\n--- Processing Census Year: {year} ---")
            try:
                rows_processed = process_csv_file(file_path, file_offset)
                file_offset += 10000  # Increment offset for next file
                total_files_processed += 1
                logger.info(f"Successfully processed {file_name}. Rows: {rows_processed}")
            
            except Exception as e:
                logger.error(f"Failed to process {file_name}: {e}")
                failed_files.append(file_name)
        
        else:
            logger.warning(f"File not found: {file_name}")
    
    # Final summary
    logger.info("\n--- Import Process Summary ---")
    logger.info(f"Total Files Processed: {total_files_processed}")
    if failed_files:
        logger.warning(f"Failed Files: {failed_files}")
    
    logger.info("Census Data Import Completed")

if __name__ == "__main__":
    main()
