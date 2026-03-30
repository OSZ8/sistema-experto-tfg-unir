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

## 📅 Fase 6: Expansión de Base de Conocimientos y Despliegue DevOps
**Estado:** Completado
- **Carga Masiva de Hechos (Riot DataDragon API)**: Ejecutado el pipeline automatizado `fetch_datadragon.py` extrayendo la información oficial del parche remoto para elevar la Base de Datos a la increíble cifra de **172 campeones al completo** presentes en el Título Oficial. El script se fusionó conservando la lógica heurística (`matchups`, `tank`, `shielding` custom tags) de la base original, posibilitando una combinatoria de cientos de miles de cruces de fase de selección.
- **Isomorfismo de Contenedores (Docker)**: Creados `Dockerfile` y `.dockerignore`. Se ha implementado un flujo de ejecución de Grado de Producción aislando el framework Flask a través del servidor WSGI `Gunicorn` (multihilo). El proyecto es ahora oficialmente un artefacto DevOps "Deploy-Ready" (preparado para ser elevado a Google Cloud, AWS o plataformas equivalentes sin configuración adicional y respetando normas de Ciberseguridad con permisos capados `useradd`). Se añadió `gunicorn` al `requirements.txt`.

## 📅 Fase 7: Algoritmo de Cohesión Espacial (Anti-Solapamiento de Roles)
**Estado:** Completado
- **Cálculo de Huecos Libres de Draft**: Detectado e implementado un sistema correctivo crucial en `inference.py`. El Sistema Experto original sufría de sobresaturación estadística (recomendaba los 5 mejores campeones en bruto, resultando en casos irreales como "3 Toplaners y 2 Junglas").
- **Exclusión Mutua**: El motor iterativo ahora rastrea qué "Roles" han sido ya cubiertos en las cartas de tu Composición Aliada. Acto seguido elimina de raíz todas las recomendaciones matemáticas que pertenezcan a ese mismo Rol para evitar dobles picks.
- **Multiversatilidad**: El output final garantiza retornar un Top 5 donde existe siempre **1 Campeón Óptimo distinto por cada Rol restante**, asegurándole al usuario (sea Support, Medio o ADC) que siempre tendrá un "Mejor Pick" específico para su calle basándose en pura Inteligencia Artificial aplicada.

## 📅 Fase 8: Mapeo de Posiciones Meta (Top, Jungla, Medio...) y Agrupación Visual
**Estado:** Completado
- **Reestructuración de Datos (Positions vs. Classes)**: Creado y ejecutado `assign_positions.py` reconfigurando la base de 172 campeones. Ahora la IA discierne entre la *Clase* de Riot (Ej: Mago, Asesino) y la *Posición* en el mapa donde se juega realmente ese campeón (Ej: Ahri -> Medio, Akshan -> Top/Medio).
- **Asignación Semántica de Draft UI**: Los 5 slots de selección aliados han sido titulados (Top, Jungla, Medio, ADC, Apoyo). El motor asume ahora tácitamente el rol que le falte a la composición aliada en base a qué casillas se dejen vacías, permitiendo sobreescribir picks Flexibles (Ej. Vladimir) simplemente arrastrándolos a la casilla de "Medio" o "Top".
- **Agrupación Modular (DOM)**: El algoritmo heurístico `evaluate_draft` ya no escupe un Top 5 genérico absoluto, sino un Array Anidado (Dict) que agrupa estructuralmente los mejores campeones (Top 3) exclusivos para cada Rol vacante. El UI renderiza esto con nuevas insignias, jerarquía y etiquetas secundarias, multiplicando las opciones estratégicas sin saturar la pantalla.

## 📅 Fase 9: Transparencia "Explainable AI" (XAI) y Modo Debugger
**Estado:** Completado
- **XAI Implementado (`engine/knowledge_base.py`)**: Alterada profundamente la estructura de las reglas lógicas (Forward Chaining). Ahora la clase `Fact` guarda el parámetro `source` de "Quién" generó la regla. `Engine.run` ahora interpola dinámicamente dichos orígenes en las explicaciones.
- **Traceabilidad**: Ya no dice "Comprar Armadura porque hay atacantes físicos". Ahora indica "Alerta Regla Anti-Ataques Básicos disparada por presencia de Tiradores/ADCs: [Xayah, Vayne]." Nivel académico Matrícula TFG.
- **Terminal de Debug TFG**: Implementado un botón "Ver Tripas Matemáticas (Debug)" al pie de página que despliega una consola Hextécnica de log de terminal. Imprime en formato JSON raw la puntuación algorítmica y los Matchups sin procesar para enseñarlo al Tribunal.

---

*(Este documento se irá actualizando de forma continua cada vez que implementemos nuevos módulos o correcciones).*
