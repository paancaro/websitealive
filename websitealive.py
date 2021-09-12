from modulos.pac_websitealive import construir_monitor
import sys,os,requests
sys.path.insert(0, '\modulos')
from modulos import pac_os,pac_email,pac_websitealive

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
os.system('cls')
for mon in Monitor:
    print('Testing: ' + mon.url)
    r = requests.get(mon.url, timeout = tiempo_espera_por_prueba)
    print (r.status_code)
    if r.status_code != 200:
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
for mon in Monitor:
    print(mon)

















