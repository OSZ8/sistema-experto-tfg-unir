# Implementación de Nuevas Reglas y Testing (Pytest)

## Resumen del Objetivo
Para dar el salto definitivo al "Nivel TFG de Ingeniería del Software", vamos a ampliar el número de reglas lógicas del motor de inferencia (añadiendo Anti-Escudos, Anti-CC y Supervivencia ante Asesinos). Inmediatamente después, crearemos una *suite* de pruebas de automatización con `pytest` para certificar matemáticamente que el motor de inferencia Forward-Chaining no tiene fallos al deducir resultados.

## User Review Required

> [!IMPORTANT]
> A continuación se detalla qué reglas vamos a añadir y cómo van a interactuar. También propondremos la instalación de `pytest` (una dependencia de Python muy estandarizada en la industria). Revisa si las nuevas lógicas que propongo te encajan para el juego.

## Proposed Changes

### 1. Base de Hechos - Expansión de Items y Tags

#### [MODIFY] `data/items.json`
Dado que crearemos reglas nuevas, necesitamos que el sistema pueda recomendar los objetos correctos. Añadiremos:
- **Colmillo de Serpiente** (Tag: `anti_shield`)
- **Reloj de Arena de Zhonya / Ángel Guardián** (Tag: `anti_assassin` / `survival`)
- **Botas de Mercurio / Fajín** (Tag: `tenacity` / `anti_cc`)

#### [MODIFY] `docs/diccionario_etiquetas.md`
Añadiremos los tags correspondientes que dispararán estas reglas: `shielding`, `cc_heavy`, `assassin` (oficial Riot), a tu chuleta de documentación.

### 2. Capa de Lógica - Ampliación del Motor

#### [MODIFY] `engine/inference.py`
Se inyectarán 3 reglas lógicas nuevas en el motor:
- **Regla Anti-Escudos**: `Si (enemigo.tag == 'shielding') -> recomendar('anti_shield')`
- **Regla Tenacidad (Control de Adversario)**: `Si (enemigos.count('cc_heavy') >= 2) -> recomendar('tenacity')`
- **Regla Supervivencia (Asesinos)**: `Si (enemigos.count('assassin') >= 2) -> recomendar('survival')`

### 3. Capa de Pruebas Unitarias (Tests Automáticos)

#### [MODIFY] `requirements.txt`
Añadiremos `pytest`, el estándar de la industria en Python para testing.

#### [NEW] `tests/test_inference.py`
Crearé tu primer script de testing automatizado de caja blanca. Instanciará el `Engine` de forma aislada, inyectará hechos ficticios de campeones (por ejemplo, "Equipo con 3 Asesinos") y hará un `assert` asumiendo que el resultado tiene obligatoriamente el tag `survival`. Probará todas las reglas.

## Open Questions

> [!TIP]
> Dado que los *Tests Unitarios* se correrán desde consola (poniendo `pytest tests/test_inference.py`), ¿quieres que configure estos tests para que usen directamente tu archivo `champions.json` real de la carpeta `/data/`, o prefieres que los tests operen sobre unos datos 100% aisaldos y falsos (mockeados en memoria) para demostrar mayor madurez arquitectónica? (Yo recomiendo hacer *mocking* aislado).

## Verification Plan

### Automated Tests
- Correr en consola `python -m pytest tests/` y ver que hay `X passed` cubriendo todas las ramas de decisión vitales de las 7 reglas (las 4 iniciales + 3 nuevas).
