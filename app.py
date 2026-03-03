from datetime import datetime
import webbrowser
import requests
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = recognizer.listen(source)

        user_msg = recognizer.recognize_google(audio)
        print(f"You said: {user_msg}")
        return user_msg.lower()

    except:
        speak("Sorry, I did not understand that.")
        return ""

# Corpus
greet_msgs = ["hi", "hello", "hey", "hi there", "hello there"]
date_msgs = ["date", "tell me date", "today's date"]
time_msgs = ["time", "tell me time", "current time"]
news_msgs = ["tell me new", "news", "headlines"]

def get_news():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=695e07af402f4b119f0703e9b19f4683"
    response = requests.get(url)

    if response.status_code != 200:
        speak("Unable to fetch news")
        return

    data = response.json()

    if "articles" not in data:
        speak("No news available")
        return

    articles = data["articles"]

    for article in articles[:5]:
        title = article.get("title")
        if title:
            speak(title)

chat = True

while chat:
    user_msg = listen()

    if not user_msg:
        continue

    if user_msg in greet_msgs:
        speak("Hello User. How may I help you ?")

    elif user_msg in date_msgs:
        today = datetime.now().date()
        speak(f"Today's date is {today}")

    elif user_msg in time_msgs:
        current_time = datetime.now().time()
        speak(current_time.strftime("Time is %I:%M:%S %p"))

    elif "open" in user_msg:
        website_name = user_msg.split()[-1]
        webbrowser.open(f"https://www.{website_name}.com")
        speak(f"Opening {website_name}")

    elif user_msg in news_msgs:
        get_news()

    elif "calculate" in user_msg:
        expression = user_msg.replace("calculate", "").strip()
        try:
            result = eval(expression, {"__builtins__": None})
            speak(f"Result is {result}")
        except:
            speak("Invalid calculation")

    elif user_msg == "bye-bye":
        speak("Goodbye")
        chat = False

    else:
        # Echo reply
        speak("You said " + user_msg)

