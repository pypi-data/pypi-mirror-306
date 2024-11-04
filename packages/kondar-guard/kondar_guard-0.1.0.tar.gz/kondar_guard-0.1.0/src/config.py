from dataclasses import dataclass
from enum import Enum
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

STORAGE_DIR = ROOT_DIR / "storage"


class CryptModeCode(str, Enum):
    ENCRYPT_IN_MEMORY: str = "ENCRYPT_IN_MEMORY"
    DECRYPT_IN_MEMORY: str = "DECRYPT_IN_MEMORY"


@dataclass(frozen=True, slots=True)
class CryptMode:
    description: str
    code: CryptModeCode


CRYPT_MODES: dict[str, CryptMode] = {
    "1": CryptMode(
        description="Encrypt file (convert in memory)",
        code=CryptModeCode.ENCRYPT_IN_MEMORY
    ),
    "2": CryptMode(
        description="Decrypt file (convert in memory)",
        code=CryptModeCode.DECRYPT_IN_MEMORY
    ),
}
