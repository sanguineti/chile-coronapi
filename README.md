# chile-coronapi

API para obtener datos acerca de contagios de coronavirus (COVID-19) en Chile.

# Sobre el uso de la API
Esta API es abierta y puede ser utilizada en cualquier proyecto. Se solicita que, en caso de utilizarla, me contactes por [Telegram](https://t.me/fsanguineti) para poder linkear el proyecto a este repositorio y llevar un mejor manejo de en dónde se está utilizando. 

# Colaboraciones
Cualquier persona es libre de colaborar con este proyecto. Simplemente se debe hacer un fork, añadir la característica y hacer un Pull Request bien documentado de lo que se quiere añadir. Se agradece contactarme por [Telegram](https://t.me/fsanguineti) en este caso.

# Endpoints v1
| GET Request                                                               | Output                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| https://chile-coronapi.herokuapp.com/api/v1/latest/regions                | Obtener datos de contagios por región, correspondientes al último informe del minsal. ([Minsal](https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/) , [El Desconcierto](https://www.eldesconcierto.cl/2020/03/18/datos-los-mapas-y-graficos-de-la-evolucion-y-efectos-del-coronavirus-en-chile-y-en-el-mundo/) )                                                       |
| https://chile-coronapi.herokuapp.com/api/v1/latest/regions?id={region-id} | Obtener datos de contagios para una región específica. En region-id debe ir el número de región del sistema antigio, Metropolitana es id=13.  ([Minsal](https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/) , [El Desconcierto](https://www.eldesconcierto.cl/2020/03/18/datos-los-mapas-y-graficos-de-la-evolucion-y-efectos-del-coronavirus-en-chile-y-en-el-mundo/) |
| https://chile-coronapi.herokuapp.com/api/v1/latest/national               | Obtener estadísticas a nivel nacional, para el día actual (Worldmeters, [NovelCOVID API](https://www.worldometers.info/coronavirus/))                                                                                                                                                                                                                                                                      |

# Sobre la fuente de los datos

Los datos para los endpoints con información regional son obtenidos desde el Ministerio de Salud de Chile y recopilados por Meritxell Freixas@ El Desconcierto. Se actualizan alrededor del mediodía todos los días. El Endpoint que da las estadísticas a nivel nacional obtiene la información directamente desde NovelCOVID API, actuando como wrapper para obtener la información de Chile.


## Instalar el proyecto

Basta con clonar el repositorio, e instalar los requerimientos:

```
pip install requirements.txt
```

Luego usar los archivos .template para generar el setup.py y el .env
Se debe especificar una `SECRET_KEY` sólo en producción. Esto se puede hacer, por ejemplo, ejecutando en la consola de python:

```python
import uuid
uuid.uuid4().hex
```

Para development, se pueden utilizar los datos de prueba que hay en la carpeta `fixtures`. 
Si se desea simular el comportamiento de la aplicación, se debe crear una cuenta en DataWrapper, subir el archivo y generar un token para obtener los datos desde ese gráfico.

Para correr la aplicación en un servidor local, se puede hacer simplemente ejecutando `flask run`en la raíz del proyecto.

