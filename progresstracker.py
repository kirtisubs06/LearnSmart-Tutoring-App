import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from collections import namedtuple
import pandas as pd
from email_validator import EmailNotValidError, validate_email
import streamlit as st
import pdfkit
from datetime import date

from skill import EnglishSkill, MathSkill


class ProgressTracker:
    @staticmethod
    def get_session_scores():
        summary = st.session_state.get("summary")
        if summary is None:
            return None

        Summary = namedtuple('Summary', ['challenges', 'points'])
        session_scores = {
            key: Summary(challenges=values[0], points=values[1])
            for key, values in summary.items()
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

    @staticmethod
    def send_summary(name, email, assessment):
        if name == "":
            st.sidebar.error("Please enter your name.")
        if email == "":
            st.sidebar.error("Please enter an email address.")
        if name == "" or email == "":
            return

        skill_table, summary_table, vocabulary_words, grammar_sentences, spelling_words, writing_prompts, arithmetic_problems = \
            ProgressTracker.get_summary_text()

        if skill_table == "" or summary_table == "":
            st.sidebar.error("No summary available")
            return

        v_words = ', '.join(vocabulary_words)
        g_sentences = '<br>'.join(grammar_sentences)
        w_prompts = '<br>'.join(writing_prompts)
        s_words = ', '.join(spelling_words)
        a_problems = '<br>'.join(arithmetic_problems)

        today = date.today().strftime("%Y-%m-%d")
        html_template = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .main-title {{ color: black; font-size: 24px; font-weight: bold; margin-bottom: 20px; text-align: center;}}
                    .section-title {{ color: black; padding: 5px; font-size: 18px; font-weight: bold; margin-top: 20px; text-align: center; border-bottom: 0px solid #999;}}
                    .assessment-section {{ margin-top: 20px; }}
                    .question-section {{ margin-top: 20px; }}
                    .date {{ text-align: center; font-size: 14px; font-weight: bold;}}
                </style>
            </head>
            <body>
                <div class="main-title">Assessment Report</div>
                <div class="date">{today}</div>
                <div class="section-title">Skills scores</div>
                <div>{skill_table}</div>
                <br>
                <div class="section-title">Total score</div>
                <div>{summary_table}</div>
                <br><br>
                <div class="section-title">Assessment</div>
                <div class="assessment-section">{assessment}</div>
                <div class="section-title">Questions</div>
                <div class="question-section"><b>Vocabulary words: </b>{v_words}</div>
                <div class="question-section"><b>Grammar sentences:</b><br>{g_sentences}</div>
                <div class="question-section"><b>Writing prompts: </b><br>{w_prompts}</div>
                <div class="question-section"><b>Spelling words: </b><br>{s_words}</div>
                <div class="question-section"><b>Arithmetic problems: </b><br>{a_problems}</div>
            </body>
            </html>
            """

        """
        html = html_template.format(
            today=today,
            skill_table=skill_table,
            summary_table=summary_table,
            assessment=assessment,
            vocabulary_words=', '.join(vocabulary_words),
            grammar_sentences='<br>'.join(grammar_sentences),
            writing_prompts='<br>'.join(writing_prompts),
            spelling_words=', '.join(spelling_words),
            arithmetic_problems=', '.join(arithmetic_problems)
        )
        """
        html = html_template
        filename = f"{name}-assessment-{today}.pdf"
        pdfkit.from_string(html, filename)

        subject = "LearnSmart Assessment Report"

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = os.environ["EMAIL_ID"]
        message["To"] = email

        with open(filename, "rb") as file:
            attach = MIMEApplication(file.read(), _subtype="pdf")
            attach.add_header("Content-Disposition", "attachment", filename=filename)
            message.attach(attach)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.environ["EMAIL_ID"], os.environ["EMAIL_PASSWORD"])
            server.send_message(message)

        os.remove(filename)

    @staticmethod
    def add_skill_track(skill, question, point):
        skill_key = skill.value
        if skill is EnglishSkill.READING:
            skill_key = "Reading"
        Summary = namedtuple('Summary', ['challenges', 'points'])
        if st.session_state.get("summary") is None:
            st.session_state["summary"] = {
                EnglishSkill.VOCABULARY.value: Summary(challenges=0, points=0),
                EnglishSkill.GRAMMAR.value: Summary(challenges=0, points=0),
                "Reading": Summary(challenges=0, points=0),
                EnglishSkill.WRITING.value: Summary(challenges=0, points=0),
                EnglishSkill.SPELLING.value: Summary(challenges=0, points=0),
                MathSkill.ARITHMETIC.value: Summary(challenges=0, points=0),
            }
            st.session_state["questions"] = {
                "vocabulary_words": [],
                "spelling_words": [],
                "writing_prompts": [],
                "grammar_sentences": [],
                "arithmetic_problems": []
            }

        challenges = st.session_state["summary"][skill_key].challenges + 1
        points = st.session_state["summary"][skill_key].points + point
        st.session_state["summary"][skill_key] = Summary(challenges=challenges, points=points)
        if skill is EnglishSkill.VOCABULARY:
            st.session_state["questions"]["vocabulary_words"].append(question)
        elif skill is EnglishSkill.GRAMMAR:
            st.session_state["questions"]["grammar_sentences"].append(question)
        elif skill is EnglishSkill.WRITING:
            st.session_state["questions"]["writing_prompts"].append(question)
        elif skill is EnglishSkill.SPELLING:
            st.session_state["questions"]["spelling_words"].append(question)
        elif skill is MathSkill.ARITHMETIC:
            st.session_state["questions"]["arithmetic_problems"].append(question)

    @staticmethod
    def get_summary_text():
        summary = st.session_state.get("summary")
        questions = st.session_state.get("questions")
        if summary is None:
            return "", "", [], [], [], []

        table_style = "width: 100%; border: 3px solid #999; " \
                      "background-color: #E6F1F6; color: black;"
        header_style = "background-color: #A6C9E2; font-weight: bold; padding: 0px 0; text-align: left; " \
                       "font-size: 15px; color: black;"
        cell_style = "padding: 3px; text-align: left; border-bottom: 2px solid #999; border-right: 2px solid #999;" \
                     "font-size: 14px; color: black;"

        table_data = []
        total_challenges = 0
        total_points = 0

        for skill, summary_data in summary.items():
            challenges = summary_data.challenges
            points = summary_data.points
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

        return skill_table, total_table, questions["vocabulary_words"], questions["grammar_sentences"], \
               questions["spelling_words"], questions["writing_prompts"], questions["arithmetic_problems"]
