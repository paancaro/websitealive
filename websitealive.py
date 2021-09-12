from modulos.pac_websitealive import construir_monitor, espera_siguiente_prueba
import sys,os,requests
sys.path.insert(0, '\modulos')
from modulos import pac_os,pac_email,pac_websitealive
#Deshabilita el chequeo de Certificados para validar self-certicates e IPs en hostname 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Leer archivo de configuracion
dic_configuracion = pac_os.toml_leer_archivo("config.toml")
#Parametros de configuracion
tiempo_espera_entre_pruebas=dic_configuracion['general']['tiempo_espera_entre_pruebas']
tiempo_espera_por_prueba=dic_configuracion['general']['tiempo_espera_por_prueba']
cuantos_eventos_disparan=dic_configuracion['general']['cuantos_eventos_disparan']
enviar_correo=dic_configuracion['general']['enviar_correo']
escribe_en_log_eventos=dic_configuracion['general']['escribe_en_log_eventos']
zona_horaria=dic_configuracion['general']['zona_horaria']
informacion_consola=dic_configuracion['general']['informacion_consola']
if (dic_configuracion['general']['validar_certificado'] == 1):
    validar_certificado = True
else:
    validar_certificado = False

#Leer configuracion del servidor
server = pac_email.lee_configuracion_server(dic_configuracion)
#Leer configuracion del correo
correo = pac_email.CorreoElectronico(
    dic_configuracion['email']['config']['to'],
    '',
    '',
    dic_configuracion['email']['build']['subject'],
    dic_configuracion['email']['build']['body'],
    dic_configuracion['email']['config']['sender'])
#Construye el monitor
Monitor = pac_websitealive.construir_monitor(dic_configuracion)
#Ejecuta Monitor: Chequeo de websites
error=False
while True:
    os.system('cls')
    for mon in Monitor:
        #r=requests.Session()
        #r.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
        try:
            r = requests.get(mon.url, timeout = tiempo_espera_por_prueba, verify=validar_certificado )
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            error=True
            print (pac_websitealive.colored(255,0,0,'Timeout exceeded: '+ mon.url))
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            error=True
            print (pac_websitealive.colored(255,0,0,'Bad URL constructed: '+ mon.url))
        except requests.exceptions.RequestException:
            # catastrophic error. bail.
            error=True
            print (pac_websitealive.colored(255,0,0,'Failed to establish a connection: '+ mon.url))
            #raise SystemExit(e)
        #Guarda respuesta
        if error:
            mon.response_time= round(tiempo_espera_por_prueba*1000,0)
            mon.response_code= 408
            error=False
        else:
            mon.response_time= round((r.elapsed.total_seconds())*1000,0)
            mon.response_code= r.status_code
        if mon.response_code != 200:
            mon.consecutive_failures+=1
            mon.consecutive_success=0
            mon.state='down'
        else:
            mon.consecutive_failures=0
            mon.consecutive_success+=1
            mon.state='up'
    #Ejecuta monitor: Envio de correos
    for mon in Monitor:
        if mon.consecutive_failures > cuantos_eventos_disparan or mon.consecutive_success > cuantos_eventos_disparan:
            if mon.previous_state != mon.state:
                mon.previous_state=mon.state
                if enviar_correo:
                    correo.subject=dic_configuracion['email']['build']['subject'] + ' ' + mon.url + ' is ' +  mon.state
                    correo.body=dic_configuracion['email']['build']['body'] + ' ' + mon.url + ' is ' +  mon.state
                    pac_email.enviar_correo(server,correo)
    # Resultado a pantalla
    pac_websitealive.imprimir_monitor(Monitor)
    print (zona_horaria + ': '+ pac_websitealive.hora_zona(zona_horaria) + '\n')
    pac_websitealive.espera_siguiente_prueba(tiempo_espera_entre_pruebas)















