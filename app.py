# Importing the Streamlit library
import streamlit as st

# The main function for the Streamlit app
def main():
    # Title of the web app
    st.title("Simple Streamlit App")

    # A text input for the user to enter text
    user_input = st.text_input("Enter some text:")

    # Display the entered text
    st.write("You entered:", user_input)

# Run the app
if __name__ == "__main__":
    main()