from sys import argv
import toml,os
from io import open

#Construccion de clase EventoLog
class EventoLog:
    def __init__(self, date_time, url, state, response):
        self.date_time = date_time
        self.url = url
        self.state = state
        self.response = response

    def __str__(self):
        return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))


# Leer un archivo de configuracion tipo TOML (lo importa en diccionario python (Parecido a JSON))
def toml_leer_archivo(data):
    parsed = (toml.load(data))
    return parsed

def eventolog_texto (eventolog):
    texto = eventolog.date_time + ' | ' + eventolog.url + ' | ' + eventolog.state + ' | ' + eventolog.response + '\n'
    return texto

def escribir_log(nombrefile,eventolog):
    if (os.path.exists(nombrefile)):
        logeventos = open (nombrefile,"a")
    else:
        logeventos = open (nombrefile,"w")
        logeventos.write('DateTime | URL | State | Response \n')
    logeventos.write(eventolog_texto (eventolog))
    logeventos.close()
