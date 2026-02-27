import os

file_path = r'd:\Docker\ProyectZomboid-DedicatedServer2\.env'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('Mods=') or line.startswith('#MOD_IDS='):
        # Separar la clave (Mods) del valor
        prefix, mods_part = line.split('=', 1)
        
        # Quitar los saltos de línea al final para procesar
        has_newline = '\n' in mods_part
        mods_str = mods_part.rstrip('\r\n')
        
        mods = mods_str.split(';')
        
        fixed_mods = []
        for mod in mods:
            if mod.strip():
                # Quitar todas las barras iniciales por si acaso (sean 1, 2 o ninguna)
                clean_mod = mod.lstrip('\\')
                # Agregar exactamente 2 barras
                fixed_mods.append('\\\\' + clean_mod)
            else:
                # Conservar elementos vacíos (por ejemplo, si hay punto y coma al final o juntos)
                fixed_mods.append(mod)
                
        # Volver a unir
        new_line = prefix + '=' + ';'.join(fixed_mods)
        if has_newline:
            new_line += '\n'
        new_lines.append(new_line)
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("¡Listo! Las líneas de mods se han corregido.")
