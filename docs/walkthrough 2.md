# Resumen de Arquitectura de Datos (Módulo ETL)
En sintonía con tus instrucciones e intenciones formativas para el **TFG**, he implementado la capa de Extracción, Transformación y Carga (**ETL**) de datos sobre Inteligencia Estratégica en League of Legends justificándola bajo limitaciones teóricas documentadas de *Big Data*.

## Herramientas Añadidas
Hemos añadido dependencias clave (`beautifulsoup4` y `python-dotenv`) para el *web scraping* y la gestión de permisos en archivo local (`.env`).

La información reside ahora en tres **Scripts Ejecutables (`/scripts`)**:

### 1. Extracción Estática (DataDragon) ✓
El fichero `scripts/fetch_datadragon.py` se conecta vía `HTTP GET` al servicio estático *DataDragon* de League of Legends para buscar el parche actual del juego, reconfigurando y rellenando los campeones base de la aplicación.
* **Propósito**: Obtener Estructura Básica Rápida.

### 2. Mock Web Scraper (Winrates) ✓
El módulo `scripts/scraper_winrates.py` aborda la recolección de métricas estadísticas y *Matchups* no provistos directamente por Riot.
En caso de usarse en la vida real, parsea HTML utilizando `BeatifulSoup` para rellenar la matriz de porcentajes de victorias locales (que nuestro motor evalúa en *RunTime* con `base_winrate * 0.3 + counters * 0.7`).
* **Propósito**: Resolver el coste de proceso Big Data extrayendo de APIs de terceros (como OP.GG). 

### 3. Prueba de Concepto Riot API (PoC) ✓
El script `scripts/riot_api_poc.py` contiene todo el esqueleto nativo para **evaluar Partidas (Match-V5) e IDs de jugador (Account-V1)** con tu *Developer API Key* real.
Dentro detalla un recorrido lineal *pipeline*, imprimiendo por consola lo largo que es computar decenas de miles de eventos en League of Legends por segundo con sus cuotas restrictivas.

> [!CAUTION] 
> Asegúrate de **NO SUBIR** nunca tu fichero local `.env` a GitHub para que nadie se adueñe de tu API Key. Precisamente para eso hemos configurado `.env.example` dentro del código base.

## Verificación Recomendada
En tu memoria del TFG, bastará con citar ambas capas o ejecutar estos scripts por consola en orden cronológico (*Fetch -> Scrape*) adjuntando pantallas o logs de la ejecución como aval de que conoces las arquitecturas nativas.
