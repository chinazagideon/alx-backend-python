import csv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seed as seed

# print(asyncio.run(fetch_data("https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2024/12/3888260f107e3701e3cd81af49ef997cf70b6395.csv")))

def open_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def verify_inserted_data():
    """Verify that data was inserted correctly"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM user_data")
    results = cursor.fetchall()
    
    print("\nVerifying inserted data:")
    print("user_id | name | email | age")
    print("-" * 50)
    for row in results:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
    
    cursor.close()
    connection.close()

def parse_and_insert_csv_data(path):
    # Connect to database
    connection = seed.connect_to_prodev()
    
    # Read CSV data from local file
    data = open_file(path)
    lines = data.strip().split("\n")
    
    # Skip the header row (first row)
    data_rows = lines[1:]
    
    for row in data_rows:
        # Parse CSV row properly, handling quoted values
        parsed_row = list(csv.reader([row]))[0]
        
        # Extract values (remove quotes)
        name = parsed_row[0].strip('"')
        email = parsed_row[1].strip('"')
        age = parsed_row[2].strip('"')
        
        # Insert into user_data table
        # Note: user_id is AUTO_INCREMENT, so we don't need to specify it
        try:
            seed.insert_data(connection, "user_data", f"'{name}', '{email}', {age}")
            print(f"Inserted: {name}, {email}, {age}")
        except Exception as e:
            print(f"Error inserting {name}: {e}")
    
    connection.close()
    print("Data insertion completed!")

def delete_data():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM user_data")
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    parse_and_insert_csv_data("python-generators-0x00/user_data.csv")
    # verify_inserted_data()
    # delete_data()