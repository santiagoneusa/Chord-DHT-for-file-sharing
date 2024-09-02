# Reto 1: Arquitectura P2P y comunicación entre procesos mediante API REST, RPC y MOM

Asignatura: Tópicos Especiales en Telemática - ST0263

Estudiantes: David Grisales Posada (dgrisalesp@eafit.edu.co) & Santiago Neusa Ruiz (sneusar@eafit.edu.co)

Profesor: Edwin Nelson Montoya Múnera (emontoya@eafit.edu.co)

# 1. Descripción

* Red P2P basada en Chord y DHT utilizada para envío y recepción de dummy data.
* Adjuntar fotografías del resultado final

## 1.1. Aspectos cumplidos

* Requerimientos funcionales
* Requerimientos no funcionales

## 1.2. Aspectos no cumplidos

* Requerimientos funcionales
* Requerimientos no funcionales

# 2. Información general

2.1 Arquitectura: Detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
2.1.1 Diseño de clases
![image](https://github.com/user-attachments/assets/64e906bc-5528-4b3f-a5d7-5425a9927c47)
![image](https://github.com/user-attachments/assets/13e29464-c88f-471b-8ea5-5965d7114a97)

2.1.2 Comunicación entre nodos y servidor
En esta parte se puede ver la comunicación entre los peers y el servidor.
La comunicación de los peers con el servidor se realiza para las peticiones de Register, Unregister, PeersByZone, get_available_zone. Y el servidor responde a cada una de estas peticiones con la estructura definida.
La comunicación entre los peers se realiza para enviar datos y recibir los datos con las funciones RecieveFile y SendFile.
![image](https://github.com/user-attachments/assets/b1b629b2-fa16-4bfa-a033-36bfff5a419f)
2.1.3
En este caso puede verse cómo se empiezan a llenar las zonas o subespacios.
En una primera instancia deben llenarse los subespacios, llendo del espacio cero al espacio n.
Luego se empiezan a llenar aleatoriamente los ids de los nodos para ubicarlos en la zona a la que pertenezca el peer.
![image](https://github.com/user-attachments/assets/017b126f-503c-4627-8d77-1bed4108afe3)




* Patrones
* Mejores prácticas utilizadas

# 3. Descripción del ambiente de desarrollo

## 3.1. Aspectos técnicos

* Lenguaje de programación con números de versiones
* Librerias con números de versiones
* Paquetes con números de versiones

## 3.2. Compilación y ejecución

> pip install -r requirements.txt

Configuración de los parámetros del proyecto

* ip
* puertos
* variables de ambiente
* parámetros

# 4. Descripción del ambiente de ejecución

* En producción lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
* Como se lanza el servidor.
* IP o nombres de dominio en nube o en la máquina servidor.

# 5. Información adicional

Guía de cómo un usuario utilizaría el software.

# Referencias
* Referencias a YouTube
* Referencias bibliográficas
* Referencias de GitHub
