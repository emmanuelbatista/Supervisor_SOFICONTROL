__author__ = 'chapo'


import MySQLdb
import time
import socket
import os
import config


encabezado39msn1 = "GET /A/B/7F260009813900000008"
encabezado39msn2 = "GET /A/B/7F260009823900000008"
encabezado39msn3 = "GET /A/B/7F260009833900000008"
encabezado39msn4 = "GET /A/B/7F260009843900000008"
_39 = ""
final39 = " HTTP/1.1"

def SincronizarReloj():
    global r, comando
    r = os.system('ntpdate {0}'.format(config.ntpserver))
    if r == 0:
        config.logging.info("Reloj Sincronizado")
    else:
        config.logging.info("No Hora Valida")

def ConexionDB():
    global comando, _39, r, secuenciaIp

    db = MySQLdb.connect(host=secuenciaIp, user='admin', passwd='petrolog', db='eventosg4', connect_timeout=15)
    config.logging.info("Comunicacion con Base de Datos Correcta!!!")
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT fecha_adquisicion FROM eventos')
    temp = cursor.fetchone()
    fechaBd = temp['fecha_adquisicion']

    # Close DB object
    cursor.close()
    db.close()

    # Get ntp time
    #r = os.system('ntpdate {0}'.format(config.ntpserver))

    hora = str(fechaBd)
    fecha = str(fechaBd)
    fechaAcomprar = "{0} {1}".format(hora[11:], fecha[:-9])
    aa = time.strptime(fechaAcomprar, '%H:%M:%S %Y-%m-%d')
    if r == 0:
        tiempoDB = time.mktime(aa)
        tiempoSys = time.mktime(time.localtime())
        minutosDesincronizados = (tiempoSys - tiempoDB)/60
        entero =int(round(minutosDesincronizados))
        config.logging.debug(hex(entero))
        config.logging.info(format(entero, '#06X'))
        valor =format(entero, '#06X')

        if entero >= 11:
            _39 = "{0}{1}".format(_39, valor[2:])
            config.logging.info( minutosDesincronizados)
        else:
            _39="{0}{1}".format(_39, "000A")
            config.logging.info( "Todo Normal 000A")
    else:
        config.logging.info("No Internet   codigo de Error!!!! 0001")
        _39= "{0}{1}".format(_39, "0001")


def adquierefecha(ip):
    global comando, _39, r, secuenciaIp
    # Construct DB object
    secuenciaIp = "192.168.1.{0}".format(ip)
    config.logging.info("Equipo Remoto {0} ".format(secuenciaIp))

    if ip > 52:
        _39 = "{0}{1}".format(_39, "0000")

    else:

        try:
            config.logging.info("Intentando comunicacion con Base de Datos")
            ConexionDB()
        except MySQLdb.Error, e:
            config.logging.info("Reintentando comunicacion con Base de Datos")
            try:
                time.sleep(2)
                ConexionDB()
            except MySQLdb.Error, e:
                config.logging.info("Reintentando comunicacion con Base de Datos")
                try:
                    time.sleep(2)
                    ConexionDB()
                except MySQLdb.Error, e:
                    config.logging.info("Comunicacion con Base de Datos Fallida")
                    config.logging.info("Error {0}  0005".format(e.args))
                    _39="{0}{1}".format(_39,"0005")

#GET /A/B/7F260009333900000008 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 FFED 0000 0000 HTTP/1.1
ip = 1
config.logging.info("Inicializando...")
time.sleep(30)
SincronizarReloj()

while True:
    try:
        if ip <= 14:
            adquierefecha(ip)
            config.logging.debug(_39)
            if ip == 14:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("nebulalisten.com", 3001))
                s.send("{0}{1}{2}".format(encabezado39msn4, _39, final39))
                config.logging.info("Envio 39  --->{0}{1}{2}".format(encabezado39msn4, _39, final39))
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
                s.send("{0}{1}{2}".format(encabezado39msn4, _39, final39))
                config.logging.info("Envio 39  --->{0}{1}{2}".format(encabezado39msn4, _39, final39))
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
                s.send("{0}{1}{2}".format(encabezado39msn4, _39, final39))
                config.logging.info("Envio 39  --->{0}{1}{2}".format(encabezado39msn4, _39, final39))
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
            time.sleep(900)
            SincronizarReloj()

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
    except socket.gaierror,e:
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