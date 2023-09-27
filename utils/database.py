import streamlit as st
import pymongo

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection(ttl=3600):
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data(collection: str, query = None):
    db = client["python-konkurs"]

    if query is None:
        items = db[collection].find()
    else:
        items = db[collection].find(query)

    items = list(items)
    return items

def insert_data(collection: str, dict):
    db = client["python-konkurs"]
    result = db[collection].insert_one(dict)
    return result.inserted_id
