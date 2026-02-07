"""
VIOLA - AI Voice Assistant
A Python-based voice assistant that listens to commands and performs various tasks.

SUPPORTED COMMANDS:
==================

Web Navigation:
  - "open google"      : Opens Google search
  - "open youtube"     : Opens YouTube channel
  - "open github"      : Opens GitHub profile
  - "open stack overflow" : Opens Stack Overflow

Music Control:
  - "play [song name]" : Plays a song from library (virtual, checkpoint, ping, overthinker, playlist)
  - "play the [song]"  : Plays with "the" prefix (e.g., "play the virtual")
  - "play"             : Lists all available songs

Information:
  - "what is the time" : Announces current time
  - "tell me the time" : Announces current time
  - "what is your name" : Assistant introduces itself
  - "who are you"      : Assistant introduces itself

News:
  - "tell me news" or "give me news" : Tells top 5 latest headlines from India
  - "latest news"      : Tells top 5 latest headlines from India

Control:
  - "stop listening"   : Exit the program

Wake Word: "Viola" (case-insensitive)
"""

import speech_recognition as sr
import webbrowser
import pyttsx3
import sys
import musicLibrary
import newsLibrary

def speak(text):
    """
    Convert text to speech using pyttsx3 engine with female voice.
    
    Args:
        text (str): The text to be spoken
    
    Returns:
        None
    """
    try:
        # Initialize the text-to-speech engine
        engine = pyttsx3.init()
        
        # Set speech rate (higher = faster, lower = slower)
        engine.setProperty('rate', 150)
        
        # Set voice to female (voices[1] is typically the female voice)
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)  # Female voice
        
        # Queue the text to be spoken
        engine.say(text)
        
        # Block until the speech finishes
        engine.runAndWait()
        
        # Stop the engine
        engine.stop()
    except Exception as e:
        print(f"Error in speak: {e}")
        sys.stdout.flush()

def process_command(c):
    """
    Process user commands and perform corresponding actions.
    
    Args:
        c (str): The command string to process (case-insensitive)
    
    Returns:
        None
    """
    c = c.lower()
    print("Processing command: " + c)
    
    # Web Navigation Commands
    if "open google" in c:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")
    
    elif "open youtube" in c:
        speak("Opening Youtube...")
        webbrowser.open("https://www.youtube.com/@LotusOutlook")
    
    elif "open github" in c:
        speak("Opening GitHub...")
        webbrowser.open("https://github.com/lotus-outlook-6")
    
    # Information Commands
    elif "what is the time" in c or "tell me the time" in c:
        from datetime import datetime
        time = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")
    
    elif "what is your name" in c or "who are you" in c:
        speak("I am Viola, your AI assistant")
    
    # Music Control Commands
    elif "play" in c:
        # Extract song name from command (e.g., "play virtual" -> "virtual")
        # Remove "play" from start and handle "the" as a word, not substring
        song_name = c.replace("play", "", 1).strip()  # Remove first occurrence of "play"
        
        # Remove "the" if it's at the beginning as a separate word
        if song_name.startswith("the "):
            song_name = song_name[4:].strip()
        
        if song_name:
            # Try to find the song in the music library
            link = musicLibrary.get_music_link(song_name)
            if link:
                speak(f"Playing {song_name}")
                webbrowser.open(link)
            else:
                available_songs = ", ".join(musicLibrary.list_available_songs())
                speak(f"Sorry, I don't have {song_name} in my library. Available songs are: {available_songs}")
        else:
            # User said "play" without specifying a song
            available_songs = ", ".join(musicLibrary.list_available_songs())
            speak(f"Available songs are: {available_songs}")
    
    # News Commands
    elif "news" in c or "headlines" in c:
        speak("Fetching the latest news from India. Please wait...")
        headlines = newsLibrary.get_india_news()
        
        # Speak each headline
        for headline in headlines:
            speak(headline)
        
        speak("That's all the news for now.")
    
    # Default case: command not recognized
    else:
        speak("I didn't understand that command")

    

if __name__ == "__main__":
    """
    Main entry point of the Viola voice assistant.
    Continuously listens for the wake word "Viola" and processes user commands.
    """
    
    print("Starting Viola...")
    try:
        speak("Initializing Viola...")
    except Exception as e:
        print(f"Warning: Initial speak failed - {e}")
        print("Continuing anyway...")
    
    # Main listening loop
    while True:
        # Create a speech recognizer object
        r = sr.Recognizer()
        
        try:
            # Use the microphone as the audio source
            with sr.Microphone() as source:
                # Adjust recognizer to ambient noise to improve accuracy
                r.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for the wake word
                print("Listening...")
                try:
                    # Listen for audio input (timeout=2 seconds)
                    audio = r.listen(source, timeout=2, phrase_time_limit=2)
                except sr.WaitTimeoutError:
                    print("No speech detected, retrying...")
                    continue
                
                # Recognize speech using Google Speech Recognition API
                print("Recognizing...")
                try:
                    word = r.recognize_google(audio)
                    print(f"Heard: {word}")
                except sr.UnknownValueError:
                    print("Could not understand, retrying...")
                    continue
                
                # Check for stop command first
                if "stop listening" in word.lower():
                    print("Stop listening command detected, exiting...")
                    speak("Stopping Viola. Goodbye!")
                    break
                
                # Check if the wake word "viola" was detected
                if "viola" in word.lower():
                    print("Wake word detected!")
                    speak("Yes, how can I help you?")
                    print("Viola is listening for a command...")
                    
                    try:
                        # Listen for the actual command (timeout=10 seconds)
                        audio = r.listen(source, timeout=10, phrase_time_limit=10)
                    except sr.WaitTimeoutError:
                        print("Timed out, returning to listen mode...")
                        continue
                    
                    # Recognize the command
                    print("Recognizing...")
                    try:
                        command = r.recognize_google(audio)
                        print(f"Command received: {command}")
                        # Process the recognized command
                        process_command(command)
                    except sr.UnknownValueError:
                        speak("I didn't understand that command")
        
        except sr.WaitTimeoutError:
            # Timeout while listening for wake word, continue
            pass
        except Exception as e:
            # Handle any other exceptions
            print("Error!!! {0}".format(e))
            import traceback
            traceback.print_exc()