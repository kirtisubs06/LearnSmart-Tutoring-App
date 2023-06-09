from enum import Enum


class EnglishSkill(Enum):
    """
    An enumeration representing different english skills
    """

    VOCABULARY = ("Vocabulary",
                  "Expanding vocabulary and understanding word meanings.",
                  "As an exceptional language coach, your expertise lies in helping users expand their vocabulary "
                  "effectively. "
                  "Please generate a word at the {level} level of difficulty in English. "

                  "Remember:"
                  "- Easy Level: Choose a word that is simple and commonly used."
                  "- Intermediate Level: Select a word that is more advanced or less commonly used."
                  "- Advanced Level: Find a word that is challenging and may require higher language proficiency."

                  "Your response should be preceded by the text 'Word:'"
                  )

    def __init__(self, value, description, prompt):
        self._value_ = value
        self.description = description
        self.prompt = prompt

    @staticmethod
    def from_value(value):
        for skill in EnglishSkill:
            if skill.value == value:
                return skill


class MathSkill(Enum):
    """
    An enumeration representing different math skills
    """

    ARITHMETIC = ("Arithmetic", "Sharpen your mental math skills with a series of quick-fire arithmetic challenges.")

    def __init__(self, value, description):
        self._value_ = value
        self.description = description

    @staticmethod
    def from_value(value):
        for skill in MathSkill:
            if skill.value == value:
                return skill
