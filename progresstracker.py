import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email_validator import EmailNotValidError, validate_email
import streamlit as st

from skill import EnglishSkill, MathSkill


class ProgressTracker:
    @staticmethod
    def get_session_scores():
        return st.session_state.get("summary")

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
    def send_summary(email, feedback):
        if email == "":
            st.sidebar.error("Please enter an email address")
            return

        summary_text = ProgressTracker.get_summary_text()

        if summary_text == "":
            st.sidebar.error("No summary available")
            return

        # Set up the email content
        subject = "LearnSmart Session Summary"

        # Create the MIME message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = os.environ["EMAIL_ID"]
        message["To"] = email

        # Create the HTML part of the message
        html = f"""
        <html>
        <body>
            <p>{summary_text}</p>
            <p>{feedback}</p>
        </body>
        </html>
        """

        # Attach the HTML part to the message
        message.attach(MIMEText(html, "html"))

        # Create an SMTP session
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            # Replace with your email credentials
            server.login(os.environ["EMAIL_ID"], os.environ["EMAIL_PASSWORD"])
            server.send_message(message)

    @staticmethod
    def add_skill_track(skill, point):
        print(skill.value, point)
        if st.session_state.get("summary") is None:
            st.session_state["summary"] = {
                EnglishSkill.VOCABULARY.value: (0, 0),
                EnglishSkill.GRAMMAR.value: (0, 0),
                EnglishSkill.READING.value: (0, 0),
                EnglishSkill.WRITING.value: (0, 0),
                EnglishSkill.SPELLING.value: (0, 0),
                MathSkill.ARITHMETIC.value: (0, 0),
            }

        challenges = st.session_state["summary"][skill.value][0] + 1
        points = st.session_state["summary"][skill.value][1] + point
        st.session_state["summary"][skill.value] = (challenges, points)

    @staticmethod
    def get_summary_text():
        summary = st.session_state.get("summary")
        if summary is None:
            return ""
        summary_text = ""
        total_challenges = 0
        total_points = 0
        for skill, (challenges, points) in summary.items():
            total_challenges += challenges
            total_points += points
            summary_text += f"<span style='font-size: small;'><b>{skill}</b>: <b>{challenges}</b> challenges, <b>{points}</b> points</span><br>"
        summary_text += f"<br><span style='font-size: medium;'><b>Challenges: <b>{total_challenges}</b>, <b>Points: {total_points}</b></span><br>"
        return summary_text
