import os
from supabase import create_client
from dotenv import load_dotenv

def init_database():
    """
    Initialize the database schema
    """
    # Load environment variables
    load_dotenv()
    
    # Get Supabase credentials
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("Error: Supabase credentials not found in environment variables")
        return False
    
    try:
        # Connect to Supabase
        supabase = create_client(supabase_url, supabase_key)
        
        # Read schema SQL
        with open("database/schema.sql", "r") as f:
            schema_sql = f.read()
        
        # Execute SQL (note: this is a simplified example, as Supabase doesn't directly support
        # executing arbitrary SQL through the client. In a real application, you would use
        # the Supabase dashboard or a migration tool)
        print("Please execute the following SQL in your Supabase SQL editor:")
        print(schema_sql)
        
        # Create storage bucket if it doesn't exist
        try:
            supabase.storage.create_bucket("files", {"public": True})
            print("Storage bucket 'files' created successfully")
        except Exception as e:
            if "already exists" in str(e):
                print("Storage bucket 'files' already exists")
            else:
                print(f"Error creating storage bucket: {str(e)}")
        
        return True
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        return False

if __name__ == "__main__":
    init_database()
