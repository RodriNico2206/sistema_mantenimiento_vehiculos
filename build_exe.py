# build_exe.py
"""
Script para construir el ejecutable de Windows (.exe)
Sistema de Mantenimiento de Vehículos - Tkinter + SQLite

No requiere archivo .spec. Genera todo directamente con argumentos de PyInstaller.

Uso:
    python build_exe.py
"""

import os
import sys
import subprocess
import shutil


def limpiar_todo():
    """Elimina carpetas de caché, build, dist y archivos .spec antiguos"""
    carpetas = ['build', 'dist', '__pycache__']
    for carpeta in carpetas:
        ruta = os.path.join(os.getcwd(), carpeta)
        if os.path.exists(ruta):
            print(f"🗑 Eliminando {carpeta}/...")
            shutil.rmtree(ruta)

    # Eliminar archivos .spec en la raiz (se regeneran si es necesario)
    for archivo in os.listdir('.'):
        if archivo.endswith('.spec'):
            print(f"🗑 Eliminando {archivo}...")
            os.remove(archivo)

    # Limpiar __pycache__ en subcarpetas
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'), ignore_errors=True)
            dirs.remove('__pycache__')


def verificar_pyinstaller():
    """Verifica si PyInstaller está instalado"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} está instalado")
        return True
    except ImportError:
        print("✗ PyInstaller no está instalado")
        print("Instálalo con: pip install pyinstaller")
        return False


def construir_ejecutable():
    """Construye el ejecutable usando PyInstaller directamente sin .spec"""
    print("▶ Iniciando construcción limpia del ejecutable...")

    # Verificar que main.py existe
    if not os.path.exists('main.py'):
        print("✗ Error: No se encontró main.py en la carpeta actual")
        print("  Asegúrate de ejecutar este script desde la carpeta del proyecto")
        return False

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconsole",           # Sin ventana de consola (app de Windows)
        "--name", "SistemaMantenimientoVehiculos",
        "--distpath", "dist",    # Carpeta de salida
        "--workpath", "build",   # Carpeta de trabajo temporal
        "--specpath", ".",       # Donde guardar el .spec temporal
        "main.py"                # Punto de entrada
    ]

    print(f"▶ Ejecutando PyInstaller...")
    print(f"    Comando: {' '.join(cmd)}")
    print("")

    resultado = subprocess.run(cmd)

    if resultado.returncode == 0:
        exe_path = os.path.join('dist', 'SistemaMantenimientoVehiculos.exe')
        if os.path.exists(exe_path):
            tamano = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\n✓ ¡Ejecutable construido exitosamente!")
            print(f"  Ubicación: {exe_path}")
            print(f"  Tamaño: {tamano:.2f} MB")
            return True
        else:
            print("\n✗ Error: No se encontró el archivo .exe después de construir")
            return False
    else:
        print("\n✗ Error al construir el ejecutable")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("  Constructor de Ejecutable - Sistema Mantenimiento Vehículos")
    print("=" * 60)

    if not verificar_pyinstaller():
        sys.exit(1)

    limpiar_todo()
    exito = construir_ejecutable()

    if exito:
        print("\n" + "=" * 60)
        print("  ¡Listo! El archivo .exe está en la carpeta dist/")
        print("=" * 60)
    else:
        sys.exit(1)