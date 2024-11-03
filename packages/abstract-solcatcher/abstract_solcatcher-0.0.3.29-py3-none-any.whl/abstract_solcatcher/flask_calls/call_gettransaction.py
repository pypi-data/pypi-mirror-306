import psycopg2
import json
from solRpcs import Client

client = Client()

# Establish a connection to the database
conn = psycopg2.connect(
    dbname="solcatcher", 
    user="partners", 
    password="solcatch123!!!456", 
    host="192.168.0.100",
    port=5432
)

# Create a cursor object
cur = conn.cursor()

# Create table if it does not exist
create_table = """
CREATE TABLE IF NOT EXISTS gettransaction (
    id SERIAL PRIMARY KEY,
    signature VARCHAR(255) UNIQUE NOT NULL,
    transaction_data JSONB NOT NULL
);
"""
cur.execute(create_table)
conn.commit()

# Data to be inserted
signature = "4LqCrcBSe2gn1wy5MkGu5yycDyHAUgCGPfwqs95FgJczg6odB9b9gSxbeaicg9KV8bXENiuvrYyhD2YcCxFMgQij"
transaction_data = client.get_transaction(signature)
# Prepare your SQL command
query = "INSERT INTO gettransaction (signature, transaction_data) VALUES (%s, %s)"
cur.execute(query, (signature, json.dumps(transaction_data)))
# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
