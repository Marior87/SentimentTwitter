# Análisis de Sentimiento en Tweets

En este proyecto, vamos a ver cómo podemos realizar análisis de Sentimiento en Tweets sin necesidad de tener conocimientos avanzados sobre técncas de NLP.

**NOTA IMPORTANTE:** En este proyecto vamos a utilizar una capa gratis del servicio de análisis de texto de Goggle Cloud Platform (GCP). Se explicará brevemente cómo solicitar el acceso a la API respectiva y utilizarla para el fin requerido. No obstante, se recomienda que cada paso que se de durante la configuración de dicho servicio se haga de forma consciente, ya que en caso de no hacerlo, se pueden incurrir en costos no planificados.

**Fuente**: Este proyecto fue adaptado del siguiente [artículo](https://www.freecodecamp.org/news/how-to-make-your-own-sentiment-analyzer-using-python-and-googles-natural-language-api-9e91e1c493e/). Puede ser de utilidad en caso de que algunos conceptos no queden claros en este documento.

## Requisitos

- Python >= 3.7 (aunque es muy posible que funcione en la mayoría de las versiones 3.\*).
- Cuenta en GCP.
- Cuenta de Desarrollador en Twitter.

Con respecto a los dos últimos requisitos, se detallarán un poco más a continuación.

### Cuenta en GCP

Al momento de escribir este tutorial, es posible crear una cuenta en GCP a partir de una cuenta Google regular (Gmail). Si es la primera vez que la configuramos, Google nos dará de forma gratuita 300 USD en créditos a ser utilizados en 12 meses.

Incluso es posible que quieras crearte una cuenta Gmail nueva para hacer este proyecto, esto también lo puedes hacer de forma gratuita ingresando a [Gmail](https://google.com/gmail).

Una vez creada la cuenta, ingresamos a la [consola de GCP](https://console.cloud.google.com). Si es la primera vez que la utilizamos, nos va a pedir una serie de datos, incluídos datos sobre una Tarjeta de Crédito. **Puesto que los Términos de Servicio pueden cambiar en cualquier momento, recomiendo leerlos atentamente**. Actualmente indican que solo requieren esa información para verificar la cuenta y para que exista un medio de cobro en caso de que se incurran en gastos.

#### Creación del Proyecto en GCP

Una vez dentro de la consola, se nos mostrará el dashboard donde aparecerá un resumen de los servicios que tenemos activos, si es la primera vez que la usas seguramente no tendrá mucha información.

Un proyecto en GCP no es más que una forma de manejar los servicios que queramos incorporar de manera centralizada. Los proyectos permiten controlar gastos y autorizaciones de acceso a servicios que se configuren dentro de GCP. Para poder utilizar cualquier servicio es necesario crear un proyecto.

Si durante la bienvenida no nos indicó que debemos crear un proyecto, podemos utilizar el siguiente [link](https://console.cloud.google.com/projectcreate).

#### Activación del Servicio de NLP y obtención de llave de permiso en GCP

Para utilizar la API de Cloud Natural Language en nuestra aplicación, debemos activar dicha API dentro del proyecto y obtener una llave de acceso en formato JSON, en las siguientes imágenes se detalla dicho procedimiento:

Al activar la API, pide la vinculación con la cuenta de facturación.

Le podemos dar un nombre cualquiera a la cuenta de servicio.

### Cuenta en Twitter Developers

Puesto que el interés de la aplicación no es solo el análisis de sentimiento, sino el que estos provengan desde Twitter, debemos contar con una cuenta en [Twitter Developers](https://developer.twitter.com/en).

Este paso es quizás el que tome más tiempo, ya que acceder a la API de Twitter requiere crear dentro de la cuenta de Twitter Developers una App, y para ello debemos llenar un registro en donde exponemos el uso que le daremos a dicha aplicación.

Una vez autorizada la creación de la App, podemos navegar hasta el [detalle de la misma](https://developer.twitter.com/en/apps). Ahí buscamos en la pestaña Keys and Tokens, en caso de ser necesario hacer click en el botón “Create” en “Access token & access token secret”.

Crear un archivo json con la siguiente estructura:

Keys.json:

```
{
    "Access_token":"Twitter-Access-Token",
    "Access_token secret":"Twitter-Access-Token-Secret",
    "API_key":"Twitter-API-Key",
    "API_secret key":"Twitter-API-Secret Key"
}
```

Una vez se tenga este archivo, se cuenta con todo lo necesario para probar la aplicación.

## Probando la aplicación

Para verificar que todo funcione correctamente, se incluye un archivo que se puede ejecutar en línea de comando y observar los resultados.

Los pasos a seguir son los siguientes:

### Clonar este repositorio

```
git clone https://github.com/Marior87/SentimentTwitter.git
cd SentimentTwitter
```

### Crear entorno virtual de Python e instalar dependencias

```
python3 -m venv <nombre_cualquiera>
```

En mi caso, < nombre cualquiera > es "sent".

```
source sent/bin/activate
pip3 install -r requirements.txt
```

### Configurar variable de entorno de Google

En la línea de comandos:

```
export GOOGLE_APPLICATION_CREDENTIALS=<path-to-gcp-credential-file.json>
```

< path-to-gcp-credential-file.json > es el archivo que descargamos con las credenciales de Google.

**Nota:** Esto puede ser diferente para Sistemas Operativos Windows, en mi caso estoy en Ubuntu pero debe servir de la misma manera para entornos Mac.

### Ejecutar archivo de prueba

```
python3 aplicacion.py -q NLP
```

Se puede sustituir "NLP" por cualquier otro query de búsqueda de interés, si es más de una palabra se debe utilizar entre comillas dobles: "Machine Learning".
