import os
import tempfile

import streamlit as st
from langchain.llms import AzureOpenAI
from langchain import LLMMathChain

from level import Level
from skill import EnglishSkill, MathSkill
from stats import Stats
from topic import Topic

from gtts import gTTS


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


def get_stats():
    return Stats()


llm = load_llm(0.9)
stats = get_stats()


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
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
    os.environ["SQL_SERVER"] = st.secrets["SQL_SERVER"]
    os.environ["SQL_DATABASE"] = st.secrets["SQL_DATABASE"]
    os.environ["SQL_USERNAME"] = st.secrets["SQL_USERNAME"]
    os.environ["SQL_PASSWORD"] = st.secrets["SQL_PASSWORD"]
    os.environ["MYSQL_CONNECTION_STRING"] = st.secrets["MYSQL_CONNECTION_STRING"]


def homepage():
    show_app_title_and_introduction()
    show_sidebar()
    topic = get_topic()
    skill = get_skill(topic)
    level = get_level()
    session_start, topic_changed, skill_changed, level_changed = \
        initialize_session(topic, skill, level)
    show_lesson(skill)
    next_challenge = show_next_challenge()
    label = st.session_state["question"][0]
    question = st.session_state["question"][1]
    if next_challenge or session_start or topic_changed or skill_changed or level_changed:
        clear_answer()
        label, question = get_question(skill, level)
    show_question(skill, label, question)
    answer = get_answer(skill)
    show_submit()
    evaluate(topic, skill, question, answer)


def show_app_title_and_introduction():
    st.title("Welcome to LearnSmart!")
    st.write(f"""
        LearnSmart is a tool to enhance your English and Math skills!

        It is an interactive app that helps you learn and improve your proficiency in English and Math. 
        Dive straight into a vast collection of practice exercises, covering a wide range of skills,
        to strengthen your knowledge and understanding of these subjects.

        Whether you're a student looking to excel in school or someone wanting to sharpen your skills, 
        LearnSmart provides a comprehensive learning experience. From grammar and vocabulary to 
        problem-solving and mathematical concepts, explore a wide range of topics and level up your 
        abilities.

        With interactive exercises and real-time feedback, you can track your progress and identify areas 
        for improvement. LearnSmart is your go-to tool for mastering English and Math in an enjoyable and 
        effective way. 

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


def show_lesson(skill):
    st.header(skill.value)
    st.markdown(f"_{skill.description}_")


def show_next_challenge():
    return st.button(f"Next challenge", on_click=clear_answer, type="primary")


def clear_answer():
    st.session_state["answer"] = ""
    st.session_state["numeric_answer"] = 0.0


def get_question(skill, level):
    response = llm(skill.question_generation_prompt.format(level=level))
    label, question = process_question(response)
    st.session_state["question"] = (label, question)
    return label, question


def show_question(skill, label, question):
    if skill is EnglishSkill.SPELLING:
        audio_display(question)
    else:
        st.write(f"**{label}**")
        st.write(question)


def audio_display(question):
    tts = gTTS(question)
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_filename = temp_file.name
    temp_file.close()
    tts.save(temp_filename)

    # Generate a unique ID for the audio element
    audio_id = st.empty().audio(temp_filename, format='audio/wav')

    # Function to handle the button click event
    def play_audio():
        with open(temp_filename, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        audio_id.audio(audio_bytes, format='audio/wav')


def process_question(question):
    if not question:
        return None, None

    label, text = question.split(":", 1)
    return label.strip(), text.strip()


def get_answer(skill):
    if skill is EnglishSkill.WRITING or skill is EnglishSkill.READING:
        answer = st.text_area(label="Answer", key="answer")
    elif skill is MathSkill.ARITHMETIC:
        answer = st.number_input(label="Answer", key="numeric_answer")
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
    response = ""
    if skill is MathSkill.ARITHMETIC:
        llm_math = LLMMathChain.from_llm(llm, verbose=True)
        response = llm_math.run(question)
        key, value = response.split(":", 1)
        answer, value = round(float(answer), 2), round(float(value), 2)
        score = 1.0 if answer == value else 0.0
        response = f"Score: {score}\nCorrect answer: {value}"
    process_response(response)


def evaluate_english(skill, question, answer):
    response = llm(skill.answer_evaluation_prompt.format(question=question, answer=answer))
    process_response(response)


def process_response(response):
    key = ""
    value = ""
    for line in response.splitlines():
        if ':' in line:
            if value:
                process(key.strip(), value.strip())
            key, value = line.split(":", 1)
        else:
            value += line

    if value:
        process(key.strip(), value.strip())


def process(key, value):
    if key == "Score":
        process_score(value)
    else:
        st.write(f"**{key}:**")
        st.write(value)


def process_score(value):
    score = float(value)
    print("Score:", score)
    if 0.0 <= score <= 0.5:
        st.error("Keep trying! You can do better!")
    elif 0.5 < score <= 0.8:
        st.warning("Good job! Almost there!")
    else:
        st.success("Great job!")


if __name__ == "__main__":
    main()
