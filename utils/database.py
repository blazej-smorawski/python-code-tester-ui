import pymongo.server_api
import streamlit as st
import pymongo


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection(ttl=3600):
    return pymongo.MongoClient(st.secrets["mongo"]["uri"], server_api=pymongo.server_api.ServerApi('1'))

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=1)
def get_data(collection: str, query = None):
    db = client[st.secrets["mongo"]["collection"]]

    if query is None:
        items = db[collection].find()
    else:
        items = db[collection].find(query)

    items = list(items)
    return items

def insert_data(collection: str, dict, keep_id=False):
    db = client[st.secrets["mongo"]["collection"]]
    result = db[collection].insert_one(dict)
    if not keep_id:
        del dict['_id']
    return result.inserted_id

def replace_data(collection: str, dict):
    db = client[st.secrets["mongo"]["collection"]]
    result = db[collection].replace_one({"_id": dict["_id"]}, dict)
    