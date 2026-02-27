
import os
import re

# Ruta al archivo de spawn regions (relativa al host)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPAWN_FILE = os.path.join(BASE_DIR, 'server-data/Server/servertest_spawnregions.lua')

# Configuración del nuevo punto de spawn
NEW_SPAWN_NAME = "Echo Creek, KY"
NEW_SPAWN_LINE = '		{ name = "Echo Creek, KY", file = "media/maps/Echo Creek, KY/spawnpoints.lua" },'

def update_spawn_regions():
    if not os.path.exists(SPAWN_FILE):
        print(f"Error: No se encontró el archivo en {SPAWN_FILE}")
        return

    with open(SPAWN_FILE, 'r') as f:
        content = f.read()

    # Comprobar si ya existe el nombre en el archivo (usando regex para ignorar espacios/comillas simples/dobles)
    # Buscamos 'name = "Echo Creek, KY"' o 'name = \'Echo Creek, KY\''
    exists = re.search(r'name\s*=\s*["\']' + re.escape(NEW_SPAWN_NAME) + r'["\']', content)

    if exists:
        print(f"El punto de spawn '{NEW_SPAWN_NAME}' ya existe en el archivo. No se realizaron cambios.")
        return

    # Si no existe, buscamos el final de la lista (antes del último '}')
    # Buscamos el último '}' antes de 'end'
    lines = content.splitlines()
    new_lines = []
    inserted = False

    for i in range(len(lines)):
        # Si encontramos el cierre de la tabla principal '}' antes del final de la función
        if '}' in lines[i] and not inserted and i > 1:
            # Verificamos si la línea anterior tiene contenido de tabla para insertar antes del cierre
            if any(x in lines[i] for x in ['}', 'end']):
                # Insertar antes de la línea que contiene el cierre de la tabla si esta está sola o es el final
                if lines[i].strip() == '}':
                   new_lines.append(NEW_SPAWN_LINE)
                   inserted = True
        new_lines.append(lines[i])

    if not inserted:
        # Fallback si el parseo lineal falla, intentamos una inserción más simple
        print("Aviso: No se pudo determinar la posición exacta, intentando inserción alternativa...")
        content_lines = content.splitlines()
        for idx, line in enumerate(content_lines):
            if '}' in line and idx > 0:
                content_lines.insert(idx, NEW_SPAWN_LINE)
                inserted = True
                break
        final_content = "\n".join(content_lines)
    else:
        final_content = "\n".join(new_lines)

    with open(SPAWN_FILE, 'w') as f:
        f.write(final_content)
    
    print(f"Punto de spawn '{NEW_SPAWN_NAME}' agregado con éxito.")

if __name__ == "__main__":
    print("=== PZ SPAWN REGIONS UPDATER ===")
    update_spawn_regions()
