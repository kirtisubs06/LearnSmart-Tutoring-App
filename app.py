import os

import streamlit as st
from langchain.llms import AzureOpenAI
from langchain import LLMMathChain
from streamlit.runtime.state import NoValue

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
    print(question)
    show_question(label, question)
    # Get answer
    answer = get_answer(skill)
    print(answer)
    # Submit button
    show_submit()
    # Evaluate the answer
    evaluate(topic, skill, question, answer)


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
    topic = Topic.from_value(st.sidebar.selectbox(
        "Select a topic:",
        [topic.value for topic in Topic]))
    return topic


def get_skill(topic):
    skill = None
    if topic is Topic.ENGLISH:
        skill = EnglishSkill.from_value(st.sidebar.selectbox(
            "Select a skill:",
            [skill.value for skill in EnglishSkill]
        ))
    elif topic is Topic.MATH:
        skill = MathSkill.from_value(st.sidebar.selectbox(
            "Select a skill:",
            [skill.value for skill in MathSkill]
        ))
    return skill


def get_level():
    level = Level.from_value(st.sidebar.selectbox(
        "Select a difficulty level:",
        [level.value for level in Level]))
    return level


def initialize_session(topic, skill, level):
    session_start = "topic" not in st.session_state or \
                    "skill" not in st.session_state or \
                    "level" not in st.session_state
    topic_changed = st.session_state.get("topic") != topic
    skill_changed = st.session_state.get("skill") != skill
    level_changed = st.session_state.get("level") != level

    st.session_state["topic"] = topic
    st.session_state["skill"] = skill
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
    st.session_state["numeric_answer"] = 0.0


def get_question(topic, skill, level):
    # Get the generated question from LLM
    response = llm(skill.question_generation_prompt.format(level=level))
    # Parse the response and get the label and the text
    label, question = process_question(skill, response)
    st.session_state["question"] = (label, question)
    return label, question


def show_question(label, question):
    st.write(f"**{label}**")
    st.write(question)


def process_question(skill, question):
    if not question:
        return None, None

    label, text = question.split(":", 1)
    return label.strip(), text.strip()


def get_answer(skill):
    if skill is EnglishSkill.WRITING or skill is EnglishSkill.READING:
        answer = st.text_area(label="Answer", key="answer")
    elif skill is MathSkill.ARITHMETIC:
        answer = st.number_input(label="Answer", key="numeric_answer", step=None, value=NoValue())
    else:
        answer = st.text_input(label="Answer", key="answer")

    return answer


def show_submit():
    return st.button(f"Submit", type="primary")


def evaluate(topic, skill, question, answer):
    if not answer:
        return
    if topic is Topic.MATH:
        evaluate_math(skill, question, answer)
    elif topic is Topic.ENGLISH:
        evaluate_english(skill, question, answer)


def evaluate_math(skill, question, answer):
    llm_math = LLMMathChain.from_llm(llm, verbose=True)
    response = llm_math.run(question)
    key, value = response.split(":", 1)
    answer, value = round(float(answer), 2), round(float(value), 2)
    score = 1.0 if answer == value else 0.0
    response = f"Score: {score}\nCorrect answer: {value}"
    process_response(skill, response)


def evaluate_english(skill, question, answer):
    response = llm(skill.answer_evaluation_prompt.format(question=question, answer=answer))
    process_response(skill, response)


def process_response(skill, response):
    key = ""
    value = ""
    for line in response.splitlines():
        if ':' in line:
            if value:
                process(skill, key.strip(), value.strip())
            key, value = line.split(":", 1)
        else:
            value += line

    if value:
        process(skill, key.strip(), value.strip())


def process(skill, key, value):
    if key == "Score":
        process_score(value)
    else:
        st.write(f"**{key}:**")
        st.write(value)


def process_score(value):
    score = float(value)
    print("Score:", score)
    if 0.0 <= score <= 0.5:
        st.error("Keep trying. You can do better!")
    elif 0.5 < score <= 0.8:
        st.warning("Good job! Almost there.")
    else:
        st.success("Great job!")


if __name__ == "__main__":
    main()
