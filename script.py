#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import ldap
import ldap.modlist as modlist
import getpass

#Abrimos el fichero JSON
fichero = open("fichero.json","r")
datos = json.load(fichero)

#Inicializamos LDAP y añadimos la credenciales con la contraseña.
passwd = getpass.getpass("Password: ")
uri = ldap.initialize("ldap://localhost:389")
uri.simple_bind_s("cn=admin,dc=agomez,dc=gonzalonazareno,dc=org","%s" % (passwd))

#Iniciamos dos variables que guarden el UID y el GID
uidNumber = 3000
gidNumber = 3000

#Recorremos las "Personas" y las añadimos a LDAP
for i in datos["personas"]:
        dn="uid=%s,ou=Personas,dc=agomez,dc=gonzalonazareno,dc=org" % str(i["usuario"].encode("utf-8"))
        atributos = {}
        atributos['objectclass'] = ['top','posixAccount','person','inetOrgPerson','ldapPublicKey']
        atributos['cn'] = str(i["nombre"].encode("utf-8"))
        atributos['uid'] = str(i["usuario"].encode("utf-8"))
        atributos['sn'] = str(i["apellidos"].encode("utf-8"))
        atributos['uidNumber'] = str(uidNumber)
        atributos['gidNUmber'] = str(gidNumber)
        atributos['mail'] = str(i["correo"].encode("utf-8"))
        atributos['sshPublicKey'] = str(i["clave"].encode("utf-8"))
        atributos['homeDirectory'] = ['/home/%s' % (str(i["usuario"].encode("utf-8")))]
        atributos['loginShell'] = ['/bin/bash']
        ldif = modlist.addModlist(atributos)
        uri.add(dn,ldif)
        uidNumber = uidNumber + 1
        print "Usuario " + i["usuario"].encode("utf-8") + " añadido"


#Cerramos la conexión con LDAP y cerramos el fichero JSON
uri.unbind_s()
fichero.close()