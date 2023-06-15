import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import namedtuple
import pandas as pd
from email_validator import EmailNotValidError, validate_email
import streamlit as st

from skill import EnglishSkill, MathSkill


class ProgressTracker:
    @staticmethod
    def get_session_scores():
        summary = st.session_state.get("summary")
        if summary is None:
            return None

        Summary = namedtuple('Summary', ['challenges', 'points'])
        session_scores = {
            key: Summary(challenges, points)
            for key, (challenges, points) in summary.items()
        }
        return session_scores

    @staticmethod
    def is_valid_email(email):
        if not email:
            return False

        try:
            validate_email(email, check_deliverability=True)
            return True
        except EmailNotValidError:
            return False

    # Function to send a verification email
    @staticmethod
    def send_summary(name, email, feedback):
        if name == "":
            st.sidebar.error("Please enter your name.")
        if email == "":
            st.sidebar.error("Please enter an email address.")
        if name == "" or email == "":
            return

        summary_text = ProgressTracker.get_summary_text()

        if summary_text == "":
            st.sidebar.error("No summary available")
            return

        subject = "LearnSmart Session Summary"

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = os.environ["EMAIL_ID"]
        message["To"] = email

        html = """
        <html>
        <body>
            <p><u>{name}'s scores:</u></p>
            <p>{summary}</p>
            <hr style='margin-top: 0.5em; margin-bottom: 0.5em;'>
            <p>{feedback}</p>
        </body>
        </html>
        """.format(name=name, summary=summary_text, feedback=feedback)

        message.attach(MIMEText(html, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.environ["EMAIL_ID"], os.environ["EMAIL_PASSWORD"])
            server.send_message(message)

    @staticmethod
    def add_skill_track(skill, point):
        skill_key = skill.value
        if skill is EnglishSkill.READING:
            skill_key = "Reading"
        if st.session_state.get("summary") is None:
            Summary = namedtuple('Summary', ['challenges', 'points'])

            st.session_state["summary"] = {
                EnglishSkill.VOCABULARY.value: Summary(0, 0),
                EnglishSkill.GRAMMAR.value: Summary(0, 0),
                "Reading": Summary(0, 0),
                EnglishSkill.WRITING.value: Summary(0, 0),
                EnglishSkill.SPELLING.value: Summary(0, 0),
                MathSkill.ARITHMETIC.value: Summary(0, 0),
            }

        challenges = st.session_state["summary"][skill_key][0] + 1
        points = st.session_state["summary"][skill_key][1] + point
        st.session_state["summary"][skill_key] = (challenges, points)

    @staticmethod
    def get_summary_text():
        summary = st.session_state.get("summary")
        if summary is None:
            return "", ""

        table_style = "border-collapse: collapse; width: 100%; border: 1px solid #ddd; " \
                      "background-color: #E6F1F6; color: white;"
        header_style = "background-color: #A6C9E2; font-weight: bold; padding: 0px 0; text-align: center; " \
                       "border-bottom: 2px solid #ddd; font-size: 12px; color: white;"
        cell_style = "padding: 3px; text-align: left; border-bottom: 1px solid #ddd; font-size: 12px; color: black;"

        table_data = []
        total_challenges = 0
        total_points = 0

        for skill, (challenges, points) in summary.items():
            total_challenges += challenges
            total_points += points
            table_data.append([skill, challenges, points])

        df = pd.DataFrame(table_data, columns=["Skill", "Challenges", "Points"])
        total_table_data = [
            ["Total challenges:", total_challenges],
            ["Total points:", total_points],
            ["Score:", f"{round((total_points * 100 / total_challenges), 2)}%"]
        ]
        total_df = pd.DataFrame(total_table_data, columns=["Metric", "Value"])

        skill_table = df.to_html(index=False, justify="left", border=0)
        skill_table = skill_table.replace('<table', f'<table style="{table_style}"')
        skill_table = skill_table.replace('<th', f'<th style="{header_style}"')
        skill_table = skill_table.replace('<td', f'<td style="{cell_style}"')

        total_table = total_df.to_html(index=False, justify="left", border=0)
        total_table = total_table.replace('<table', f'<table style="{table_style}"')
        total_table = total_table.replace('<th', f'<th style="{header_style}"')
        total_table = total_table.replace('<td', f'<td style="{cell_style}"')

        return skill_table, total_table

















