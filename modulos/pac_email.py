from modulos import pac_websitealive
import smtplib

#Construccion de clase CorreoElectronico
class CorreoElectronico:
    def __init__(self, to, cc, bcc, subject, body, sender,msg_up,msg_down):
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.body = body
        self.sender = sender
        self.msg_up = msg_up
        self.msg_down = msg_down

    def __str__(self):
        return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

#Construccion de clase ServidorCorreo
class ServidorCorreo:
    def __init__(self, server, port, login, password):
        self.server = server
        self.port = port
        self.login = login
        self.password = password
        
    def __str__(self):
        return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))   

#Impresion de una Clase
def imprimir_clase (Clase,var):
    for var in vars(Clase):
        print(getattr(Clase, var))

def enviar_correo (Server, Correo):
    try:
        with smtplib.SMTP(Server.server, Server.port) as smtp:
            print('\nStarting connection to email server ' + Server.server + '.')
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            print('Authenticating .... ' + Server.server + ', puerto ' + str(Server.port) + '.')
            smtp.login(Server.login, Server.password)
            # Version inicial
            #msg = f'Subject: {Correo.subject}\n\n{Correo.body}'
            #smtp.sendmail(Correo.sender, Correo.to, msg)
            # Version incluyendo CC y BCC
            message = "From: %s\r\n" % Correo.sender + "To: %s\r\n" % Correo.to  + "CC: %s\r\n" % Correo.cc + "Subject: %s\r\n" % Correo.subject  + "\r\n" + Correo.body
            toaddrs = [Correo.to] + [Correo.cc] + [Correo.bcc]
            smtp.sendmail(Correo.sender, toaddrs , message)
            smtp.quit()
            print('Email sent')
            return True
    except smtplib.SMTPServerDisconnected:
        print (pac_websitealive.colored(255, 0, 0,'Server cannot be connected: Check configurations.'))
        return False
    except smtplib.SMTPException:
        print (pac_websitealive.colored(255, 0, 0,'Email cannot be sent: General failure.'))
        return False
def lee_configuracion_server (dic_configuracion):
    server = ServidorCorreo(
        dic_configuracion['email']['server']['server'],
        dic_configuracion['email']['server']['port'],
        dic_configuracion['email']['server']['login'],
        dic_configuracion['email']['server']['password'])
    return server


