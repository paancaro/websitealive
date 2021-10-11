"""
Compilacion
pyinstaller.exe --onefile -i:logo.ico websitealive.py

Instalacion dependencias

Conversor de Zona  horaria
pip install pytz

Modulo de solicitud de requerimientos http: / https:
pip install requests

Creacion de tablas elegantes por pantalla 
pip install tabulate

Text to Speech
pip install gTTS

MP3 player para Python
pip install pygame

Gestor de formato TOML
pip install toml

Gestor de envio de correos electronicos
pip install smtplib


"""
from modulos.pac_websitealive import construir_monitor, espera_siguiente_prueba
import sys,os,requests
sys.path.insert(0, '\modulos')
from modulos import pac_os,pac_email,pac_websitealive
#Deshabilita el chequeo de Certificados para validar self-certicates e IPs en hostname 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


version='1.0.5'
#Leer archivo de configuracion
dic_configuracion = pac_os.toml_leer_archivo("config.toml")
#Parametros de configuracion
tiempo_espera_entre_pruebas=dic_configuracion['general']['tiempo_espera_entre_pruebas']
titulo_principal=dic_configuracion['general']['titulo_principal']
tiempo_espera_por_prueba=dic_configuracion['general']['tiempo_espera_por_prueba']
cuantos_eventos_disparan=dic_configuracion['general']['cuantos_eventos_disparan']
enviar_correo=dic_configuracion['general']['enviar_correo']
escribe_en_log_eventos=dic_configuracion['general']['escribe_en_log_eventos']
nombre_log_eventos=dic_configuracion['general']['nombre_log_eventos']
zona_horaria=dic_configuracion['general']['zona_horaria']
msg_up=dic_configuracion['messages']['msg_up']
msg_down=dic_configuracion['messages']['msg_down']
alert_tts=dic_configuracion['tts']['alert_tts']
language_tts=dic_configuracion['tts']['language_tts']
if (dic_configuracion['general']['validar_certificado'] == 1):
    validar_certificado = True
else:
    validar_certificado = False

#Leer configuracion del servidor
server = pac_email.lee_configuracion_server(dic_configuracion)
#Leer configuracion del correo
correo = pac_email.CorreoElectronico(
    dic_configuracion['email']['config']['to'],
    dic_configuracion['email']['config']['cc'],
    dic_configuracion['email']['config']['bcc'],
    dic_configuracion['email']['build']['subject'],
    dic_configuracion['email']['build']['body'],
    dic_configuracion['email']['config']['sender'],msg_up,msg_down)
#Construye el monitor
Monitor = pac_websitealive.construir_monitor(dic_configuracion)
#Ejecuta Monitor: Chequeo de websites
error=False
os.system('cls')
print(pac_websitealive.colored(0,0,255,titulo_principal) + "Version:" +version)
while True:
    pac_websitealive.imprimir_monitor(Monitor)
    for mon in Monitor:
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
            respuesta_sitio=False
            print (pac_websitealive.colored(255,0,0,'Failed to establish a connection: '+ mon.url))
            #raise SystemExit(e)
        #Guarda respuesta
        if error:
            mon.response_time= round(tiempo_espera_por_prueba*1000,0)
            mon.response_code= 408
            respuesta_sitio=False
            error=False
        else:
            mon.response_time= round((r.elapsed.total_seconds())*1000,0)
            mon.response_code= r.status_code
            if r.status_code == 200 or r.status_code == 401:
                respuesta_sitio=True
        if respuesta_sitio != True:
            mon.consecutive_failures+=1
            mon.consecutive_success=0
            mon.state=msg_down
        else:
            mon.consecutive_failures=0
            mon.consecutive_success+=1
            mon.state=msg_up
            respuesta_sitio=False
    #Ejecuta monitor: Envio de correos
    for mon in Monitor:
        if mon.consecutive_failures > cuantos_eventos_disparan or mon.consecutive_success > cuantos_eventos_disparan:
            if mon.previous_state != mon.state:
                pac_os.play_alert_message(alert_tts + ' ' + mon.alias + ' ' + mon.state,language_tts)
                mon.previous_state=mon.state
                if enviar_correo:
                    correo.subject=dic_configuracion['email']['build']['subject'] + ' ' + mon.url + ' is ' +  mon.state
                    correo.body=dic_configuracion['email']['build']['body'] + ' ' + mon.alias + ' ' + mon.url + ' is ' +  mon.state
                    envia_correo = pac_email.enviar_correo(server,correo)
                    if escribe_en_log_eventos and envia_correo:
                        eventolog = pac_os.EventoLog(zona_horaria + ': '+ pac_websitealive.hora_zona(zona_horaria), 'Email sent To: ' + correo.to , ' Site: ' +  mon.url  , 'State: ' + mon.state, 'Alias: ' + mon.alias)
                        pac_os.escribir_log(nombre_log_eventos,eventolog)
                if escribe_en_log_eventos:
                    eventolog = pac_os.EventoLog(zona_horaria + ': '+ pac_websitealive.hora_zona(zona_horaria), mon.url, mon.alias, mon.state, str(mon.response_code))
                    pac_os.escribir_log(nombre_log_eventos,eventolog)
    # Resultado a pantalla
    #pac_websitealive.imprimir_monitor(Monitor)
    pac_websitealive.espera_siguiente_prueba(tiempo_espera_entre_pruebas)
    os.system('cls')
    print(pac_websitealive.colored(0,0,255,titulo_principal) +  ' | ' + pac_websitealive.colored(255,255,0,zona_horaria + ': '+ pac_websitealive.hora_zona(zona_horaria)) +  ' | ' +pac_websitealive.colored(100,100,100," Version:" + version))













