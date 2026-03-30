# Plan de Arquitectura Backend 2.0 (Fase Final)

Este plan aborda las tres mejoras de perfil "Senior" necesarias para culminar el ecosistema Backend del TFG y lograr la máxima puntuación académica en la memoria técnica del proyecto.

## User Review Required

> [!IMPORTANT]
> El sistema dará un inmenso salto cualitativo al tener en cuenta también a los aliados. Vamos a modificar el corazón del motor para que, si falta algo vital en tu equipo (ej. Daño Mágico), puntúe mejor a los campeones que suplen esa carencia. 
> Además, aseguraremos la robustez de la API. Revisa las reglas aliadas propuestas en la sección de Lógica antes de darme luz verde.

## Proposed Changes

### 1. Refactorización de Rendimiento (Caché en Memoria / Singleton)

#### [NEW] `data/data_loader.py`
Crearé una clase `DataLoader` aplicando el patrón **Singleton**. Esta clase leerá los JSONs del disco duro *solo la primera vez* que se instancie. Las siguientes 10.000 peticiones leerán directamente de la memoria RAM.
- **Ventaja en el TFG**: Explicar el salto de O(N) operaciones de disco a O(1) lecturas en memoria.

#### [MODIFY] `app.py` y `engine/inference.py`
- Eliminar las llamadas sueltas `open(...)`.
- Sustituir la carga de datos por instancias del nuevo `DataLoader`.

### 2. Sinergia Aliada (Ally Draft Logic)

#### [MODIFY] `engine/inference.py`
Se expandirá la Evaluación del Motor (añadiendo hechos tipo `ally_champion_tag`).
Añadiremos **2 nuevas reglas maestras**:
- **Regla Frontline (Falta Tanque)**: Si ya hay al menos un aliado, pero ninguno tiene el Tag `tank`, el motor deducirá el hecho `Recomendar Campeón: Tanque`.
- **Regla Daño Mágico (Exceso de AD)**: Si hay más de 2 aliados con `physical_damage` o `marksman` y ninguno con `magic_damage`, deducirá el hecho `Recomendar Campeón: Mago / AP`.

Y lo más importante, alteraremos la matemática de recomendación: 
Si a un `Candidato (Campeón)` le encaja un Tag demandado por el equipo aliado (ej. es Tanque cuando falta Tanque), **recibirá un +15% de Bonus a su Score final**, alzándolo por encima de los *counters* puros pero que arruinarían vuestra composición. *(Es decir, elegir al campeón ideal para la partida global, no solo para ganar su calle)*.

### 3. Integridad REST (Validaciones HTTP)

#### [MODIFY] `app.py`
La función `/api/recommend` recibirá un escudo defensivo:
- Respuesta `400 Bad Request` si los arrays superan los 5 campeones.
- Respuesta `400 Bad Request` si en un mismo equipo hay IDs repetidas (ej. 2 Teemos).
- Respuesta `400 Bad Request` si el PayLoad JSON viene roto.

### 4. Actualización del Historial

#### [MODIFY] `docs/historial_cambios.md`
Anotaremos de forma narrativa en un bloque "Fase 4: Perfeccionamiento Backend" estos tres cambios como broche de oro al desarrollo de Software.

## Open Questions

> [!TIP]
> De cara a las *Pruebas Unitarias* (testing), ¿Te gustaría que actualice también la suite automática `tests/test_inference.py` introduciendo nuevos tests que validen si un usuario malicioso o estas nuevas reglas aliadas reaccionan bien para no bajar la cobertura de tu proyecto al introducir lógica nueva? (Lo recomiendo encarecidamente para mantener el sobresaliente en código limpio).

## Verification Plan

### Test de Integridad Web
- Enviar una petición mediante código o Postman con fallos (6 campeones en vez de 5) y recibir código `HTTP 400` validando la protección.
- Ejecutar suite `pytest tests/` confirmando el correcto funcionamiento global.
