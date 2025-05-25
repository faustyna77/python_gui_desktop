Kolegium Nauk Przyrodniczych
Uniwersytet Rzeszowski




Przedmiot:
Nierelacyjne bazy danych 

Projekt 

Autor:
Faustyna Misiura 119041




Rzeszów 2025









Dokumentacja projektu – System zarządzania GPIO z Firebase
1. Informacje ogólne
Projekt jest aplikacja desktopowa wykonana we frameworku Kivy (Python), aplikacja ma na celu służyc zdalnemu kontrolowaniu oświetlenia w domku jednorodzinnym/ mieszkaniu w bloku. 
 
2. Charakterystyka projektu
Aplikacja desktopowa umożliwiająca logowanie użytkownika i sterowanie pinami GPIO za pomocą interfejsu graficznego zbudowanego w Kivy. Dane przechowywane są w systemie Firebase Realtime Database. Użytkownik może logować się, włączać/wyłączać piny, dodawać i usuwać GPIO, wyświetlać aktualny podgląd stanu GPIO  oraz zarządzać  oświetleniem w podziale na pomieszczenia.


3. Model danych i system bazodanowy
Użyty model danych: klucz–wartość
System bazodanowy: Firebase Realtime Database
Przykład struktury danych:

{
  "gpios": {
    "digital": {
      "g2": 1,
      "g4": 0
    }
  }
}

Rys.1 Zrzut ekranu bazy danych 



Rys.2 Zrzut eranu do oszczególnych wejść/wyjść 




Powyższa baza danych została utworzona w procesie konfiguracji Firebase, natomaist dane dla poszczególnych wyjść zostały przypisane defaultowo jako 0 lub 1 i są to dane typu int 






4. Uzasadnienie wyboru
Firebase oferuje prosty i szybki dostęp do danych oraz wbudowaną autentykację użytkowników. Model klucz–wartość świetnie nadaje się do reprezentacji stanów pinów GPIO, a użycie Kivy pozwala stworzyć wygodny interfejs użytkownika.
5. Architektura aplikacji
Aplikacja została napisana w Pythonie z użyciem biblioteki Kivy. Składa się z następujących ekranów:
- LoginScreen: logowanie użytkownika
- PanelScreen: wybór pokoju
- RoomScreen: sterowanie GPIO w konkretnym pokoju
Dostęp do bazy realizowany jest przez REST API Firebase z użyciem tokena autoryzacyjnego.



Rys.3 Panel logowania

Logowanie zostało przeprowadzone za pomcą firebase authorization, o zamieszczeniu użytkowników, którzy mają dostęp do aplikacji w panelu Firebase 

Rys.4 Użytkownicy, którzy posiadają uprawnienia zalogowania się do aplaikcji 

Fragment kodu, odpowiedzilany za logikę logowania do aplaikcji:


# ------------------ Firebase operacje ------------------
def login_to_firebase(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    return response.json()



 
6. Operacje CRUD
- CREATE: Dodanie nowego pinu (np. g100)


- READ: Odczyt danych z Firebase (opcjonalny widok statusu)


- UPDATE: Zmiana stanu GPIO (ON/OFF)

Widok po aktualizacji pinu jest widoczny na sprzęcie fizycznym:


-DODAWANIE pinu




- DELETE: Usunięcie pinu



7. Przypadek użycia
Użytkownik loguje się do systemu. Wybiera pokój 'Kuchnia'. Włącza GPIO o nazwie 'g2', które odpowiada za światło. Dodaje nowe GPIO 'g100' dla wentylatora, a następnie je usuwa.
8. Zalety rozwiązania
- Bezpieczeństwo dzięki Firebase Authentication
- Prosta struktura bazy danych (klucz–wartość)
- Intuicyjny interfejs użytkownika
- Łatwa możliwość rozbudowy o kolejne urządzenia/pokoje


9.Przewaga wobec rozwiązań alternatywnych 
Przewaga firebase realtime nad typowymi relacyjnymi bazami danych:

Cecha
Firebase Realtime DB
np. PostgreSQL / REST API
Struktura danych
JSON (drzewo)
relacyjna (tabele, zapytania SQL)
Wyszukiwanie (query)
ograniczone
zaawansowane
Skalowalność do Big Data
ograniczona
lepiej w Firestore / BigQuery
Analiza danych
utrudniona
SQL idealny




Przewaga  nie relacyjnej Firebase nad innymi dostępnymi nierelacyjnymi bazami danych 

Skalowalność automatyczna
✅ Tak
✅ Tak
✅ Tak
✅ Wysoka
✅ Tak

Model danych
JSON (drzewo)
BSON (dokumenty)
JSON / KV
JSON / tablice
Klucz–wartość




9. Załączniki
Linki do repozytorium wraz z projektem
część frontendowa projektu-
część hardwarowa- 

