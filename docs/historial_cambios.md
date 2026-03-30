# Historial de Cambios y Progreso del Desarrollo (TFG)

Este documento centraliza todos los hitos, decisiones arquitectónicas y módulos desarrollados para el Sistema Experto de League of Legends. Servirá como bitácora y base teórica para la redacción de la memoria del Trabajo de Fin de Grado.

---

## 📅 Fase 0: Arquitectura Base Inicial
**Estado:** Completado
- **Backend**: Despliegue de Flask (`app.py`) y creación de Endpoints REST (`/api/recommend`).
- **Frontend**: Prototipo estático de UI/UX con Glassmorphism (`index.html`, `styles.css`) implementando selectores clásicos.
- **Base de Hechos (DB)**: Almacenamiento JSON para el diccionario de campeones (`champions.json`) e ítems (`items.json`).
- **Motor de Inferencia Inicial**: Construcción de `engine/knowledge_base.py` (Clases `Engine`, `Fact`, `Rule`) y el núcleo en `engine/inference.py` con 4 reglas básicas (Curaciones, Tanques, Ataques Básicos y Magia).

---

## 📅 Fase 1: Arquitectura de Datos (Data Entry & ETL)
**Estado:** Completado
- **Aproximación Teórica**: Se realizó una investigación sobre Web Scraping (U.GG) y se construyó una Prueba de Concepto (`riot_api_poc.py`). Se determinó que para los *matchups* específicos, el coste técnico de Big Data / Anti-Bots (Cloudflare) excede la viabilidad del TFG.
- **Decisión Arquitectónica**: Implementación de un modelo Mixto:
  -  Extracción estática automatizada de roles y campeones mediante la conectividad a la API oficial **Riot DataDragon** (`fetch_datadragon.py`).
  -  Inyección manual por parte del Experto (Data Entry Humano) de `matchups`, `winrates` y `tags`.
- **Estandarización de Conocimiento**: Creación de `docs/diccionario_etiquetas.md` para unificar cómo el motor debe referirse a reglas personalizadas (`healing_self`, `magic_damage`, etc.).

---

## 📅 Fase 2: Expansión de la Base de Conocimiento (Nuevas Reglas)
**Estado:** Completado
- Se amplió la capacidad deductiva del sistema inyectando en `data/items.json`:
  1. *Colmillo de Serpiente* (Contraescudos).
  2. *Botas de Mercurio* (Tenacidad Anti-Control).
  3. *Reloj de Arena de Zhonya* (Supervivencia y Anti-Asesinos).
- Se crearon 3 **Nuevas Reglas** en el Forward Chaining del `inference.py` que detonan al detectar los tags `shielding`, `cc_heavy`, `assassin`.

---

## 📅 Fase 3: Validación Académica (Testing Automático)
**Estado:** Completado
- **Bug Fix Crítico**: Refactorizada la clase `Engine` en el motor base. Anteriormente empleaba un `Set()` (conjuntos únicos) para almacenar los hechos (Facts), lo que provocaba que la acumulación de múltiples campeones con el mismo rol (p. ej. Dos tanques) fuesen colapsados en un único hecho, bloqueando contadores condicionales. 
- **Suite de Pruebas**: Implantación del marco `pytest` para testing automático.
- **Scripts de Validación**: Creación de `tests/test_inference.py`. Usando metodologías "Mock" inyectamos hechos ficticios desconectados de la base de datos real para evaluar la resiliencia algorítmica. 
- **Cobertura**: 8 de 8 tests pasados exitosamente analizando cruces y flujos lógicos.

---

## 📅 Fase 4: Perfeccionamiento Backend (Validaciones, Caché y Sinergia Aliada)
**Estado:** Completado
- **Caché Singleton**: Creada clase estática en `data/data_loader.py`. Se han neutralizado las lecturas consecutivas de archivos de disco (`O(N)`) a la memoria RAM (`O(1)`), acelerando el rendimiento masivo del TFG.
- **Validaciones REST API**: Fortificación de `app.py`. Ahora la ruta `/api/recommend` cuenta con manejo de errores `400 Bad Request` validando que la estructura JSON esté intacta, que el máximo de campeones no exceda de 5, y que no existan IDs duplicadas en un Draft.
- **Lógica de Draft Completo (Aliados)**:
  - Modificado el motor de inferencia clásico para evaluar un nuevo tipo de hecho (`ally_champion_tag`).
  - Añadidas las Reglas Reversas: **Regla Frontline** (Detecta si a tu equipo le falta un Tanque) y **Regla Daño Mágico** (Detecta si todo tu equipo es Daño Físico).
  - Implementado el multiplicador algorítmico Heurístico: Si un campeón suple la necesidad de la regla reversa, adquiere un `+15%` de puntuación extra, haciendo que el Sistema Experto no solo recomiende a quién le hace counter al rival, sino a qué campeón balancea tu equipo.

---

## 📅 Fase 5: Rediseño Premium de Interfaz Web (UI/UX)
**Estado:** Completado
- **Arquitectura de Interfaz 5v5**: Se sustituyó el selector obsoleto HTML estático (`<select>`) por un diseño de "Arena de Draft". 
- **Integración DataDragon (CDN)**: La aplicación web extrae renderizados de escudos (Assets PNG) directamente desde la API estática de parche remoto (`14.6.1`) inyectándolos en un Roster fotográfico de campeones con barra de búsqueda para la selección.
- **Glassmorphism y Estilo**: Migración de `styles.css` a estándares WebGL / e-sports UI usando gradientes dorados (`--gold`), contornos `hextech` (`--cyan`), animaciones de Hover y un modelo responsivo. Todo el output del Sistema Experto (el informe devuelto por Python) aparece con animaciones de opacidad (fade-in) e inyección de miniaturas.

---

*(Este documento se irá actualizando de forma continua cada vez que implementemos nuevos módulos o correcciones).*
