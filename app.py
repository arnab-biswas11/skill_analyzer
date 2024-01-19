# Importing the Streamlit library
import streamlit as st
from src.data_extractor.web_scapper import web_scrap

# The main function for the Streamlit app
def main():
    st.title("Skill Analyzer")
    user_input = st.text_input("Enter role:")

    op = web_scrap(job_title=user_input).extract_jobs()

    st.write("parsed:", op)

# Run the app
if __name__ == "__main__":
    main()