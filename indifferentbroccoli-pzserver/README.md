# Project Zomboid Build 42 - Dedicated Server (Docker/Podman)

Este repositorio contiene una configuración optimizada para correr un servidor dedicado de **Project Zomboid (B42)** en sistemas Linux utilizando Docker o Podman. Incluye herramientas automatizadas para resolver los problemas comunes de carga de mods en la nueva versión.

## 🚀 Características
- **Optimizado para Build 42:** Configuración adaptada a los nuevos requisitos del motor.
- **Auto-Fix de Mods:** Incluye un script (`pz_mod_fixer.py`) que resuelve automáticamente la sensibilidad a mayúsculas de Linux.
- **Fácil Configuración:** Gestión de variables a través de `.env`.
- **Playit.gg Integration:** Soporte opcional para túneles si no tienes IP pública o no puedes abrir puertos.

---

## 🛠️ Guía de Instalación (Paso a Paso)

Si vas a realizar una instalación desde cero, sigue estos pasos para asegurar que el servidor y los mods carguen correctamente:

### 1. Clonar el repositorio y preparar archivos
```bash
git clone <tu-repo-url>
cd indifferentbroccoli-pzserver
cp .env.example .env
```

### 2. Configurar el servidor
Edita el archivo `.env` para establecer el nombre del servidor, contraseñas y, lo más importante, la lista de mods.
- `MODS`: Lista de IDs de los mods separados por `;`.
- `WORKSHOP_ITEMS`: Lista de IDs numéricos de la Workshop separados por `;`.
*No es necesario agregar manualmente el prefijo `\\` aquí, el script lo hará por ti.*

### 3. Primer arranque (Descarga de archivos)
Lanza el servidor. La primera vez tardará varios minutos porque debe descargar el juego (~6GB) y todos los mods.
```bash
podman-compose up -d
```
Puedes monitorear el progreso con: `podman logs -f projectzomboid`. **Espera a que Steam termine todas las descargas antes de continuar.**

### 4. Reparación de Mods y Configuración
Una vez que los mods estén descargados, debes aplicar los parches de compatibilidad para Build 42 y Linux:
```bash
# Corregir sensibilidad a mayúsculas y formato de configuración
podman unshare python3 pz_mod_fixer.py

# (Opcional) Agregar puntos de spawn de Echo Creek
podman unshare python3 add_spawn_point.py
```

### 5. Reinicio Final
Para que el servidor reconozca los cambios en los archivos `.ini` y los nuevos enlaces simbólicos:
```bash
podman-compose restart projectzomboid
```

¡Listo! El servidor ya debería aceptar conexiones y los clientes verán los mods correctamente configurados.

---

## 📦 Guía de Mods (Build 42)

La Build 42 en Linux tiene dos desafíos principales que este repositorio soluciona:

### 1. El Formato de Doble Backslash (`\\`)
A diferencia de versiones anteriores, la Build 42 en servidores Linux requiere que los nombres de los mods en el archivo de configuración lleven una doble barra invertida (ej: `\\ModName`). Esto evita errores de "Mod Not Found" en el cliente.

### 2. Sensibilidad a Mayúsculas (Case Sensitivity)
Muchos mods son creados en Windows, donde `Media` y `media` son lo mismo. En Linux, el servidor fallará al cargar animaciones o scripts si el mod busca `animsets` pero la carpeta se llama `AnimSets`.

### 🔧 Cómo usar el Auto-Fixer
Hemos incluido un script llamado `pz_mod_fixer.py` que automatiza estas correcciones. El script es **idempotente** (puedes ejecutarlo tantas veces como quieras sin riesgo) y debe ejecutarse desde el **HOST** (tu máquina, fuera del contenedor).

```bash
# Ejecutar la reparación desde la carpeta raíz del proyecto
podman unshare python3 pz_mod_fixer.py

# Reiniciar para aplicar cambios
podman-compose restart projectzomboid
```

**¿Qué hace este script?**
- **Sincronización:** Escanea las carpetas de mods y crea enlaces simbólicos en minúsculas.
- **Limpieza de Huérfanos:** Si eliminas un mod, el script detecta y borra los enlaces simbólicos rotos para mantener el servidor limpio.
- **Gestión de Configuración:** Corrige automáticamente el archivo `servertest.ini`, asegurando que todos los mods tengan el formato `\\ModID` y eliminando caracteres invisibles que corrompen la carga.
- **Mantenimiento Dinámico:** Úsalo cada vez que añadas o quites mods para garantizar que la configuración sea siempre 100% compatible.

### ⚠️ Persistencia de Configuración
Por defecto, este contenedor tiene `GENERATE_SETTINGS=true`, lo que significa que el servidor puede sobreescribir tus cambios manuales en el archivo `.ini` al arrancar.
- El script `pz_mod_fixer.py` ya soluciona esto actualizando también tu archivo `.env`.
- **Para los Spawn Points:** Si notas que se borran al reiniciar, te recomendamos cambiar a `GENERATE_SETTINGS=false` en el `docker-compose.yml` una vez que tu configuración esté lista.

### 📍 Gestor de Spawn Points (`add_spawn_point.py`)
Muchos mods de mapa requieren agregar puntos de spawn manualmente. Hemos incluido un script para automatizar la adición de **Echo Creek, KY**:

```bash
# Agregar Echo Creek a la lista de regiones de spawn
podman unshare python3 add_spawn_point.py
```
*El script verifica automáticamente si el punto ya existe antes de agregarlo para evitar duplicados.*

---

## 🧠 ¿Por qué es necesario este setup?

Si has intentado montar un servidor de Project Zomboid B42 en Linux con muchos mods, habrás notado que:
1. **Los mods aparecen como [NotFound]:** Esto ocurre porque el cliente de PZ Build 42 espera que los mods publicados por servidores Linux tengan un prefijo `\\` para escapar correctamente los nombres en el protocolo de red.
2. **Errores de archivos no encontrados (Red Log):** La mayoría de los modders trabajan en Windows (sistema de archivos insensible a mayúsculas). Suben carpetas como `Media/AnimSets`. Linux busca `media/animsets` y, al no encontrar la coincidencia exacta de mayúsculas, el mod falla silenciosamente o con errores rojos.

### La solución de este repositorio
Este "template" no solo levanta el contenedor, sino que proporciona el **Fixer de Mayúsculas** más avanzado hasta la fecha para PZ:
- **Symlinking Recursivo:** En lugar de renombrar archivos (que rompería las act_ualizaciones de Steam), creamos pequeños enlaces simbólicos en minúsculas. Así, el juego encuentra el archivo tanto si lo busca en mayúsculas como en minúsculas.
- **Sanitización de Configuración:** El script limpia automáticamente tabulaciones, retrocesos y otros caracteres invisibles que suelen corromper los archivos `.ini` al copiar y pegar listas largas de mods.

---

## �️ Instalación y Uso Profesional

1. **Clonar y Configurar:**
   ```bash
   git clone <tu-repo>
   cd indifferentbroccoli-pzserver
   cp .env.example .env
   ```
2. **Editar .env:** Añade tus `MODS` y `WORKSHOP_ITEMS`. No te preocupes por el formato, pon los nombres tal cual.
3. **Lanzar y Reparar:**
   ```bash
   podman-compose up -d
   # Espera a que los logs digan que Steam terminó de descargar todo
   podman unshare python3 pz_mod_fixer.py
   podman-compose restart projectzomboid
   ```

---

## 📂 Estructura del Proyecto
- `pz_mod_fixer.py`: Script de mantenimiento de mods (ejecutar desde el host).
- `docker-compose.yml`: Define los servicios de Zomboid y el túnel Playit.gg.
- `server-data/`: Directorio persistente para la configuración y el mundo.
- `server-files/`: Directorio donde vive el juego y los mods descargados.

---

## 🤝 Créditos y Contribuciones
Este proyecto utiliza la imagen base de [indifferentbroccoli](https://github.com/indifferentbroccoli/projectzomboid-server-docker). Las mejoras de automatización y el script de reparación de mods han sido desarrollados para garantizar la estabilidad en la Build 42.

¡Si encuentras un bug o tienes una mejora, abre un Issue o un PR!
