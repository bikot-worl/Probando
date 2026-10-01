import os
from pathlib import Path

def obtener_tamano_formateado(tamano_bytes):
    """Convierte bytes a un formato legible (B, KB, MB, GB)."""
    for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamano_bytes < 1024.0:
            return f"{tamano_bytes:.1f} {unidad}"
        tamano_bytes /= 1024.0
    return f"{tamano_bytes:.1f} PB"


def obtener_tamano_directorio(ruta_dir):
    """Calcula el tamaño total acumulado de una carpeta y su contenido."""
    total = 0
    try:
        for entrada in os.scandir(ruta_dir):
            try:
                if entrada.is_file(follow_symlinks=False):
                    total += entrada.stat().st_size
                elif entrada.is_dir(follow_symlinks=False):
                    total += obtener_tamano_directorio(entrada.path)
            except (PermissionError, FileNotFoundError):
                continue
    except (PermissionError, FileNotFoundError):
        pass
    return total


def generar_lineas_arbol(ruta_carpeta, prefijo=""):
    """
    Función recursiva que genera cada línea del árbol con nombres y pesos.
    """
    lineas = []
    ruta = Path(ruta_carpeta)

    if not ruta.exists():
        return [f"La ruta '{ruta_carpeta}' no existe."]

    try:
        elementos = sorted(list(ruta.iterdir()), key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return [f"{prefijo}[Acceso Denegado]"]

    total_elementos = len(elementos)

    for i, elemento in enumerate(elementos):
        es_ultimo = (i == total_elementos - 1)
        conector = "└── " if es_ultimo else "├── "

        try:
            if elemento.is_dir():
                peso_bytes = obtener_tamano_directorio(elemento)
                peso_txt = obtener_tamano_formateado(peso_bytes)
                lineas.append(f"{prefijo}{conector}{elemento.name}/ [{peso_txt}]")

                extension_prefijo = "    " if es_ultimo else "│   "
                lineas.extend(generar_lineas_arbol(elemento, prefijo + extension_prefijo))
            else:
                peso_bytes = elemento.stat().st_size
                peso_txt = obtener_tamano_formateado(peso_bytes)
                lineas.append(f"{prefijo}{conector}{elemento.name} [{peso_txt}]")
        except (PermissionError, FileNotFoundError):
            lineas.append(f"{prefijo}{conector}{elemento.name} [Sin acceso]")

    return lineas


def guardar_estructura_directorio(ruta_objetivo=".", archivo_salida="sistemap.txt"):
    """
    Genera el reporte de la carpeta, lo imprime en consola y lo guarda/actualiza en un .txt
    """
    ruta = Path(ruta_objetivo).resolve()
    peso_total_raiz = obtener_tamano_directorio(ruta)
    peso_raiz_txt = obtener_tamano_formateado(peso_total_raiz)

    # Encabezado del reporte
    encabezado = [
        "=" * 60,
        f"ESTRUCTURA DE DIRECTORIO: {ruta}",
        f"Tamaño Total: {peso_raiz_txt}",
        "=" * 60,
        ""
    ]

    # Generar contenido del árbol
    lineas_arbol = generar_lineas_arbol(ruta)
    contenido_completo = "\n".join(encabezado + lineas_arbol)

    # Muestra el resultado en la consola
    print(contenido_completo)

    # Guarda o sobrescribe (actualiza) el archivo de texto
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(contenido_completo)

    print("\n" + "=" * 60)
    print(f"El resultado ha sido guardado/actualizado en: {archivo_salida}")
    print("=" * 60)


if __name__ == "__main__":
    # '.' analiza la carpeta actual donde se ejecuta el script.
    # Puedes cambiar '.' por una ruta completa, por ejemplo: "/sdcard/Download"
    RUTA_A_ANALIZAR = "." 
    ARCHIVO_REPORTE = "sistemap.txt"

    guardar_estructura_directorio(RUTA_A_ANALIZAR, ARCHIVO_REPORTE)
