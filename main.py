import os
import requests
from dotenv import load_dotenv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import Screen

load_dotenv()

import os
import requests
from dotenv import load_dotenv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from dotenv import load_dotenv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

# Wczytaj dane z .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

def login_to_firebase(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    return response.json()

def set_gpio(gpio_pin: str, value: int):
    app = App.get_running_app()
    token = getattr(app, "user_token", None)
    url = f"https://console-control-1ddfc-default-rtdb.firebaseio.com/gpios/digital/{gpio_pin}.json"
    if token:
        url += f"?auth={token}"
    response = requests.put(url, json=value)
    return response.ok

def add_gpio(gpio_pin: str, value: int):
    return set_gpio(gpio_pin, value)

def delete_gpio(gpio_pin: str):
    app = App.get_running_app()
    token = getattr(app, "user_token", None)
    url = f"https://console-control-1ddfc-default-rtdb.firebaseio.com/gpios/digital/{gpio_pin}.json"
    if token:
        url += f"?auth={token}"
    response = requests.delete(url)
    return response.ok

def get_gpio(gpio_pin: str):
    app = App.get_running_app()
    token = getattr(app, "user_token", None)
    url = f"https://console-control-1ddfc-default-rtdb.firebaseio.com/gpios/digital/{gpio_pin}.json"
    if token:
        url += f"?auth={token}"
    response = requests.get(url)
    if response.ok:
        return response.json()
    return None

# ------------------ Styl ------------------
def stylized_button(text):
    return Button(
        text=text,
        font_size=16,
        background_color=(0.2, 0.6, 0.8, 1),
        color=(1, 1, 1, 1),
        size_hint=(1, None),
        height=50
    )

def stylized_input(hint):
    return TextInput(
        hint_text=hint,
        font_size=16,
        foreground_color=(0, 0, 0, 1),
        background_color=(1, 1, 1, 1),
        padding_y=(10, 10),
        size_hint=(1, None),
        height=40
    )

# ------------------ Ekrany ------------------
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=15, padding=40)

        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.status_label = Label(text="Zaloguj się", font_size=20)
        self.email_input = stylized_input("Email")
        self.password_input = stylized_input("Hasło")
        self.password_input.password = True
        self.login_button = stylized_button("Zaloguj")
        self.login_button.bind(on_press=self.attempt_login)

        layout.add_widget(self.status_label)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.login_button)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def attempt_login(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        result = login_to_firebase(email, password)
        if "idToken" in result:
            App.get_running_app().user_token = result["idToken"]
            self.status_label.text = "Zalogowano!"
            self.manager.current = "panel"
        else:
            error = result.get("error", {}).get("message", "Nieznany błąd")
            self.status_label.text = f"Błąd: {error}"

class RoomScreen(Screen):
    def __init__(self, room_name, gpio_pin, **kwargs):
        super().__init__(**kwargs)
        self.gpio_pin = gpio_pin
        self.room_name = room_name

        layout = BoxLayout(orientation='vertical', spacing=15, padding=40)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.status = Label(text=f"Pokój: {room_name}", font_size=20)
        layout.add_widget(self.status)
        self.gpio_status_label = Label(text="Stan: (nieznany)", font_size=16)
        layout.add_widget(self.gpio_status_label)

        btn_on = stylized_button(f"Włącz {gpio_pin}")
        btn_on.bind(on_press=self.turn_on)
        layout.add_widget(btn_on)

        btn_off = stylized_button(f"Wyłącz {gpio_pin}")
        btn_off.bind(on_press=self.turn_off)
        layout.add_widget(btn_off)

        self.new_gpio_input = stylized_input("np. g100")
        self.new_gpio_value = stylized_input("Wartość 0 lub 1")
        layout.add_widget(self.new_gpio_input)
        layout.add_widget(self.new_gpio_value)

        btn_add = stylized_button("Dodaj GPIO")
        btn_add.bind(on_press=self.add_new_gpio)
        layout.add_widget(btn_add)

        self.delete_gpio_input = stylized_input("GPIO do usunięcia")
        layout.add_widget(self.delete_gpio_input)

        btn_delete = stylized_button("Usuń GPIO")
        btn_delete.bind(on_press=self.delete_selected_gpio)
        layout.add_widget(btn_delete)

        btn_back = stylized_button("Wróć")
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

        Clock.schedule_interval(lambda dt: self.update_gpio_status(), 5)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_gpio_status(self):
        value = get_gpio(self.gpio_pin)
        if value is not None:
            self.gpio_status_label.text = f"Stan: {value}"
        else:
            self.gpio_status_label.text = "Błąd odczytu"

    def turn_on(self, instance):
        success = set_gpio(self.gpio_pin, 1)
        self.status.text = f"{self.gpio_pin} = 1" if success else "Błąd"

    def turn_off(self, instance):
        success = set_gpio(self.gpio_pin, 0)
        self.status.text = f"{self.gpio_pin} = 0" if success else "Błąd"

    def add_new_gpio(self, instance):
        pin = self.new_gpio_input.text.strip()
        value_text = self.new_gpio_value.text.strip()
        try:
            value = int(value_text)
            if value not in (0, 1): raise ValueError
        except:
            self.status.text = "Nieprawidłowa wartość"
            return
        success = add_gpio(pin, value)
        self.status.text = f"Dodano {pin}" if success else "Błąd dodawania"

    def delete_selected_gpio(self, instance):
        pin = self.delete_gpio_input.text.strip()
        success = delete_gpio(pin)
        self.status.text = f"Usunięto {pin}" if success else "Błąd usuwania"

    def go_back(self, instance):
        self.manager.current = "panel"

class PanelScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=15, padding=40)

        with self.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.status = Label(text="Wybierz pokój", font_size=20)
        layout.add_widget(self.status)

        for room in ["Kuchnia", "Korytarz", "Łazienka"]:
            btn = stylized_button(room)
            btn.bind(on_press=self.room_selected)
            layout.add_widget(btn)

        btn_logout = stylized_button("Wyloguj")
        btn_logout.bind(on_press=self.logout)
        layout.add_widget(btn_logout)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def room_selected(self, instance):
        mapping = {
            "Kuchnia": "kuchnia",
            "Korytarz": "korytarz",
            "Łazienka": "lazienka"
        }
        self.manager.current = mapping.get(instance.text, "panel")

    def logout(self, instance):
        App.get_running_app().user_token = None
        self.manager.current = "login"

class FirebaseLoginApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(PanelScreen(name="panel"))
        sm.add_widget(RoomScreen("Kuchnia", "g2", name="kuchnia"))
        sm.add_widget(RoomScreen("Korytarz", "g4", name="korytarz"))
        sm.add_widget(RoomScreen("Łazienka", "g18", name="lazienka"))
        return sm

if __name__ == "__main__":
    FirebaseLoginApp().run()