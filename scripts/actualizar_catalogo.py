#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
Script interactivo para la gestión, cifrado y sincronización mensual
del Catálogo de Características (totCsPC / 2022-5).

Permite:
1. Mantener tus archivos locales en texto plano (F:\proyectos\CaractCatalog\2022-5)
2. Cifrar con AES-256 (.enc) y sincronizar al repositorio Git (totCsPC)
3. Subir automáticamente a GitHub con un commit claro
4. Probar la carga directa en memoria a Pandas DataFrame o dict JSON
5. Desencriptar desde el repositorio si necesitas restaurar datos
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

try:
    from crypto_loader import CryptoLoader
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from crypto_loader import CryptoLoader

# Rutas predeterminadas
LOCAL_DIR = r"F:\proyectos\CaractCatalog\2022-5"
REPO_DIR = r"C:\Users\epena.MYINGSAIFDT\totCsPC\NewCat\2022-5"
REPO_ROOT = r"C:\Users\epena.MYINGSAIFDT\totCsPC"
KEY_PATH = r"F:\proyectos\CaractCatalog\secret.key"

CATEGORIES = [
    ("250-CP", "11743-CP", "Computadoras Portátiles"),
    ("250-CP", "11744-WSP", "Workstations Portátiles"),
    ("250-CP", "11745-TB", "Tablets"),
    ("252-CE", "11735-CE", "Computadoras de Escritorio"),
    ("252-CE", "11736-TU", "Computadoras Todo en Uno"),
    ("252-CE", "11740-ET", "Estaciones de Trabajo"),
    ("252-CE", "11741-MN", "Monitores"),
    ("252-CE", "11749-PI", "Pantallas Interactivas"),
]


def print_header():
    print("\n" + "=" * 75)
    print("        GESTOR INTERACTIVO DE CATÁLOGO Y SINCRONIZACIÓN CIFRADA")
    print("=" * 75)
    print(f"Carpeta Local (Texto Plano):  {LOCAL_DIR}")
    print(f"Repositorio Git (Cifrado):    {REPO_DIR}")
    print(f"Clave Secreta Local:          {KEY_PATH} (Existe: {'SÍ' if os.path.exists(KEY_PATH) else 'NO'})")
    print("-" * 75)


def get_loader():
    if not os.path.exists(KEY_PATH):
        print(f"\n[ERROR] No se encontró el archivo de clave en: {KEY_PATH}")
        print("Cree la clave primero desde la opción 5.")
        return None
    return CryptoLoader(key_path=KEY_PATH)


def ver_estado():
    print_header()
    print("ESTADO ACTUAL DE ARCHIVOS:\n")
    print(f"{'Catálogo':<10} | {'Código':<12} | {'Categoría':<26} | {'Archivos Locales (Plano)':<28} | {'En Repo (.enc)':<15}")
    print("-" * 100)

    for cat, cod, nombre in CATEGORIES:
        loc_folder = os.path.join(LOCAL_DIR, cat, cod)
        rep_folder = os.path.join(REPO_DIR, cat, cod)

        loc_files = []
        if os.path.exists(loc_folder):
            loc_files = [f for f in os.listdir(loc_folder) if f.endswith(('.json', '.csv')) and not f.endswith('.enc')]

        rep_files = []
        if os.path.exists(rep_folder):
            rep_files = [f for f in os.listdir(rep_folder) if f.endswith('.enc')]

        loc_str = f"{len(loc_files)} archivos ({', '.join(loc_files)[:20]}...)" if loc_files else "0 archivos (Pendiente)"
        rep_str = f"{len(rep_files)} archivos .enc" if rep_files else "0 archivos (.gitkeep)"

        print(f"{cat:<10} | {cod:<12} | {nombre:<26} | {loc_str:<28} | {rep_str:<15}")
    print("-" * 100)


def sincronizar_y_subir():
    print_header()
    loader = get_loader()
    if not loader:
        return

    print("Iniciando proceso de cifrado y sincronización hacia el repositorio Git...\n")
    total_encrypted = 0

    for cat, cod, nombre in CATEGORIES:
        loc_folder = os.path.join(LOCAL_DIR, cat, cod)
        rep_folder = os.path.join(REPO_DIR, cat, cod)

        if not os.path.exists(loc_folder):
            os.makedirs(loc_folder, exist_ok=True)

        os.makedirs(rep_folder, exist_ok=True)

        local_files = [f for f in os.listdir(loc_folder) if f.endswith(('.json', '.csv')) and not f.endswith('.enc')]
        target_enc_names = [f + ".enc" for f in local_files]

        # Limpiar .enc antiguos
        for old_file in os.listdir(rep_folder):
            if old_file.endswith('.enc') and old_file not in target_enc_names:
                old_path = os.path.join(rep_folder, old_file)
                try:
                    os.remove(old_path)
                    print(f"[-] Eliminado .enc antiguo en repo: {cat}/{cod}/{old_file}")
                except Exception as e:
                    print(f"[!] No se pudo eliminar {old_path}: {e}")

        if not local_files:
            # Si no hay archivos, mantener .gitkeep para que git conserve la carpeta
            gitkeep_path = os.path.join(rep_folder, ".gitkeep")
            if not os.path.exists(gitkeep_path):
                with open(gitkeep_path, "w", encoding="utf-8") as f:
                    pass
            print(f"[i] {cat}/{cod} ({nombre}): Carpeta vacía, preservando .gitkeep")
            continue
        else:
            # Si hay archivos, eliminar .gitkeep si existe
            gitkeep_path = os.path.join(rep_folder, ".gitkeep")
            if os.path.exists(gitkeep_path):
                os.remove(gitkeep_path)

        # Cifrar cada archivo local al repo
        for file in local_files:
            src_file = os.path.join(loc_folder, file)
            dst_file = os.path.join(rep_folder, file + ".enc")
            try:
                loader.encrypt_file(src_file, dst_file)
                size_kb = os.path.getsize(dst_file) / 1024
                print(f"[+] Cifrado: {cat}/{cod}/{file} -> {file}.enc ({size_kb:.1f} KB)")
                total_encrypted += 1
            except Exception as e:
                print(f"[ERROR] Error al cifrar {src_file}: {e}")

    print(f"\nProceso de cifrado completado. Total de archivos cifrados generados/actualizados: {total_encrypted}")

    resp = input("\n¿Deseas confirmar los cambios (git commit) y enviarlos a GitHub (git push)? (s/n): ").strip().lower()
    if resp == 's':
        try:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            custom_msg = input(f"Mensaje de commit (Enter para: 'Actualización catálogo 2022-5 - {now_str}'): ").strip()
            commit_msg = custom_msg if custom_msg else f"Actualización catálogo 2022-5 - {now_str}"

            print("\nEjecutando git add...")
            subprocess.run(["git", "add", "-A"], cwd=REPO_ROOT, check=True)

            print("Ejecutando git commit...")
            res_commit = subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_ROOT, capture_output=True, text=True)
            print(res_commit.stdout)

            print("Ejecutando git push origin main...")
            res_push = subprocess.run(["git", "push", "origin", "main"], cwd=REPO_ROOT, capture_output=True, text=True)
            print(res_push.stdout)
            if res_push.stderr:
                print(res_push.stderr)

            print("\n[ÉXITO] ¡Cambios sincronizados correctamente con GitHub!")
        except Exception as e:
            print(f"[ERROR] Error durante la sincronización Git: {e}")
    else:
        print("Sincronización Git cancelada.")


def probar_carga_memoria():
    print_header()
    loader = get_loader()
    if not loader:
        return

    print("Selecciona una categoría para probar la carga directa en memoria (Pandas DataFrame):")
    for idx, (cat, cod, nombre) in enumerate(CATEGORIES, 1):
        print(f"  {idx}. [{cat}/{cod}] {nombre}")

    try:
        op = int(input("\nOpción (1-8): ").strip())
        if 1 <= op <= len(CATEGORIES):
            cat, cod, nombre = CATEGORIES[op - 1]
            rep_folder = os.path.join(REPO_DIR, cat, cod)
            csv_enc_files = [f for f in os.listdir(rep_folder) if f.endswith('.csv.enc')]
            if not csv_enc_files:
                print(f"[!] No hay archivos .csv.enc aún en {cat}/{cod}. Agregue los archivos primero.")
                return

            target_file = os.path.join(rep_folder, csv_enc_files[0])
            print(f"\nCargando directamente en memoria desde: {target_file}...")
            df = loader.read_csv(target_file)
            print(f"\n[ÉXITO] DataFrame cargado en memoria exitosamente!")
            print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
            print(f"Columnas: {list(df.columns)}")
            print("\nPrimeras 5 filas:")
            print(df.head())
        else:
            print("Opción no válida.")
    except Exception as e:
        print(f"[ERROR] No se pudo cargar: {e}")


def restaurar_a_local():
    print_header()
    loader = get_loader()
    if not loader:
        return

    print("[ATENCIÓN] Esto leerá los archivos .enc del repositorio y los desencriptará en tu carpeta local.")
    conf = input("¿Deseas continuar? (s/n): ").strip().lower()
    if conf != 's':
        return

    for cat, cod, nombre in CATEGORIES:
        rep_folder = os.path.join(REPO_DIR, cat, cod)
        loc_folder = os.path.join(LOCAL_DIR, cat, cod)

        if not os.path.exists(rep_folder):
            continue

        os.makedirs(loc_folder, exist_ok=True)
        for enc_file in os.listdir(rep_folder):
            if enc_file.endswith('.enc'):
                src_path = os.path.join(rep_folder, enc_file)
                plain_name = enc_file[:-4]  # Quitar .enc
                dst_path = os.path.join(loc_folder, plain_name)
                try:
                    loader.decrypt_file(src_path, dst_path)
                    print(f"[+] Restaurado: {cat}/{cod}/{plain_name}")
                except Exception as e:
                    print(f"[ERROR] Error al desencriptar {src_path}: {e}")

    print("\n[ÉXITO] Restauración completada en F:\\proyectos\\CaractCatalog\\2022-5.")


def ver_clave():
    print_header()
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, 'rb') as f:
            key_data = f.read().decode('utf-8', errors='replace')
        print(f"Ubicación de la Clave: {KEY_PATH}")
        print(f"Valor de la Clave:    {key_data}")
        print("\n[IMPORTANTE] Mantén este archivo y su contenido seguro.")
        print("Nunca lo compartas en repositorios públicos ni lo subas a GitHub.")
    else:
        print(f"No existe clave en {KEY_PATH}.")


def main():
    while True:
        print_header()
        print("MENÚ PRINCIPAL:")
        print("  1. [Sincronizar y Subir a GitHub]     (Cifra archivos locales -> Actualiza Repo -> Git Push)")
        print("  2. [Ver Estado de Archivos]           (Compara archivos locales vs encriptados en Repo)")
        print("  3. [Probar Carga de Datos en Memoria] (Demuestra lectura con Pandas sin tocar disco)")
        print("  4. [Restaurar / Desencriptar a Local] (Recupera archivos planos desde los .enc del Repo)")
        print("  5. [Ver / Respaldar Clave Secreta]")
        print("  0. [Salir]")
        print("-" * 75)

        opcion = input("Selecciona una opción (0-5): ").strip()
        if opcion == '1':
            sincronizar_y_subir()
            input("\nPresiona Enter para volver al menú...")
        elif opcion == '2':
            ver_estado()
            input("\nPresiona Enter para volver al menú...")
        elif opcion == '3':
            probar_carga_memoria()
            input("\nPresiona Enter para volver al menú...")
        elif opcion == '4':
            restaurar_a_local()
            input("\nPresiona Enter para volver al menú...")
        elif opcion == '5':
            ver_clave()
            input("\nPresiona Enter para volver al menú...")
        elif opcion == '0':
            print("\n¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
