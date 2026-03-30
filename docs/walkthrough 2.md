# Resumen de Arquitectura de Datos (Módulo ETL)
En sintonía con tus instrucciones e intenciones formativas para el **TFG**, he implementado la capa de Extracción, Transformación y Carga (**ETL**) de datos sobre Inteligencia Estratégica en League of Legends justificándola bajo limitaciones teóricas documentadas de *Big Data*.

## Herramientas Añadidas
Hemos añadido dependencias clave (`python-dotenv`) para la gestión de permisos en archivo local (`.env`).
Tras analizar la viabilidad del web scraping en la arquitectura actual, se ha optado por un modelo mixto de **Data Entry Manual** sumado a la sincronización estática de Riot Games, lo cual refuerza una estructura predecible y robusturable para la memoria del TFG.

La información reside en **Scripts Ejecutables (`/scripts`)** y en el conocimiento de dominio (Manual):

### 1. Extracción Estática (DataDragon) ✓
El fichero `scripts/fetch_datadragon.py` se conecta vía `HTTP GET` al servicio estático *DataDragon* de League of Legends para buscar el parche actual del juego, reconfigurando y rellenando los campeones base de la aplicación.
* **Propósito**: Obtener Estructura Básica Rápida manteniendo el trabajo manual intacto.

### 2. Base de Hechos Local (Data Entry Manual) ✓
La arquitectura ha prescindido del script de web scraping (`scraper_winrates.py`) que simulaba extracción de datos debido a medidas anti-bots en dominios modernos (Cloudflare) que obligarían al sobrecoste de Selenium. 
* **Propósito**: El usuario alimentará el sistema (`data/champions.json`) aplicando el **conocimiento del dominio** real (etiquetando, ajustando matchups). Esto valida la figura del "Experto" en este sistema experto.

### 3. Prueba de Concepto Riot API (PoC) ✓
El script `scripts/riot_api_poc.py` contiene todo el esqueleto nativo para **evaluar Partidas (Match-V5) e IDs de jugador (Account-V1)** con tu *Developer API Key* real.
Dentro detalla un recorrido lineal *pipeline*, imprimiendo por consola lo largo que es computar decenas de miles de eventos en League of Legends por segundo con sus cuotas restrictivas.

> [!CAUTION] 
> Asegúrate de **NO SUBIR** nunca tu fichero local `.env` a GitHub para que nadie se adueñe de tu API Key. Precisamente para eso hemos configurado `.env.example` dentro del código base.

## Verificación Recomendada
En tu memoria del TFG, bastará con citar ambas capas o ejecutar estos scripts por consola adjuntando pantallas o logs de la ejecución como aval de que conoces las arquitecturas nativas y manejas los Json estaticos como DB.
