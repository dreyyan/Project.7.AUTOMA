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
import pygame

import time, json
import sys, os, subprocess

''' UTILITIES '''
# UTILITY: Load 'entities.json'
def load_entities():
    with open("entities.json", 'r', encoding="utf-8") as file:
        return json.load(file)
    
# UTILITY: Display Bot's Response
def response(bot_response) -> None:
    pygame.mixer.init()
    pygame.mixer.music.load("assets/type_SFX.mp3")
    pygame.mixer.music.set_volume(0.1)

    character_delay_animation(f"[AUTOMA]: ", 0.03, 0)
    delay(1)

    pygame.mixer.music.play()
    character_delay_animation(f"{bot_response}", 0.03, 1)

    pygame.mixer.music.fadeout(500)
    
# UTILITY: Display Header
def display_header():
    character_delay_animation(f"     `~`~`~ [A].[U].[T].[O].[M].[A]. ~`~`~`", 0.03, 1)
    character_delay_animation(f"{'#' * 48}", 0.02, 1)

''' PROCESS '''
# PROCESS: Welcomes the User
def greet():
    response("Hi, I'm A.U.T.O.M.A. Ask me anything!")

# PROCESS: Get User Prompt via Voice Recognition
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

# PROCESS: Use NLP English Model to Create 'doc' Object
def process_prompt(user_prompt):
    pygame.mixer.init()
    pygame.mixer.music.load("assets/type_SFX.mp3")
    pygame.mixer.music.set_volume(0.1)

    nlp = spacy.load("en_core_web_sm") # load spacy NLP english model
    character_delay_animation(f"   [You]: ", 0.03, 0)
    delay(1)

    pygame.mixer.music.play()
    character_delay_animation(f"{user_prompt}", 0.03, 1)
    pygame.mixer.music.fadeout(500)

    doc = nlp(user_prompt)
    return doc

# PROCESS: Register Specified Browser
def register_browser():
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# PROCESS: Return Command Name of Specified Browser
def get_specified_browser(lowercase_text, browsers_dict):
    for browser_friendly_lower, command_name in browsers_dict.items():
        if browser_friendly_lower in lowercase_text:
            return command_name
    return None

# PROCESS: Return Command Name of Specified App
def get_specified_app(lowercase_text, apps_dict):
    for app_friendly_lower, command_name in apps_dict.items():
        if app_friendly_lower in lowercase_text:
            return command_name
    return None

# PROCESS: Open the Specified Browser
def open_browser(specified_browser):
    try:
        register_browser()
        response(f"I'm opening {specified_browser} for you...")
        
        browser = webbrowser.get(specified_browser)
        browser.open('https://www.google.com')

    except webbrowser.Error:
        response(f"{specified_browser} is currently not available.")

# PROCESS: Close the Specified Browser
def close_browser(specified_browser):
    try:
        response(f"Closing {specified_browser}...")
        subprocess.run(["taskkill", "/im", f"{specified_browser}.exe", "/f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except webbrowser.Error:
        response(f"{specified_browser} is currently not available.")

# PROCESS: Open the Specified Application
def open_app(specified_app):
    try:
        subprocess.Popen(f"{specified_app}.exe")

    except Exception as e:
        response(f"I apologize, but it seems that I am unable to open {specified_app}...")

# PROCESS: Close the Specified Application
def close_app(specified_app):
    try:
        response(f"Closing {specified_app}...")
        subprocess.run(["taskkill", "/im", f"{specified_app}.exe", "/f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except Exception as e:
        response(f"I apologize, but it seems that I am unable to close {specified_app}...")

# PROCESS: Load Browser Names
def load_browser_entities(entities):
    browsers_dict = entities.get("browsers", {})
    browsers_dict = {browser.lower(): command for browser, command in browsers_dict.items()}
    return browsers_dict

# PROCESS: Load Application Names
def load_app_entities(entities):
    apps_dict = entities.get("applications", {})
    apps_dict = {browser.lower(): command for browser, command in apps_dict.items()}
    return apps_dict

# PROCESS: Open Action Handler
def handle_open(lowercase_text):
    entities = load_entities()
    browsers_dict = load_browser_entities(entities)
    apps_dict = load_app_entities(entities)
    
    specified_browser = get_specified_browser(lowercase_text, browsers_dict)
    specified_app = get_specified_app(lowercase_text, apps_dict)

    if specified_browser:
        open_browser(specified_browser)
    elif specified_app:
        open_app(specified_app)
    else:
        response("Sorry, I don't recognize which app or browser to open.")

# PROCESS: Close Action Handler
def handle_close(lowercase_text):
    entities = load_entities()
    browsers_dict = load_browser_entities(entities)
    apps_dict = load_app_entities(entities)

    specified_browser = get_specified_browser(lowercase_text, browsers_dict)
    specified_app = get_specified_app(lowercase_text, apps_dict)

    if specified_browser:
        close_browser(specified_browser)
    elif specified_app:
        close_app(specified_app)
    else:
        response("Sorry, I don't recognize which app or browser to close.")

    specified_app = get_specified_app(lowercase_text, apps_dict)
    if specified_app:
        close_app(specified_app)

# MAIN: Exit Conversation
def shutdown_AUTOMA():
    response("See you!")
    delay(1)
    exit(0)

# MAIN: Start Chatbot Conversation
def initiate_AUTOMA():
    clear_screen()

    pygame.mixer.init()
    pygame.mixer.music.load("assets/background_SFX.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()

    # 2. Display TUI Header
    display_header()
    # 3. Welcome User
    greet()

    # 4. Prompt User Response via Voice Recognition
    # user_response = listen_for_response()
    
    user_response = "Can you open Google Chrome for me?"
    # user_response = "Please close Google Chrome."
    # user_response = "Can you open notepad for me please?"
    # user_response = "Goodbye AUTOMA"

    # 5. Process User Response as Prompt
    doc = process_prompt(user_response)

    lowercase_text = doc.text.lower()

    
    # 6. Initiate Task based on Prompt
    if "open" in lowercase_text:
        handle_open(lowercase_text)
    elif "close" in lowercase_text:
        handle_close(lowercase_text)
    elif "bye" in lowercase_text:
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