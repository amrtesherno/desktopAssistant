from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
from weather import Weather
from twilio.rest import Client


def talkToMe(audio):
    "speaks audio passed as argument"

    print(audio)
    for line in audio.splitlines():  
        tts = gTTS(text=audio, lang='en')
        tts.save('audio.mp3')
        os.system('mpg123 audio.mp3')
#        os.system('say ' + audio)

#    use the system's inbuilt say command instead of mpg123
#        text_to_speech = gTTS(text=audio, lang='en')
#        text_to_speech.save('audio.mp3')
#        os.system('mpg123 audio.mp3')

    
def myCommand():
    "listens for commands"

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)
        print("Done listening!")
    with open("microphone-results.wav", "wb") as f:
        f.write(audio.get_wav_data())

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand();

    return command


def assistant(command):
    "if statements for executing commands"

    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        print('Done!')

    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            print('Done!')
        else:
            pass

    elif 'what\'s up' in command:
        talkToMe('Just doing my thing')

    elif 'good morning' in command:
        talkToMe('good morning Amr')
    elif 'hi' in command:
        talkToMe('hi')

    elif 'gym' in command:
    	account_sid = "AC82310a5c62ab010073049c0c38eacd37"
        auth_token  = "a347f87c86e3b20c2c6f3bbda0a285f0"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to="+2001143555614", 
            from_="+16182198504",
            body="hi will go to gym to day")
        print(message.sid)
        talkToMe('yes you have to go to gym today at 5pm. and i will send text massage to your friend Ahmed ')
        talkToMe('massage send')
    elif 'who is ' in command:
        talkToMe('he is  a developer  he create amazing site and now he work to develop me to be his personal assistant')

    elif 'are you' in command:
        talkToMe('Yes Amr told me that my name will be body')
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            talkToMe(str(res.json()['joke']))
        else:
            talkToMe('oops!I ran out of jokes')

    elif 'current weather in' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather()
            location = weather.lookup_by_location(city)
            condition = location.condition()
            talkToMe('The Current weather in %s is %s The tempeture is %.1f degree' % (city, condition.text(), (int(condition.temp())-32)/1.8))

    elif 'weather forecast in' in command:
        reg_ex = re.search('weather forecast in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather()
            location = weather.lookup_by_location(city)
            forecasts = location.forecast()
            for i in range(0,3):
                talkToMe('On %s will it %s. The maximum temperture will be %.1f degree.'
                         'The lowest temperature will be %.1f degrees.' % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))


    elif 'email' in command:
        talkToMe('Who is the recipient?')
        recipient = myCommand()

        if 'John' in recipient:
            talkToMe('What should I say?')
            content = myCommand()

            #init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)

            #identify to server
            mail.ehlo()

            #encrypt session
            mail.starttls()

            #login
            mail.login('amrtesherno', '442352442352')

            #send message
            mail.sendmail('John Fisher', 'JARVIS2.0@protonmail.com', content)

            #end mail connection
            mail.close()

            talkToMe('Email sent.')

        else:
            talkToMe('I don\'t know what you mean!')


talkToMe('hi Amr I am ready for your command ')

#loop to continue executing multiple commands
while True:
    assistant(myCommand())
