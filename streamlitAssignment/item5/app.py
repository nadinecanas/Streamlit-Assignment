# mysql_data_pipeline.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text


# DATABASE CONFIGURATION — Replace with your own
DB_USER = 'root'
DB_PASSWORD = None
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'streamlit_demo'

# Connect to MySQL database
@st.cache_resource
def get_connection():
    if DB_PASSWORD is None:
        connection_url = f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        connection_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    engine = create_engine(connection_url)
    return engine

engine = get_connection()

# BONUS: Simple Authentication
st.sidebar.header("🔐 User Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

def authenticate(user, pwd):
    # VERY basic check — replace with real user table in production!
    return user == "admin" and pwd == "admin123"

if authenticate(username, password):
    st.success(f"Welcome, {username}!")

    # Main content
    st.title("📊 Data Pipeline with MySQL Database")

    # Fetch and filter data
    st.subheader("📥 View Existing Records")
    table_name = st.selectbox("Select table to view", ["employees", "departments"])  # Example tables

    filter_query = st.text_input("Optional SQL filter (e.g., department = 'Sales')")

    query = f"SELECT * FROM {table_name}"
    if filter_query.strip():
        query += f" WHERE {filter_query}"

    with engine.connect() as conn:
        result_df = pd.read_sql(text(query), conn)

    st.dataframe(result_df)

    # Insert new row with form
    st.subheader(f"➕ Add New Record to `{table_name}`")

    with st.form(key='insert_form'):
        if table_name == 'employees':
            emp_name = st.text_input("Employee Name")
            emp_age = st.number_input("Age", min_value=18, max_value=100, step=1)
            emp_dept = st.text_input("Department")
            submit = st.form_submit_button("Insert Employee")

            if submit:
                insert_query = text("""
                    INSERT INTO employees (name, age, department) VALUES (:name, :age, :dept)
                """)
                with engine.connect() as conn:
                    conn.execute(insert_query, {"name": emp_name, "age": emp_age, "dept": emp_dept})
                    conn.commit()
                st.success("✅ New employee inserted!")

        elif table_name == 'departments':
            dept_name = st.text_input("Department Name")
            location = st.text_input("Location")
            submit = st.form_submit_button("Insert Department")

            if submit:
                insert_query = text("""
                    INSERT INTO departments (name, location) VALUES (:name, :location)
                """)
                with engine.connect() as conn:
                    conn.execute(insert_query, {"name": dept_name, "location": location})
                    conn.commit()
                st.success("✅ New department inserted!")

else:
    st.warning("Please enter valid credentials to access the app.")

