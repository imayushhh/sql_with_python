import tkinter as tk
from tkinter import *
import asyncio
import asyncpg

root = Tk()

# Function to add data to the database
async def get_data(name, age, address, phone_number):
    try:
        conn = await asyncpg.connect(
            user='postgres',
            password='Ayush@1998',
            database='postgres',
            host='localhost',
            port='5432'
        )

        # Creating the table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Members (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            address VARCHAR(255),
            phone_number VARCHAR(15)
        );
        """
        await conn.execute(create_table_query)

        # Inserting data into the Members table
        insert_data_query = """
        INSERT INTO Members (name, age, address, phone_number)
        VALUES ($1, $2, $3, $4);
        """
        member_data = (name, age, address, phone_number)
        await conn.execute(insert_data_query, *member_data)
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await conn.close()

# Function to search for a member by ID
async def search_data_by_id(member_id):
    try:
        conn = await asyncpg.connect(
            user='postgres',
            password='Ayush@1998',
            database='postgres',
            host='localhost',
            port='5432'
        )

        # Searching for the record by ID
        search_query = "SELECT * FROM Members WHERE id = $1"
        member_data = await conn.fetch(search_query, member_id)

        if member_data:
            print(f"Member found: {member_data}")
            display_search(member_data)  # Update the UI with the search result
        else:
            print("No member found with that ID.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await conn.close()

# Function to display the search result in the UI
def display_search(member_data):
    listbox.delete(0, END)  # Clear previous results
    for row in member_data:
        listbox.insert(END, f"ID: {row['id']} | Name: {row['name']} | Age: {row['age']} | Address: {row['address']} | Phone: {row['phone_number']}")

# Function to handle the search button click
def on_search_button_click():
    member_id = Id_Search.get()
    if member_id:
        asyncio.run(search_data_by_id(member_id))
    else:
        print("Please enter an ID to search.")

# Function to handle the add button click
def on_add_button_click(name, age, address, phone_number):
    asyncio.run(get_data(name, age, address, phone_number))

canvas = Canvas(root, height=480, width=900)
canvas.pack()

frame = Frame()
frame.place(relx=0.3, rely=0.1, relwidth=0.8, relheight=0.8)

# Adding the "Add Data" section
label = Label(frame, text="Add Data")
label.grid(row=0, column=1)

label = Label(frame, text="Name")
label.grid(row=1, column=0)

entry_name = Entry(frame)
entry_name.grid(row=1, column=1)

label = Label(frame, text="Age")
label.grid(row=2, column=0)

entry_age = Entry(frame)
entry_age.grid(row=2, column=1)

label = Label(frame, text="Address")
label.grid(row=3, column=0)

entry_address = Entry(frame)
entry_address.grid(row=3, column=1)

label = Label(frame, text="Phone Number")
label.grid(row=4, column=0)

entry_number = Entry(frame)
entry_number.grid(row=4, column=1)

button = Button(frame, text="Add", command=lambda: on_add_button_click(
    entry_name.get(), entry_age.get(), entry_address.get(), entry_number.get()))
button.grid(row=5, column=1)

# Adding the "Search Data" section
label = Label(frame, text="Search Data")
label.grid(row=6, column=1)

label = Label(frame, text="Search By ID")
label.grid(row=7, column=0)

Id_Search = Entry(frame)
Id_Search.grid(row=7, column=1)

search_button = Button(frame, text="Search", command=on_search_button_click)
search_button.grid(row=7, column=2)

# Listbox to display search results
listbox = Listbox(frame, width=80, height=10)
listbox.grid(row=8, column=1, columnspan=2)

root.mainloop()
