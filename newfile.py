import json
import os
import re
import shutil

def generar_paginas_dibujos():
    html_template_path = 'plantilla.html'
    json_path = 'dibujos.json'
    output_dir = 'draw'

    if not os.path.exists(html_template_path):
        print(f"Error: No se encontró el archivo '{html_template_path}'.")
        return
    
    if not os.path.exists(json_path):
        print(f"Error: No se encontró el archivo '{json_path}'.")
        return

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    with open(html_template_path, 'r', encoding='utf-8') as f:
        html_template_content = f.read()

    with open(json_path, 'r', encoding='utf-8') as f:
        dibujos_data = json.load(f)

    if isinstance(dibujos_data, dict):
        dibujos_data = [dibujos_data]

    total_elementos = len(dibujos_data)
    generados = 0

    for index, item in enumerate(dibujos_data):
        numero_publicacion = total_elementos - index
        output_file_name = f"publicacion_{numero_publicacion}.html"
        output_file_path = os.path.join(output_dir, output_file_name)

        if "fileURL" in item:
            if isinstance(item["fileURL"], list):
                item["fileURL"] = [
                    url.replace("Imagenes/", "../draws/") for url in item["fileURL"]
                ]
            elif isinstance(item["fileURL"], str):
                item["fileURL"] = item["fileURL"].replace("Imagenes/", "../draws/")

        json_item_str = json.dumps(item, ensure_ascii=False, indent=12)

        pattern = r"const sampleItem\s*=\s*\{[\s\S]*?\};"
        replacement = f"const sampleItem = {json_item_str};"
        updated_html = re.sub(pattern, replacement, html_template_content)

        updated_html = updated_html.replace("Imagenes/", "../draws/")

        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)

        print(f"Generado: {output_file_path}")
        generados += 1

    print(f"\n¡Proceso completado! Se generaron {generados} archivos en '{output_dir}/'.")

if __name__ == '__main__':
    generar_paginas_dibujos()
