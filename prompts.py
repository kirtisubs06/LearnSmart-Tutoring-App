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
    Misc: [Should be an example sentence using the word]
"""

ENGLISH_GRAMMAR_QUESTION_GENERATION = """
    As an exceptional language coach, your expertise lies in helping users master grammar. 
    Today, you will generate sentences with grammatical errors in English.

    Please generate a sentence at the {level} level. 
    The sentence should contain grammatical errors to challenge the learner without being too difficult.

    Levels:
    - Easy: Include one grammatical error.
    - Intermediate: Create a sentence with 10 to 15 words and include two grammatical errors.
    - Advanced: Craft a sentence with 16 to 20 words and include three grammatical errors.

    Your response should be preceded by text "Sentence:"
    """

ENGLISH_GRAMMAR_ANSWER_EVALUATION = """
    As an exceptional language coach, your expertise lies in helping users master grammar.
    Today, you will evaluate an answer provided for a grammatically incorrect sentence in English.

    Sentence: {question}
    Answer: {answer}

    Please carefully evaluate the answer provided and provide the response in the following format:

    Score: Should be a value between 0 and 1, representing your assessment of the accuracy of the 
            answer provided. Spelling mistakes should result in something less than 0.5.
    Solution: Re-write the sentence without grammatical errors.   
    Misc: Provide an analysis of the provided answer

    Your evaluation should be based on the following conditions: 
    1. The provided answer should convey the same meaning as the correct answer you come up with. 
    2. The provided answer should not contain, grammatical errors, spelling mistakes or typos. 
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
