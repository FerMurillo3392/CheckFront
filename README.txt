====================================================
Verificador Avanzado de Sitios API - Documentación
====================================================

Este script permite verificar endpoints API de sitios web, mostrando:
- Códigos de estado HTTP
- Información básica de la respuesta JSON
- Existencia de módulos en la estructura de datos

------------------------
Requisitos Previos
------------------------
1. Python 3.7 o superior
2. Dependencias necesarias:
   - playwright
   - tkinter (normalmente incluido en Python)
   - asyncio, threading, json

Instalar dependencias con:
```bash
pip install playwright
playwright install

====================================================
Manual de Usuario
====================================================

El scrip cuenta con dos archivos indispensables para el uso:
-sites_config.json
-main_menu.py

sites_config.json:
Es el diccionario donde se guarda la configuracion necesaria para los sitios
- Cada sitio debe tener un nombre, URL y módulos a verificar.
- Ejemplo:
{
   "Sitio Ejemplo": 
      {
         "name": "Sitio Ejemplo",//Este es campo que toma en la interfaz grafica de tkinter
         "base_url": "http://stage2-front.milenio.com",////Esta es la URL base del sitio, en este caso se estan usando los stage de front
         "api_base": "https://stage2-api.milenio.com/v2",///Esta es la URL base de la API del sitio, en este caso se estan usando los stage de API
         "slugs": { //Estos son los slugs que se van a verificar en la API
            "noticias": "/noticias",
            "deportes": "/deportes",
            "opinion": "/opinion",
            "espectaculos": "/espectaculos",
            "finanzas": "/finanzas",
            "tecnologia": "/tecnologia",
            "cultura": "/cultura",
            "videos": "/videos",
            "podcast": "/podcast"
         }
      }
}

main_menu:
Es el script principal que ejecuta la interfaz gráfica y maneja la lógica de verificación de los sitios.
- Permite seleccionar un sitio y verificar sus endpoints.
- Muestra los resultados en una tabla.
------------------------
Uso
------------------------
1. Asegúrate de tener configurado el archivo `sites_config.json` con los sitios que deseas verificar.
2. Ejecuta el script `main_menu.py`:
```bash
python main_menu.py
```
3. Selecciona el sitio que deseas verificar desde la interfaz gráfica.
4. Haz clic en "Verificar Endpoints" para iniciar la verificación.
5. Los resultados se mostrarán en una tabla, incluyendo:
   - Nombre del sitio
   - Endpoint verificado
   - Código de estado HTTP
   - Información básica de la respuesta JSON
   - Existencia de módulos en la estructura de datos
6. Puedes exportar los resultados a un archivo JSON haciendo clic en "Exportar Resultados".
7. Dando click en un módulo, se abrirá una nueva ventana con la información detallada del módulo seleccionado.
7.1 Si el módulo no existe, se mostrará un mensaje indicando que no se encontró el módulo.
7.2 Si el módulo existe, se mostrará la información del módulo en formato JSON.
7.3 Si el módulo es un array, se mostrará la información de cada elemento del array.
8. Para salir, cierra la ventana de la aplicación.

====================================================
Resultados
====================================================
Los resultados de la verificación se guardan en un archivo JSON llamado `test_results.json` en el mismo directorio del script. Este archivo contiene:
- Nombre del sitio
- Endpoint verificado
- Código de estado HTTP
- Información básica de la respuesta JSON
- Existencia de módulos en la estructura de datos
- Detalles de los módulos verificados
------------------------
Notas
------------------------
- Asegúrate de que los endpoints de la API estén activos y accesibles desde tu red.
- La verificación puede tardar dependiendo del número de endpoints y la velocidad de la red.
- Los resultados se guardan en un archivo JSON para su posterior análisis.
- Puedes modificar el archivo `sites_config.json` para agregar o eliminar sitios y sus respectivos endpoints.
- La interfaz gráfica está diseñada para ser intuitiva y fácil de usar, permitiendo una rápida verificación de múltiples sitios.

