# Introducción

En este repositorio se entrega la resolución del problema propuesto en la tarea 2 de sistemas distribuidos.

# Ejecución de la aplicación

En primera instancia, desde el directorio api-kafka se debe ejecutar el siguiente comando desde la consola:

```bash
docker-compose up -d
```
Esto construirá las imágenes de los contenedores correspondientes al sistema de login y block de la API y también las ejecutará junto a las imágenes relacionadas al servidor de Apache Kafka.

Sin embargo, debido a que el Docker del sistema de bloqueo se ejecuta antes que el contenedor del Broker, el servicio de block ofrecido por la aplicación es levantado de forma manual. De esta manera, para realizar lo dicho se debe abrir una nueva consola establecida en el directorio api-kafka. Luego, se ejecuta el siguiente comando:
```bash
docker exec -it api-kafka_api-security_1 python /app/app.py
```
Con ello, ya está la aplicación ejecutándose. Lo único que falta es crear un tópico en el servidor de Apache Kafka. Para esto, desde una nueva consola establecida en el directorio api-kafka se ingresa el siguiente comando:
```bash
docker exec -it api-kafka_kafka_1 /opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic mytopic
```
Así, la aplicación se encuentra lista para utilizar.

# Método de uso de los servicios

Para utilizar el servicio de login de la aplicación, se debe hacer un request del tipo POST al siguiente link: localhost:3000/login. Además, los datos a enviar deben estar en formato JSON con la siguiente estructura:
```json
{
	"user": "usuario",
	"pass": "contraseña"
}
```
Donde en "usuario" y en "contraseña" se ha de reemplazar con la información correspondiente. La respuesta a esto será la misma entrada válida dispuesta en el request POST.

Para el caso del sistema de bloqueo, se debe realizar una petición GET al link localhost:5000/blocked. La respuesta a esto será una variable con la lista de usuarios bloqueados.

# Respuestas a preguntas

1. ¿Por qué Kafka funciona bien en este escenario?

Kafka funciona bien para este tipo de casos debido a que se requiere un sistema de seguridad en tiempo real. Esto quiere decir que si se intenta ingresar con fuerza bruta a una cuenta del sistema, la aplicación debe ser capaz de bloquear al usuario en el momento que corresponde. Si el servicio demora más de la cuenta, puede suceder en ese tiempo que el atacante ya haya ingresado al sistema y haber cumplido su objetivo.

2. Basado en las tecnologías que usted tiene a su disposición (Kafka, backend), ¿qué haría usted para manejar una
gran cantidad de usuarios al mismo tiempo?

Para manejar varios usuarios al mismo tiempo, aumentaría la cantidad de particiones del tópico implementado y, adicionalmente, agregaría consumidores de dichas particiones de tal forma que se repartan el trabajo de procesar la transmisión de datos de los usuarios (productores).


