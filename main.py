import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import subprocess
import random
import pyttsx3
import requests


chatstr = ""

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 130)
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()


def get_weather():
    base_url = "http://api.weatherapi.com/v1/current.json"
    talk("which city do you want to know about")
    print("Listening...")
    city = takecommand()
    from api_key import wkey
    params = {
        "key": wkey,
        "q": city,
        "aqi": "no"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        talk(f"Weather information for {city}:")
        talk(f"Temperature: {data['current']['temp_c']}°C")
        talk(f"Description: {data['current']['condition']['text']}")
        talk(f"Probability of Rain: {data['current']['precip_mm']} mm")
    else:
        talk("Error retrieving weather information.")

def news():
    from api_key import newskey
    main_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey="+newskey
    news = requests.get(main_url).json()
    article = news["articles"]
    news_article=[]
    for arti in article:
        news_article.append(arti['title'])
    for i in range(1):
        talk(news_article[i])

def chat(query):
    global chatstr
    print(chatstr)
    from api_key import key
    openai.api_key = key
    chatstr += f"Dipanjan: {query}\n zero two: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatstr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    talk(response["choices"][0]["text"])
    chatstr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

    #with open(f"Openai/prompt- {random.randint(1, 84719284712)}", "w") as f:
    with open(f"openai/{'', join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)




def ai(prompt):
    from api_key import key
    openai.api_key = key
    text = f"OpenAI response for prompt: {prompt}\n ********************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("openai"):
        os.mkdir("openai")

    with open(f"Openai/prompt- {random.randint(1,84719284712)}","w") as f:
    #with open(f"openai/{'', join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def notepad():
    talk("Tell me the query. I am ready to write")
    print("writing")
    writes = takecommand()

    time = datetime.datetime.now().strftime("%H:%M")
    filename =str(time).replace(":","-") + "-note.txt"
    with open(filename,"w") as file:
        file.write(writes)
    #path_1 = "C:\\Users\\ASUS\\PycharmProjects\\zerotwo"+str(filename)
    #path_2 = "C:\\Users\\ASUS\\PycharmProjects\\zerotwo\\Notepad"+str(filename)
    #os.rename(path_1, path_2)
    #os.startfile(path_2)



def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Zero Two"

talk("you have logged into zero two")
while True:
    print("Listening...")
    query = takecommand()
    sites =[["youtube","https://youtube.com"],["wikipedia","https://wikipedia.com"],["google","https://google.com"],["spotify", "https://www.spotify.com"], ["facebook", "https://www.facebook.com"],["instagram", "https://www.instagram.com"],["gmail", "https://mail.google.com/mail/"],["amazon", "https://www.amazon.in"],]
    for site in sites:
        if f"open {site[0]}" in query.lower():
            talk(f"Opening {site[0]}")
            webbrowser.open(site[1])
    if "time" in query:
        strfTime = datetime.datetime.now().strftime("%H hours %M minutes")
        talk(f"The time is{strfTime}")
    elif "open chrome".lower() in query.lower():
        talk(f"Opening chrome")
        subprocess.Popen("C:\Program Files\Google\Chrome\Application\chrome.exe")
    elif "open vs code".lower() in query.lower():
        talk(f"Opening vs code")
        subprocess.Popen("C:\\Users\ASUS\AppData\Local\Programs\Microsoft VS Code\Code.exe")
    elif "ai".lower() in query.lower():
        talk(f"yes sir")
        ai(prompt=query)
    elif "stop".lower() in query.lower():
        exit()
    elif "reset chat".lower() in query.lower():
        chatstr = ""
        print("resent chat")
    elif "open notepad".lower() in query.lower():
        notepad()
    elif "news".lower() in query.lower():
        news()
    elif "weather".lower() in query.lower():
        get_weather()
    else:
        print("Chatting...")
        chat(query)