from enum import Enum

import prompts


class EnglishSkill(Enum):
    """
    An enumeration representing different english skills
    """

    VOCABULARY = ("Vocabulary",
                  "Expanding vocabulary and understanding word meanings.",
                  prompts.ENGLISH_VOCABULARY_QUESTION_GENERATION_PROMPT,
                  prompts.ENGLISH_VOCABULARY_ANSWER_EVALUATION_PROMPT)
    GRAMMAR = ("Grammar",
               "Enhancing grammatical knowledge and correcting sentence errors.",
               prompts.ENGLISH_GRAMMAR_QUESTION_GENERATION_PROMPT,
               prompts.ENGLISH_GRAMMAR_ANSWER_EVALUATION_PROMPT)
    READING = ("Reading Comprehension",
               "Improving reading comprehension skills and understanding written passages.",
               prompts.ENGLISH_READING_QUESTION_GENERATION_PROMPT,
               prompts.ENGLISH_READING_ANSWER_EVALUATION_PROMPT)
    WRITING = ("Writing",
               "Developing writing abilities by creating coherent and expressive paragraphs.",
               prompts.ENGLISH_WRITING_QUESTION_GENERATION_PROMPT,
               prompts.ENGLISH_WRITING_ANSWER_EVALUATION_PROMPT)
    SPELLING = ("Spelling",
                "Enhancing spelling skills through auditory word recognition and accurate spelling practice.",
                prompts.ENGLISH_VOCABULARY_QUESTION_GENERATION_PROMPT,
                prompts.ENGLISH_SPELLING_ANSWER_EVALUATION_PROMPT)

    def __init__(self, value, description, question_generation_prompt, answer_evaluation_prompt):
        self._value_ = value
        self.description = description
        self.question_generation_prompt = question_generation_prompt
        self.answer_evaluation_prompt = answer_evaluation_prompt

    @staticmethod
    def from_value(value):
        for skill in EnglishSkill:
            if skill.value == value:
                return skill


class MathSkill(Enum):
    """
    An enumeration representing different math skills
    """

    ARITHMETIC = ("Arithmetic",
                  "Sharpen your mental math skills with a series of quick-fire arithmetic challenges.",
                  prompts.MATH_QUESTION_GENERATION_PROMPT,
                  prompts.MATH_ANSWER_EVALUATION_PROMPT)

    def __init__(self, value, description, question_generation_prompt, answer_evaluation_prompt):
        self._value_ = value
        self.description = description
        self.question_generation_prompt = question_generation_prompt
        self.answer_evaluation_prompt = answer_evaluation_prompt

    @staticmethod
    def from_value(value):
        for skill in MathSkill:
            if skill.value == value:
                return skill
