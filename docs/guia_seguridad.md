# Guía de Gestión y Cifrado del Catálogo de Características (2022-5)

## Arquitectura de Seguridad
1. **Versión Local (Texto Plano):** `F:\proyectos\CaractCatalog\2022-5`
   - Los archivos `.json` y `.csv` se mantienen en texto plano en tu disco local para fácil visualización y edición en Excel/VS Code.
2. **Clave Secreta Local:** `F:\proyectos\CaractCatalog\secret.key`
   - Clave simétrica AES-256 (Fernet) utilizada para cifrar/descifrar. **Nunca se sube a GitHub ni se comparte públicamente**.
3. **Repositorio GitHub (Cifrado):** `NewCat/2022-5/`
   - Todos los archivos se almacenan con extensión `.enc` (cifrado autenticado AES-256).

---

## Flujo de Actualización Mensual
Cada mes cuando tengas los nuevos archivos:
1. Pega los 2 archivos nuevos (`.json` y `.csv`) dentro de su subcarpeta correspondiente en `F:\proyectos\CaractCatalog\2022-5\`.
2. Abre la terminal en `F:\proyectos\CaractCatalog\` y ejecuta:
   ```bash
   python actualizar_catalogo.py
   ```
3. Selecciona la opción `1. [Sincronizar y Subir a GitHub]`.
   - El script cifrará automáticamente los archivos, actualizará el repositorio Git y hará `push` a GitHub con un solo clic.

---

## Consumo de Datos Cifrados en Python (Data Loader)
Para analizar o procesar los archivos cifrados en tus proyectos o scripts sin guardarlos en texto plano en disco:

```python
from scripts.crypto_loader import CryptoLoader

# Inicializar con la clave local
loader = CryptoLoader()

# 1. Cargar CSV cifrado directamente a Pandas DataFrame
df = loader.read_csv("NewCat/2022-5/252-CE/11735-CE/catalogo_caracteristicas_xxxx(ce).csv.enc")
print(df.head())

# 2. Cargar JSON cifrado directamente a dict/list
data = loader.read_json("NewCat/2022-5/252-CE/11735-CE/catalogo_caracteristicas_xxxx(ce).json.enc")
```
