import os

import streamlit as st

from level import Level
from skill import EnglishSkill, MathSkill
from topic import Topic


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
    # Show sidebar
    show_sidebar()
    # Get the selected topic
    topic = get_topic()
    # Get the selected Skill
    skill = get_skill(topic)
    # Get the selected level
    level = get_level()


def get_topic():
    topic = st.sidebar.selectbox(
        "Select a topic:",
        [topic.value for topic in Topic])
    return topic


def get_skill(topic):
    skill = None
    if topic is Topic.ENGLISH.value:
        skill = st.sidebar.selectbox(
            "Select a skill:",
            [skill.value for skill in EnglishSkill]
        )
    elif topic is Topic.MATH.value:
        skill = st.sidebar.selectbox(
            "Select a skill:",
            [skill.value for skill in MathSkill]
        )
    return skill


def get_level():
    level = st.sidebar.selectbox(
        "Select a difficulty level:",
        [level.value for level in Level])
    return level


def show_app_title_and_introduction():
    st.title("Welcome to LearnSmart!")
    st.write(f"""
            LearnSmart is a tool to enhance your English and Math skills!

            It is an interactive app that helps you learn and improve your proficiency in English and Math. 
            Dive into engaging lessons, practice exercises, and quizzes to strengthen your knowledge and 
            understanding of these subjects.

            Whether you're a student looking to excel in school or someone wanting to sharpen your skills, 
            LearnSmart provides a comprehensive learning experience. From grammar and vocabulary to 
            problem-solving and mathematical concepts, explore a wide range of topics and level up your 
            abilities.

            With interactive exercises and real-time feedback, you can track your progress and identify areas 
            for improvement. LearnSmart is your go-to tool for mastering English and Math in an enjoyable and 
            effective way. Join hundreds of learners who have already completed 0 
            sessions and conquered 0 challenges on their learning journey.

            Start your learning journey with LearnSmart today and unlock your full potential in English and Math!
        """)


def show_sidebar():
    st.sidebar.title("LearnSmart")


if __name__ == "__main__":
    main()
