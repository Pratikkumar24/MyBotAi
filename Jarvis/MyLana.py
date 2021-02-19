import pyttsx3
import datetime
# import PyAudio
import speech_recognition as sr


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices)
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning, Sir!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon, Sir!")
    else:
        speak("Good Evening, Sir!")

    speak("I am your assistant, LAANA. Sir, How may I help you.")

def takecommand():
    '''
        takes microphone user as input and returns in string

    '''
    # print(sr.__version__)
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            # r.pause_thresold = 1
            audio = r.listen(source)

    except KeyboardInterrupt:
        speak("You ended the listening process, Sir")

    print("listened!")

    try:
        print("Recongnizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said:{query}\n")

    except Exception as e:
        print("Say that again, Sir!...")
        speak("Say that again, Sir!")
        return "None"
    except KeyboardInterrupt:
        speak("You ended the recognizing part, Sir")
        return "None"
    return query 

if __name__ == '__main__':
    
    wishme()
    print(takecommand())
