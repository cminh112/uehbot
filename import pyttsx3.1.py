import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser as wb
import subprocess
import os
import platform
import random
import requests
import time
import re

# Khởi tạo và cấu hình giọng nói
UEHbot = pyttsx3.init()
voice = UEHbot.getProperty('voices')
UEHbot.setProperty('voice', voice[0].id)  # Giọng nam
rate = UEHbot.getProperty('rate')  # Tốc độ nói
UEHbot.setProperty('rate', 150)

def speak(audio):
    print('U.E.H.b.o.t.: ' + audio)
    UEHbot.say(audio)
    UEHbot.runAndWait()

def date():
    today = datetime.datetime.now()
    day = today.day
    month = today.strftime("%B")  # Lấy tên tháng (ví dụ: January, February)
    year = today.year
    speak(f"Today is {month} {day}, {year}.")

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%p")
    speak(Time)

def welcome():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir")
    elif hour >= 18 and hour < 24:
        speak("Good Night Sir")
    speak('How can I help you?')

def command():
    c = sr.Recognizer()
    with sr.Microphone() as source:
        c.pause_threshold = 2
        try:
            print("Listening for your command...")
            audio = c.listen(source, timeout=10)
            query = c.recognize_google(audio, language='en')
            print("Bạn: " + query)
        except sr.UnknownValueError:
            speak("Sorry, I could not understand what you said. Please type the command.")
            query = input('Your order is: ')  # Nếu không nhận diện được, người dùng có thể gõ lệnh
        except sr.RequestError as e:
            speak("Sorry, I couldn't reach the speech recognition service. Please try again later.")
            query = input('Your order is: ')  # Nếu lỗi kết nối, người dùng có thể gõ lệnh
        except sr.WaitTimeoutError:
            speak("No sound detected within 10 seconds. Please type the command.")
            query = input('Your order is: ')  # Sau 10 giây nếu không nghe thấy gì, người dùng nhập lệnh
    return query

# Mở ứng dụng mà không cần khai báo từng ứng dụng
def open_application(app_name):
    system = platform.system()  # Kiểm tra hệ điều hành
    try:
        if system == "Windows":
            # Tìm kiếm ứng dụng và mở nếu có
            subprocess.run(["start", app_name], shell=True)

        elif system == "Darwin":  # macOS
            # Mở ứng dụng bằng cách dùng lệnh open -a
            subprocess.run(["open", "-a", app_name])

        elif system == "Linux":
            # Tìm kiếm và mở ứng dụng
            subprocess.run([app_name])

        else:
            speak(f"Unsupported operating system: {system}")
    except Exception as e:
        speak(f"An error occurred while opening the application: {e}")

# Tắt hoặc khởi động lại máy tính
def shutdown_computer():
    speak("Shutting down the computer now.")
    os.system("shutdown /s /f /t 1" if platform.system() == "Windows" else "shutdown now")

def restart_computer():
    speak("Restarting the computer now.")
    os.system("shutdown /r /f /t 1" if platform.system() == "Windows" else "sudo shutdown -r now")

# Điều chỉnh âm lượng
def adjust_volume(action):
    import pyautogui
    try:
        if action == 'increase':
            pyautogui.press('volumeup')
            speak("Increasing volume")
        elif action == 'decrease':
            pyautogui.press('volumedown')
            speak("Decreasing volume")
    except Exception as e:
        speak(f"An error occurred while adjusting volume: {e}")

# Danh sách các câu chào tạm biệt ngẫu nhiên
def random_goodbye():
    goodbyes = [
        "UEH bot is quitting sir. Goodbye boss.",
        "Goodbye, hope to see you again soon!",
        "It was nice assisting you! Take care.",
        "Goodbye, have a wonderful day ahead!",
        "See you later, take care!"
    ]
    return random.choice(goodbyes)

# Hàm lấy thông tin thời tiết
def get_weather(city):
    API_KEY = "28a9aee594b1c32287f4e14d88e8f231"  # Thay bằng API key của bạn từ OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        
        # Kiểm tra phản hồi từ API
        if response.status_code == 200:  # Kiểm tra mã trạng thái HTTP (200 nghĩa là thành công)
            data = response.json()
            
            # Kiểm tra nếu phản hồi có khóa "main" và "weather"
            if "main" in data and "weather" in data:
                main = data["main"]
                weather = data["weather"][0]
                temp = main["temp"]
                description = weather["description"]
                return f"The weather in {city} is {description} with a temperature of {temp}°C."
            else:
                return "Weather data is not available for this city."
        else:
            return "Unable to get weather information. Please try again later."
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"

# Main Program
if __name__ == "__main__":
    welcome()
    while True:
        query = command().lower()

        # Lệnh tìm kiếm Google
        if "google" in query:
            speak("What should I search, boss?")
            search = command().lower()
            url = f"https://www.google.com/search?q={search}"
            wb.get().open(url)
            speak(f"Here is your {search} on Google")

        # Lệnh tìm kiếm YouTube
        elif "youtube" in query:
            speak("What should I search, boss?")
            search = command().lower()
            url = f"https://www.youtube.com/search?q={search}"
            wb.get().open(url)
            speak(f"Here is your {search} on YouTube")
            
        # Lệnh kiểm tra ngày tháng năm
        elif "date" in query or "today" in query:
            date()  # Gọi hàm ngày tháng năm

        # Lệnh kiểm tra giờ
        elif "time" in query:
            time()

        # Lệnh mở ứng dụng
        elif "open" in query:
            app_name = query.replace("open", "").strip()
            open_application(app_name)

        # Lệnh tắt máy
        elif "shutdown" in query:
            shutdown_computer()

        # Lệnh khởi động lại máy
        elif "restart" in query:
            restart_computer()

        # Lệnh điều chỉnh âm lượng
        elif "increase" in query:
            adjust_volume('increase')
        elif "decrease" in query:
            adjust_volume('decrease')

        # Lệnh hỏi thời tiết
        elif "weather" in query:
            if "in" in query:
                city = query.split("in")[-1].strip()
                weather_info = get_weather(city)
                speak(weather_info)
            elif "weather" in query:
                speak("Which city would you like to know the weather for?")
                city = command().lower()
                weather_info = get_weather(city)
                speak(weather_info)

        # Lệnh thoát
        elif "quit" in query or "goodbye" in query:
            speak(random_goodbye())
            quit()
