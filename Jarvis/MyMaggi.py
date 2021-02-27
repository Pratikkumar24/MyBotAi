#!/bin/bash
from Modules.module import *

class myBot():
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        self.checkInternet()
        self.dictionary=PyDictionary()
        self.week = ["monday","tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        
    def youtubeLink(self, query, limit=1):
        videosSearch = VideosSearch(query, limit = limit)
        link = re.findall("('link': ')(https://.*?)'",str(videosSearch.result()))
        for li in link:
            if re.search('channel', str(li)):
                link.remove(li)

        return link

    def speak(self,audio):
        self.engine.say(audio)
        self.engine.runAndWait()
   
    def checkInternet(self):
        try :
            statucode = requests.get("https://www.google.com/").status_code
        except Exception:
            self.speak("Sir, You need to connect yourself to internet, please check your internet connection.")
            sys.exit() 
   
    def wishme(self):
        hour = int(datetime.now().hour)
        if hour>=0 and hour<12:
            self.speak("Good Morning, Sir!")
        elif hour>=12 and hour<18:
            self.speak("Good Afternoon, Sir!")
        else:
            self.speak("Good Evening, Sir!")
        
        number = datetime.today().weekday()
        today =self.week[number]

        self.speak("I am your assistant, "+str(today)+". How may I help you.")
        return today

    def takecommand(self):

        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                # r.adjust_for_ambient_noise(source, duration=5)
                print("Listening...")
                r.threshold = 1  
                audio = r.listen(source)

        except KeyboardInterrupt:
            print("You ended the listening process, Sir")
            sys.exit()

        try:
            print("Recognizing ...")
            query = r.recognize_google(audio, language='en-in')

        except Exception as e:
            return "None"

        except KeyboardInterrupt:
            print("You ended the recognizing part, Sir")
            sys.exit()
            return "None"
        return query 

    def runCommand(self,query):
        if query == "none":
            return

        elif 'quit' in query or 'exit' in query or 'stop' in query:
            print("\nQuiting...\n")
            self.speak("Bye Sir, hope you are satisfied with my care")
            myobj = gTTS(text="and see you again, Sir", lang="hi", slow= False)
            myobj.save("tmp.mp3")
            playsound("tmp.mp3")
            os.remove("tmp.mp3")
            sys.exit()
        
        elif 'speed' in query:
            self.speak("Checking the download speed, upload speed and ping of your internet..")
            print("\nLoading......\n")
            
            st = speedtest.Speedtest() 
            self.checkInternet()
            dspeed = st.download() * 10**(-6)
            upspeed = st.upload() * 10**(-6)
            print("\nDownload Speed: {:.2f}mbps".format(round(dspeed, 2)))
            self.speak("Download Speed is {:.2f} m b p s".format(round(dspeed, 2)))
            print("Upload Speed: {:.2f}mbps".format(round(upspeed, 2)))
            self.speak("Upload Speed is {:.2f} m b p s".format(round(upspeed, 2)))
            servernames =[]   
            st.get_servers(servernames)   
            print(str(st.results.ping) +"ms ping\n")  
            self.speak("And your ping is "+ str(st.results.ping))

        elif 'bored' in query or "boring" in query:
            text = "Sir, if that is the case, would you like to listen to a joke"
            m = gTTS(text, lang="hi")
            m.save("tmp.mp3")
            playsound("tmp.mp3")
            os.remove("tmp.mp3")

            ans = self.takecommand()
            if "yes" in ans:  
                text = "Okay! let me search a joke for you."
                m = gTTS(text, lang="hi")
                m.save("tmp.mp3")
                playsound("tmp.mp3")
                os.remove("tmp.mp3")
                joke = laughs.get_joke()
                m = gTTS(joke, lang="hi")
                m.save("tmp.mp3")
                playsound("tmp.mp3")
                os.remove("tmp.mp3")

            else:
                m = gTTS("Then what I can do for you", lang="hi")
                m.save("tmp.mp3")
                playsound("tmp.mp3")
                os.remove("tmp.mp3")

        elif "joke" in query:
            text = "Okay! let me search a joke for you."
            self.speak(text)
            
            joke = laughs.get_joke()
            print(joke)
            self.speak(joke)
            
        elif "time" in query:

            strtime = datetime.now().strftime("%H:%M:%S")
            self.speak("Sir, current time is "+ strtime)

        elif "open" in query:
            self.speak("what you want me to search for you")
            ans = self.takecommand().lower()
            chromepath = "D:\Chrome\chrome.exe"
            webbrowser.get(chromepath).open_new_tab(f"{ans}")
       
        elif "who is" in query or "something about" in query:
            
            if re.search("who is", query):
                x = re.search("(.*who is )(.*)", query)
                self.speak("So you wanna know about "+ str(x.group(2)))
                anotherquery = self.takecommand().lower()
                if "yes" in anotherquery or "yup" in anotherquery:
                    try:
                        results = wikipedia.summary(query, sentences=1)
                        print(results)
                        self.speak("According to wikipedia "+ str(results))
                    except wikipedia.exceptions.PageError as e:
                        self.speak("Couldn't search about "+ str(x.group(2))+", maybe spelling mistake")
                else:
                    self.speak("Then what you wanted to know, sir.")
                    return
            else:
                x = re.search("(.*something about )(.*)", query)
                self.speak("So you wanna know about "+ str(x.group(2)))
                anotherquery = self.takecommand().lower()
                if "yes" in anotherquery or "yup" in anotherquery:
                    try:
                        results = wikipedia.summary(query, sentences=1)
                        print(results)
                        self.speak("According to wikipedia "+ str(results))
                    except wikipedia.exceptions.PageError as e:
                        self.speak("Couldn't search about "+ str(x.group(2))+", maybe spelling mistake")
                else:
                    self.speak("Then what you wanted to know, sir.")
                    return

        elif "youtube" in query:
            limit = 1
            if"open youtube" in query:
                self.speak("opening youtube")
                webbrowser.open_new_tab("http://www.youtube.com")
            else:
                try:
                    if re.search("limit", query) or re.search("min",query) or re.search("minimum",query) or re.search("url",query):
                        numbers = re.findall(r"\d+", query)
                        if len(numbers)>1:
                            limit = int(numbers[1])
                        else:
                            limit = int(numbers[0])       
                except Exception:
                    pass

                title = query.replace('open','XXX').replace('play','XXX').replace('search','XXX')
                title = re.findall("(?:XXX)(.*youtube)", title)[0]
                title = title.replace(' in ',' ').replace(' on ',' ').replace('from','\b').replace('show' ,'\b').replace('youtube','\b')
                urlList = self.youtubeLink(title,limit)
                print("\n Searching title: " + title + " With "+ str(limit)+" url")
                self.speak("opening "+title+" in youtube")
                for url in urlList:
                    webbrowser.open_new_tab(str(url[1]))

        elif "mean" in query and "what" in query:
            self.speak("Searching the meaning from python dictonary")
            try:
                useless = re.findall("(?:)(.*what)", query)[0]
                query = query.replace(useless,"")
            except Exception as e:   
                self.speak("Please use the word WHAT!! in your sentence")
                return

            if re.search(" of ", query):
                query = re.findall(r"(?:.*of )(\w{3,})", query)[0]

            elif re.search(" mean ", query) or re.search(" means ", query):
                query = re.findall(r"(\w{3,})( means?)", query)[0][0]

            print("["+query+"]")
            self.speak("So you want to search the meaning of " + query)
            res = self.takecommand().lower()
            print("UserSaid: "+ res)
            if re.search("yes",res) or re.search("yup", res) or re.search("ha", res):
                result = self.dictionary.meaning(query)
                print(result["Noun"])
                self.speak(result["Noun"])
            elif re.search("no",res) or re.search("na", res):
                self.speak("Sir then please type the spelling of the word you want to search")
                word = input("Enter the word sir: ")
                result = self.dictionary.meaning(word)
                print(result["Noun"])
                self.speak(result["Noun"])
   
        elif "you can do" in query:
            self.speak("Sir, These are the task I can do for you now..")
            print("1) Internet speed")

            # self.speak("2) Ask current Time")
            print("2) Ask current Time")
            
            # self.speak("3) Can know something about in according to wikipedia")
            print("3) Can know something about it according to wikipedia")

            # self.speak("4) Open Youtube")
            print("4) Open Youtube or <anything> on/in/from youtube <optional='limit no. of url'>")

            print("5) Check the meaning of a word in dictionary")

            print("6) Can tell a joke")

            print("7) are you bored! ")
            # self.speak("5) To Quit yourself")
            print("8) To Quit yourself")
            
        elif "good" in query or "nice" in query or "amazing" in query:
            self.speak("Thank you sir!")

        elif "hey" in query:
            self.speak("Yes sir!, I am listening to you!")

        elif "message" in query:
            if "after" in query:
                
            now = datetime.now()
            kit.sendwhatmsg("+918830271663","Hello ", now.hour, now.minute+2)

            # print("time: "+ str(time.hour())+ " "+ str(time.minute()))
        
if __name__ == '__main__':
    bot = myBot()
    today = bot.wishme()
    while(1):
        print("Today's assistant:-> "+ today)
        query = bot.takecommand().lower()
        if "none" not in query:
            print("UserSaid: " + str(query))
            if re.search("alexa", query) or re.search("hey google", query):
                text = "Sir, Please dont speak about alexa or google assistant. Those are useless dumb guys and nothing in front of me!"
                myobj = gTTS(text=text + "Kyuki sab ke sab chor hai saale!", lang="hi", slow=True)
                myobj.save("tmp.mp3")
                playsound("tmp.mp3")
                os.remove("tmp.mp3")
            elif today in query:
                query = query.replace(today, "\b")
                bot.runCommand(query)

