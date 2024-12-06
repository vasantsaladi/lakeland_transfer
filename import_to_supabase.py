import pandas as pd
import numpy as np
from supabase import create_client
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv('.env.local')
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url:
    raise ValueError("SUPABASE_URL environment variable is not set")
if not key:
    raise ValueError("SUPABASE_KEY environment variable is not set")

supabase = create_client(url, key)

def clean_data(df):
    df = df.copy()
    
    # Convert float columns to int, replacing NaN with None
    int_columns = [
        'source_pk', 'census_year', 'person_id', 'record_id', 'attribute_id',
        'family_id', 'dwelling', 'family', 'occupation_id', 'marital_level_id',
        'ownership_id', 'relationship_id'
    ]
    
    for col in int_columns:
        if col in df.columns:
            df[col] = df[col].replace({np.nan: None})
            df[col] = df[col].apply(lambda x: int(float(x)) if pd.notna(x) else None)
    
    # Replace empty strings and 'Unknown' with None for string columns
    string_columns = [
        'first_name', 'last_name', 'relation_to_hoh', 'hoh_first_name',
        'hoh_last_name', 'sex', 'race', 'marital_status', 'work',
        'business', 'owned_rented'
    ]
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].replace({'': None, 'Unknown': None})
    
    df = df.replace({np.nan: None})
    return df

def insert_records(table_name, data, batch_size=50, max_retries=3):
    """Insert records with duplicate handling"""
    for start in range(0, len(data), batch_size):
        batch = data.iloc[start:start + batch_size]
        records = batch.to_dict('records')
        
        for attempt in range(max_retries):
            try:
                # Try insert first (faster than upsert)
                supabase.table(table_name).insert(records).execute()
                break
            except Exception as e:
                if 'duplicate key' in str(e).lower() or 'duplicate constraint' in str(e).lower():
                    try:
                        # If duplicate, try individual upserts
                        for record in records:
                            try:
                                supabase.table(table_name).upsert(record).execute()
                            except Exception as inner_e:
                                print(f"Warning: Failed to upsert record in {table_name}: {str(inner_e)}")
                                continue
                        break
                    except Exception as upsert_e:
                        print(f"Warning: Batch upsert failed for {table_name}: {str(upsert_e)}")
                        if attempt == max_retries - 1:
                            raise
                elif attempt == max_retries - 1:
                    print(f"Failed to insert into {table_name} after {max_retries} attempts: {str(e)}")
                    raise
                time.sleep(1)  # Wait before retry

def import_census_data():
    print("Reading CSV file...")
    df = pd.read_csv('data/lakeland_combined_census_cleaned.csv')
    df = clean_data(df)
    
    try:
        # 1. Insert census_records first (no foreign key dependencies)
        print("Inserting into census_records table...")
        records_df = df[['record_id', 'census_year', 'person_id', 'source_pk']].drop_duplicates(subset=['record_id'])
        insert_records('census_records', records_df)

        # 2. Insert personal_attributes (depends on census_records)
        print("Inserting into personal_attributes table...")
        attrs_df = df[[
            'attribute_id', 'person_id', 'race', 'sex', 'age', 'record_id'
        ]].drop_duplicates(subset=['attribute_id'])
        insert_records('personal_attributes', attrs_df)

        # 3. Insert relationships (depends on census_records)
        print("Inserting into relationships table...")
        relationships_df = df[[
            'relationship_id', 'attribute_id', 'person_id',
            'family_id', 'relation_to_hoh', 'record_id'
        ]].drop_duplicates(subset=['relationship_id'])
        insert_records('relationships', relationships_df)

        # 4. Insert families (depends on relationships)
        print("Inserting into families table...")
        families_df = df[[
            'family_id', 'person_id', 'family', 'dwelling',
            'hoh_first_name', 'hoh_last_name', 'relationship_id', 'census_year'
        ]].drop_duplicates(subset=['family_id'])
        insert_records('families', families_df)

        # 5. Insert marital_levels (depends on census_records)
        print("Inserting into marital_levels table...")
        marital_df = df[[
            'marital_level_id', 'attribute_id', 'person_id',
            'marital_status', 'record_id'
        ]].drop_duplicates(subset=['marital_level_id'])
        insert_records('marital_levels', marital_df)

        # 6. Insert property_ownership (depends on census_records)
        print("Inserting into property_ownership table...")
        property_df = df[[
            'ownership_id', 'attribute_id', 'person_id',
            'owned_rented', 'record_id'
        ]].drop_duplicates(subset=['ownership_id'])
        insert_records('property_ownership', property_df)

        # 7. Insert occupations (depends on census_records)
        print("Inserting into occupations table...")
        occupations_df = df[[
            'occupation_id', 'attribute_id', 'person_id',
            'work', 'business', 'record_id'
        ]].drop_duplicates(subset=['occupation_id'])
        insert_records('occupations', occupations_df)

        # 8. Finally insert persons (has most foreign key dependencies)
        print("Inserting into persons table...")
        persons_df = df.copy()
        # Rename columns to match database schema
        persons_df['personal_attribute_id'] = persons_df['attribute_id']
        persons_df['property_ownership_id'] = persons_df['ownership_id']
        persons_df = persons_df[[
            'person_id', 'first_name', 'last_name', 'personal_attribute_id',
            'family_id', 'relationship_id', 'marital_level_id',
            'property_ownership_id', 'occupation_id'
        ]].drop_duplicates(subset=['person_id'])
        insert_records('persons', persons_df)

        print("Data import completed successfully!")

    except Exception as e:
        print(f"Error during import: {str(e)}")
        raise

if __name__ == "__main__":
    import_census_data()