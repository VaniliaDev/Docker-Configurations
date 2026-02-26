# Reporte de Errores - Project Zomboid (Nueva Ejecución)

He vuelto a analizar el archivo completo `console.txt` tras la última ejecución del servidor. **El error crítico sigue siendo exactamente el mismo**, pero a continuación detallo de nuevo todos los problemas encontrados:

## 💥 1. Error Crítico Principal (Causa del Crasheo)
El juego crashea en la pantalla de carga (probablemente dando la pantalla de error en rojo y negro al final de la carga) debido a este error fatal interactuando con el diccionario del mundo guardado:

```text
zombie.world.WorldDictionaryException: Missing dictionary string on client: NC_HandCraftPanelLayout
```

**Explicación:** 
El servidor está intentando inicializar el mundo (`WorldDictionary`), pero detecta que falta una clave de registro llamada `NC_HandCraftPanelLayout`. Este código `NC_` es típico del mod **"Neat_Crafting"** o de alguna extensión de menús de crafteo.
Esto ocurre habitualmente si intentas cargar una partida antigua o ya generada donde antes sí que estaba presente o funcionaba correctamente ese mod, pero ahora está corrupto, desactualizado o se ha modificado la lista de mods provocando desincronización de sus recetas o componentes.

**Solución sugerida:**
- **Si es un mundo nuevo / de pruebas:** La ruta más rápida es **borrar la partida actual** del servidor para que se reinicialice el mundo por completo y regenere los diccionarios limpios sin esa dependencia huérfana.
- **Si es un mundo que quieres conservar:** Deberás asegurarte de que el mod "Neat_Crafting" o "NeatUI_Framework" está exactamente en la misma versión con la que se creó el servidor, o intentar cargar el mundo usando un mod que limpie diccionarios oxidados (como el mod *ErrorMagnifier* o borrar temporalmente los items corruptos del save).

## ⚠️ 2. Advertencias Importantes Concurrentes

Aparte del crasheo principal, hay otros errores importantes que debes tener en cuenta, ya que afectarán a la jugabilidad:

### ❌ Error Numérico de Mods
```text
ERROR: mods isn't a valid workshop item ID
```
Aparece repetido **más de 150 veces** al iniciar la conexión. Esto significa que hay un problema en el archivo de configuración (`server.ini` o el `.env`). Donde el servidor espera una lista de números (los IDs de Workshop), parece que está recibiendo o leyendo literalmente la palabra `"mods"` o `"WorkshopItems=mods"`. Revisa la variable que carga los IDs de Workshop en el entorno.

### ❌ Animaciones Erróneas o Perdidas
Hay cientos de advertencias relacionadas con animaciones faltantes correspondientes al modelo "bob" y a mods como:
- `miumau_ded`, `kitty_startled` etc. (Mod de gatos o mascotas como DynamixKitty)
- `sapph_cookingwok`, `sapph_cakewish`, `bobsapph_grind_meatgrinder` (Mod Sapphire's Heaters / Sapph's Cooking)
- `bob_yoga_...`, `bob_dancing...` (Mods de los emotes de personaje, baile, True Actions)

Todo esto significa que alguno de los mods de animaciones (`True Actions`, `Sapph's Cooking`, etc.) que estás usando o bien no está encontrando el framework de animación requerido, o está mal empaquetado y no cargan sus texturas/animaciones nativas.

### ❌ Archivos Lua que Fallan al Cargar
Varios sub-módulos del juego indican que no han podido realizarse o han "estallado", muy probablemente por interacciones no compatibles entre los mods y la build actual (ej. mod de Campamentos):

```text
require("ISUI/ISInventoryPaneContextMenu") failed
require("Camping/CCampfireSystem") failed
require("BuildingObjects/ISAnimalPickMateCursor") failed
```

### ❌ Variables de Entorno no Establecidas
Hay un bloque enorme advirtiendo que faltan decenas de configuraciones básicas del servidor (`MISSING in SettingsTable:`), tales como:
- `PVPLogToolChat`, `Mods`, `WorkshopItems`, `Map`, `SpawnPoint`, `AntiCheatSafety`, `NightLength`.
Esto apoya la teoría de que la migración o inyección de variables de tu archivo `.env` hacia las configuraciones del juego no se está transmitiendo correctamente o el servidor no encuentra el archivo `.ini` clásico generándolo de esta forma con configuraciones faltantes y en blanco.
