# chile-coronapi

API para obtener datos acerca de contagios de coronavirus (COVID-19) en Chile. Utiliza los datos oficiales del Gobierno de Chile y el Ministerio de Salud. Los datos se manejan en el repositorio hermano [covid19-data](https://github.com/jorgeperezrojas/covid19-data) y se actualizan prácticamente en tiempo real. Para más información, revisar otros datos interesantes sobre el coronavirus en Chile o revisar cómo se realiza el scraping, referir a ese repositorio.

## IMPORTANTE
Esta API no entrega ni entregará *nunca jamás* información sobre los pacientes `recuperados` que entrega el Ministerio de Salud, dado que ese dato carece de rigurosidad y validez científica. 
Instamos, además, a que si realizas un proyecto consumiendo esta API, por favor no consumas esa información desde otra fuente, ni mucho menos intentes reportar pacientes activos. 
Esto para que seamos responsables con los datos que entregamos.

## Sobre el uso de la API
Esta API es abierta y puede ser utilizada en cualquier proyecto. Se solicita que, en caso de utilizarla, nos contactes por [Telegram](https://t.me/fsanguineti) para poder linkear el proyecto a este repositorio y llevar un mejor manejo de en dónde se está utilizando. También nos puedes enviar un [correo](mailto:franco.sanguineti@ug.uchile.cl)

## Colaboraciones y Issues
Cualquier persona es libre de colaborar con este proyecto. Simplemente se debe hacer un fork, añadir la característica y hacer un Pull Request (**en Develop**) bien documentado de lo que se quiere añadir. Se agradece contactarnos por [Telegram](https://t.me/fsanguineti) o [mail](mailto:franco.sanguineti@ug.uchile.cl).

Por otra parte, se agradece que reportes un bug si lo encuentras mientras estás utilizando esta API. Asimismo, también se agradece la solicitud de nuevas features. Para ambas cosas, sencillamente déjanos una Github Issue.

## Endpoints 
A continuación se detallan todas las formas para poder consumir la API acompañado del dato que se entrega. Cabe destacar que los endpoints v2 y v1 han sido deprecados. Se sugiere utilizar los endpoints v4 en caso de estar disponibles, ya que se planea deprecar v3 a futuro.

### Endpoints v4

| GET Request                                                                               | Output                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| https://chile-coronapi.herokuapp.com/api/v4/historical/communes                           | Se obtienen los datos históricos que el Gobierno ha publicado para todas las comunas agrupadas por región. Estos datos son entregados por parte del ministerio con poca frecuencia, usualmente cada un par de días o un poco más. Para este caso, sólo están disponibles los contagiados confirmados, que es lo único que el gobierno ha entregado de forma oficial. Usualmente un 0 representa que no hay datos significativos para esta comuna.                        |
| https://chile-coronapi.herokuapp.com/api/v4/historical/communes?id={commune-id}           | Se obtienen los datos de la misma forma que en el endpoint anterior, sin embargo, al igual que con las regiones, se puede obtener para una comuna en específico, entregando el *commune-id*, sin los corchetes. La lista de los IDs de comuna está disponible en el endpoint de [models communes](https://chile-coronapi.herokuapp.com/api/v4/models/communes).                                                                                                          |
| https://chile-coronapi.herokuapp.com/api/v4/historical/communes?region_code={region-code} | Se obtienen los datos de la misma forma que en el endpoint anterior, sin embargo, se pueden obtener todas las comunas para una región en específico, entregando el *region-code*, sin los corchetes. La lista de los códigos de regiones está disponible en el endpoint de [models region](https://chile-coronapi.herokuapp.com/api/v3/models/regions).                                                                                                        |
| https://chile-coronapi.herokuapp.com/api/v4/models/communes                               | Se obtiene una lista con todas las comunas del país, agrupadas por región, junto a su ID y a qué región del país pertenecen.                                                                                                                                                                                                                                                                                                                                                                   |


### Endpoints v3

| GET Request                                                                     | Output                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| https://chile-coronapi.herokuapp.com/api/v3/historical/nation                   | Se obtienen los datos, desde el 7 de marzo hasta el día de hoy, de contagiados confirmados, muertes y "recuperados" (según el gobierno al menos, ese dato sigue siendo bastante cuestionable). Estos datos corresponden al total a nivel país.                                                                                                                                                                                                                           |
| https://chile-coronapi.herokuapp.com/api/v3/historical/regions                  | Se obtienen los datos históricos de contagiados y muertes por región. En el caso de los contagiados, los datos están disponibles desde el 7 de marzo hasta el día de hoy. Para el caso de las muertes, los datos están sólo disponibles desde el 1 de abril, que es desde dónde el Gobierno tiene publicadas las cifras oficiales.                                                                                                                                       |
| https://chile-coronapi.herokuapp.com/api/v3/historical/regions?id={region-id}   | Se obtienen los datos de contagiados y muertes por región de la misma forma que en el endpoint anterior, sin embargo, si se entrega el parámetro de region-id (sin los corchetes) se reciben los datos para la región indicada. Los códigos de las regiones corresponden al antiguo sistema de regiones numeradas (e.g, Metropolitana es 13.) Se pueden consultar todos los códigos de regiones disponibles utilizando el Endpoint de *models* que se detalla más abajo. |
| https://chile-coronapi.herokuapp.com/api/v3/historical/communes                 | Se obtienen los datos históricos que el Gobierno ha publicado para todas las comunas. Estos datos son entregados por parte del ministerio con poca frecuencia, usualmente cada un par de días o un poco más. Para este caso, sólo están disponibles los contagiados confirmados, que es lo único que el gobierno ha entregado de forma oficial. Usualmente un 0 representa que no hay datos significativos para esta comuna.                                             |
| https://chile-coronapi.herokuapp.com/api/v3/historical/communes?id={commune-id} | Se obtienen los datos de la misma forma que en el endpoint anterior, sin embargo, al igual que con las regiones, se puede obtener para una comuna en específico, entregando el *commune-id*, sin los corchetes. La lista de los IDs de comuna está disponible en el endpoint de *models* de más abajo.                                                                                                                                                                   |
| https://chile-coronapi.herokuapp.com/api/v3/latest/nation                       | Se obtienen los datos de contagiados, muertes y recuperados para el último día en que el gobierno ha realizado un reporte. El gobierno actualmente realiza un reporte todas las mañanas, con los datos cortados hasta el día anterior a las 21:00 hrs.                                                                                                                                                                                                                   |
| https://chile-coronapi.herokuapp.com/api/v3/latest/regions                      | Datos de regiones para el último día reportado por el ministerio. Con este endpoint se obtiene el último reporte para todas las regiones.                                                                                                                                                                                                                                                                                                                                |
| https://chile-coronapi.herokuapp.com/api/v3/latest/regions?id={region-id}       | Datos de regiones para el último día reportado por el ministerio. Con este endpoint se obtiene el último reporte para la región señalada en el region-id.                                                                                                                                                                                                                                                                                                                |
| https://chile-coronapi.herokuapp.com/api/v3/latest/communes                     | Datos de comunas para el último día reportado por el ministerio. Con este endpoint se obtiene el último reporte para todas las comunas.                                                                                                                                                                                                                                                                                                                                  |
| https://chile-coronapi.herokuapp.com/api/v3/latest/communes?id={commune-id}     | Datos de comunas para el último día reportado por el ministerio. Con este endpoint se obtiene el último reporte para la comuna señalada en el commune-id.                                                                                                                                                                                                                                                                                                                | 
| https://chile-coronapi.herokuapp.com/api/v3/models/regions                      | Se obtiene una lista de todas las regiones junto a su ID respectivo.                                                                                                                                                                                                                                                                                                                                                                                                     |
| https://chile-coronapi.herokuapp.com/api/v3/models/communes                     | Se obtiene una lista con todas las comunas del país, junto a su ID y a qué región del país pertenecen.                                                                                                                                                                                                                                                                                                                                                                   |


## Instalación del proyecto

Basta con clonar el repositorio, e instalar los requerimientos:

```
pip install requirements.txt
```

Luego usar los archivos .template para generar el setup.py y el .env. Vienen configurados con las variables por defecto para trabajar en *development*. Se debe especificar una `SECRET_KEY` sólo en producción. Esto se puede hacer, por ejemplo, ejecutando en la consola de python:

```python
import uuid
uuid.uuid4().hex
```

Para correr la aplicación en un servidor local, se puede hacer simplemente ejecutando `flask run` en la raíz del proyecto.

## Sobre la fuente de los datos
Los datos son las cifras oficiales publicadas por el Gobierno de Chile y el Ministerio de Salud en sus respectivos sitios web. Para los datos que se utilizan en esta API, la actualización es prácticamente en tiempo real, por medio de scraping. Esta API consume los datos directamente desde ese repositorio, por lo que los tiempos de respuesta son bastante buenos y suele ser menor a los 500 milisegundos.

En general, los datos son obtenidos desde el sitio del [gobierno](https://www.gob.cl/coronavirus/cifrasoficiales/), que actualiza muchísimo más rápido que el sitio del [ministerio de salud](.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/), a excepción de los datos respectivos a casos contagiados, que sólo se publican en el sitio del Minsal.

### Datos de Regiones (Models Regions)
Los datos de las regiones son obtenidos desde el sitio del [INE](https://regiones.ine.cl/) e incluyen datos como:
- Nombre de la región
- Información de la región como:
  - Código de  región, que corresponde al antiguo sistema de regiones numeradas(Ej. Metropolitana es 13).
  - Latitud y Longitud  ,   
  - Población de la región
  - Área geográfica en *km²* de la región

### Datos de Comunas (Models Communes)
Los datos son obtenidos mayoritariamente desde el sitio de la [biblioteca del congreso nacional](http://reportescomunales.bcn.cl/2017/index.php/Categor%C3%ADa:Comunas) e incluyen:
- Nombre de la comuna
- Información de la comuna tal como
  - Id o CUT (Código Único Territorial)
  - Área geográfica en *km²* de la comuna
  - Índice de desarrollo humano (Hay unas comunas que su valor es 0, pues no hay datos de ellas).
  - Número de habitantes de la comuna
  - Región y código de ésta que corresponde al antiguo sistema de regiones numeradas


## Publicaciones 

Este proyecto se encuentra enlistado en dos colecciones importantes de APIs:

* [Postman Covid-19 API](https://covid-19-apis.postman.com)
* [Rapidapi Covid-19](https://rapidapi.com/collection/coronavirus-covid-19)

## Proyectos que utilizan la API
* Trabajo de Tesis, DAEM Linares. Matías Vergara Montoya. Inacap sede Talca
* [Dashboard visualización de datos](https://samuelramirez.shinyapps.io/Dashboard_Covid19-Chile/)
* [Covid Monitor APP Android](https://github.com/pabloTP87/CovidMonitor)
* [iCloud Shortcut de Contagiados](https://www.icloud.com/shortcuts/6c295cbb11c7428cbbb60d9734e63323?fbclid=IwAR244tD23_ur5JlKiyGmljaBSovLlOgIwTCR2Aiu1V9PY2j_NNqL_skI1ZU)

## Equipo
* Franco Sanguineti [@sanguineti](https://github.com/sanguineti). Mantenedor. 
* Cristóbal Mesías [@cmesiasd](https://github.com/cmesiasd). Ha trabajado principalmente en la implementación del scraping, nuevas features y solución de bugs de la API.
* José Pacheco [@checopa](https://github.com/checopa). Ha trabajado en la implementación de nuevas features y solución de bugs de la API. 

## Colaboradores
* Fabián Villena [@fvillena](https://github.com/fvillena). Ha agregado información por comuna, como el área geográfica, el indice de desarrollo humano y la cantidad de población de ellas. 
* Marcel Augsburger [@maugsbur](https://github.com/maugsbur). Ha realizado refactor en endpoints de la API.

