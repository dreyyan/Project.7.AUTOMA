''' MODULES '''
from modules.character_delay_animation import character_delay_animation
from modules.clear_screen import clear_screen
from modules.delay import delay
from modules.display_format import display_format
from modules.display_function import display_function
from modules.display_header import display_header
from modules.display_line import display_line
from modules.error_message import error_message
from modules.insert_spaces import insert_spaces
from modules.line_delay_animation import line_delay_animation
from modules.press_enter_to_continue import press_enter_to_continue

''' IMPORTS '''
import spacy
import speech_recognition as sr
from halo import Halo

import time, sys, json

# UTILITY: Display user's prompt
def prompt(user_prompt) -> None:
    character_delay_animation(f"[You]: {user_prompt}", 0.03)

# UTILITY: Display bot response
def response(bot_response) -> None:
    character_delay_animation(f"[AUTOMA]: {bot_response}", 0.03)

# UTILITY: Load entities.json
def load_entities():
    with open("entities.json", 'r', encoding="utf-8") as file:
        return json.load(file)

''' MAIN: Voice Recognition '''
'''
# 1. Create an instance of 'Recognizer'
recognizer = sr.Recognizer()

# 2. Use 'Microphone' as audio source
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=1) # Noise reduction

    # 3. Prompt user to speak with AUTOMA
    response("What would you like to do?")
    user_audio_prompt = recognizer.listen(source) # Record audio from 'Microphone'

    try:
        spinner = Halo(spinner='dots') # Insert spinner
        spinner.start() # Start spinner

        # 4. Convert speech ~> text
        translated_text = recognizer.recognize_google(user_audio_prompt) # type: ignore

        spinner.stop()

    # ERROR: Speech not recognized
    except sr.UnknownValueError:
        response("Sorry, I could not understand the audio.")

    # ERROR: Google API failed
    except sr.RequestError:
        response("Server is busy, please try again later...")
'''
# DEBUG
translated_text:str = "Can you open Google Chrome for me?"

''' MAIN: Natural Language Processing(NLP) '''
# 5. Display translated text
prompt(translated_text)

# 6. Load spacy NLP english model
nlp = spacy.load("en_core_web_sm") 

# 7. convert translated text into an NLP object
doc = nlp(translated_text)

# 8. load entities list if an entity is recognized
if doc.ents:
    entities = load_entities()
    print(entities)

""" while True:
    print("[ TOKENIZATION ]")
    display_format('#', 16)

    # 1. Tokenization [ Splitting Text ]
    for token in doc:
        print(f'{token.text}')

    print()
    print("[ NAMED ENTITY RECOGNITION ]")
    display_format('#', 28)

    # 2. NER [ Named Entity Recognition ]
    for token in doc.ents:
        print(f'{token.text} >> {token.label_}')

    print()
    print("[ PART-OF-SPEECH ]")
    display_format('#', 18)

    # 3. POS [ Part-of-speech ]
    for token in doc:
        print(f'{token.text} >> {token.pos_}')

    print()
    print("[ LEMMATIZATION ]")
    display_format('#', 17)

    # 4. Lemmatization [ Extracting base form of words ]
    for token in doc:
        print(f'{token.text} >> {token.lemma_}')

    print()
    print("[ DEPENDENCY PARSING ]")
    display_format('#', 22)

    # 5. Dependency Parsing [ Finding relationships ]
    for token in doc:
        print(f'{token.text} >> {token.dep_} >> {token.head.text}')
    break
 """