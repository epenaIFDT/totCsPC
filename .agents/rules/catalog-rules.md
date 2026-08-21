# Reglas del Proyecto Catálogo de Características (totCsPC)

## Directivas de Seguridad Obligatorias
1. **Protección de Claves:** El archivo `secret.key` jamás debe agregarse al control de versiones de Git ni exponerse en commits o logs públicos.
2. **Cifrado Obligatorio en Repositorio:** Cualquier archivo añadido a `NewCat/2022-5/` debe estar cifrado con extensión `.enc` mediante `crypto_loader.py` antes de realizar `git push`.
3. **Preservar Separación Local/Remoto:** Mantener `F:\proyectos\CaractCatalog\2022-5` como fuente local en texto plano y `totCsPC\NewCat\2022-5` como destino cifrado.
4. **Validación de Estructura:** Asegurar siempre la correspondencia de las 7 subcarpetas:
   - `250-CP/11743-CP` (Computadoras Portátiles)
   - `250-CP/11744-WSP` (Workstations Portátiles)
   - `250-CP/11745-TB` (Tablets)
   - `252-CE/11735-CE` (Computadoras de Escritorio)
   - `252-CE/11740-ET` (Estaciones de Trabajo)
   - `252-CE/11741-MN` (Monitores IT)
   - `252-CE/11749-PI` (Pantallas Interactivas)
