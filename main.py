import openai
import speech_recognition as sr
import pyttsx3

# Set up OpenAI API Key (Replace with your API key)
openai.api_key = "your_openai_api_key_here"

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Set speech speed

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech from the microphone
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            print("Could not request results, please check your internet connection.")
            return None

# Function to generate response using OpenAI GPT
def get_response(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change to GPT-4 if available
            messages=[{"role": "user", "content": query}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Main function to run the voice agent
def voice_agent():
    while True:
        user_input = listen()
        if user_input:
            if user_input.lower() in ["exit", "quit", "stop"]:
                print("Goodbye!")
                speak("Goodbye!")
                break
            response = get_response(user_input)
            print(f"AI: {response}")
            speak(response)

if __name__ == "__main__":
    voice_agent()
