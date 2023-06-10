from enum import Enum

import prompts


class EnglishSkill(Enum):
    """
    An enumeration representing different english skills
    """

    VOCABULARY = ("Word Wizard",
                  "Expanding vocabulary and understanding word meanings.",
                  prompts.ENGLISH_VOCABULARY_QUESTION_GENERATION,
                  prompts.ENGLISH_VOCABULARY_ANSWER_EVALUATION
                  )
    GRAMMAR = ("Grammar Guru",
               "Enhancing grammatical knowledge and correcting sentence errors.",
               prompts.ENGLISH_GRAMMAR_QUESTION_GENERATION,
               prompts.ENGLISH_GRAMMAR_ANSWER_EVALUATION
               )

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
                  prompts.ENGLISH_VOCABULARY_QUESTION_GENERATION,
                  prompts.ENGLISH_VOCABULARY_ANSWER_EVALUATION
                  )

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
