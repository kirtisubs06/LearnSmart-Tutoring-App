import os

import streamlit as st


def main():
    """
    The main function that serves as the entry point for the Streamlit application.
    """
    st.set_page_config(page_title="Learning Smart", layout="wide")
    set_env()
    homepage()



def set_env():
    os.environ["OPENAI_API_TYPE"] = st.secrets["OPENAI_API_TYPE"]
    os.environ["OPENAI_API_BASE"] = st.secrets["OPENAI_API_BASE"]
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["MODEL_NAME"] = st.secrets["MODEL_NAME"]
    os.environ["DEPLOYMENT_NAME"] = st.secrets["DEPLOYMENT_NAME"]
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
    os.environ["SQL_DATABASE"] = st.secrets["SQL_DATABASE"]
    os.environ["SQL_USERNAME"] = st.secrets["SQL_USERNAME"]
    os.environ["SQL_PASSWORD"] = st.secrets["SQL_PASSWORD"]
    os.environ["MYSQL_CONNECTION_STRING"] = st.secrets["MYSQL_CONNECTION_STRING"]


def homepage():
    """
    The homepage function represents the main user interface of the Streamlit application.
    """
    # Show title and intro
    show_app_title_and_introduction()


def show_app_title_and_introduction():
    st.title("Welcome to LearnSmart!")


if __name__ == "__main__":
    main()