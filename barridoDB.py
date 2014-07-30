__author__ = 'chapo'


import MySQLdb
import time
import socket
import os
import config
import re
import comunicacionG4
import mosquitto

encabezado39msn1 = "GET /A/B/7F260009813900000008"
encabezado39msn2 = "GET /A/B/7F260009823900000008"
encabezado39msn3 = "GET /A/B/7F260009833900000008"
encabezado39msn4 = "GET /A/B/7F260009843900000008"
_39 = ""
final39 = " HTTP/1.1"

# Create Mosquitto Client for Watchdog broker
mqttcWC = mosquitto.Mosquitto("pingWC")

def on_connect_pingWC(mosq, obj, rc):
    config.logging.info("Supervisor Watchdog Client connected")
    mqttcWC.subscribe("#", 0)

def ping():
    pingMatch = None
    while pingMatch is None:
        time.sleep(10)
        config.logging.info("Trying to ping google")
        pingResult = os.popen("ping -c 1 www.google.com").read()
        pingMatch = re.search(', 1 received', pingResult)
        if pingMatch != None:
            config.logging.info("ping to google succesfull")
        else:
            config.logging.info("ping to google fail")


def SincronizarReloj():
    global r, comando
    r = 200
    while r != 0:
        time.sleep(10)
        config.logging.info("Trying to syncronize the clock")
        r = os.system('ntpdate {0}'.format(config.ntpserver))
        if r == 0:
            config.logging.info("Reloj Sincronizado")
        else:
            config.logging.info("No Hora Valida... Reintentando")


def ConexionDB():
    global comando, _39, r, secuenciaIp

    #DB Connect
    db = MySQLdb.connect(host=secuenciaIp, user='admin', passwd='petrolog', db='eventosg4', connect_timeout=10)
    config.logging.info("Comunicacion con Base de Datos Correcta!!!")
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT fecha_adquisicion FROM eventos')
    temp = cursor.fetchone()
    fechaBd = temp['fecha_adquisicion']

    # Close DB object
    cursor.close()
    db.close()

    hora = str(fechaBd)
    fecha = str(fechaBd)
    fechaAcomprar = "{0} {1}".format(hora[11:], fecha[:-9])
    aa = time.strptime(fechaAcomprar, '%H:%M:%S %Y-%m-%d')
    tiempoDB = time.mktime(aa)
    tiempoSys = time.mktime(time.localtime())
    minutosDesincronizados = (tiempoSys - tiempoDB)/60
    entero =int(round(minutosDesincronizados))
    config.logging.debug(hex(entero))
    config.logging.info(format(entero, '#06X'))
    valor =format(entero, '#06X')

    if entero >= 11:
        _39 = "{0}{1}".format(_39, valor[2:])
        config.logging.info("Tiempo de desconexion = {0}".format(minutosDesincronizados))
    else:
        _39="{0}{1}".format(_39, "000A")
        config.logging.info( "Todo Normal 000A")


def adquierefecha(ip):
    global comando, _39, r, secuenciaIp
    # Construct DB object
    secuenciaIp = "192.168.1.{0}".format(ip)
    config.logging.info("Equipo Remoto {0} ".format(secuenciaIp))

    if ip > 52:
        entero =int(round(counter))
        config.logging.debug(hex(entero))
        config.logging.info(format(entero, '#06X'))
        valor =format(entero, '#06X')
        _39 = "{0}{1}".format(_39, valor[2:])

    else:
        c = 0
        while c <= config.reintentosdb:
            c += 1
            try:
                config.logging.info("Intentando comunicacion con Base de Datos")
                ConexionDB()
            except MySQLdb.Error:
                time.sleep(2)
            else:
                break
        if c >= config.reintentosdb:
            config.logging.info("Comunicacion con Base de Datos Fallida")
            _39="{0}{1}".format(_39,"0005")

#GET /A/B/7F260009333900000008 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 FFED 0000 0000 HTTP/1.1
ip = 1
config.logging.info("Inicializando...")
ping()
SincronizarReloj()
config.logging.info("Iniciando")
tiempoBarrido = 1500
pruebaConexion = 0
comunicacionG4.SendCommand("01A61")
counter = 0

# Connect to mqtt watchdog server
mqttcWC.on_connect = on_connect_pingWC
mqttcWC.connect('localhost', 1884)

while True:
    try:

        # mqtt client loop for watchdog keep alive
        config.logging.debug("ping: Watchdog Keep Alive")
        mqttcWC.loop(0)

        if ip <= 14:
            adquierefecha(ip)
            config.logging.debug(_39)
            if ip == 14:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("nebulalisten.com", 3001))
                s.send("{0}{1}{2}".format(encabezado39msn1, _39, final39))
                config.logging.info("Envio 39  --->{0}{1}{2}".format(encabezado39msn1, _39, final39))
                config.logging.info("Respuesta correcta!!!!  {0}".format(s.recv(1024)))
                s.close()
                _39 = ""
            ip += 1
        elif (ip > 14) and (ip <= 28):
            adquierefecha(ip)
            config.logging.debug(_39)
            if ip == 28:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("nebulalisten.com", 3001))
                s.send("{0}{1}{2}".format(encabezado39msn2, _39, final39))
                config.logging.info("Envio 39  --->{0}{1}{2}".format(encabezado39msn2, _39, final39))
                config.logging.info("Respuesta correcta!!!!  {0}".format(s.recv(1024)))
                s.close()
                _39 = ""
            ip += 1
        elif (ip > 28) and (ip <= 42):
            adquierefecha(ip)
            config.logging.debug(_39)
            if ip == 42:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("nebulalisten.com", 3001))
                s.send("{0}{1}{2}".format(encabezado39msn3, _39, final39))
                config.logging.info("Envio 39  --->{0}{1}{2}".format(encabezado39msn3, _39, final39))
                config.logging.info("Respuesta correcta!!!!  {0}".format(s.recv(1024)))
                s.close()
                _39 = ""
            ip += 1
        elif (ip > 42) and (ip <= 56):
            adquierefecha(ip)
            config.logging.debug(_39)
            if ip == 56:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("nebulalisten.com", 3001))
                s.send("{0}{1}{2}".format(encabezado39msn4, _39, final39))
                config.logging.info("Envio 39  --->{0}{1}{2}".format(encabezado39msn4, _39, final39))
                config.logging.info("Respuesta correcta!!!!  {0}".format(s.recv(1024)))
                s.close()
                _39 = ""
            ip += 1
        else:
            ip = 1
            if pruebaConexion <= 0:
                tiempoBarrido = 1500

            counter += 1
            config.logging.info("barridos realizados  ---> {0}".format(counter))
            if counter >= 50:
                counter = 0
                comunicacionG4.SendCommand("01A60")

                t = 0
                while t < 60:
                    # mqtt client loop for watchdog keep alive
                    config.logging.debug("Watchdog Keep Alive")
                    mqttcWC.loop(0)
                    time.sleep(1)
                    t += 1

                comunicacionG4.SendCommand("01A61")
            else:
                t = 0
                while t < tiempoBarrido:
                    # mqtt client loop for watchdog keep alive
                    config.logging.debug("Watchdog Keep Alive")
                    mqttcWC.loop(0)
                    time.sleep(1)
                    t += 1

            pruebaConexion = 0
            ping()

    except socket.timeout, e:
        s.close()
        config.logging.info("-----Time Out socket No hay internet-------")
        config.logging.info("39 sin internet  --->{0}{1}{2}".format(encabezado39msn4,_39,final39))
        if ip == 14:
            _39 = ""
        elif ip == 28:
            _39 = ""
        elif ip == 42:
            _39 = ""
        elif ip == 56:
            _39 = ""
        ip += 1
        pruebaConexion += 1
        if pruebaConexion >= 4:
            config.logging.info("No internet reiniciando router")
            comunicacionG4.SendCommand("01A60")
            time.sleep(60)
            comunicacionG4.SendCommand("01A61")
            tiempoBarrido = 120

    except socket.gaierror, e:
        s.close()
        config.logging.info("-----Socket No hay internet-------")
        config.logging.info("39 sin internet  --->{0}{1}{2}".format(encabezado39msn4,_39,final39))
        if ip == 14:
            _39 = ""
        elif ip == 28:
            _39 = ""
        elif ip == 42:
            _39 = ""
        elif ip == 56:
            _39 = ""
        ip += 1
        pruebaConexion += 1

        if pruebaConexion >= 4:
            config.logging.info("No internet reiniciando router")
            comunicacionG4.SendCommand("01A60")
            time.sleep(60)
            comunicacionG4.SendCommand("01A61")
            tiempoBarrido = 120
    except socket.error,e:
        s.close()
        config.logging.info("-----Socket Error-------")
        config.logging.info("39 sin internet  --->{0}{1}{2}".format(encabezado39msn4,_39,final39))
        if ip == 14:
            _39 = ""
        elif ip == 28:
            _39 = ""
        elif ip == 42:
            _39 = ""
        elif ip == 56:
            _39 = ""
        ip += 1