# Implementación de Extracción Manual y Gestión de Tags

Eliminar la capa de Web Scraping por completo debido a las restricciones técnicas de las webs modernas (Cloudflare, React) y establecer un flujo estable de *Data Entry* manual para el TFG. Además, estandarizar el uso de Tags de Riot y etiquetas personalizadas para el motor de inferencia.

## User Review Required

> [!IMPORTANT]
> Revisa este plan de acción. Básicamente voy a borrar el scraper y crearte un documento oficial que podrás listar como anexo en tu TFG con todas las "Etiquetas Personalizadas" (Tags) que entiende nuestro sistema experto. Así sabrás exactamente qué variables ponerle a cada nuevo campeón que añadas manualmente. ¿Te parece correcto proceder?

## Proposed Changes

### 1. Limpieza del Scraper (ETL Layer)

#### [DELETE] `c:\Users\osanchez\Documents\GitHub\sistema-experto-tfg-unir\scripts\scraper_winrates.py`
Borraremos este archivo ya que no vamos a utilizar el *mocking* de scraping. Todo el conocimiento y estadísticas de los campeones se inyectará "orgánicamente" por el autor (tú) como parte del conocimiento del dominio del sistema experto.

### 2. Actualización de Documentos

#### [MODIFY] `c:\Users\osanchez\Documents\GitHub\sistema-experto-tfg-unir\docs\walkthrough 2.md`
Actualizaré el texto para reflejar que la estrategia del TFG descarta el scraper intencionadamente por viabilidad técnica y abraza la actualización manual de la Base de Hechos vía `champions.json`.

#### [NEW] `c:\Users\osanchez\Documents\GitHub\sistema-experto-tfg-unir\docs\diccionario_etiquetas.md`
Crearé un nuevo documento que te servirá como "Chuleta" para rellenar manualmente tu `data/champions.json`. Contendrá:
- **Tags de Riot Oficiales**: `Fighter`, `Mage`, `Marksman`, etc.
- **Tags Custom del Motor**: `healing_self`, `healing_support`, `auto_attacker`, `tank` (este es de riot pero se procesa en el sistema), `magic_damage`.
- **Estructura Base Manual**: Un ejemplo de los campos (`base_winrate`, `matchups` y `tags`) para que copies y pegues directamente.

### 3. Ajustes en DataDragon

#### [MODIFY] `c:\Users\osanchez\Documents\GitHub\sistema-experto-tfg-unir\scripts\fetch_datadragon.py`
El script *ya preserva* los tags manuales y los winrates que pongas tú. Pero añadiré un comentario/salida en consola más explícito para avisarte cada vez que se ejecute y se baje el nuevo parche.

## Open Questions

> [!TIP]
> Actualmente las reglas previas evaluaban curaciones (healing), tanques, daño mágico y autoataques. ¿Te gustaría que en el diccionario de etiquetas añada alguna tag predictiva tuya más genérica que preveas implementar luego (por ejemplo, 'shielding' para escudos, 'assassin_combo' u otras)?

## Verification Plan

### Automated Tests
- Ejecutar `python scripts/fetch_datadragon.py` y comprobar que no pisa tu trabajo manual.

### Manual Verification
- Comprobar que tienes a tu disposición `docs/diccionario_etiquetas.md` listo para consultar cuando edites `champions.json`.
