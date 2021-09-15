from gtts import gTTS
from io import open 
import toml,os,pygame,time


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
    try:
        myobj = gTTS(text=message, lang=language, slow=False)
        myobj.save("alert.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load('alert.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        else:
            pygame.mixer.quit()
        if os.path.exists("alert.mp3"):
            os.remove("alert.mp3")
    except:
        print('Sound file cannot be played.') 
