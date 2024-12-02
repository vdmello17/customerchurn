import streamlit as st
import sqlite3
import pandas as pd
import os

# Path to your SQLite database file
DB_PATH = "customer churn db.db"

# Function to check if the database file exists
def check_db_exists():
    if not os.path.exists(DB_PATH):
        st.error(f"Database file not found at {DB_PATH}")
        return False
    return True

# Function to connect to the database and get all table names
def get_table_names():
    if not check_db_exists():
        return []
    
    conn = sqlite3.connect(DB_PATH)
    try:
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql(query, conn)
        conn.close()
        return tables['name'].tolist()
    except sqlite3.Error as e:
        conn.close()
        st.error(f"SQLite error: {e}")
        return []
    except Exception as e:
        conn.close()
        st.error(f"General error: {str(e)}")
        return []

# Function to fetch data from a selected table
def get_data_from_table(table_name):
    if not check_db_exists():
        return None
    
    conn = sqlite3.connect(DB_PATH)
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        conn.close()
        st.error(f"SQLite error: {e} when fetching data from {table_name}")
        return None
    except Exception as e:
        conn.close()
        st.error(f"General error: {str(e)} when fetching data from {table_name}")
        return None

# Function to execute a custom SQL query
def execute_query(query):
    if not check_db_exists():
        return None

    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        conn.close()
        st.error(f"SQLite error: {e} when executing query: {query}")
        return None
    except Exception as e:
        conn.close()
        st.error(f"General error: {str(e)} when executing query: {query}")
        return None

# Streamlit App
st.title("Database Query Interface")

# Display all tables as buttons
st.header("Choose a table to view")
tables = get_table_names()

if tables:  # Check if tables are fetched successfully
    for table in tables:
        if st.button(table):
            data = get_data_from_table(table)
            if data is not None:
                st.write(f"### Data from the '{table}' table")
                st.dataframe(data)
else:
    st.warning("No tables found in the database.")

# Allow users to enter a custom SQL query
st.header("Custom SQL Query")

query_input = st.text_area("Enter your SQL query:")

if st.button("Run Query"):
    if query_input:
        result = execute_query(query_input)
        if result is not None:
            st.write("### Query Result:")
            st.dataframe(result)
        else:
            st.error("Query execution failed. Please check the SQL syntax or table names.")
    else:
        st.warning("Please enter a SQL query to run.")
