import time,sys
from tabulate import tabulate
#Construccion de clase MonitorWebsite
class MonitorWebsite:
    def __init__(
        self, url, consecutive_failures, consecutive_success, state, previous_state,response_time,response_code):
        self.url = url
        self.consecutive_failures = consecutive_failures
        self.consecutive_success = consecutive_success
        self.state = state
        self.previous_state = previous_state
        self.response_time = response_time
        self.response_code = response_code

    def __str__(self):
        return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

def construir_monitor (dic_configuracion):
    lista_monitor = []
    websites = dic_configuracion['sites']['websites']
    for website in websites:
        lista_monitor.append(MonitorWebsite(website,0,0,'up','up',0,200))
    return lista_monitor

def espera_siguiente_prueba (tiempo):
    a = 0
    sys.stdout.write('Activity ')
    sys.stdout.flush()
    for a in range(tiempo):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)


def imprimir_monitor(Monitor):
    array_Monitor=[]
    for mon in Monitor:
        array_Monitor.append([mon.url,mon.state,mon.response_time,mon.consecutive_success,mon.consecutive_failures,mon.response_code])
    print(tabulate(array_Monitor,headers=["URL","State","Time(ms)","Success","Fails","Response"],tablefmt="pretty"))

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)