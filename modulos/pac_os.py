from gtts import gTTS
from playsound import playsound
from io import open 
import toml,os


#Construccion de clase EventoLog
class EventoLog:
    def __init__(self, date_time, url, alias, state, response):
        self.date_time = date_time
        self.url = url
        self.alias = alias
        self.state = state
        self.response = response

    def __str__(self):
        return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))


# Leer un archivo de configuracion tipo TOML (lo importa en diccionario python (Parecido a JSON))
def toml_leer_archivo(data):
    parsed = (toml.load(data))
    return parsed

def eventolog_texto (eventolog):
    texto = eventolog.date_time + ' | ' + eventolog.url + ' | ' + ' | ' + eventolog.alias + ' | ' + eventolog.state + ' | ' + eventolog.response + '\n'
    return texto

def escribir_log(nombrefile,eventolog):
    if (os.path.exists(nombrefile)):
        logeventos = open (nombrefile,"a")
    else:
        logeventos = open (nombrefile,"w")
        logeventos.write('DateTime | URL |  Alias  | State | Response \n')
    logeventos.write(eventolog_texto (eventolog))
    logeventos.close()

def play_alert_message (message,language):
    myobj = gTTS(text=message, lang=language, slow=False)
    myobj.save("alert.mp3")
    try:
        playsound('alert.mp3')
    except:
        print()
    if os.path.exists("alert.mp3"):
        os.remove("alert.mp3") 
