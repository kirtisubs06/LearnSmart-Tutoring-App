ENGLISH_VOCABULARY_QUESTION_GENERATION = """
    As a world class vocabulary coach, please generate a word in lowercase at the {level} level of difficulty in English. 
    Your response should be preceded by the text 'Word:'"
"""

ENGLISH_VOCABULARY_ANSWER_EVALUATION = """
    Word: {question}, Meaning: {answer}
    Please carefully evaluate the meaning provided for the word and provide the response in the following format:

    Score: [Should be a float value between 0 and 1, representing your assessment of the accuracy of the answer provided]
    [insert newline here]
    Solution: [Provide the correct meaning of the word]
    [insert newline here]
    Usage: [Should be an example sentence using the word]
"""

MATH_QUESTION_GENERATION = """
    Generate a word in lowercase at the {level} level of difficulty in English. 
    Your response should be preceded by the text 'Word:'"
"""

MATH_ANSWER_EVALUATION = """
    Word: {question}, Meaning: {answer}
    Please carefully evaluate the meaning provided for the word and provide the following information:

    Confidence Score: [Should be a value between 0 and 1, representing your assessment of the accuracy of the answer provided]
    Solution: [Provide the correct meaning of the word.]
    Usage: [Should be an example sentence using the word]
"""
