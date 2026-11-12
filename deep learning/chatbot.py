
import speech_recognition as sr
import pyttsx3
import pywhatkit as pk
import sounddevice as sd
import webbrowser
import subprocess
import datetime
import urllib.parse
import numpy as np
import re


# ==========================================
# INITIALIZATION
# ==========================================

listener = sr.Recognizer()
engine = pyttsx3.init()

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

SAMPLE_RATE = 16000
ASSISTANT_NAME = "shubham"


# ==========================================
# SPEAK FUNCTION
# ==========================================

def speak(text):

    print("\nAssistant:", text)

    engine.say(text)
    engine.runAndWait()


# ==========================================
# MICROPHONE FUNCTION
# No PyAudio required
# ==========================================

def hear():

    try:

        print("\nListening... Speak now!")

        duration = 6

        audio = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        audio_data = sr.AudioData(
            audio.tobytes(),
            SAMPLE_RATE,
            2
        )

        command = listener.recognize_google(
            audio_data,
            language="en-IN"
        )

        command = command.lower().strip()

        print("You:", command)

        command = re.sub(
            r"\b" + ASSISTANT_NAME + r"\b",
            "",
            command
        ).strip()

        return command

    except sr.UnknownValueError:

        print("Could not understand audio")
        return ""

    except sr.RequestError as e:

        print("Google Speech API error:", e)
        return ""

    except Exception as e:

        print("Microphone error:", e)
        return ""


# ==========================================
# OPEN APPLICATIONS
# ==========================================

def open_app(app):

    applications = {

        "notepad": ["notepad.exe"],
        "calculator": ["calc.exe"],
        "paint": ["mspaint.exe"],
        "file explorer": ["explorer.exe"],
        "command prompt": ["cmd.exe"],
        "powershell": ["powershell.exe"]

    }

    if app in applications:

        try:

            subprocess.Popen(applications[app])

            speak("Opening " + app)

        except Exception as e:

            speak("Unable to open application")
            print(e)

    elif app in ["vscode", "visual studio code"]:

        try:

            subprocess.Popen(["code"])

            speak("Opening Visual Studio Code")

        except Exception as e:

            speak("VS Code is not available")
            print(e)

    else:

        speak("Application not found in my allowed list")


# ==========================================
# OPEN WEBSITES
# ==========================================

def open_website(site):

    websites = {

        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://github.com",
        "linkedin": "https://www.linkedin.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "gmail": "https://mail.google.com",
        "chatgpt": "https://chatgpt.com"

    }

    site = site.lower().strip()

    if site in websites:

        webbrowser.open(websites[site])

        speak("Opening " + site)

    else:

        speak("Website not found")


# ==========================================
# PLAY SONG ON YOUTUBE
# ==========================================

def play_song(song):

    song = song.strip()

    if not song:

        speak("Please tell me the song name")
        return

    try:

        speak("Playing " + song + " on YouTube")

        pk.playonyt(song)

    except Exception as e:

        speak("Unable to play song")
        print("YouTube error:", e)


# ==========================================
# GOOGLE SEARCH
# ==========================================

def google_search(query):

    query = query.strip()

    if query:

        speak("Searching Google for " + query)

        url = (
            "https://www.google.com/search?q="
            + urllib.parse.quote_plus(query)
        )

        webbrowser.open(url)

    else:

        speak("Please tell me what to search")


# ==========================================
# TIME
# ==========================================

def tell_time():

    current_time = datetime.datetime.now().strftime(
        "%I:%M %p"
    )

    speak("The current time is " + current_time)


# ==========================================
# DATE
# ==========================================

def tell_date():

    current_date = datetime.datetime.now().strftime(
        "%A, %d %B %Y"
    )

    speak("Today's date is " + current_date)


# ==========================================
# COMMAND PROCESSOR
# ==========================================

def process_command(cmd):

    cmd = cmd.lower().strip()

    if not cmd:
        return True

    print("\nProcessing command:", cmd)

    # EXIT
    if any(word in cmd for word in [
        "exit",
        "quit",
        "stop assistant",
        "goodbye"
    ]):

        speak("Goodbye Shubham!")
        return False

    # PLAY SONG
    # Examples:
    # Play Arijit Singh
    # Open YouTube and play Arijit Singh

    if "play" in cmd:

        song = cmd.split("play", 1)[1].strip()

        song = re.sub(
            r"\b(on|in)\s+youtube\b",
            "",
            song
        ).strip()

        song = re.sub(
            r"\byoutube\b",
            "",
            song
        ).strip()

        play_song(song)

        return True

    # OPEN WEBSITE OR APPLICATION
    if cmd.startswith(("open ", "visit ", "go to ")):

        target = re.sub(
            r"^(open|visit|go to)\s+",
            "",
            cmd
        ).strip()

        # Remove speech recognition filler
        target = re.sub(
            r"^(the|d|a)\s+",
            "",
            target
        ).strip()

        websites = [
            "youtube",
            "google",
            "github",
            "linkedin",
            "facebook",
            "instagram",
            "gmail",
            "chatgpt"
        ]

        if target in websites:

            open_website(target)

        else:

            open_app(target)

        return True

    # SEARCH GOOGLE
    if cmd.startswith("search"):

        query = re.sub(
            r"^search( for)?\s*",
            "",
            cmd
        ).strip()

        google_search(query)

        return True

    # TIME
    if "time" in cmd:

        tell_time()
        return True

    # DATE
    if "date" in cmd or "today" in cmd:

        tell_date()
        return True

    # GREETING
    if "hello" in cmd or "hi" in cmd:

        speak("Hello Shubham! How can I help you?")
        return True

    # ASSISTANT IDENTITY
    if "your name" in cmd or "who are you" in cmd:

        speak("I am Shubham's personal AI assistant.")
        return True

    # HELP
    if "help" in cmd or "commands" in cmd:

        speak(
            "I can open websites, open applications, "
            "play songs, search Google, tell date and time, "
            "and stop the assistant."
        )

        return True

    # UNKNOWN COMMAND
    speak("Sorry, I don't understand this command yet.")

    return True


# ==========================================
# MAIN FUNCTION
# ==========================================

def run():

    speak("Hello Shubham!")

    speak("Your personal AI assistant is ready.")

    speak("Tell me what you want me to do.")

    running = True

    while running:

        command = hear()

        if command:

            running = process_command(command)


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":

    try:

        run()

    except KeyboardInterrupt:

        print("\nAssistant stopped by keyboard.")

    except Exception as e:

        print("\nUnexpected error:", e)
