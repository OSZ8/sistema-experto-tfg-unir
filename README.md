# Sistema Experto para la Toma de Decisiones Estratégicas en League of Legends

Este proyecto ha sido desarrollado como parte del **Trabajo de Fin de Grado (TFG)** en el **Grado en Ingeniería Informática** con mención en **Ingeniería del Software** de la **Universidad Internacional de La Rioja (UNIR)**.

## Descripción

El objetivo de este sistema experto es asistir a los jugadores de _League of Legends_ durante las fases críticas de selección de campeones (_draft_) e itemización previa a la partida. Utilizando un motor de inferencia basado en reglas y datos obtenidos de la **API de Riot Games**, el sistema recomienda las opciones con mayor probabilidad de victoria frente a la composición del equipo enemigo.

## Stack Tecnológico

- **Lenguaje:** Python
- **Framework Web:** Flask
- **Almacenamiento:** Archivos JSON (Base de hechos estática)
- **Lógica:** Motor de Inferencia (Sistemas Expertos)
- **Integración:** Riot Games API (vía `requests`)

## Estructura del Proyecto

De acuerdo con la metodología de ingeniería, el repositorio se organiza de la siguiente manera (provisionalmente):

- `/api`: Gestión de peticiones a la API de Riot.
- `/data`: Almacenamiento de datos estáticos de campeones y base de hechos (JSON).
- `/engine`: Núcleo del sistema experto (motor de inferencia y reglas).
- `/web`: Interfaz de usuario y rutas de Flask.
- `/tests`: Pruebas unitarias para validar las recomendaciones.
- `/docs`: Documentación técnica y diagramas.

## Licencia

Este proyecto se publica bajo la licencia abierta **MIT**. El código fuente es íntegramente de elaboración propia, cumpliendo con los requisitos académicos de la titulación.

## Autor

- **Oscar Sánchez García** - Estudiante del Grado en Ingeniería Informática, UNIR.

---

_Nota: Este repositorio es público y su enlace figura en la portada de la memoria del TFG según la normativa vigente._
