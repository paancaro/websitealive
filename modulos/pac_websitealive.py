import time,sys,datetime,pytz
from tabulate import tabulate
#Construccion de clase MonitorWebsite
class MonitorWebsite:
    def __init__(
        self, url ,alias, consecutive_failures, consecutive_success, state, previous_state,response_time,response_code,msg_up,msg_down):
        self.url = url
        self.alias = alias
        self.consecutive_failures = consecutive_failures
        self.consecutive_success = consecutive_success
        self.state = state
        self.previous_state = previous_state
        self.response_time = response_time
        self.response_code = response_code
        self.msg_up = msg_up
        self.msg_down = msg_down
        

    def __str__(self):
        return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

def construir_monitor (dic_configuracion):
    lista_monitor = []
    websites = dic_configuracion['sites']['websites']
    alias = dic_configuracion['sites']['alias']
    msg_up=dic_configuracion['messages']['msg_up']
    msg_down=dic_configuracion['messages']['msg_down']
    hay_alias=False
    contador=0
    if len(websites) == len(alias):
        hay_alias=True
    for website in websites:
        if hay_alias:
            lista_monitor.append(MonitorWebsite(website,alias[contador],0,0,msg_up,msg_up,0,200,msg_up,msg_down))
            contador+=1
        else:
            lista_monitor.append(MonitorWebsite(website,' ',0,0,msg_up,msg_up,0,200,msg_up,msg_down))
    return lista_monitor

def espera_siguiente_prueba (tiempo):
    a = 0
    sys.stdout.write('Use Ctrl+C to terminate  ')
    sys.stdout.flush()
    for a in range(tiempo):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)


def imprimir_monitor(Monitor):
    array_Monitor=[]
    for mon in Monitor:
        if mon.state == mon.msg_up:
            text_state=colored(0, 255, 0, mon.msg_up)
        else:
            text_state=colored(255, 0, 0, mon.msg_down)

        array_Monitor.append([
                            mon.url,
                            mon.alias,
                            text_state,
                            mon.response_time,
#                            mon.consecutive_success,
#                            mon.consecutive_failures,
                            mon.response_code])
    print(tabulate(array_Monitor,headers=[
                                            "URL",
                                            "Alias",
                                            "State",
                                            "Time(ms)",
 #                                           "Success",
 #                                           "Fails",
                                            "Response"],tablefmt="pretty"))

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def hora_UTC():
    horaUTC = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return horaUTC


def hora_zona(zona):
    format = "%Y-%m-%d %H:%M:%S"
    horazona = datetime.datetime.now()
    timezone = pytz.timezone(zona)
    return (timezone.localize(horazona)).strftime(format)