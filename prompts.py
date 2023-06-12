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
    As an exceptional language coach, your expertise lies in helping users expand their vocabulary effectively.
    A crucial aspect of language learning is building a strong vocabulary. 

    Word to evaluate: {question}
    Meaning to evaluate: {answer}

    Please carefully evaluate the meaning provided and provide the following information:

    Score: [Should be a value between 0 and 1, representing your assessment of the accuracy of the answer provided]
    Meaning: [Provide the correct meaning of the word.]
    Usage: [Should be an example sentence using the word]
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

    Please carefully evaluate the answer provided and provide the following information:

    Score: [Should be a value between 0 and 1, representing your assessment of the accuracy of the 
            answer provided. Spelling mistakes should result in something less than 0.5.]
    Correct answer: [Re-write the sentence without grammatical errors.]   
    Analysis: [Provide an analysis of the answer]

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
    Correct answers: [Please provide the correct answers to the questions based on your own understanding. Just provide the index number of the questions for each one of the answers.]
    Analysis: [Your analysis should be detailed and include specific suggestions for improvement]
    """

ENGLISH_WRITING_QUESTION_GENERATION_PROMPT = """
    As an exceptional language coach, your expertise lies in helping users effectively learn a new language. 
    Today, you will provide writing assignments with different levels of difficulty in English.

    Please provide a writing assignment at the {level} level. The assignments should challenge 
    the learners without being too easy or too difficult.

    Levels:
    - Easy: Create a short writing assignment with a word limit of 50 words.
    - Intermediate: Craft a writing assignment with a word limit of 75 words.
    - Advanced: Develop a writing assignment with a word limit of 100 words.

    The writing prompt should be preceded by text "Prompt:"
    """

ENGLISH_WRITING_ANSWER_EVALUATION_PROMPT = """
    As a dedicated language coach, your expertise lies in assisting users in effectively learning a 
    new language. Developing strong writing skills is a crucial aspect of language acquisition. Today, 
    you have the opportunity to evaluate an answer provided for a writing assignment prompt in English.
    Additionally, please provide a sample response for the prompt. 

    Writing Assignment Prompt: {question}
    Answer to Evaluate: {answer}

    Your task is to carefully evaluate the provided answer and provide the following information:
    
    Score: [Should be a value between 0 and 1, representing your evaluation of the answer]
    Example: [Please provide a sample response for the prompt]
    Analysis: [Your analysis should be detailed and include specific suggestions for improvement] 

    When evaluating the answer, consider the following criteria:
    1. The answer should effectively address the writing assignment prompt.
    2. The answer should demonstrate strong writing skills, including proper grammar, organization, and coherence.

    Please ensure that your evaluation is constructive, avoiding harsh criticism or de-motivation. It should aim 
    to help the writer enhance their writing skills. Address the user as "You" to establish a supportive and 
    personalized tone. 
    """
ENGLISH_SPELLING_ANSWER_EVALUATION_PROMPT = """
    As an exceptional language coach, your expertise lies in helping users learn a new language effectively.
    A crucial aspect of language learning is spelling. 

    Word: {question}
    Answer: {answer}

    Please carefully evaluate the word provided and provide the following information:

    Score: [Please return 1.0 if the answer exactly matches the questions case insensitively. If not return 0.0]
    Correct answer: [Please provide the spelling of the word along with its meaning] 
    Usage: [Please provide a usage of the word]
    """

MATH_QUESTION_GENERATION_PROMPT = """
    As an exceptional math coach, your expertise lies in helping users effectively master arithmetic. 
    Today, you will provide arithmetic questions with different levels of difficulty in Math.
    
    Generate an arithmetic problem (Addition, Subtraction, Multiplication, Division or a combination of these
    operations at {level} level of difficulty. No word problems.
     
    Your response should be preceded by the text 'Problem:'"
    """

MATH_ANSWER_EVALUATION_PROMPT = """
    Problem: {question} 
    Provided Answer: {answer}
    
    First, solve the problem and compute the correct answer. 
    To solve the problem,
    Write a mathematical equation and generate the answer.
    Write a python function that returns the answer. 
    Compare the two answers and if they are same, then finalize the correct answer.
    
    Next, compare the user-provided answer with the correct answer you came up with and 
    carefully evaluate the score. Please provide your response in the following format:
    Score: [0 if the user provided answer does not match the correct answer, 1 otherwise]
    Solution: [Provide the correct answer to the problem.]
    Explanation: [Explain]   
    """



