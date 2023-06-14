import os
import tempfile

import streamlit as st
from langchain.llms import AzureOpenAI
from langchain import LLMMathChain
from matplotlib import pyplot as plt

import prompts
from progresstracker import ProgressTracker
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


def main():
    st.set_page_config(page_title="Learning Smart", layout="wide")
    set_env()
    llm = load_llm(0.9)
    stats = Stats()
    stats.connect()
    homepage(llm, stats)


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
    os.environ["EMAIL_ID"] = st.secrets["EMAIL_ID"]
    os.environ["EMAIL_PASSWORD"] = st.secrets["EMAIL_PASSWORD"]


def homepage(llm, stats):
    show_app_title_and_introduction(stats)
    topic, skill, level = show_sidebar(llm)
    topic_changed, skill_changed, level_changed = \
        initialize_session(stats, topic, skill, level)
    show_lesson(skill)

    label = st.session_state["question"][0]
    question = st.session_state["question"][1]
    next_challenge = st.session_state["next_challenge"]
    if next_challenge or topic_changed or skill_changed or level_changed:
        clear_answer()
        label, question = get_question(llm, stats, skill, level)
        clear_next_challenge()
    show_question(skill, label, question)
    answer = get_answer(skill)
    show_submit_and_next_challenge()
    evaluate(llm, topic, skill, question, answer)
    show_stats_and_rating(stats)
    show_progress_tracking(llm)
    show_copyright()


def show_app_title_and_introduction(stats):
    total_challenges = stats.get_total_counters()
    total_sessions = stats.get_session_counter()
    st.title("Welcome to LearnSmart!")
    st.write(f"""
        LearnSmart is an interactive app that helps you enhance your English and Math skills. 
        Dive into a collection of practice exercises, covering various skills, to strengthen your knowledge 
        and understanding of these subjects.

        Whether you're a student or someone wanting to sharpen your skills, LearnSmart provides a comprehensive 
        learning experience. From grammar and vocabulary to problem-solving and mathematical concepts, explore 
        a wide range of topics and level up your abilities. Join hundreds of learners who have completed 
        **{total_sessions}** sessions and conquered **{total_challenges}** challenges. 
        
        Start your learning journey with LearnSmart today and unlock your full potential in English and Math!
    """)


def show_sidebar(llm):
    st.sidebar.title("LearnSmart")
    topic = get_topic()
    skill = get_skill(topic)
    level = get_level()
    return topic, skill, level


def show_progress_tracking(llm):
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.header("Session Scores")
    name = get_name()
    email = get_email()
    send = show_send_summary()
    session_scores = ProgressTracker.get_session_scores()
    print(session_scores)
    if send:
        if session_scores is not None:
            feedback = llm(prompts.ASSESSMENT_FEEDBACK_PROMPT.format(
                session_scores=ProgressTracker.get_session_scores()))
            if ":" in feedback:
                label, feedback = feedback.split(":", 1)
            print(feedback)
            ProgressTracker.send_summary(name, email, feedback)
    st.sidebar.markdown(ProgressTracker.get_summary_text(), unsafe_allow_html=True)


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


def get_name():
    return st.sidebar.text_input(label="Name:", key="name")


def get_email():
    return st.sidebar.text_input(label="Email:", key="email")


def initialize_session(stats, topic, skill, level):
    session_start = "topic" not in st.session_state or \
                    "skill" not in st.session_state or \
                    "level" not in st.session_state
    stats.increment_session_counter()
    topic_changed = st.session_state.get("topic") != topic
    skill_changed = st.session_state.get("skill") != skill
    level_changed = st.session_state.get("level") != level

    st.session_state["topic"] = topic
    st.session_state["skill"] = skill
    st.session_state["level"] = level

    if session_start:
        st.session_state["question"] = None, None
        st.session_state["next_challenge"] = True

    return topic_changed, skill_changed, level_changed


def show_lesson(skill):
    st.header(skill.value)
    st.markdown(f"_{skill.description}_")


def show_next_challenge():
    return st.button(f"Next challenge", on_click=clear_answer, type="primary")


def show_send_summary():
    return st.sidebar.button(f"Send summary", type="primary")


def clear_answer():
    st.session_state["answer"] = ""
    st.session_state["numeric_answer"] = 0.0
    st.session_state["next_challenge"] = True


def clear_next_challenge():
    st.session_state["next_challenge"] = False


def get_question(llm, stats, skill, level):
    stats.increment_stats_counters(skill, level)
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


def show_submit_and_next_challenge():
    col1, col2, col3 = st.columns((1, 2, 7))
    with col1:
        st.button(f"Submit", type="primary")
    with col2:
        show_next_challenge()


def evaluate(llm, topic, skill, question, answer):
    if not answer:
        return
    if topic is Topic.MATH:
        evaluate_math(llm, skill, question, answer)
    elif topic is Topic.ENGLISH:
        evaluate_english(llm, skill, question, answer)


def evaluate_math(llm, skill, question, answer):
    response = ""
    if skill is MathSkill.ARITHMETIC:
        llm_math = LLMMathChain.from_llm(llm, verbose=True)
        response = llm_math.run(question)
        key, value = response.split(":", 1)
        answer, value = round(float(answer), 2), round(float(value), 2)
        score = 1.0 if answer == value else 0.0
        response = f"Score: {score}\nCorrect answer: {value}"
    process_response(skill, question, answer, response)


def evaluate_english(llm, skill, question, answer):
    response = llm(skill.answer_evaluation_prompt.format(question=question, answer=answer))
    process_response(skill, question, answer, response)


def process_response(skill, question, answer, response):
    key = ""
    value = ""
    for line in response.splitlines():
        if ':' in line:
            if value:
                process(skill, question, answer, key.strip(), value.strip())
            key, value = line.split(":", 1)
        else:
            value += line

    if value:
        process(skill, question, answer, key.strip(), value.strip())


def process(skill, question, answer, key, value):
    if key == "Score":
        points = process_score(value)
        ProgressTracker.add_skill_track(skill, points)
    else:
        st.write(f"**{key}:**")
        st.write(value)


def process_score(value):
    score = float(value)
    print("Score:", score)
    points = 0
    if 0.0 <= score <= 0.5:
        st.error("Keep trying! You can do better!")
    elif 0.5 < score <= 0.8:
        st.warning("Good job! Almost there!")
        points = 0.5
    else:
        st.success("Great job!")
        points = 1
    return points


def show_app_stats(stats):
    """
    Display the app stats in the main section.
    """
    st.markdown("<h1 style='font-size: 24px;'>App Stats</h1>", unsafe_allow_html=True)
    counter_dict = stats.get_counters()

    # Consolidate the counters by skill only
    data = []
    for skill in list(MathSkill) + list(EnglishSkill):
        skill_count = sum(counter_dict.get((skill.value, level.value), 0) for level in Level)
        data.append((skill.value, skill_count))

    # Extract the skill and count data
    skills, counts = zip(*data)

    # Create a wider bar chart
    plt.figure(figsize=(15, 6))  # Increase the width to 15 inches

    plt.bar(skills, counts, color='#4e98e0')

    # Customize the chart
    plt.xlabel('Skill', fontsize=14)  # Increase the font size for x-axis label
    plt.ylabel('Count', fontsize=14)  # Increase the font size for y-axis label
    plt.title('App Stats', fontsize=16)  # Increase the font size for title
    plt.xticks(rotation=45, fontsize=18)  # Increase the font size for x-axis tick labels
    plt.yticks(fontsize=18)  # Increase the font size for y-axis tick labels
    plt.tight_layout()

    # Display the bar chart
    st.pyplot(plt)

    # Display skill and count as text line by line
    text = ""
    for skill, count in zip(skills, counts):
        text += f"<span style='font-size: smaller;'>{skill}: <b>{count}</b> challenges</span><br>"
    st.markdown(text, unsafe_allow_html=True)


def show_review_form(stats):
    st.markdown("<h1 style='font-size: 24px;'>Rate App</h1>", unsafe_allow_html=True)
    rating = st.slider("Scale", 1, 5, 3, key="slider_rating", format="%d",
                       help="Drag the slider to rate the app")
    comment = st.text_input("Please leave any comments or suggestions for improvement:")
    if st.button("Submit Review", key="submit", type="primary"):
        if rating > 0:
            stats.add_review(rating, comment)
            st.success("Thank you for your review!")
        else:
            st.warning("Please select a star rating before submitting.")


# Display the review stats
def show_review_stats(stats):
    num_reviews, avg_rating = stats.get_review_stats()
    st.write(
        f'<span style="font-size: smaller;">Average rating: **{avg_rating} ({num_reviews}** reviews)</span>',
        unsafe_allow_html=True)
    st.write('<span style="font-size: smaller;">★</span>' * int(
        round(avg_rating)) + '<span style="font-size: smaller;">☆</span>' * int(5 - round(avg_rating)),
             unsafe_allow_html=True)


def show_reviews(stats):
    st.markdown("<h1 style='font-size: 24px;'>Reviews</h1>", unsafe_allow_html=True)
    top_reviews = stats.get_top_reviews()
    for review in top_reviews:
        rating_stars = '<span style="font-size: smaller;">★</span>' * int(round(review[0]))
        review = f'<span style="font-size: smaller;">{review[1]}</span>'
        st.write(f"{rating_stars} {review}", unsafe_allow_html=True)


def show_stats_and_rating(stats):
    # Define the column layout
    col1, col2, col3, col4, col5 = st.columns((4, 0.5, 2.5, 0.5, 3))

    # Display the usage stats in the columns
    with col1:
        show_app_stats(stats)
    with col3:
        show_review_form(stats)
        show_review_stats(stats)
    with col5:
        show_reviews(stats)


def show_copyright():
    footer_html = """
            <div style="position: absolute; bottom: 0; width: 100%; text-align: center; color: gray;">
                <p style="font-size: 12px;">© 2023 LEARNSMART TUTORING LLC. All rights reserved.</p>
            </div>
            """

    st.markdown(footer_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
