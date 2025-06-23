import pandas as pd
import os
from datetime import datetime
import cv2
import numpy as np
import platform
import subprocess

archivo_csv = 'asistencia.csv'

if not os.path.exists(archivo_csv):
    df = pd.DataFrame(columns=['Nombre', 'Fecha', 'Hora'])
    df.to_csv(archivo_csv, index=False)

def registrar_asistencia_manual(nombre):
    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M:%S")
    
    df = pd.read_csv(archivo_csv)
    ya_registrado = ((df['Nombre'] == nombre) & (df['Fecha'] == fecha)).any()

    if not ya_registrado:
        nuevo = {'Nombre': nombre, 'Fecha': fecha, 'Hora': hora}
        df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
        df.to_csv(archivo_csv, index=False)
        print(f"Asistencia registrada para {nombre} a las {hora}")
    else:
        print(f"{nombre} ya registró asistencia hoy.")

def registrar_asistencia_qr():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    print("Escanea tu código QR... Presiona 'q' para salir.")
    while True:
        _, frame = cap.read()
        datos, puntos, _ = detector.detectAndDecode(frame)

        cv2.imshow("Lector QR", frame)

        if datos:
            nombre = datos.strip()
            print(f"QR detectado: {nombre}")
            registrar_asistencia_manual(nombre)
            break

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def ver_lista_asistencias():
    usuario = input("Usuario: ")
    while usuario != "UserUIDE":
        usuario = input("Usuario incorrecto, pruebe otra vez: ")

    contraseña = input("Contraseña: ")
    while contraseña != "Uide.asu.123":
        contraseña = input("Contraseña incorrecta, pruebe otra vez: ")

    print("Acceso permitido. Lista de asistencias:\n")
    df = pd.read_csv(archivo_csv)
    print(df)

    ruta = os.path.abspath(archivo_csv)
    os.startfile(ruta)

print("Bienvenidos al registro de asistencia")
print("1 - Registro de asistencia manual")
print("2 - Registro de asistencia con código QR")
print("3 - Ver la lista de asistencias")

opcion = input("Elija una opción (1-3): ")

if opcion == "1":
    print("Registro manual seleccionado")
    nombre = input("Ingrese su nombre completo: ").strip()
    registrar_asistencia_manual(nombre)

elif opcion == "2":
    print("Registro por código QR seleccionado")
    registrar_asistencia_qr()

elif opcion == "3":
    print("Acceso a la lista de asistencias")
    ver_lista_asistencias()

else:
    print("Ingrese una opción válida (1, 2 o 3)")
