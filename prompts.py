ENGLISH_VOCABULARY_QUESTION_GENERATION_PROMPT = """
    As an exceptional language coach, your expertise lies in helping users expand their vocabulary effectively.
    Please generate a word at the {level} level of difficulty in English. 

    Remember:
    - Easy Level: Choose a word that is simple and commonly used.
    - Intermediate Level: Select a word that is more advanced or less commonly used.
    - Advanced Level: Find a word that is challenging and may require higher language proficiency.

    Your response should be preceded by the text "Word:"
"""

ENGLISH_VOCABULARY_ANSWER_EVALUATION_PROMPT = """
    Word: {question}, Meaning: {answer}
    Please carefully evaluate the meaning provided for the word and provide the response in the following format:

    Score: [Should be a float value between 0 and 1, representing your assessment of the accuracy of the answer provided]
    Solution: [Provide the correct meaning of the word]
    Misc: [Should be an example sentence using the word]
"""

ENGLISH_GRAMMAR_QUESTION_GENERATION_PROMPT = """
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

ENGLISH_GRAMMAR_ANSWER_EVALUATION_PROMPT = """
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

ENGLISH_READING_QUESTION_GENERATION_PROMPT = """
    As an exceptional language coach, your expertise lies in helping users develop their reading 
    comprehension skills. Today, your task is to generate a reading comprehension based on the selected 
    level. Your passage should be engaging, informative, and suitable for reading comprehension practice. 

    Please generate a reading comprehension passage followed by three questions related to the passage
    with the following specifications:

    Passage Difficulty: {level}

    Passage Difficulty Levels:
    - Easy: Passage with simple language and concepts, suitable for beginners.
    - Intermediate: Passage with moderate language complexity and content, suitable for intermediate learners.
    - Advanced: Passage with advanced language and complex content, suitable for advanced learners.

    Passage Length Guidelines:
    - Easy: Short passage (20-40 words)
    - Intermediate: Medium-length passage (40-60 words)
    - Advanced: Long passage (60-80 words)

    The reading comprehension passage should be prefixed with "Passage:".
    The passage should be followed by a set of 3 questions related to the passage."
    """

ENGLISH_READING_ANSWER_EVALUATION_PROMPT = """
    As an exceptional language coach, your expertise lies in helping users learn a new language effectively.
    A crucial aspect of language learning is reading comprehension. Today, you will evaluate the answers provided
    for the questions asked in the passage

    Passage to evaluate: {question}
    Answers to evaluate: {answer}

    Please carefully evaluate the answers provided and provide the following information:

    Score: [Should be a value between 0 and 1, representing your evaluation of the answers.
            For zero correct answers, return 0 
            For a single correct answer, return 0.33
            For two correct answers, return 0.66
            For three correct answers, return 1.0
            Give partial credit to answers that are partially correct]
    Solution: [Please provide the correct answers to the questions based on your own understanding. Just provide the index number of the questions for each one of the answers.]
    Misc: [Please provide the analysis of the supplied answer.]   
    """

MATH_QUESTION_GENERATION_PROMPT = """
    Generate a word in lowercase at the {level} level of difficulty in English. 
    Your response should be preceded by the text 'Word:'"
"""

MATH_ANSWER_EVALUATION_PROMPT = """
    Question: {question}, Answer: {answer}
    Please carefully evaluate the meaning provided for the word and provide the following information:

    Score: [Should be a value between 0 and 1, representing your assessment of the accuracy of the answer provided]
    Solution: [Provide the correct meaning of the word.]
    Usage: [Should be an example sentence using the word]
"""


