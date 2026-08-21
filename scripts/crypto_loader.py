"""
Módulo CryptoLoader para Catálogo de Características.
Permite cargar archivos cifrados (.enc) directamente a memoria (Pandas DataFrame o dict JSON)
sin necesidad de exponer archivos en texto plano en el disco.
"""

import os
import io
import json
from pathlib import Path
from typing import Optional, Union, Any
import pandas as pd
from cryptography.fernet import Fernet


class CryptoLoader:
    def __init__(self, key: Optional[Union[str, bytes]] = None, key_path: Optional[str] = None):
        """
        Inicializa el cargador con una clave o ruta al archivo de clave.
        """
        if key:
            if isinstance(key, str):
                key = key.encode('utf-8')
            self.cipher = Fernet(key)
        else:
            resolved_key_path = self._resolve_key_path(key_path)
            with open(resolved_key_path, 'rb') as f:
                key_bytes = f.read().strip()
            self.cipher = Fernet(key_bytes)

    def _resolve_key_path(self, custom_path: Optional[str]) -> str:
        candidates = []
        if custom_path:
            candidates.append(custom_path)
        if os.environ.get("CATALOG_SECRET_KEY_PATH"):
            candidates.append(os.environ.get("CATALOG_SECRET_KEY_PATH"))
        candidates.extend([
            r"F:\proyectos\CaractCatalog\secret.key",
            os.path.join(os.path.expanduser("~"), ".caract_catalog_secret.key"),
            "secret.key"
        ])
        for p in candidates:
            if os.path.exists(p):
                return p
        raise FileNotFoundError(
            f"No se encontró el archivo de clave secreta. Lugares verificados: {candidates}"
        )

    def encrypt_bytes(self, data: bytes) -> bytes:
        return self.cipher.encrypt(data)

    def decrypt_bytes(self, data: bytes) -> bytes:
        return self.cipher.decrypt(data)

    def encrypt_file(self, src_path: str, dst_path: str) -> None:
        with open(src_path, 'rb') as f:
            data = f.read()
        encrypted = self.encrypt_bytes(data)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        with open(dst_path, 'wb') as f:
            f.write(encrypted)

    def decrypt_file(self, src_path: str, dst_path: str) -> None:
        with open(src_path, 'rb') as f:
            data = f.read()
        decrypted = self.decrypt_bytes(data)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        with open(dst_path, 'wb') as f:
            f.write(decrypted)

    def read_csv(self, enc_filepath: str, encoding: str = 'utf-8', **pandas_kwargs) -> pd.DataFrame:
        """Carga un archivo CSV cifrado directamente a un DataFrame de Pandas en memoria."""
        with open(enc_filepath, 'rb') as f:
            encrypted_data = f.read()
        decrypted_bytes = self.decrypt_bytes(encrypted_data)
        return pd.read_csv(io.BytesIO(decrypted_bytes), encoding=encoding, **pandas_kwargs)

    def read_json(self, enc_filepath: str, encoding: str = 'utf-8') -> Any:
        """Carga un archivo JSON cifrado directamente a un objeto Python (dict o list) en memoria."""
        with open(enc_filepath, 'rb') as f:
            encrypted_data = f.read()
        decrypted_bytes = self.decrypt_bytes(encrypted_data)
        return json.loads(decrypted_bytes.decode(encoding))
