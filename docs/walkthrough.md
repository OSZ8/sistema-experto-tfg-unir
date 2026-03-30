# Resumen de Implementación
He completado la integración del prototipo del Sistema Experto para el proceso de *draft* e *itemización* de **League of Legends** como parte técnica de tu TFG. 

## Cambios Realizados

> [!NOTE] 
> Todas las referencias relativas a la base de datos *SQLite* fueron omitidas por recomendación inicial. En su lugar se ha completado un sistema de inferencias estático y modular en base a diccionarios de hechos en repositorios locales (`data/champions.json` y `data/items.json`).

1. **Diseño de Interfaz Premium (Glassmorphism + Hextech)**: 
   - Estilizado de la aplicación bajo un formato inmersivo y reactivo para una mejor experiencia de usuario, utilizando tecnología web (`HTML`, `CSS`,`JS`) con paletas consistentes con *League of Legends*.
   
2. **Setup de Backend (Flask)**:
   - Configuración inicial y creación del punto de enlace (`/api/recommend`) que recibe selecciones en el draft.
   - Creación de un sistema mock bajo `api/riot.py` que permite una integración limpia a futuro con *DataDragon* o la *Riot API*.

3. **Arquitectura del Sistema Experto**: 
   - Creación de un motor basado en reglas (`Forward Chaining`).
   - El sistema detecta "etiquetas" del equipo rival, genera hechos internos, e interacciona con un conjunto de reglas (Ej. Si el contrario tiene Curación -> Recomendar Cortacuras).

4. **Validaciones en Win Rate (Porcentaje de Victoria)**:
   - Se ha añadido la lógica avanzada por la cual el motor pesa el porcentaje de victoria global con las métricas de enfrentamientos directos (*Matchups*).

## Instrucciones de Validación

> [!TIP]
> Prueba correr la app manualmente para interactuar con ella:
> ```bash
> python app.py
> ```
> O navega a `http://127.0.0.1:5000` si ya se encuentra en ejecución en tu terminal.

- Abre el sitio web e introduce **Campeones** en la lista enemiga.
- **Caso de Uso Sugerido:** Selecciona a *Malphite* y a *Soraka*.
- Podrás observar cómo **Vayne** es recomendada por contar con la puntuación de _counters_ sumada al WIN RATE.
- Observarás cómo aparecerán los **Items Cortacuras** por la curación de *Soraka*.

---

¡Disfruta desarrollando este TFG! El diseño arquitectónico está consolidado para que sigas añadiendo reglas personalizadas en `engine/inference.py`.
