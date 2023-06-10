import json
import os

import streamlit as st
from langchain.llms import AzureOpenAI

from level import Level
from skill import EnglishSkill, MathSkill
from topic import Topic


def load_llm(temperature):
    os.environ["OPENAI_API_TYPE"] = st.secrets["OPENAI_API_TYPE"]
    os.environ["OPENAI_API_BASE"] = st.secrets["OPENAI_API_BASE"]
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["DEPLOYMENT_NAME"] = st.secrets["DEPLOYMENT_NAME"]
    os.environ["OPENAI_API_VERSION"] = st.secrets["OPENAI_API_VERSION"]
    os.environ["MODEL_NAME"] = st.secrets["MODEL_NAME"]
    return AzureOpenAI(temperature=temperature,
                       deployment_name=os.environ["DEPLOYMENT_NAME"],
                       model_name=os.environ["MODEL_NAME"])


llm = load_llm(0.9)


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
    # Initialize session
    session_start, topic_changed, skill_changed, level_changed = \
        initialize_session(topic, skill, level)
    # Show the lesson
    show_lesson(topic, skill, level)
    # Show next button
    button_clicked = show_next_challenge()
    label = st.session_state["question"][0]
    question = st.session_state["question"][1]
    # If this is the start of a session or the "next challenge" button was clicked
    # generate the question
    if button_clicked or session_start or topic_changed or skill_changed or level_changed:
        clear_answer()
        label, question = get_question(topic, skill, level)
    # Show question
    show_question(label, question)
    # Get answer
    answer = get_answer()
    # Evaluate the answer
    evaluate(skill, question, answer)


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


def get_topic():
    topic = st.sidebar.selectbox(
        "Select a topic:",
        [topic.value for topic in Topic])
    return topic


def get_skill(topic):
    skill = None
    if topic is Topic.ENGLISH.value:
        skill = EnglishSkill.from_value(st.sidebar.selectbox(
            "Select a skill:",
            [skill.value for skill in EnglishSkill]
        ))
    elif topic is Topic.MATH.value:
        skill = MathSkill.from_value(st.sidebar.selectbox(
            "Select a skill:",
            [skill.value for skill in MathSkill]
        ))
    return skill


def get_level():
    level = st.sidebar.selectbox(
        "Select a difficulty level:",
        [level.value for level in Level])
    return level


def initialize_session(topic, skill, level):
    session_start = False
    topic_changed = False
    skill_changed = False
    level_changed = False

    if "topic" not in st.session_state:
        session_start = True
        st.session_state["topic"] = topic
    elif st.session_state["topic"] != topic:
        topic_changed = True
        st.session_state["topic"] = topic

    if "skill" not in st.session_state:
        session_start = True
        st.session_state["skill"] = skill
    elif st.session_state["skill"] != skill:
        skill_changed = True
        st.session_state["skill"] = skill

    if "level" not in st.session_state:
        session_start = True
        st.session_state["level"] = level
    elif st.session_state["level"] != level:
        level_changed = True
        st.session_state["level"] = level

    if session_start:
        st.session_state["question"] = None, None
    return session_start, topic_changed, skill_changed, level_changed


def show_lesson(topic, skill, level):
    st.header(skill.value)
    st.markdown(f"_{skill.description}_")


def show_next_challenge():
    return st.button(f"Next challenge", on_click=clear_answer, type="primary")


def clear_answer():
    st.session_state["answer"] = ""


def get_question(topic, skill, level):
    # Get the generated question from LLM
    response = llm(skill.question_generation_prompt.format(level=level))
    # Parse the response and get the label and the text
    label, question = process_question(skill, response)
    st.session_state["question"] = (label, question)
    return label, question


def show_question(label, question):
    # Display
    st.write(f"**{label}**")
    st.write(question)


def process_question(skill, question):
    print(question)
    if not question:
        return

    keywords = []
    if skill is EnglishSkill.VOCABULARY:
        keywords = ["Word:", "Word "]
    elif skill is EnglishSkill.GRAMMAR:
        keywords = ["Sentence:", "Sentence "]

    lines = question.splitlines()

    for line in lines:
        for keyword in keywords:
            if line.startswith(keyword):
                word = line[len(keyword):].strip()
                return keyword.strip(), word

    return None


def get_answer():
    answer = st.text_input(label="Answer", key="answer")
    return answer


def evaluate(skill, question, answer):
    if not answer:
        return
    response = llm(skill.answer_evaluation_prompt.format(question=question, answer=answer))
    print(response)
    lines = response.splitlines()
    for line in lines:
        if len(line) <= 0:
            continue

        key, value = line.split(":", 1)
        process(skill, key, value)


def process(skill, key, value):
    if key == "Score":
        score = float(value)
        if 0.0 <= score <= 0.5:
            st.error("Keep trying. You can do better!")
        elif 0.5 < score <= 0.8:
            st.warning("Good job! Almost there.")
        else:
            st.success("Great job!")

    if skill is EnglishSkill.VOCABULARY:
        if key == "Solution":
            st.write("**Meaning:**")
            st.write(value)
        elif key == "Misc":
            st.write("**Usage:**")
            st.write(value)
    elif skill is EnglishSkill.GRAMMAR:
        if key == "Solution":
            st.write("**Correct Answer:**")
            st.write(value)
        elif key == "Misc":
            st.write("**Analysis:**")
            st.write(value)


if __name__ == "__main__":
    main()
