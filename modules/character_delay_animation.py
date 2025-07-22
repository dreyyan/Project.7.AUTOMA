import time
# UTILITY: Display text with a typing effect
def character_delay_animation(string_input, seconds, print_newline):
    for char in string_input:
        print(char, end="", flush=True)
        time.sleep(seconds)
    if print_newline:
       print()  