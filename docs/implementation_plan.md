# Plan de Implementación de Datos (ETL)

Para lograr el nivel académico requerido en el TFG y demostrar conocimientos de Integración de Sistemas y Análisis de Datos (Big Data), el proyecto transicionará de utilizar datos estáticos "hardcodeados" a generarlos a través de diferentes scripts de recolección (ETL - Extraer, Transformar y Cargar).

## User Review Required

> [!IMPORTANT]
> Vamos a incorporar nuevos módulos que necesitarán acceso a internet (llamadas HTTP) y dependencias adicionales en Python para extraer datos tanto estructurales como estadísticos. Revisa si la estructura a continuación cumple con lo que presentarás en la memoria del TFG.

## Proposed Changes

### 1. Dependencias del Sistema

#### [MODIFY] `requirements.txt`
Se añadirán dependencias como `beautifulsoup4` (para web scraping) y `python-dotenv` (para gestionar de manera segura la *API Key* de Riot Games sin subirla al código público de GitHub).

### 2. Módulo de Extracción de Datos Base (DataDragon)

#### [NEW] `scripts/fetch_datadragon.py`
Este script se conectará al servicio gratuito y público **DataDragon** de Riot Games.
- Obtendrá la última versión del parche activo del juego.
- Descargará el diccionario completo de campeones (ID, Nombre, Tags de RolBase).
- Descargará el catálogo de objetos (ID, Nombre, Descripción).
- Inyectará la estructura base en el repositorio de nuestro sistema experto `data/champions.json` y `data/items.json`.

### 3. Módulo de Estadísticas (Web Scraper)

#### [NEW] `scripts/scraper_winrates.py`
Dado que los datos de porcentaje de victoria (*winrate*) y enfrentamientos (*matchups*) no se ofrecen procesados nativamente por Riot, este script empleará `BeautifulSoup` para extraer de manera ética las matrices de counters desde una web pública de análisis de League of Legends (ej. U.GG). 
- Cruzará la información scrapeada con el `champions.json` generado por *DataDragon*, enriqueciendo la base de hechos para el motor de inferencia.

### 4. Prototipo Académico (Riot API - Match V5)

#### [NEW] `scripts/riot_api_poc.py`
Para documentarlo magistralmente en tu memoria como "prueba de concepto" (Proof of Concept - PoC), desarrollaremos este script que demuestra y comenta el código exacto necesario para conseguir este cálculo 100% nativo.
- Se configurará para usar tu **Riot API Key**.
- Incluirá las llamadas a los endpoints:
  - `account-v1` para conseguir las identificaciones de un jugador experto.
  - `match-v5` para obtener los IDs de sus últimas 10-20 partidas.
  - `match-v5` (Details) para inspeccionar quién ganó el enfrentamiento en top lane (ej. *Malphite* contra *Tryndamere*) calculando manualmente el _winrate_.
- Este archivo dejará constancia comentada de por qué se descarta esta vía en producción (Limitaciones de peticiones por segundo, latencia O(N), costes de computación, arquitectura Big Data) para enriquecer la argumentación científica del TFG.

---

## Open Questions

> [!WARNING]
> ¿Estás de acuerdo con añadir las librerías `beautifulsoup4` y `python-dotenv` al `requirements.txt`?
> Para la prueba de concepto académica (`riot_api_poc.py`), dejaré el esqueleto preparado con marcadores como `TU_API_KEY_AQUI` para que después puedas simplemente poner una *Developer Key* de Riot temporal, ejecutarlo y hacer capturas de consola para tu memoria. ¿Te parece bien este planteamiento de prueba de concepto (PoC)?

## Verification Plan

### Automated Tests
- Ejecutar `python scripts/fetch_datadragon.py` y comprobar que inyecta estructura JSON real del servidor actual de League of Legends.
- Ejecutar el *scraper* y verificar que se inyectan los datos de porcentaje de victoria real.

### Manual Verification
- Comprobar que en el Frontend (`index.html`) los campeones tienen nombre y datos procedentes de las extracciones programadas.
