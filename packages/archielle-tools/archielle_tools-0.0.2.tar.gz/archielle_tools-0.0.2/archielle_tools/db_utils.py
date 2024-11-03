import mysql.connector
from mysql.connector import Error
from .config import validate_token

def insert_leads_into_db(missing_leads, db_config, user_token):
    validate_token(user_token)  # Validate the user's token
    
    try:
        connection = mysql.connector.connect(**db_config)
        
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()

            for _, lead in missing_leads.iterrows():
                insert_query = f"""
                    INSERT INTO tblleads (name, title, company, description, country, zip, city, state, address, assigned, 
                                          dateadded, status, source, email, phonenumber)
                    VALUES (
                        '{lead.get('full_name', '')}',
                        '{lead.get('title', '')}',
                        'Klaviyo Lead',
                        'Imported from Klaviyo',
                        '{lead.get('location_country', '')}',
                        '{lead.get('location_zip', '')}',
                        '{lead.get('location_city', '')}',
                        '{lead.get('location_region', '')}',
                        '{lead.get('location_address1', '')}',
                        2,
                        NOW(),
                        2,
                        3,
                        '{lead.get('email', '')}',
                        '{lead.get('phone', '')}'
                    )
                """
                cursor.execute(insert_query)
            connection.commit()
            print("Records inserted successfully into tblleads table.")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
