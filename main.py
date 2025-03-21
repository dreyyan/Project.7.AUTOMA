 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#       Project: AUTOMA(Advanced Utility Task-Optimized Machine Assistant)  #
#        Author: dreyyan                                                    #
#      Language: Python                                                     #
#  Date Started: 03/15/2025                                                 #
# Date Finished: 03/16/2025                                                 #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# LIBRARIES: Spacy(NLP), Google API(speech-to-text), Halo(Spinner)
''' IMPORTS: LIBRARY '''
import spacy
import speech_recognition as sr
from halo import Halo

''' IMPORTS: STANDARD '''
import time, sys

''' FUNCTIONS: UTILITY '''
# UTILITY: Display text with a typing effect
def character_delay_animation(string_input, seconds):
    for char in string_input:
        print(char, end="", flush=True)
        time.sleep(seconds)
    print()

# UTILITY: Display user's prompt
def prompt(user_prompt):
    character_delay_animation(f"[You]: {user_prompt}", 0.03)

# UTILITY: Display bot response
def response(bot_response):
    character_delay_animation(f"[AUTOMA]: {bot_response}", 0.03)

''' FUNCTIONS: SPEECH RECOGNITION '''
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
        translated_text = recognizer.recognize_google(user_audio_prompt)

        # 5. Display translated text
        spinner.stop()
        prompt(translated_text)

    # ERROR: Speech not recognized
    except sr.UnknownValueError:
        response("Sorry, I could not understand the audio.")

    # ERROR: Google API failed
    except sr.RequestError:
        response("Server is busy, please try again later...")

# nlp = spacy.load("en_core_web_sm") # Load spacy NLP english model
# doc = nlp() # Process with NLP
