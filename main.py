''' MODULES '''
from modules.character_delay_animation import character_delay_animation
from modules.clear_screen import clear_screen
from modules.delay import delay
from modules.display_format import display_format
from modules.display_function import display_function
from modules.display_line import display_line
from modules.error_message import error_message
from modules.insert_spaces import insert_spaces
from modules.line_delay_animation import line_delay_animation
from modules.press_enter_to_continue import press_enter_to_continue

''' IMPORTS '''
import spacy
import speech_recognition as sr
from halo import Halo
import webbrowser

import time, json
import sys, os, subprocess

''' UTILITIES '''
# UTILITY: load model & entities
def prepare_data():
    entities = load_entities() # load entities
    
    browsers_dict = entities.get("browsers", {})
    browsers_dict = {browser.lower(): command for browser, command in browsers_dict.items()}

    return entities, browsers_dict

# UTILITY: load 'entities.json'
def load_entities():
    with open("entities.json", 'r', encoding="utf-8") as file:
        return json.load(file)
    
# UTILITY: display bot response
def response(bot_response) -> None:
    character_delay_animation(f"[AUTOMA]: ", 0.03, 0)
    delay(1.5)
    character_delay_animation(f"{bot_response}", 0.03, 1)
    
# UTILITY: display header
def display_header():
    character_delay_animation(f"     `~`~`~ [A].[U].[T].[O].[M].[A]. ~`~`~`", 0.03, 1)
    character_delay_animation(f"{'#' * 48}", 0.03, 1)
    
''' PROCESS '''
# PROCESS: welcome user
def greet():
    response("Hi, I'm A.U.T.O.M.A. Ask me anything!")

# PROCESS: get user prompt via voice recognition
def listen_for_response():
    # create an instance of 'Recognizer'
    recognizer = sr.Recognizer()

    # use 'Microphone' as audio source
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1) # Noise reduction

        # prompt user to speak with AUTOMA
        response("What would you like to do?")
        user_audio_prompt = recognizer.listen(source) # Record audio from 'Microphone'

        try:
            spinner = Halo(spinner='dots') # Insert spinner
            spinner.start() # Start spinner

            # convert speech ~> text
            translated_text = recognizer.recognize_google(user_audio_prompt) # type: ignore

            spinner.stop()

        # ERROR: Speech not recognized
        except sr.UnknownValueError:
            response("Sorry, I could not understand the audio.")

        # ERROR: Google API failed
        except sr.RequestError:
            response("Server is busy, please try again later...")

    return translated_text

# PROCESS: use NLP english model to create doc object
def process_prompt(user_prompt): 
    nlp = spacy.load("en_core_web_sm") # load spacy NLP english model
    character_delay_animation(f"[You]: ", 0.03, 0)
    character_delay_animation(f"{user_prompt}", 0.03, 1)
    doc = nlp(user_prompt)
    return doc

# PROCESS: register browsers for recognition
def register_browser():
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))   

# PROCESS: open the specified browser
def open_browser(entities, doc, browsers_dict): 
    lowercase_text = doc.text.lower()
    for browser_friendly_lower, command_name in browsers_dict.items():
        if browser_friendly_lower in lowercase_text:
            specified_browser = command_name

            try:
                register_browser()
                response(f"I'm opening {specified_browser} for you...")
                
                browser = webbrowser.get(specified_browser)
                browser.open('https://www.google.com')
                break

            except webbrowser.Error:
                response(f"{browser_friendly_lower} is currently not available.")

# PROCESS: close the specified browser
def close_browser(entities, doc, browsers_dict):
    lowercase_text = doc.text.lower()
    for browser_friendly_lower, command_name in browsers_dict.items():
        if browser_friendly_lower in lowercase_text:
            specified_browser = command_name

            try:
                response(f"Closing {specified_browser}...")
                subprocess.run(["taskkill", "/im", f"{specified_browser}.exe", "/f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                break

            except webbrowser.Error:
                response(f"{browser_friendly_lower} is currently not available.")

# MAIN: Exit conversation
def shutdown_AUTOMA():
    response("See you!")
    exit(0)

# MAIN: Start chatbot conversation
def initiate_AUTOMA():
    clear_screen()

    # 1. Data Preparation
    entities, browsers_dict = prepare_data()
    # 2. Display TUI Header
    display_header()
    # 3. Welcome User
    greet()

    # 4. Prompt User Response via Voice Recognition
    # user_response = listen_for_response()
    
    # user_response = "Can you open Google Chrome for me?"
    # user_response = "Please close Google Chrome."
    user_response = "Goodbye AUTOMA"

    # 5. Process User Response as Prompt
    doc = process_prompt(user_response)

    text = doc.text.lower()

    # 6. Initiate Task based on Prompt
    if "open" in text:
        open_browser(entities, doc, browsers_dict)
    elif "close" in text:
        close_browser(entities, doc, browsers_dict)
    elif "bye" in text:
        shutdown_AUTOMA()

''' MAIN '''
initiate_AUTOMA()

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