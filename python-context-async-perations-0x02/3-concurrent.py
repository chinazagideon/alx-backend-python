
import asyncio
import email
from itertools import islice
import time 
import aiosqlite
import os
import io, csv
import logging
from typing import List, Tuple, Generator

MY_DATABASE = "alx_prodev.db" 
path = "python-context-async-perations-0x02/user_data.csv"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration for batch processing
BATCH_SIZE = 100  # Process 100 records at a time
MAX_CONCURRENT_TASKS = 10  # Limit concurrent database operations
CHUNK_SIZE = 1000  # Read CSV in chunks to avoid memory issues

# use context manager to setup connection 
async def initialize_db():
     """Initializes the database by creating the users table."""
     query = """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NULL,
                email TEXT UNIQUE NOT NULL
            )"""
     async with aiosqlite.connect(MY_DATABASE) as mydb:
         logger.info(f"Database Connection established: {MY_DATABASE}")
         await mydb.execute(query)
         await mydb.commit()

async def run_update_query(conn, query_data):
    """Adds a single user to the database."""
    try:
        insert_query, params = query_data
        await conn.execute(insert_query, params)
        await conn.commit()
        return True
    except aiosqlite.IntegrityError as duplicateExc:
        logger.warning(f"Duplicate email found: {params[2] if len(params) > 2 else 'unknown'}")
        return False
    except Exception as exc:
        logger.error(f"Error inserting user: {type(exc).__name__}: {exc}")
        return False

async def batch_insert_users(conn, user_batch: List[Tuple[str, tuple]]):
    """Insert a batch of users concurrently with limited concurrency."""
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
    
    async def insert_with_semaphore(user_data):
        async with semaphore:
            return await run_update_query(conn, user_data)
    
    tasks = [insert_with_semaphore(user_data) for user_data in user_batch]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successful = sum(1 for result in results if result is True)
    failed = len(results) - successful
    
    # logger.info(f"Batch processed: {successful} successful, {failed} failed")
    return successful, failed

def gen_query_insert(**data):
    """Generate SQL insert query and parameters tuple."""
    columns = ", ".join(data.keys())
    value_tuple = tuple(data.values())
    symbols = ', '.join('?' for _ in data)
    query = f"INSERT INTO users ({columns}) VALUES ({symbols})"
    return query, value_tuple

def process_csv_chunk(csv_reader, chunk_size: int) -> Generator[List[Tuple[str, tuple]], None, None]:
    """Process CSV file in chunks to avoid memory issues."""
    chunk = []
    for row_dict in csv_reader:
        try:
            # Convert age to integer, handle empty values
            age = int(row_dict['age']) if row_dict['age'].strip() else None
            user_data = gen_query_insert(
                name=row_dict['name'].strip(),
                age=age,
                email=row_dict['email'].strip()
            )
            chunk.append(user_data)
            
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
                
        except (ValueError, KeyError) as e:
            logger.warning(f"Skipping invalid row: {row_dict}, Error: {e}")
            continue
    
    # Yield remaining chunk if not empty
    if chunk:
        yield chunk

async def fetch_data(conn, query):
    """Fetch data from the database."""
    try:
        cursor = await conn.execute(query)
        results = await cursor.fetchall()
        return results 
    except Exception as exc:
        logger.error(f"Error fetching data: {type(exc).__name__}: {exc}")
        return False
    

def add_connection(func):
    async def wrapper(*args, **kwargs):
        async with aiosqlite.connect(MY_DATABASE) as mydb:
            return await func(mydb, *args, **kwargs)
    return wrapper
    
# @add_connection
async def async_fetch_users():
    """Fetch users from the database."""
    try:
        
        cursor = await conn.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        return results
    except Exception as exc:
        logger.error(f"Error fetching users: {type(exc).__name__}: {exc}")
        return False
# @add_connection
async def async_fetch_older_users():
    """Fetch older users from the database."""
    try:
        cursor = await conn.execute("SELECT * FROM users WHERE age > 30")
        results = await cursor.fetchall()
        return results
    except Exception as exc:
        logger.error(f"Error fetching older users: {type(exc).__name__}: {exc}")
        return False

async def fetch_concurrently():
    logger.info("Starting concurrent CSV processing task")
    
    # Clean up previous database file if it exists for a fresh start
    if os.path.exists(MY_DATABASE):
        os.remove(MY_DATABASE)
        logger.info(f"Removed existing {MY_DATABASE}")

    await initialize_db()

    # Process CSV file in chunks
    total_processed = 0
    total_successful = 0
    total_failed = 0
    
    start_time = time.time()
    
    try:
        with open(path, 'r', newline='', encoding='utf-8') as file:
            csvfile = csv.DictReader(file)
            
            async with aiosqlite.connect(MY_DATABASE) as mydb:
                logger.info(f'Database connection established for processing: {MY_DATABASE}')
                
                # Process CSV in chunks
                for chunk_num, user_chunk in enumerate(process_csv_chunk(csvfile, CHUNK_SIZE), 1):
                    # logger.info(f"Processing chunk {chunk_num} with {len(user_chunk)} records")
                    
                    # Process chunk in batches
                    for i in range(0, len(user_chunk), BATCH_SIZE):
                        batch = user_chunk[i:i + BATCH_SIZE]
                        successful, failed = await batch_insert_users(mydb, batch)
                        
                        total_successful += successful
                        total_failed += failed
                        total_processed += len(batch)
                        
                        # logger.info(f"Batch {i//BATCH_SIZE + 1} of chunk {chunk_num}: "
                        #           f"{successful} successful, {failed} failed")
                        
                        # Small delay to prevent overwhelming the database
                        await asyncio.sleep(0.01)
    
    except FileNotFoundError:
        logger.error(f"CSV file not found: {path}")
        return
    except Exception as e:
        logger.error(f"Error processing CSV: {type(e).__name__}: {e}")
        return
    
    end_time = time.time()
    processing_time = end_time - start_time

    # Fetch users from the database
    async with aiosqlite.connect(MY_DATABASE) as mydb:
        users = await async_fetch_users(mydb)
        logger.info(f"Users: {list(islice(users, 10))}\n")
    
    # Fetch older users from the database
    async with aiosqlite.connect(MY_DATABASE) as mydb:
        older_users = await async_fetch_older_users(mydb)
        logger.info(f"Older users: {list(islice(older_users, 10))}\n")
    

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())


