#Construccion de clase MonitorWebsite
class MonitorWebsite:
    def __init__(self, url, consecutive_failures, consecutive_success, state, previous_state):
        self.url = url
        self.consecutive_failures = consecutive_failures
        self.consecutive_success = consecutive_success
        self.state = state
        self.last_state = previous_state

    def __str__(self):
        return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

def construir_monitor (dic_configuracion):
    lista_monitor = []
    websites = dic_configuracion['sites']['websites']
    for website in websites:
        lista_monitor.append(MonitorWebsite(website,0,0,'up','up'))
    return lista_monitor

