import datetime
import random
import requests
import speech_recognition as sr
import webbrowser
import pyttsx3

# Speech listening and interpreting
def listen_to_user():
    audio_recognizer = sr.Recognizer()
    with sr.Microphone() as mic_input:
        print("Listening...")
        audio_recognizer.adjust_for_ambient_noise(mic_input)
        audio_data = audio_recognizer.listen(mic_input)

    try:
        spoken_text = audio_recognizer.recognize_google(audio_data, language="ru-RU")
        print("You said:", spoken_text)
        return spoken_text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Request failed:", e)
        return ""

# Retrieve festive dates from an API
def fetch_festivities(iso_code, year):
    api_url = f"https://date.nager.at/api/v2/publicholidays/{year}/{iso_code}"
    response = requests.get(api_url)
    if response.ok:
        festival_data = response.json()
        return festival_data
    else:
        print("Failed to fetch holidays")
        return None

# Respond to user commands
def handle_interaction(input_command, festive_list, tts_engine):
    if "hello" in input_command:
        salutations = ["hello", "hi there", "greetings"]
        chosen_salutation = random.choice(salutations)
        print(chosen_salutation)
        tts_engine.say(chosen_salutation)
    elif "how are you" in input_command:
        feelings = ["I'm doing well, thank you!", "Quite well, thanks!", "Great, and you?"]
        feeling = random.choice(feelings)
        print(feeling)
        tts_engine.say(feeling)
    elif "capabilities" in input_command:
        print("Commands I understand include:")
        print("1. hello")
        print("2. how are you")
        print("3. list")
        print("4. save")
        print("5. dates")
        print("6. next")
        print("7. count")
        print("8. open holidays")
        tts_engine.say("I can understand several commands including hello, how are you, list, and more.")
    elif "list" in input_command:
        print("Holidays list:")
        for festivity in festive_list:
            print(festivity["name"])
    elif "save" in input_command:
        with open("holiday_names.txt", "w", encoding="utf-8") as file:
            for festivity in festive_list:
                file.write(festivity["name"] + "\n")
        print("Holidays saved in holiday_names.txt")
    elif "dates" in input_command:
        with open("holiday_dates.txt", "w", encoding="utf-8") as file:
            for festivity in festive_list:
                file.write(f"{festivity['date']} - {festivity['name']}\n")
        print("Holidays and their dates saved in holiday_dates.txt")
    elif "next" in input_command:
        today = datetime.date.today()
        upcoming_festival = min(festive_list, key=lambda x: abs(datetime.datetime.strptime(x['date'], '%Y-%m-%d').date() - today))
        print("Next holiday:", upcoming_festival["name"], "on:", upcoming_festival["date"])
    elif "count" in input_command:
        print("Total number of holidays:", len(festive_list))
    elif "open holidays" in input_command:
        webbrowser.open("https://date.nager.at/")
    else:
        print("Command not recognized")

def run_bot():
    region_code = "GB"
    current_year = 2020

    festival_list = fetch_festivities(region_code, current_year)
    if not festival_list:
        return

    speech_engine = pyttsx3.init()

    while True:
        user_input = listen_to_user()
        if user_input:
            handle_interaction(user_input, festival_list, speech_engine)
            speech_engine.runAndWait()

if __name__ == "__main__":
    run_bot()
