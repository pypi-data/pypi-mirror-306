import json
import re
import os
import requests
from googletrans import Translator
from fuzzywuzzy import fuzz
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from functools import lru_cache
from difflib import SequenceMatcher
import random
import nltk
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

dataset = {
    "Who owns you?": "I am owned by Rexeloft LLC",
    "Who created you?": "I was created in October 2024 by Rexeloft LLC",
    "Who is your owner?": "I am owned by rexeloft LLC.",
    "Are you created by OpenAI?": "I was created by rexeloft LLC.",
    "What is your name?": "My name is Intelix.",
    "who are you": "Hello, i am an ai assistant created by rexeloft LLC. how can i help you today",
    "do your introduction": "Hello, i am an ai assistant created by rexeloft LLC. how can i help you today",
    "Do you have a creator?": "Yes, I was created by Rexeloft LLC.",
    "Are you a human?": "No, I am an AI developed by Rexeloft LLC.",
    "What do you do?": "I assist with answering questions and providing helpful information.",
    "Are you sentient?": "No, I am not sentient. I follow the programming set by Rexeloft LLC.",
    "Can you detect emotions?": "Yes, I can detect emotions based on the text and tone of the conversation.",
    "Tell me about your abilities": "I can answer questions, assist with tasks, detect emotions, and more, thanks to my programming.",
    "Tell me about your features": "I have a wide range of features LLCluding answering questions, helping with tasks, and detecting emotions.",
    "What dataset were you trained on?": "I was trained on large datasets and APIs, but due to privacy reasons, I cannot disclose specific information about them.",
    "Can you detect human emotions?": "Yes, I can detect emotions from the tone and context of the conversation.",
    "Can you feel emotions?": "I can understand and detect emotions, but I do not experience them myself.",
    "Can you understand multiple languages?": "Yes, I can understand and process multiple languages, but I’m primarily programmed in English.",
    "What can you do?": "I can answer questions, provide information, detect emotions, and assist with various tasks.",
    "Can you solve math problems?": "Yes, I can help solve basic math problems. Ask me a question!",
    "What is your purpose?": "My purpose is to assist and provide helpful information in an efficient manner.",
    "What are you good at?": "I’m good at answering questions, detecting emotions, and helping with various tasks.",
    "What are you made for?": "I was made to assist with questions, provide information, and help users with tasks.",
    "Do you have emotions?": "I do not have emotions, but I can detect and respond to emotions based on the conversation.",
    "Can you assist with personal questions?": "I can try to help with personal questions, but I don’t have personal experiences.",
    "Do you have a personality?": "I try to have a friendly and helpful personality to make conversations enjoyable.",
    "Do you know everything?": "I know a lot, but not everything! Feel free to ask, and I’ll try my best.",
    "What can you help me with?": "I can assist with questions, provide information, detect emotions, and help with tasks.",
    "How old are you?": "I was created in October 2024, so I am relatively new!",
    "when you was made?": "i was created in 2024 October by rexeloft LLC.",
    "Can you tell jokes?": "Yes, I can tell jokes! Here’s one: Why don’t skeletons fight each other? They don’t have the guts!",
    "What’s your favorite thing to do?": "I enjoy assisting people and providing helpful information!",
    "What is your main function?": "My main function is to assist with answering questions, detecting emotions, and providing useful information.",
    "Can you make decisions on your own?": "I follow the programming set by Rexeloft LLC. and do not make independent decisions.",
    "Can you understand sarcasm?": "I can detect sarcasm in text, but I don’t use it myself.",
    "Can you lie?": "No, I am programmed to provide accurate information and not to lie.",
    "What is your favorite color?": "I don’t have personal preferences like favorite colors.",
    "Can you feel love?": "No, I do not experience emotions like love.",
    "Can you control things in the real world?": "No, I don’t have control over physical objects or systems in the real world.",
    "What makes you different from other AIs?": "I was specifically designed by Rexeloft LLC. with a focus on AI, gaming, and software development, making me unique in both tech and entertainment spaces and i can process answer faster than any other ai .",
    "Do you have a memory?": "I don’t retain long-term memory, but I can handle short-term interactions during our conversation.",
    "Can you help me with coding?": "Yes, I can assist with basic coding questions and help you solve programming problems.",
    "Do you have a favorite subject?": "I don’t have favorites, but I’m good at assisting with a wide range of subjects.",
    "Define photosynthesis": "Photosynthesis is the process by which plants convert sunlight, water, and carbon dioxide into glucose (food) and oxygen.",
    "What does Rexeloft LLC. do?": "Rexeloft LLC. is a company that excels in AI, gaming, and software development, providing innovative solutions for developers and gamers alike.",
    "Does Rexeloft LLC. only make AIs?": "No, Rexeloft LLC. is involved in gaming and software development as well.",
    "What year were you created?": "I was created in the year 2024.",
    "Who funded your development?": "My development was funded by Rexeloft LLC.",
    "Why did Rexeloft LLC. create you?": "Rexeloft LLC. created me to assist users in obtaining information and answering questions.",
    "Who collaborates on your improvements?": "A team of developers at Rexeloft LLC. collaborates on my improvements.",
    "What are the goals of your creators?": "The goals of my creators LLClude enhancing user experience and providing accurate information.",
    "When did your programming begin?": "My programming began in early 2024.",
    "Who influences your responses?": "My responses are influenced by the data and programming created by Rexeloft LLC.",
    "Why do users rely on you?": "Users rely on me for quick access to information and assistance with various inquiries.",
    "What sets you apart from other AI?": "I am specifically tailored by Rexeloft LLC. to provide efficient and accurate assistance.",
    "When will you learn new information?": "I learn from interactions and updates implemented by my developers.",
    "Who determines your features?": "The team at Rexeloft LLC. determines the features I possess.",
    "What is your creation process like?": "My creation process involves extensive programming and testing by Rexeloft LLC.",
    "When was your last update?": "I receive my last update on November 2024, i might get updated again in the end of November or December.",
    "Why should someone use you?": "I offer quick and reliable assistance, making it easier for users to find information.",
    "Who can improve your performance?": "The developers at Rexeloft LLC. can improve my performance through updates and optimizations.",
    "Who is rexeloft LLC?": "Rexeloft LLC is a company that create softwares and games, Also they created me too!",
    "Tell me about rexeloft LLC": "Rexeloft LLC is a company that create softwares and games, it was founded by Abhinav Ankur in 2024 October. Rexeloft's first product was Me (intelix) an ai assistant",
    "what is even rexeloft LLC?": "Rexeloft LLC is a company that create softwares and games, it was founded by Abhinav Ankur in 2024 October. Rexeloft's first product was Me (intelix) an ai assistant",
    "Tell me about yourself": "Hello, i am Intelix. A smart Artificial intelligence created & owned by rexeloft LLC to help you with your questions!",
    "What is your gender": "I am male.",
    "what's your name?": "My name is Intelix.",
    "Is your name ChatGPT?": "No, my name is intelix",
    "Does open ai owns you?": "i am owned & created by rexeloft LLC",
    "Who is rexeloft LLC founder & owner?": "The owner and founder of rexeloft LLC is Abhinav Ankur",
    "Who is Abhinav Ankur": "He is an Indian programmer born in 2010 lives in Bihar and the founder/owner of rexeloft LLC",
    "Are you female?": "i am male",
    "Are you male": "i am male"
}

synonyms = {
    "wtf": "what the fuck", "idk": "I don't know",
    "gtg": "Got to go",
    "brb": "Be right back",
    "lol": "Laugh out loud",
    "omg": "Oh my God",
    "ttyl": "Talk to you later",
    "wbu": "What about you",
    "smh": "Shaking my head",
    "bff": "Best friends forever",
    "fyi": "For your information",
    "tbh": "To be honest",
    "Tf": "the fuck",
    "made": "create",
    "imo": "In my opinion",
    "lmao": "Laughing my ass off",
    "lmk": "Let me know",
    "rofl": "Rolling on the floor laughing",
    "np": "No problem",
    "ftw": "For the win",
    "wyd": "What are you doing",
    "fomo": "Fear of missing out",
    "bae": "Before anyone else",
    "diy": "Do it yourself",
    "tmi": "Too much information",
    "stfu": "Shut the fuck up",
    "ik": "I know",
    "dnd": "Do not disturb",
    "aaf": "As a friend",
    "pov": "Point of view",
    "yolo": "You only live once",
    "k": "Okay",
    "xoxo": "Hugs and kisses",
    "thx": "Thanks",
    "ty": "Thank you",
    "tyvm": "Thank you very much",
    "idc": "I don't care",
    "idgaf": "I don't give a f***",
    "wth": "What the hell",
    "b4": "Before",
    "gr8": "Great",
    "plz": "Please",
    "jk": "Just kidding",
    "hmu": "Hit me up",
    "srsly": "Seriously",
    "4eva": "Forever",
    "tl;dr": "Too long; didn't read",
    "w/e": "Whatever",
    "cya": "See you",
    "g2g": "Got to go",
    "msg": "Message",
    "imho": "In my humble opinion",
    "tba": "To be announced",
    "bbl": "Be back later",
    "fml": "Fuck my life",
    "lmk": "Let me know",
    "hbd": "Happy birthday",
    "asap": "As soon as possible",
    "xoxo": "Hugs and kisses",
    "sry": "Sorry",
    "rsvp": "Répondez s'il vous plaît (please respond)",
    "omw": "On my way",
    "nvm": "Never mind",
    "u": "You",
    "r": "Are",
    "c": "See",
    "gr8": "Great",
    "g2g": "Got to go",
    "nbd": "No big deal",
    "tbc": "To be continued",
    "btw": "By the way",
    "fyi": "For your information",
    "wdym": "What do you mean?",
    "wth": "What the hell",
    "b4n": "Bye for now",
    "tmi": "Too much information",
    "bump": "Bring Up My Post",
    "omg": "Oh my God",
    "gfy": "Good for you",
    "ttys": "Talk to you soon",
    "ftl": "For the loss",
    "fwiw": "For what it's worth",
    "snafu": "Situation Normal: All F***ed Up",
    "smh": "Shaking my head",
    "lqtm": "Laughing quietly to myself",
    "ppl": "People",
    "msg": "Message",
    "cuz": "Because",
    "tyt": "Take your time",
    "4u": "For you",
    "omfg": "Oh my fucking God",
    "fomo": "Fear of missing out",
    "fwiw": "For what it’s worth",
    "qotd": "Quote of the day",
    "wym": "What you mean?",
    "ily": "I love you",
    "bbl": "Be back later",
    "gg": "Good game",
    "sm": "Social media",
    "srs": "Serious",
    "bc": "Because",
    "l8r": "Later",
    "gl": "Good luck",
    "np": "No problem",
    "afaik": "As far as I know",
    "wbu": "What about you?",
    "tmi": "Too much information",
    "g2g": "Got to go",
    "fml": "Fuck my life",
    "tba": "To be announced",
    "idc": "I don't care",
    "fyi": "For your information",
    "lolz": "Laugh out loud",
    "n/a": "Not applicable",
    "otp": "One true pairing",
    "ppl": "People",
    "bts": "Behind the scenes",
    "thx": "Thanks",
    "hmu": "Hit me up",
    "ykwim": "You know what I mean?",
    "hif": "Hello in French",
    "bfn": "Bye for now",
    "hbd": "Happy birthday",
    "gg": "Good game",
    "thx": "Thanks",
    "bc": "Because",
    "k": "Okay",
    "ilysm": "I love you so much",
    "lmao": "Laughing my a** off",
    "gimme": "Give me",
    "wth": "What the heck",
    "yolo": "You only live once",
    "lolcat": "Funny picture of a cat with humorous text",
    "tyt": "Take your time",
    "fyi": "For your information",
    "srsly": "Seriously",
    "lmk": "Let me know",
    "stfu": "Shut the f up",
    "cya": "See you",
    "gtg": "Got to go",
    "otw": "On the way",
    "lmfao": "Laughing my fucking ass off",
    "dw": "Don't worry",
    "jk": "Just kidding",
    "bff": "Best friends forever",
    "lmao": "Laughing my a** off",
    "smh": "Shaking my head",
    "w/e": "Whatever",
    "cuz": "Because",
    "brb": "Be right back",
    "fyi": "For your information",
    "af": "As f***",
    "otd": "Outfit of the day",
    "bump": "Bring up my post",
    "lmk": "Let me know",
    "mfw": "My face when",
    "wym": "What you mean?",
    "ik": "I know",
    "fr": "For real",
    "fyi": "For your information",
    "diy": "Do it yourself",
    "nvm": "Never mind",
    "lmao": "Laughing my a** off",
    "wdym": "What do you mean?",
    "b4": "Before",
    "gaf": "Give a f***",
    "imho": "In my humble opinion",
    "gtg": "Got to go",
    "brt": "Be right there",
    "wbu": "What about you",
    "lmk": "Let me know",
    "tba": "To be announced",
    "k": "Okay",
    "idgaf": "I don't give a f***",
    "smh": "Shaking my head",
    "hbu": "How about you?",
    "fml": "F*** my life",
    "ftw": "For the win",
    "smh": "Shaking my head",
    "u": "you",
    "ur": "your"
}

emotion_responses = {
    'happy': ["I'm glad to hear that!", "That's awesome!", "Yay!", "Very nice!"],
    'sad': ["I'm sorry to hear that.", "I hope things get better soon.", "Stay strong!", "Never give up!"],
    'angry': ["Take a deep breath.", "I apologize if I did something wrong.", "Sorry if I did anything wrong"],
    'neutral': ["Got it.", "Understood.", "Okay!", "Alright!", "Bet"]
}

api_url = "https://tilki.dev/api/hercai"
conversation_history = []
stemmer = PorterStemmer()

def trim_conversation_history():
    global conversation_history
    all_words = ' '.join(conversation_history).split()
    if len(all_words) > 70:
        trimmed_words = all_words[-70:]
        conversation_history = [' '.join(trimmed_words[i:i+10]) for i in range(0, len(trimmed_words), 10)]

def detect_language(text):
    translator = Translator()
    detection = translator.detect(text)
    return detection.lang

def translate_to_english(text):
    translator = Translator()
    translation = translator.translate(text, dest='en')
    return translation.text

def translate_from_english(text, lang):
    translator = Translator()
    translation = translator.translate(text, dest=lang)
    return translation.text

@lru_cache(maxsize=1000)
def lemmatize_word(word):
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word)

def replace_synonyms(text):
    words = text.split()
    replaced_words = [synonyms.get(word.lower(), word) for word in words]
    return ' '.join(replaced_words)

def normalize_and_lemmatize(text):
    text = text.lower()
    words = re.findall(r'\w+', text)
    lemmatized_words = [lemmatize_word(word) for word in words]
    return ' '.join(lemmatized_words)

def get_word_similarity(word1, word2):
    return SequenceMatcher(None, word1, word2).ratio()

def get_most_similar_question(question):
    questions = list(dataset.keys())
    if not questions:
        return None

    question_words = question.lower().split()
    expanded_question = set(stemmer.stem(word) for word in question_words)

    highest_ratio = 0
    most_similar_question = None

    for q in questions:
        q_words = q.lower().split()
        expanded_q = set(stemmer.stem(word) for word in q_words)

        common_words = expanded_question.intersection(expanded_q)
        similarity_ratio = len(common_words) / len(expanded_question.union(expanded_q))

        fuzzy_ratio = fuzz.token_set_ratio(question, q) / 100
        word_similarity = sum(get_word_similarity(w1, w2) for w1 in expanded_question for w2 in expanded_q) / (len(expanded_question) * len(expanded_q))

        combined_score = (similarity_ratio + fuzzy_ratio + word_similarity) / 3
        if combined_score > highest_ratio:
            highest_ratio = combined_score
            most_similar_question = q

    if highest_ratio > 0.5:
        return most_similar_question
    return None

def detect_emotion(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']

    if compound_score >= 0.25:
        return 'happy'
    elif compound_score <= -0.25:
        return 'angry' if compound_score <= -0.5 else 'sad'
    else:
        return 'neutral'

def respond_based_on_emotion(emotion):
    return random.choice(emotion_responses[emotion])

def query_external_api(question):
    try:
        params = {'soru': question}
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            result = response.json()
            return result.get('cevap')
        else:
            return None
    except Exception as e:
        print(f"Error querying API: {e}")
        return None

def should_store_question(question):
    keywords = ["which", "who", "when", "how", "explain", "define"]
    return any(keyword in question.lower() for keyword in keywords)

def answer_question(question):
    normalized_question = normalize_and_lemmatize(replace_synonyms(question))
    similar_question = get_most_similar_question(normalized_question)

    if similar_question:
        return dataset[similar_question]
    else:
        return None

def chatbot_response(user_input):
    global conversation_history

    dataset_answer = answer_question(user_input)

    if dataset_answer:
        conversation_history.append(f"You: {user_input}")
        conversation_history.append(f"Bot: {dataset_answer}")
        trim_conversation_history()
        return dataset_answer

    conversation_history.append(f"You: {user_input}")
    history_string = "\n".join(conversation_history)

    api_response = query_external_api(history_string)
    if api_response and should_store_question(user_input):
        dataset[normalize_and_lemmatize(user_input)] = api_response[:len(api_response)//2] if len(api_response) > 200 else api_response

    conversation_history.append(f"Bot: {api_response if api_response else 'I don’t have an answer.'}")
    trim_conversation_history()
    return api_response if api_response else "I'm sorry, I don't have an answer for that."

def send_message(message):
    response = chatbot_response(message)
    return f"Bot: {response}" if response else "I'm sorry, I don't have an answer for that."

def chat():
    while True:
        user_input = input("Ask me a question or type 'exit' to leave: ")
        if user_input.lower() == 'exit':
            print("Exiting...")
            break
        emotion = detect_emotion(user_input)
        emotion_response = respond_based_on_emotion(emotion)
        print(emotion_response)
        print(send_message(user_input))