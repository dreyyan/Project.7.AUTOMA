''' MODULES '''
from modules.character_delay_animation import character_delay_animation
from modules.clear_screen import clear_screen
from modules.delay import delay
from modules.error_message import error_message

''' IMPORTS '''
import spacy
import speech_recognition as sr
import webbrowser
import pygame
import threading, queue

import time, json
import sys, os, subprocess

text_queue = queue.Queue()
audio_queue = queue.Queue()

''' UTILITIES '''
# UTILITY: Load 'entities.json'
def load_entities():
    with open("entities.json", 'r', encoding="utf-8") as file:
        return json.load(file)
    
# UTILITY: Display Bot's Response
def response(bot_response) -> None:
    pygame.mixer.init()
    type_sfx = pygame.mixer.Sound("assets/type_SFX.mp3")
    type_sfx.set_volume(5)

    character_delay_animation(f"[AUTOMA]: ", 0.03, 0)
    delay(1)

    type_sfx.play()
    character_delay_animation(f"{bot_response}", 0.03, 1)

    type_sfx.fadeout(500)
    
# UTILITY: Display Header
def display_header():
    character_delay_animation(f"     `~`~`~ [A].[U].[T].[O].[M].[A]. ~`~`~`", 0.03, 1)
    character_delay_animation(f"{'#' * 48}", 0.02, 1)

# UTILITY: Format Search Query for Browsing
def simplify_search_query(text):
    text = text.lower().strip()
    # Define phrases to remove from the start
    prefixes = [
        "can you search for",
        "could you search for",
        "please search for",
        "search for",
        "i want to search for",
        "search",
        "find",
    ]
    for prefix in prefixes:
        if text.startswith(prefix):
            return text[len(prefix):].strip("? ").strip()
    return text.strip("? ")

''' PROCESS '''
# PROCESS: Welcomes the User
def greet():
    response("Hi, I'm A.U.T.O.M.A. Ask me anything!")

# PROCESS: Listen for User Text Input
def wait_text_input():
    while True:
        user_input = input().strip()
        text_queue.put(user_input)
        if user_input.lower() == 'exit':
            break

# PROCESS: Listen for User Prompt via Voice Recognition
def listen_for_response():
    # create an instance of 'Recognizer'
    recognizer = sr.Recognizer()

    # use 'Microphone' as audio source
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1) # Noise reduction

        while True:
            try:
                # prompt user to speak with AUTOMA
                user_audio_prompt = recognizer.listen(source) # Record audio from 'Microphone'

                # convert speech ~> text
                translated_text = recognizer.recognize_google(user_audio_prompt) # type: ignore

                audio_queue.put(translated_text)

                if translated_text.lower() == 'exit':
                    break
            except sr.WaitTimeoutError:
                continue
            # ERROR: Speech not recognized
            except sr.UnknownValueError:
                continue
            # ERROR: Google API failed
            except sr.RequestError:
                error_message("API request failed", 0.2)
                break

        character_delay_animation(translated_text, 0.03)

# PROCESS: Use NLP English Model to Create 'doc' Object
def process_prompt(user_prompt):
    pygame.mixer.init()
    pygame.mixer.music.load("assets/type_SFX.mp3")
    pygame.mixer.music.set_volume(60)

    nlp = spacy.load("en_core_web_sm") # load spacy NLP english model
    delay(1)

    pygame.mixer.music.play()
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
            return command_name, None
        
    if "search" in lowercase_text:
        search_query = simplify_search_query(lowercase_text)
        return None, search_query
    return None, None

# PROCESS: Return Command Name of Specified App
def get_specified_app(lowercase_text, apps_dict):
    for app_friendly_lower, command_name in apps_dict.items():
        if app_friendly_lower in lowercase_text:
            return app_friendly_lower.title(), command_name
    return None, None

# PROCESS: Open the Specified Browser
def open_browser(specified_browser):
    try:
        register_browser()
        response(f"Opening {specified_browser}...")
        
        browser = webbrowser.get(specified_browser)
        browser.open('https://www.google.com')

    except webbrowser.Error:
        response(f"{specified_browser} is currently not available.")

# PROCESS: Close the Specified Browser
def close_browser(specified_browser):
    try:
        if specified_browser == (None, None):
            response(f"Closing...")
        else: 
            response(f"Closing {specified_browser}...")
        subprocess.run(["taskkill", "/im", f"{specified_browser}.exe", "/f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except webbrowser.Error:
        response(f"{specified_browser} is currently not available.")

# PROCESS: Open the Specified Application
def open_app(app_command, app_name):
    try:
        if app_command.endswith(':'):
            os.system(f"start {app_command}")
        else:
            subprocess.Popen(f"{app_command}", creationflags=subprocess.CREATE_NEW_CONSOLE)
        response(f"Opening {app_name}...")

    except Exception as e:
        if app_name == None:
            response("I apologize, but it seems that I am unable to open the said app...")
        else:
            response(f"I apologize, but it seems that I am unable to open {app_name}...")

# PROCESS: Close the Specified Application
def close_app(app_command):
    try:
        if not app_command.endswith(".exe"):
            app_command += ".exe"

            response(f"Closing {app_command}...")
        subprocess.run(["taskkill", "/im", app_command, "/f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except Exception as e:
        if app_command == None:
            response("I apologize, but it seems that I am unable to open the said app...")
        else:
            response(f"I apologize, but it seems that I am unable to close {app_command[0]}...")

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
    
    specified_browser, search_query = get_specified_browser(lowercase_text, browsers_dict)
    app_name, app_command = get_specified_app(lowercase_text, apps_dict)

    if specified_browser:
        open_browser(specified_browser)
    elif search_query:
        response(f"I'm searching '{search_query}' for you...")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    elif app_command:
        open_app(app_command, app_name)
    else:
        response("Sorry, I don't recognize which app or browser to open.")

# PROCESS: Close Action Handler
def handle_close(lowercase_text):
    entities = load_entities()
    browsers_dict = load_browser_entities(entities)
    apps_dict = load_app_entities(entities)

    specified_browser, search_query = get_specified_browser(lowercase_text, browsers_dict)
    specified_app = get_specified_app(lowercase_text, apps_dict)

    if specified_browser:
        close_browser(specified_browser)
    elif specified_app:
        close_app(specified_app)
    else:
        response("Sorry, I don't recognize which app or browser to close.")

''' MAIN '''
# MAIN: Exit Conversation
def shutdown_AUTOMA():
    response("See you!")
    delay(1)
    exit(0)

# MAIN: Start Chatbot Conversation
def initiate_AUTOMA():
    clear_screen()
    # 1. Setup Background Music
    pygame.mixer.init()
    pygame.mixer.music.load("assets/background_SFX.mp3")
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play()

    # 2. Display TUI Header
    display_header()

    # 3. Welcome User
    greet()

    # 4. Prompt User Response via Voice Recognition / Text Input
    audio_thread = threading.Thread(target=listen_for_response, daemon=True)
    audio_thread.start()

    text_thread = threading.Thread(target=wait_text_input, daemon=True)
    text_thread.start()

    character_delay_animation("   [You]: ", 0.03, 0)
    while True:
        # 5. Process User Response as Prompt
        if not text_queue.empty():
            txt = text_queue.get()
            doc = process_prompt(txt)
            lowercase_text = doc.text.lower()

            # 6. Initiate Task based on Prompt
            # DEBUG: Fix threading & remove redundant output
            if "open" in lowercase_text or "search" in lowercase_text:
                handle_open(lowercase_text)
                character_delay_animation("   [You]: ", 0.03, 0)
            elif "close" in lowercase_text:
                handle_close(lowercase_text)
                character_delay_animation("   [You]: ", 0.03, 0)
            elif "exit" in lowercase_text or "bye" in lowercase_text:
                shutdown_AUTOMA()

        if not audio_queue.empty():
            audio_txt = audio_queue.get()
            doc = process_prompt(audio_txt)
            audio_txt_lower = audio_txt.lower()
            character_delay_animation(audio_txt, 0.03, 1)

            if "open" in audio_txt_lower or "search" in audio_txt_lower:
                handle_open(audio_txt_lower)
                character_delay_animation("   [You]: ", 0.03, 0)
            elif "close" in audio_txt_lower:
                handle_close(audio_txt_lower)
                character_delay_animation("   [You]: ", 0.03, 0)
            elif "exit" in audio_txt_lower or "bye" in audio_txt_lower:
                shutdown_AUTOMA()
                break

        delay(0.1)
    '''
    UNOPENABLE
    - Microsoft Edge
    - Clock

    UNCLOSABLE
    - Settings
    - Notepad
    - Task Manager
    - Camera
    - Command Prompt
    - Calculator
    - File Explorer
    '''

"""     "browsers": {
        "Google Chrome": "chrome",
        "Mozilla Firefox": "firefox",
        "Safari": "safari",
        "Microsoft Edge": "edge",
        "Opera": "opera",
        "Samsung Internet": "samsung-internet",
        "UC Browser": "ucbrowser",
        "Tor Browser": "torbrowser"
    },
    
    "applications": {
        "Calculator": "calc.exe",
        "Notepad": "notepad.exe",
        "Clock": "timers.exe",
        "Camera": "microsoft.windows.camera:",
        "Command Prompt": "cmd.exe",
        "File Explorer": "explorer.exe",
        "Settings": "ms-settings:",
        "Task Manager": "taskmgr.exe"
    } """

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