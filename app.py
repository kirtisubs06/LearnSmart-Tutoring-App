import os
import random
import tempfile

import streamlit as st
from langchain.llms import AzureOpenAI
from langchain import LLMMathChain
from matplotlib import pyplot as plt

import prompts
from defaultquestions import default_questions
from progresstracker import ProgressTracker
from level import Level
from skill import EnglishSkill, MathSkill
from stats import Stats
from topic import Topic
from gtts import gTTS


def load_llm(api_key, temperature):
    os.environ["OPENAI_API_TYPE"] = st.secrets["OPENAI_API_TYPE"]
    os.environ["OPENAI_API_BASE"] = st.secrets["OPENAI_API_BASE"]
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["DEPLOYMENT_NAME"] = st.secrets["DEPLOYMENT_NAME"]
    os.environ["OPENAI_API_VERSION"] = st.secrets["OPENAI_API_VERSION"]
    os.environ["MODEL_NAME"] = st.secrets["MODEL_NAME"]
    return AzureOpenAI(temperature=temperature,
                       deployment_name=os.environ["DEPLOYMENT_NAME"],
                       model_name=os.environ["MODEL_NAME"])


def get_api_key():
    return st.secrets["OPENAI_API_KEY"]


def main():
    st.set_page_config(page_title="Learning Smart", layout="wide")
    set_env()
    stats = Stats()
    stats.connect()
    api_key = stats.get_api_key("openai")
    llm = load_llm(api_key, 0.9)
    homepage(llm, stats)
    stats.close()


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
    initialize_llm_exception_flag(llm)
    topic, skill, level = show_sidebar(llm)

    # Handle the case when default options are selected
    if topic is None or skill is None or level is None:
        st.sidebar.warning("Please select a topic, skill, and level to continue.")
        return

    topic_changed, skill_changed, level_changed = \
        initialize_session(stats, topic, skill, level)
    show_lesson(skill)
    label = st.session_state["question"][0]
    question = st.session_state["question"][1]
    next_challenge = st.session_state["next_challenge"]
    name_or_email_changed = st.session_state["name_or_email_changed"]
    if next_challenge or topic_changed or skill_changed or level_changed:
        clear_answer()
        label, question = get_question(llm, stats, skill, level)
        clear_next_challenge()
    show_question(skill, label, question)
    print("Question", question)
    answer = get_answer(skill)
    show_submit_and_next_challenge()
    if not name_or_email_changed:
        evaluate(llm, topic, skill, question, answer)
    show_summary()
    show_stats_and_rating(stats)
    show_progress_tracking(llm)
    show_copyright()


def initialize_llm_exception_flag(llm):
    if 'llm_exception' not in st.session_state:
        st.session_state['llm_exception'] = False
    test_skill = EnglishSkill.VOCABULARY
    test_level = Level.EASY
    try:
        llm(test_skill.question_generation_prompt.format(level=test_level))
    except Exception as e:
        print(e)
        st.session_state['llm_exception'] = True


def show_app_title_and_introduction(stats):
    total_challenges = stats.get_total_counters()
    total_sessions = stats.get_session_counter()
    st.title("Welcome to LearnSmart!")
    st.markdown(f"""
        <p>LearnSmart is an interactive app that helps you enhance your English and Math skills. 
        Dive into a collection of practice exercises, covering various skills, to strengthen your knowledge 
        and understanding of these subjects.</p>

        <p>Whether you're a student or someone wanting to sharpen your skills, LearnSmart provides a comprehensive 
        learning experience. From grammar and vocabulary to problem-solving and mathematical concepts, explore 
        a wide range of topics and level up your abilities. Join hundreds of learners who have completed 
        <span style='font-size: 20px;'><b>{total_sessions}</b></span> sessions and conquered 
        <span style='font-size: 20px;'><b>{total_challenges}</b></span> challenges.</p>

        <p>Start your learning journey with LearnSmart today and unlock your full potential in English and Math!</p>
        """, unsafe_allow_html=True)


def show_sidebar(llm):
    st.sidebar.title("LearnSmart")
    topic = get_topic()
    skill = get_skill(topic)
    level = get_level()
    return topic, skill, level


def show_summary():
    session_scores = ProgressTracker.get_session_scores()
    if session_scores is not None:
        st.markdown("<hr style='margin-top: 0.5em; margin-bottom: 0.5em;'>", unsafe_allow_html=True)
        st.subheader("Session Scores")

        # Get the tables as separate HTML strings
        skill_table, total_table, vocabulary_words, grammar_sentences, spelling_words, writing_prompts, arithmetic_problems = \
            ProgressTracker.get_summary_text()

        # Display the tables side by side using columns
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(skill_table, unsafe_allow_html=True)
        with col2:
            st.markdown(total_table, unsafe_allow_html=True)


def show_progress_tracking(llm):
    st.sidebar.markdown("<hr style='margin-top: 0.5em; margin-bottom: 0.5em;'>", unsafe_allow_html=True)
    name = get_name()
    email = get_email()
    send = show_send_summary()
    session_scores = ProgressTracker.get_session_scores()
    if send:
        if session_scores is not None:
            if not st.session_state['llm_exception']:
                feedback = llm(prompts.ASSESSMENT_FEEDBACK_PROMPT.format(
                    session_scores=session_scores))
                if ":" in feedback:
                    label, feedback = feedback.split(":", 1)
            else:
                feedback = session_scores
            ProgressTracker.send_summary(name, email, feedback)
            st.sidebar.success("Assessment report sent successfully")


def get_topic():
    selected_topic = st.sidebar.selectbox("Select a topic:", [topic.value for topic in Topic])
    return Topic.from_value(selected_topic)


def get_skill(topic):
    skill = None

    if topic is Topic.ENGLISH:
        if not st.session_state['llm_exception']:
            # Show all English skills if LLM is available
            english_skills = [skill.value for skill in EnglishSkill]
        else:
            # Show limited English skills if LLM is unavailable
            english_skills = ['Spelling', 'Grammar']

        selected_skill = st.sidebar.selectbox("Select an English skill:", english_skills)
        skill = EnglishSkill.from_value(selected_skill)

    elif topic is Topic.MATH:
        # Always show all Math skills
        selected_skill = st.sidebar.selectbox("Select a Math skill:", [skill.value for skill in MathSkill])
        skill = MathSkill.from_value(selected_skill)

    return skill


def get_level():
    selected_level = st.sidebar.selectbox("Select a difficulty level:", [level.value for level in Level])
    return Level.from_value(selected_level)


def name_or_email_entered():
    st.session_state["name_or_email_changed"] = True


def get_name():
    return st.sidebar.text_input(label="Name:", key="name", on_change=name_or_email_entered)


def get_email():
    return st.sidebar.text_input(label="Email:", key="email", on_change=name_or_email_entered)


def initialize_session(stats, topic, skill, level):
    session_start = "topic" not in st.session_state or \
                    "skill" not in st.session_state or \
                    "level" not in st.session_state
    if session_start:
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

    if "name_or_email_changed" not in st.session_state:
        st.session_state["name_or_email_changed"] = False

    return topic_changed, skill_changed, level_changed


def show_lesson(skill):
    st.header(skill.value)
    st.markdown(f"_{skill.description}_")


def show_next_challenge():
    return st.button(f"Next challenge", on_click=clear_answer, type="primary")


def send_summary_clicked():
    st.session_state["name_or_email_changed"] = True


def show_send_summary():
    return st.sidebar.button(f"Send summary", type="primary", on_click=send_summary_clicked)


def clear_answer():
    st.session_state["answer"] = ""
    st.session_state["numeric_answer"] = 0.0
    st.session_state["next_challenge"] = True
    st.session_state["name_or_email_changed"] = False


def clear_next_challenge():
    st.session_state["next_challenge"] = False


def get_question(llm, stats, skill, level):
    stats.increment_stats_counters(skill, level)
    if st.session_state['llm_exception']:
        question = get_default_question(skill, level)
        st.session_state["question"] = (skill.label, question)
        return st.session_state["question"]
    try:
        response = llm(skill.question_generation_prompt.format(level=level))
        label, question = process_question(response)
        st.session_state["question"] = (label, question)
        return label, question
    except Exception as e:
        print(e)
        st.session_state['llm_exception'] = True
        return get_default_question(skill, level)


def get_default_question(skill, level):
    skill_key = skill.value
    level_key = level.value
    if skill_key in default_questions and level_key in default_questions[skill_key]:
        default_question = random.choice(default_questions[skill_key][level_key])[0]
        st.session_state["question"] = default_question
        print(default_question)
        return default_question
    else:
        st.error("No default questions available for this skill and level.")
        return None, None


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
    print("Evaluating. Question:", question, "Answer:", answer)
    if not answer:
        return

    # Check if the question is from the default set
    default_answer = get_default_answer(skill, question)
    if default_answer is not None:
        evaluate_default(skill, question, answer, default_answer)
        return

    # If the question is not from the default set, proceed with LLM evaluation
    if topic is Topic.MATH:
        evaluate_math(llm, skill, question, answer)
    elif topic is Topic.ENGLISH:
        evaluate_english(llm, skill, question, answer)


def get_default_answer(skill, question):
    # Retrieve the level from session state or other means
    level = st.session_state.get("level").value if "level" in st.session_state else None
    print(level, skill.value, question)
    if level and skill.value in default_questions and level in default_questions[skill.value]:
        for q, a in default_questions[skill.value][level]:
            if q == question:
                return a
    return None


def evaluate_default(skill, question, user_answer, correct_answer):
    if skill is MathSkill.ARITHMETIC:
        user_answer_float = float(user_answer)
        correct_answer_float = float(correct_answer)
        if user_answer_float == correct_answer_float:
            process(skill, question, user_answer, "Score", 1)
        else:
            process(skill, question, user_answer, "Score", 0)
    else:
        if user_answer.strip().lower() == correct_answer.lower():
            process(skill, question, user_answer, "Score", 1)
        else:
            process(skill, question, user_answer, "Score", 0)


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
    print(">> evaluate: question:", question)
    print(">> evaluate: answer:", answer)
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
        ProgressTracker.add_skill_track(skill, question, points)
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
        text += f"<span style='font-size: medium;'>{skill}: <b>{count}</b> challenges</span><br>"
    st.markdown(text, unsafe_allow_html=True)


def show_review_form(stats):
    st.markdown("<h1 style='font-size: 24px;'>Rate App</h1>", unsafe_allow_html=True)
    rating = st.slider("Scale", 1, 5, 5, key="slider_rating", format="%d",
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
    st.markdown("<br><hr style='margin-top: 0.5em; margin-bottom: 0.5em;'>", unsafe_allow_html=True)
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
