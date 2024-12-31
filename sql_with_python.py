import asyncio
import asyncpg

# Asynchronous function to connect to the database and create a table
async def main():
    # Connect to the PostgreSQL database
    conn = await asyncpg.connect(
        user='',
        password='',
        database='',
        host='localhost',
        port='5432'
    )

    print("Connection success")

    # Create a new table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Members (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INT,
        address VARCHAR(255),
        phone_number VARCHAR(15)
    );
    """

    # Execute the CREATE TABLE statement
    await conn.execute(create_table_query)
    print("Table 'Members' created successfully")

    # Correct SQL Insert query using parameterized queries
    insert_data_query = """
    INSERT INTO Members (name, age, address, phone_number)
    VALUES ($1, $2, $3, $4);
    """

    # Get user input for the table data
    name = input("Enter the name: ")
    age = int(input("Enter the age: "))  # Convert age to an integer
    address = input("Enter the address: ")
    phone = input("Enter the phone number: ")

    # Data to insert into the Members table (parameterized)
    member_data = (name, age, address, phone)

    # Execute the insert query with data
    await conn.execute(insert_data_query, *member_data)
    print("Data inserted successfully")

    # Close the connection
    await conn.close()

# Run the asynchronous function
asyncio.run(main())
