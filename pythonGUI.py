import os
from dotenv import load_dotenv
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

load_dotenv()
FIREBASE_URL = os.getenv("FIREBASE_URL")
AUTH_KEY = os.getenv("AUTH_KEY")




class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        self.label = Label(text="Aplikacja iot z Kivy")
        button1 = Button(text="kliknij")
        button2 = Button(text="cofnij ")
        button3 = Button(text="zamknij")
        button4 = Button(text="pokaz odpowiedz z response")
        button=Button(text="pokaz tekst")
        button1.bind(on_press=self.change_text)
        button2.bind(on_press=self.change_text)
        button.bind(on_press=self.show_text)
        
        button3.bind(on_press=self.close)
        button4.bind(on_press=self.get_status)
        self.label2 = Label(text="wpisz wyjście GPIO ")
        self.input=TextInput()
        self.input.bind(text=self.change_textTwo)
        self.input2=TextInput()
        self.input2.bind(text=self.change_textTwo)
        

        
        layout.add_widget(self.label)
        layout.add_widget(self.label2)
        layout.add_widget(self.input)
        layout.add_widget(button1)
        layout.add_widget(button2)
        layout.add_widget(button3)
        layout.add_widget(button4)
        layout.add_widget(button)
       
        return layout

    def change_text(self, instance):
        self.label.text = "Kliknięto przycisk!"
    
    def close(self, instance):
        App.get_running_app().stop()
    def reset_text(self,instance):
        self.label.text="Reset"
    
    def get_status(self,instance):
        url=f"{FIREBASE_URL}/gpios/digital/g2.json?auth={AUTH_KEY}"
        response=requests.get(url)
        self.label.text=response.text
    def show_text(self,instance):
        text_catch=self.input.text
        self.label.text=text_catch
    def change_textTwo(self, instance, value):
        self.label.text = "wpisano: " + value

    
  
if __name__ == "__main__":
    MyApp().run()