
import os

# Rutas relativas al script (para ejecución desde el HOST)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, 'server-files')
CONFIG_ROOT = os.path.join(BASE_DIR, 'server-data')
WORKSHOP_PATH = os.path.join(PROJECT_ROOT, 'steamapps/workshop/content/108600')
INI_PATH = os.path.join(CONFIG_ROOT, 'Server/servertest.ini')

def clean_list(items_str, is_mod_list=False):
    # Restaurar letras escapadas accidentalmente
    items_str = items_str.replace('\t', 't').replace('\b', 'b').replace('\r', 'r').replace('\n', 'n')
    items = items_str.split(';')
    cleaned = []
    for item in items:
        item = item.strip()
        if not item: continue
        cleaned.append(item)
    return ';'.join(cleaned)

def fix_case_recursive(root):
    if not os.path.exists(root): return
    print(f"Escaneando: {root}")
    for root_dir, dirs, files in os.walk(root):
        # Evitar procesar lo que ya son symlinks para no entrar en bucle
        for name in dirs + files:
            full_path = os.path.join(root_dir, name)
            
            # 1. Limpiar enlaces rotos (de mods eliminados)
            if os.path.islink(full_path) and not os.path.exists(os.path.realpath(full_path)):
                try:
                    os.unlink(full_path)
                    continue 
                except OSError: pass

            # 2. Crear nuevos enlaces para sensibilidad a mayúsculas
            lc_name = name.lower()
            if lc_name != name:
                lc_path = os.path.join(root_dir, lc_name)
                if not os.path.exists(lc_path):
                    try:
                        # Link lowercase a Original
                        os.symlink(name, lc_path)
                    except OSError: pass

def update_ini():
    if not os.path.exists(INI_PATH):
        print(f"INI no encontrado en {INI_PATH}. Saltando limpieza de config.")
        return
    
    with open(INI_PATH, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if line.startswith('Mods='):
            val = line.split('=', 1)[1].strip()
            new_lines.append(f'Mods={clean_list(val, True)}\n')
        elif line.startswith('WorkshopItems='):
            val = line.split('=', 1)[1].strip()
            new_lines.append(f'WorkshopItems={clean_list(val)}\n')
        else:
            new_lines.append(line)
            
    with open(INI_PATH, 'w') as f:
        f.writelines(new_lines)
    print("INI actualizado con limpieza de caracteres.")

if __name__ == "__main__":
    print("=== PZ MOD FIXER PARA BUILD 42 (LINUX) ===")
    
    # 1. Corregir archivos
    print("Generando enlaces simbólicos para sensibilidad a mayúsculas...")
    fix_case_recursive(WORKSHOP_PATH)
    
    # 2. Corregir INI
    update_ini()
    
    # 3. Corregir .env (Para que sea persistente si GENERATE_SETTINGS=true)
    env_path = os.path.join(BASE_DIR, '.env')
    if os.path.exists(env_path):
        print("Actualizando .env para persistencia...")
        with open(env_path, 'r') as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if line.startswith('MODS='):
                val = line.split('=', 1)[1].strip().strip('"')
                new_lines.append(f'MODS="{clean_list(val, True)}"\n')
            else:
                new_lines.append(line)
        with open(env_path, 'w') as f:
            f.writelines(new_lines)
    
    print("¡Listo! Reinicia el servidor para aplicar cambios.")
