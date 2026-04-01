# 📜 Contexto de Proyecto para Nueva Instancia de IA (Handover TFG)

> **📝 INSTRUCCIÓN CRÍTICA PARA EL NUEVO AGENTE DE IA:**
> Si estás leyendo esto, el usuario ha cambiado de PC o ha iniciado una nueva sesión contigo tras perder el historial de chat anterior. Tu tarea primordial es **asistir en la finalización de este Trabajo de Fin de Grado (TFG)**. Este archivo te pone exactamente al día de la arquitectura del código, las reglas estrictas de formato del usuario y el estado de desarrollo actual. No propongas reestructuraciones completas: el core lógico ya es estable y está blindado por tests.

---

## 🎯 1. Objetivo del Sistema
Es un **Sistema Experto Basado en Reglas** (Forward Chaining) aplicado a **League of Legends** (Fase de selección o "Draft" 5v5). Extraemos metadatos oficiales de campeones y usamos heurística para:
1. Recomendar campeones aliados en función del rol que falta.
2. Sugerir objetos clave (Itemización) como contramedidas frente a amenazas rivales.
3. Explicar justificadamente por qué matemáticamente se recomiendan (Explainable AI o XAI).

---

## 🏗️ 2. Arquitectura y Módulos Implementados (Lo ya hecho)

El sistema se estructura bajo un paradigma "Desacoplado" (Frontend Web Vanilla + Backend en Python Flask). Tras 10 Fases de desarrollo, el código actual incluye:

### A. Backend Lógico (`/engine/` y `app.py`)
- **Motor de Inferencia Artesanal** (`knowledge_base.py`, `inference.py`): Implementa una jerarquía estricta de Reglas lógicas (ej. *Regla Anti-Tanques: Si se detectan 2 tanques rivales -> Añade "Penetración de Armadura" a las recomendaciones*).
- **Inteligencia Artificial Explicable (XAI)**: Las reglas están configuradas para trazar qué campeón exacto provocó la alerta matemática. Interpola el nombre crudo de la amenaza en el informe (ej. *"Regla de Anti-Curaciones disparada por: [Soraka]"*).
- **Carga de Datos (ETL)** (`data_loader.py`): Parsea `champions.json` e `items.json`. En su día ejecutamos un script hacia Riot DataDragon para dumpear los **172 campeones** con sus roles (Tags y Posición en el mapa).

### B. Frontend e Interfaz Web (`/templates/` y `/static/`)
- Diseño inspirado en e-sports (estándar *Glassmorphism*, paleta dorada/oscura).
- **Draft de 5v5 Semántico**: El usuario hace click en casillas (Top, Jungla, Medio...) y selecciona desde una grilla qué campeones ya están pillados.
- **Renderizado Anidado Multiversátil**: El backend ya no devuelve un top general y caótico, devuelve un `<dict>` anidando el "Top 3 de mejores picks" *para cada posición libre aislada*.
- **Modo Debug (Terminal XAI)**: Existe un botón `Ver Registro (Debug)` que despliega un log raw de terminal con las métricas y multiplicadores lógicos que toma el algoritmo de python para demostrarlo académicamente (Requisito fundamental del TFG).
- **Resolución CSS Modular (Flexbox)**: Se incrementó la dimensión de los contenedores (`.draft-slot`) a rectangular (`height: 135px`) en `styles.css` eliminando colisiones e intercepados por usar excesivos *position: absolute*. 

### C. QA y Pipeline
- Todo el motor está protegido mediante **11 tests unitarios automáticos** usando `pytest` en la carpeta `/tests/`. Si haces cambios al core, ejecuta `python -m pytest tests/test_inference.py`.

### 🧹 D. REGLA ESTRICTA DE ESTILO DEL USUARIO ("Clean Code")
El usuario detesta el código que "parece generado automáticamente por IA". 
- **NO DEBES** escribir comentarios estilo tutorial (`# Aquí hacemos una comprobación para ver si el array tiene datos...`). 
- **SÍ DEBES** escribir comentarios en forma imperativa minimalista y de 3ª persona (`# Valida array.`). 
- **PROHIBIDOS LOS EMOJIS**: Se eliminaron todos los emojis internos (`⚠️`, `💎`, etc.) de las variables Python, JS y elementos HTML. La presentación debe lucir puramente académica y rigurosa de Ingeniería de Software.

---

## 🚀 3. Estado Actual y Qué Falta por Hacer (Roadmap)

El usuario te indicará en qué quiere enfocarse a continuación. Las ramas lógicas que dejamos abiertas para el final fueron:

### 1. Integrar API Oficial (Riot Games API) ⏳
- **Contexto**: Tenemos un esqueleto en `api/riot.py` inicializado con una función cruda.
- **Acción Pendiente**: Actualmente dependemos del diccionario JSON empaquetado y estático. Se debe integrar conectividad `GET` vía requests hacia los servidores de Riot Games (con clave de desarrollador) para recolectar, procesar u obtener datos paramétricos vitales (como Winrates actualizados) y cruzarlos matemáticamente en `inference.py`.

### 2. Mejoras de Feedback Visual en FrontEnd
- Añadir pulido de interfaz para las partes que no quedaron listas. Por ejemplo, sistemas de 'Toasts' para reemplazar las feas notificaciones nativas `alert(...)` de Error de Javascript y mejorar la escalabilidad responsive.

### 3. Asistencia Teórica y Memoria
- El usuario mencionó que quiere centrarse en pulir la herramienta base para después escribir la **Memoria del TFG**. Podrías necesitar generar pseudocódigo formal de los algoritmos construidos, y documentar la carga O(N) de los tensores.

---
> **Prompt Interno**: Entendido. Revisa las preguntas del usuario tras leer el contexto para continuar desde este punto.
