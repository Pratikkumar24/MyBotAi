
try:
    from Modules.module import *
except Exception as e:
    import sys,pyttsx3
    engine = pyttsx3.init("sapi5")
    engine.say("Cannot import a module due to slow internet connection. So I need to terminate myself, Sir!")
    engine.runAndWait()
    sys.exit()
class myBot():
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        self.checkInternet()
        self.dictionary=PyDictionary()
        self.week = ["monday","tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        self.silent = 1
        
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
            r.pause_threshold = 1
            r.threshold = 1  
            r.energy_threshold = 4000
            with sr.Microphone() as source:
                print("Listening...")
                if self.silent == 1:
                    playsound('C:\\Users\\Pratik\\Desktop\\CODES\\MainCodes\\MyProjects\\AIbot\\chime\\ping.wav',True)
                audio = r.listen(source,timeout= 6, phrase_time_limit= 8)


        except KeyboardInterrupt:
            print("You ended the listening process, Sir")
            sys.exit()
        
        except Exception as e:
            self.takecommand()

        try:
            print("Recognizing ...")
            query = r.recognize_google(audio, language='en-in')

        except Exception as e:
            return "None"

        except KeyboardInterrupt:
            print("You ended the recognizing part, Sir")
            sys.exit()
            return "None"
        return query.lower()

    def OPEN(self, query):
        if "youtube" in query:
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
                text = "opening "+title+" in youtube"
                m = gTTS(text, lang="hi")
                m.save("tmp.mp3")
                playsound("tmp.mp3")
                os.remove("tmp.mp3")
                for url in urlList:
                    webbrowser.open_new_tab(str(url[1]))
        elif 'search' in query:
            title=""
            while(1):
                try:
                    title = re.findall("((?:.* search )(.*))|(.*)", query)[0][1]
                    if not len(title)>1:
                        self.speak("Sir, tell me what you want to search")
                        title = self.takecommand()
                        if 'none' not in title:
                            break
                    else:
                        break
                except:
                    self.speak("Sir! Could you please repeat it")

            self.speak("searching "+ title+" in google")
            url = "https://www.google.com.tr/search?q={}".format(title)
            webbrowser.open_new_tab(url)

        elif 'open' in query:   
            title=""
            query = " " + query
            while(1):
                try:
                    title = re.findall("((?:.* open )(.*))|(.*)", query)[0][1]
                    if len(title)<2:
                        self.speak("Sir, tell me what you want to open")
                        title = self.takecommand()
                        if 'none' not in title:
                            break
                    else:
                        break
                except:
                    self.speak("Sir! Could you please repeat it")

            if 'notepad' in title:
                self.speak("opening notepad")
                os.system("cd C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories")
                subprocess.Popen("Notepad.exe")
            elif 'chrome' in title:
                self.speak("opening chrome browser with google")
                webbrowser.open_new_tab("http://www.google.com")
            elif 'facebook' in title:
                self.speak("opening facebook")
                webbrowser.open_new_tab("https://www.facebook.com")
            elif 'instagram' in title:
                self.speak("opening instagram")
                webbrowser.open_new_tab("https://www.instagram.com/accounts/edit/?hl=en")
            elif 'whatsapp'  in title:
                self.speak("opening whatsapp")
                webbrowser.open_new_tab("https://web.whatsapp.com") 
            else:
                print("Error")
                self.speak("The Current item is not in your list, Wanna make a google search") 
                ans = self.takecommand()
                if 'yes' in ans:
                    url ="https://www.google.com.tr/search?q={}".format(title)
                    webbrowser.open_new_tab(url)
                else:
                    self.speak("as you say sir")


    def changeWindows(self):
        self.speak("at which number of slide you want to switch,Sir")
        print("<windowslides are zero indexing>")
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        time.sleep(5)
        pyautogui.keyUp('alt')
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        pyautogui.keyUp('alt')
        actual_number=[]

        number = self.takecommand()
        actual_number = re.findall(r"\d", number)
        if not len(actual_number)>0: 
            actual_number.append(1)
        pyautogui.keyDown('alt')
        numberofslidechange = int(actual_number[-1])
        for i in range(numberofslidechange):
            pyautogui.press('tab')
            time.sleep(1)
        pyautogui.keyUp('alt')
    
    def silentcommand(self):
        if 'silent' in query:
            self.speak("Sir, i am awake now. Tell me what to do")
            self.silent = 1

    def runCommand(self,query):

        if 'quit' in query or 'exit' in query or 'stop' in query:
            print("\nQuiting...\n")
            self.speak("Bye Sir, hope you are satisfied with my care")
            myobj = gTTS(text="and see you again, ba-bye Sir", lang="hi", slow= False)
            myobj.save("tmp.mp3")
            playsound("tmp.mp3")
            os.remove("tmp.mp3")
            sys.exit()
        
        elif 'shutdown' in query:
            self.speak("Shuting Down the system")
            os.system('shutdown -s')

        elif 'close' in query:
            if 'window' in query:
                self.speak("closing the current window")
                pyautogui.keyDown('alt')
                pyautogui.press('f4')
                pyautogui.keyUp('alt')
            else:
                self.speak("closing the current tab")
                pyautogui.keyDown('ctrl')
                pyautogui.press('w')
                pyautogui.keyUp('ctrl')
        
        elif 'change' in query:
            while True:
                self.changeWindows()
                 
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
                joke = pyjokes.get_joke()
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
            print("8) search anything on google by saying open or search")

            print('9) can open any application from your pc')

            print("10) can send a whatsapp message to someone")

            print("11) To Quit yourself")
            
        elif "good" in query or "nice" in query or "amazing" in query:
            self.speak("Thank you sir!")

        elif "message" in query:
            now = datetime.now()
            minutes = now.minute +2
            hour = now.hour
            if "on" in query or "at" in query: 
                numbers = re.findall(r"\d+", query)
                if " pm" in query:
                    minutes, hour = numbers[-1], (numbers[-2]+12)%24
                    if minutes>=numbers[-1] and hour>=numbers[-2]:
                        # kit.sendwhatmsg("+918830271663","Hello ", hour, minutes)
                        print("Hour: "+ hour, "Minutes: "+ minutes)
                    else:
                        print("Hour: "+ hour, "Minutes: "+ minutes)
                else:
                    print(hour, minutes)
      
        elif "music" in query:
            self.speak("Playing Music")
            dir = "C:\\Users\\Pratik\\Documents\\Rockstar Games\\GTA V\\User Music"
            songs = os.listdir(dir)
            rd = random.choice(songs)
            os.startfile(os.path.join(dir, rd))

        elif "silent" in query:
            self.speak(("I wont be listening to you untill you say silent again"))
            self.silent = 0
 
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
                print(text)
                myobj = gTTS(text=text + "Kyuki sab ke sab chor hai saale!", lang="hi", slow=False)
                myobj.save("tmp.mp3")
                playsound("tmp.mp3")
                os.remove("tmp.mp3")
                
            elif bot.silent == 1:
                if today in query:
                    query = query.replace(today, "\b")
                elif 'open' in query or 'search' in query or "youtube" in query:
                    print("the query is : "+ query)
                    bot.OPEN(query)
                else:
                    bot.runCommand(query)

            elif 'silent' in query:
                bot.silentcommand()
            