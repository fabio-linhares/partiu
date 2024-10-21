import streamlit as st
import json
from api import api_request_cached


def exibir_api_teste():
    operation = st.selectbox("Select operation", ["Create", "Read", "Update", "Delete", "Get Main Collection"])

    if operation == "Create":
        collection = st.text_input("Collection name")
        data = st.text_area("Document data (JSON format)")
        if st.button("Create Document"):
            try:
                json_data = json.loads(data)
                result = api_request_cached("POST", f"/create/{collection}", {"data": json_data})
                if result:
                    st.success(f"Document created with ID: {result['id']}")
            except json.JSONDecodeError:
                st.error("Invalid JSON format")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    elif operation == "Read":
        collection = st.text_input("Collection name")
        limit = st.number_input("Limit", min_value=1, value=10)
        if st.button("Read Documents"):
            try:
                result = api_request_cached("GET", f"/read/{collection}?limit={limit}")
                if result:
                    st.json(result)
                else:
                    st.warning("No documents found or empty result.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                if hasattr(e, 'response'):
                    st.error(f"Response content: {e.response.content}")

    elif operation == "Update":
        collection = st.text_input("Collection name")
        doc_id = st.text_input("Document ID")
        data = st.text_area("Updated data (JSON format)")
        if st.button("Update Document"):
            try:
                json_data = json.loads(data)
                result = api_request_cached("PUT", f"/update/{collection}/{doc_id}", {"data": json_data})
                if result:
                    st.success("Document updated successfully")
            except json.JSONDecodeError:
                st.error("Invalid JSON format")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    elif operation == "Delete":
        collection = st.text_input("Collection name")
        doc_id = st.text_input("Document ID")
        if st.button("Delete Document"):
            try:
                result = api_request_cached("DELETE", f"/delete/{collection}/{doc_id}")
                if result:
                    st.success("Document deleted successfully")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    elif operation == "Get Main Collection":
        if st.button("Get Main Collection"):
            try:
                result = api_request_cached("GET", "/main_collection")
                if result:
                    st.json(result)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

