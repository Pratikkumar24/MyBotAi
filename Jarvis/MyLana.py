

from Modules.module import *

class myBot():
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)

    def speak(self,audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def wishme(self):
        hour = int(datetime.datetime.now().hour)
        if hour>=0 and hour<12:
            self.speak("Good Morning, Sir!")
        elif hour>=12 and hour<18:
            self.speak("Good Afternoon, Sir!")
        else:
            self.speak("Good Evening, Sir!")

        self.speak("I am your assistant, LAANA. How may I help you.")

    def takecommand(self):
        '''
            takes microphone user as input and returns in string

        '''
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = r.listen(source)

        except KeyboardInterrupt:
            self.speak("You ended the listening process, Sir")

        try:
            print("Recongnizing...")
            query = r.recognize_google(audio, language='en-in')

        except Exception as e:
            return "None"

        except KeyboardInterrupt:
            self.speak("You ended the recognizing part, Sir")
            return "None"
        return query 

    def runCommand(self,query):
        if re.search( 'quit yourself', query ) or re.search('quit lana', query) or re.search('lana quit', query):
            print("\nQuiting...\n")
            sys.exit()
        
        elif re.search('check internet connection', query) or re.search('check internet', query):
            IPaddress=socket.gethostbyname(socket.gethostname())
            if IPaddress=="127.0.0.1":
                self.speak("No internet, sir. your localhost is "+ str(IPaddress))
            else:
                self.speak("You have a fine internet connection, sir!. with the IP address: "+ str(IPaddress))



        elif re.search("what's the time", query) or re.search("what is the time", query):
            hour = datetime.now().hour
            minute = datetime.now().minute
            self.speak("current time is "+ str(hour)+". "+str(minute))


        else:
            self.speak("Sorry sir!, Couldn't understand, could you please repeat it again")

if __name__ == '__main__':
    
    bot = myBot()
    
    # bot.wishme()

    # while(True):
    query = bot.takecommand().lower()
    bot.runCommand(query)
