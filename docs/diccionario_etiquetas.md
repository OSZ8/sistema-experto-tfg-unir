# Diccionario de Etiquetas (Tags) para el Sistema Experto

Para poder inferir conclusiones avanzadas, nuestro motor de inferencia situado en `engine/inference.py` se apoya en etiquetas (*tags*) semánticas que deben integrarse manualmente en la Base de Hechos (`data/champions.json`). 

Este enfoque de **Data Entry Manual** permite inyectar el conocimiento humano del juego (El "Experto") directamente al motor de reglas. 

## 1. Etiquetas Nativas de Riot Games (DataDragon)
Estas clases principales son importadas automáticamente al correr `scripts/fetch_datadragon.py`:

- `fighter` (Luchador)
- `tank` (Tanque) - *Nota: Evalada activamente por nuestro motor para recomendar Pen. Armadura.*
- `mage` (Mago)
- `assassin` (Asesino)
- `marksman` (Tirador)
- `support` (Apoyo)

## 2. Etiquetas Personalizadas (Custom Tags) del Motor de Inferencia
Estas son las etiquetas que **debes** añadir a mano en la propiedad `tags` de los campeones del JSON para que funcionen las 4 reglas implementadas actualmente:

| Custom Tag | Regla que lo Evalúa | ¿Qué significa en el Juego? | Ejemplo de Campeones a los que ponérselo |
| :--- | :--- | :--- | :--- |
| `healing_self` | **Anti-Curaciones** | El campeón cuenta con gran curación sobre sí mismo (Robo de vida, pasivas). | Aatrox, Dr. Mundo, Vladimir, Briar |
| `healing_support`| **Anti-Curaciones** | El campeón ejerce curación constante o masiva sobre sus aliados. | Soraka, Yuumi, Sona, Nami |
| `auto_attacker` | **Anti-Ataques Básicos** | Gran parte de su impacto DPS viene de auto-ataques (dependen de su velocidad de ataque o crítico). | Tryndamere, Master Yi, Jinx, Vayne |
| `magic_damage` | **Resistencia Mágica** | Producen daño mágico masivo u omnipresente. (A veces un Tank genera gran daño mágico compensatorio) | Sylas, Malphite, Karthus, Gwen |

> *Nota rápida:* Fíjate que el Tag nativo de "tank" y el Tag nativo de "marksman" ya se están usando como disparador para Anti-Tanque y Anti-AA. 

## 3. Ejemplo de Placeholder para añadir un Campeón en `champions.json`
Si quieres añadir o afinar un campeón a través de la DB manual, asegúrate de mantener esta estructura:

```json
{
  "NombreSinEspacios": {
    "id": "NombreSinEspacios",
    "name": "Nombre Real Formateado",
    "role": "Top/Mid/Jungle/ADC/Support",
    "tags": [
      "fighter", 
      "healing_self"
    ],
    "base_winrate": 50.5,
    "matchups": {
      "NombreDeUnCounter": 45.0,
      "NombreDeOtroCounter": 46.5
    }
  }
}
```
*Si un campeón no está todavía en el diccionario `matchups`, su peso se basará al 100% en el `base_winrate` que hayas especificado.*
