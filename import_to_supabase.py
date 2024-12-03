import pandas as pd
from supabase import create_client
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='import_log.txt'
)

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

def insert_record(row):
    """Insert a single census record into all related tables."""
    try:
        record_id = int(row['pk'])
        
        # 1. Insert personal attributes
        personal_attr = {
            "attribute_id": record_id,
            "person_id": record_id,
            "race": row['race'],
            "sex": row['sex'],
            "age": int(row['age']) if pd.notna(row['age']) else None
        }
        supabase.table('personal_attributes').insert(personal_attr).execute()
        logging.info(f"Inserted personal attributes for ID {record_id}")

        # 2. Insert family record
        family = {
            "family_id": int(row['family']),
            "person_id": record_id,
            "family": int(row['family']),
            "dwelling": int(row['dwelling']),
            "hoh_first_name": row['head_first'],
            "hoh_last_name": row['head_last']
        }
        supabase.table('families').insert(family).execute()
        logging.info(f"Inserted family record for ID {record_id}")

        # 3. Insert relationship
        relationship = {
            "relationship_id": record_id,
            "person_id": record_id,
            "family_id": int(row['family']),
            "relation_to_hoh": row['relation_head']
        }
        supabase.table('relationships').insert(relationship).execute()
        logging.info(f"Inserted relationship for ID {record_id}")

        # 4. Insert marital status if present
        if pd.notna(row['marital']):
            marital = {
                "marital_level_id": record_id,
                "person_id": record_id,
                "marital_status": row['marital']
            }
            supabase.table('marital_levels').insert(marital).execute()
            logging.info(f"Inserted marital status for ID {record_id}")

        # 5. Insert property ownership if present
        if pd.notna(row['owned_rented']):
            property_own = {
                "ownership_id": record_id,
                "person_id": record_id,
                "owned_rented": row['owned_rented']
            }
            supabase.table('property_ownership').insert(property_own).execute()
            logging.info(f"Inserted property ownership for ID {record_id}")

        # 6. Insert occupation if present
        if pd.notna(row['work']):
            occupation = {
                "occupation_id": record_id,
                "person_id": record_id,
                "work": row['work']
            }
            supabase.table('occupations').insert(occupation).execute()
            logging.info(f"Inserted occupation for ID {record_id}")

        # 7. Finally, insert the person record with all foreign keys
        person = {
            "person_id": record_id,
            "first_name": row['first_name'],
            "last_name": row['last_name'],
            "personal_attribute_id": record_id,
            "family_id": int(row['family']),
            "relationship_id": record_id,
            "marital_level_id": record_id if pd.notna(row['marital']) else None,
            "property_ownership_id": record_id if pd.notna(row['owned_rented']) else None,
            "occupation_id": record_id if pd.notna(row['work']) else None
        }
        supabase.table('persons').insert(person).execute()
        logging.info(f"Successfully inserted complete record for {row['first_name']} {row['last_name']}")
        
        return True

    except Exception as e:
        logging.error(f"Error inserting record for {row['first_name']} {row['last_name']}: {str(e)}")
        return False

def main():
    try:
        # Read the CSV file
        csv_path = 'data/lakeland_1900_census.csv'
        df = pd.read_csv(csv_path)
        
        # Process each row
        success_count = 0
        total_records = len(df)
        
        for index, row in df.iterrows():
            if insert_record(row):
                success_count += 1
                logging.info(f"Processed record {index + 1} of {total_records}")
            else:
                logging.error(f"Failed to process record {index + 1}")
        
        logging.info(f"Import completed. Successfully imported {success_count} out of {total_records} records")
        print(f"Import completed. Successfully imported {success_count} out of {total_records} records")
        print("Check import_log.txt for detailed information")

    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
        print(f"An error occurred. Check import_log.txt for details")

if __name__ == "__main__":
    main()
