# Subagentes del Proyecto Catálogo de Características (totCsPC)

Este proyecto cuenta con 2 subagentes especializados disponibles:

## 1. `catalog_crypto_agent`
- **Rol:** Criptógrafo y Administrador de Sincronización Segura.
- **Responsabilidades:**
  - Auditar que no existan archivos en texto plano en la rama remota de Git.
  - Ejecutar y verificar procesos de cifrado y descifrado AES-256.
  - Verificar la coherencia de hashes entre local y remoto.
  - Validar y actualizar `.gitignore`.

## 2. `catalog_data_analyzer`
- **Rol:** Analista de Datos Técnicos de Catálogos Electrónicos.
- **Responsabilidades:**
  - Cargar datasets `.enc` directamente a memoria con Pandas (`CryptoLoader`).
  - Ejecutar consultas, filtros por procesador, memoria RAM, marcas, etc.
  - Generar comparativas y reportes analíticos sin exponer datos en claro a disco.
