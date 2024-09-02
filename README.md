# Reto 1: Arquitectura P2P y comunicación entre procesos mediante API REST, RPC y MOM

Asignatura: Tópicos Especiales en Telemática - ST0263

Estudiantes: David Grisales Posada (dgrisalesp@eafit.edu.co) & Santiago Neusa Ruiz (sneusar@eafit.edu.co)

Profesor: Edwin Nelson Montoya Múnera (emontoya@eafit.edu.co)

# 1. Descripción

* En este proyecto se implementó una red P2P no estructurada que servía para el envío y recepción de archivos 'dummy', es decir, transmisión de texto simulando que eran archivos. La red está conectada entre sí utilizando gRPC como middleware tanto para la comunicación hacia el servidor, así como entre los mismos peers.
* La red está dividida en zonas, de tal forma que al realizar una búsqueda en el mejor de los casos se contactaría un solo nodo, mientras que al hacer flooding solo se realizaría en la zona de búsqueda. Las zonas pueden tener mínimo 6 nodos, así que realizar una búsqueda no será tan complejo en términos de recursos.
* El servidor implementado tiene la única funcionalidad de registar cuáles son los peers que están presentes en la red, mas no de la indexación y búsqueda de archivos; esas funcionalidades son exclusivas de los peers.
* Envio de archivos:
![image](https://github.com/user-attachments/assets/4fb21dd5-449f-4f8e-a84e-0da9c4df892f)
* Descarga de archivos:
![image](https://github.com/user-attachments/assets/f0f8f32c-80bc-4897-89a2-41cc72acbb89)

## 1.1. Aspectos cumplidos

* Diseño e implementación de la red P2P no estructurada en Python.
* Servicios para el envío y recepción de archivos.
* Optimización de búsqueda e indexación de archivos mediante el uso de zonas.
* Servidor gestor de sesiones de los peers.
* Creación de Bootstrap para servidor y peer.
* Implementación de los servicios utilizando gRPC.
* Dockerización de la aplicación.
* Integración continua entre GitHub Actions y DockerHub.
* Despliegue del servidor en AWS utilizando una EC2.

## 1.2. Aspectos no cumplidos

* Despliegue del peer en AWS utilizando una EC2.

# 2. Información general

## 2.1. Diseño de clases
![image](https://github.com/user-attachments/assets/64e906bc-5528-4b3f-a5d7-5425a9927c47)
![image](https://github.com/user-attachments/assets/13e29464-c88f-471b-8ea5-5965d7114a97)

## 2.2. Comunicación entre nodos y servidor
En esta parte se puede ver la comunicación entre los peers y el servidor.
La comunicación de los peers con el servidor se realiza para las peticiones de Register, Unregister, PeersByZone, get_available_zone. Y el servidor responde a cada una de estas peticiones con la estructura definida.
La comunicación entre los peers se realiza para enviar datos y recibir los datos con las funciones RecieveFile y SendFile.
![image](https://github.com/user-attachments/assets/b1b629b2-fa16-4bfa-a033-36bfff5a419f)

## 2.3. Diseño e implementación de la red.
En este caso puede verse cómo se empiezan a llenar las zonas o subespacios.
En una primera instancia deben llenarse los subespacios, llendo del espacio cero al espacio n.
Luego se empiezan a llenar aleatoriamente los ids de los nodos para ubicarlos en la zona a la que pertenezca el peer.
![image](https://github.com/user-attachments/assets/017b126f-503c-4627-8d77-1bed4108afe3)

# 3. Descripción del ambiente de desarrollo

## 3.1. Aspectos técnicos

* Se utilizó Python para la implementación de la red.
* Las librerías y sus versiones están en el archivo [requirements.txt](https://github.com/santiagoneusa/Chord-DHT-for-file-sharing/blob/main/requirements.txt).

## 3.2. Compilación y ejecución

### Usando Docker
1. Traer la imagen de docker desde [el repositorio online](https://hub.docker.com/repository/docker/santiagoneusa/p2p-unstructured-grpc/general) a su máquina local.
> docker pull santiagoneusa/p2p-unstructured-grpc
2. Correr un contenedor interactivamente, ya que la aplicación muestra resultados por consola.
> sudo docker run -it santiagoneusa/p2p-unstructured-grpc python ./src/peer/main.py

### Compilación propia
1. Clonar el repositorio de GitHub.
> git clone https://github.com/santiagoneusa/p2p-unstructured-grcp.git
2. Acceder al repositorio.
> cd p2p-unstructured-grcp
3. Crear un ambiente virtual para instalar las dependencias.
> python -m venv venv
4. Activar el ambiente virtual.
> ./venv/Scripts/activate
5. Instalar las dependencias.
> pip install -r requirements.txt
6. Crear el Bootstrap del servidor.
> cp ./src/server/.env.example ./src/server/.env
7. Correr el servidor.
> python ./src/server/main.py
8. Crear el Bootstrap del Peer.
> cp ./src/peer/.env.example ./src/peer/.env
9. Por cada Peer que desee correr debe ejecutar esta línea en una terminal distinta. Recuerde que en ./src/peer/.env debe actualizar el puerto en caso de querer añadir un Peer a la red.
> python ./src/peer/main.py

# 4. Información adicional
## Uso
El servidor solo debe ser ejecutado puesto que no tiene ninguna funcionalidad interactiva. Por otro lado, el cliente al ejecutarse muestra un menú con 4 opciones de las cuales deberá ingresar una por teclado. Cada opción representa una funcionalidad distinta de la aplicación y mostrará un 'status' y un 'message', que son componentes de la respuesta de cada servicio.

## Video
Mediante este [enlace]() puede acceder a un video explicativo del proyecto.

# Referencias
* Referencias a YouTube
* Referencias bibliográficas
* Referencias de GitHub
