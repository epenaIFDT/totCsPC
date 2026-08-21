---
name: catalog-crypto-sync
description: >-
  Guía y procedimientos para la gestión, cifrado mensual, sincronización con GitHub
  y consumo seguro en memoria del catálogo de características técnicas de Perú Compras
  (Acuerdo Marco 2022-5 / Catálogos 250-CP y 252-CE).
---

# Skill: Sincronización y Criptografía del Catálogo de Características

Este skill contiene los procedimientos operativos y buenas prácticas para la gestión del repositorio `totCsPC` y su espacio de trabajo local `F:\proyectos\CaractCatalog\`.

## 1. Arquitectura de Dos Capas
1. **Capa Local en Claro (`F:\proyectos\CaractCatalog\2022-5`):**
   - Contiene los archivos `.csv` y `.json` originales sin encriptar para uso diario.
2. **Capa Remota Cifrada (`totCsPC/NewCat/2022-5`):**
   - Contiene únicamente archivos `.enc` protegidos con AES-256 (Fernet).

## 2. Regla de Oro de Seguridad
- **NUNCA** hacer commit de archivos `.json` o `.csv` en claro dentro de `NewCat/2022-5/`.
- **NUNCA** subir `secret.key`, `*.secret`, ni `.env` a GitHub.

## 3. Flujo Operativo Mensual
1. El usuario coloca los nuevos archivos en `F:\proyectos\CaractCatalog\2022-5\<catalogo>\<codigo>\`.
2. Se ejecuta `python actualizar_catalogo.py` (Opción 1).
3. Se verifica la sincronización en GitHub.

## 4. Consumo en Memoria (Python / Pandas)
```python
from crypto_loader import CryptoLoader

loader = CryptoLoader(key_path=r"F:\proyectos\CaractCatalog\secret.key")
df = loader.read_csv("NewCat/2022-5/252-CE/11735-CE/catalogo_caracteristicas_xxxx(ce).csv.enc")
```
