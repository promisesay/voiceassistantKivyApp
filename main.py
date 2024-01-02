import speech_recognition as sr
import pyttsx3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from threading import Thread
import record_audio  # Import the module with PyAudio recording code
import webbrowser


class VoiceAssistantApp(App):
    def __init__(self, **kwargs):
        super(VoiceAssistantApp, self).__init__(**kwargs)
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.label = Button(text='Voice Assistant', font_size=20)
        layout.add_widget(self.label)

        button_listen = Button(text='Start Listening', on_press=self.start_listening)
        layout.add_widget(button_listen)

        button_record = Button(text='Record Audio', on_press=self.record_audio)
        layout.add_widget(button_record)

        button_search = Button(text='google', on_pres=self.websearch)
        layout.add_widget(button_search)
        return layout

    def start_listening(self, instance):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio)
            print("You said:", command)
            self.label.text = f'You said: {command}'

            # Process the voice command and respond
            if 'hello' in command.lower():
                response = "Hello! How can I help you?"
            elif 'time' in command.lower():
                from datetime import datetime
                current_time = datetime.now().strftime("%H:%M")
                response = f"The current time is {current_time}."
            else:
                response = "I'm sorry, I didn't understand that command."

            # Display and speak the response
            print("Response:", response)
            self.label.text += f'\nResponse: {response}'
            self.speak(response)

        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print(f"Error making the request; {e}")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def websearch(self, instance):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("listening...")
            audio = self.recognizer.listen(source)
        webbrowser.open(f'https://www.google.com/search?q={audio}')

    def record_audio(self, instance):
        # Run the record_and_save function in a separate thread to avoid freezing the GUI
        Thread(target=record_audio.record_and_save, args=('recorded_audio.wav',)).start()


if __name__ == '__main__':
    VoiceAssistantApp().run()
